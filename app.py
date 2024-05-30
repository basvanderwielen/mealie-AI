"""
Author: Bas van der Wielen
"""
import os, sys
import json
from dotenv import load_dotenv


from flask import Flask, request, jsonify
from loguru import logger

import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image
from google.oauth2 import service_account

from mealie.mealie_client import MealieClient

logger.add(sys.stderr, format="{time} {level} {message}", filter="app.py", level="DEBUG")

# Load environment variables from .env.
load_dotenv()

UPLOAD_FOLDER = 'uploads'
SERVICE_ACCOUNT_LOCATION = 'gemini/service_account.json'

mealie = MealieClient(
    os.getenv("MEALIE_SERVER_IP"),
    os.getenv("MEALIE_SERVER_PORT"),
    os.getenv("MEALIE_API_KEY"),
)

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_LOCATION)
vertexai.init(project=credentials.project_id, location="europe-west4", credentials=credentials)
model = GenerativeModel(model_name="gemini-1.0-pro-vision-001")

class FlaskAppWrapper(object):

    def __init__(self, app, **configs):
        self.app = app
        self.configs(**configs)

    def configs(self, **configs):
        for config, value in configs.items():
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'jpeg'

def upload_file():
    global LAST_UPLOADED_FILENAME  # Declare the global variable
    if 'file' not in request.files:
        logger.error('No file part in the request')
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        logger.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Ensure the upload folder exists
        filename = file.filename
        filepath = os.path.join(app_wrapped.app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logger.info('File uploaded')
        LAST_UPLOADED_FILENAME = filename  # Update the global variable
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

    logger.error('Invalid file format')
    return jsonify({'error': 'Invalid file format. Only JPG images are allowed.'}), 400

def process_image():
    with open('gemini/instructions.txt', 'r') as file:
        # Read the entire contents of the file into a variable
        instructions = file.read()

    img_path = os.path.join(app_wrapped.app.config['UPLOAD_FOLDER'], LAST_UPLOADED_FILENAME)

    logger.info(f"Uploading {img_path} and instructions to Gemini.")

    response = model.generate_content(
        [
            instructions,
            Image.load_from_file(img_path),
        ]
    )

    json_str = response.text
    logger.debug(json_str)
    json_obj = json.loads(json_str)

    logger.debug(json_obj)
    logger.info(f"Found recipe with title {json_obj['name']}")

    logger.info('Adding to Mealie')
    slug = mealie.recipe_create(json_obj['name'])
    logger.debug(f"Created recipe in Mealie with slug: {slug}")
    mealie.recipe_update(slug, json_obj)
    logger.info("Recipe uploaded!")

    return jsonify({'message': f"Processed: {json_obj['name']}"}), 200


flask_app = Flask(__name__)
app_wrapped = FlaskAppWrapper(flask_app)
app_wrapped.configs(
        UPLOAD_FOLDER = UPLOAD_FOLDER,
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit the upload size to 16 MB,
)
# Add endpoint for uploading a file
app_wrapped.add_endpoint('/upload', 'upload_file', upload_file, methods=['PUT'])
app_wrapped.add_endpoint('/process', 'process_image', process_image, methods=['GET'])

if __name__ == "__main__":
    app_wrapped.run(host='0.0.0.0', port=5000, debug=True)
