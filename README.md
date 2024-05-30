# mealie-AI
Use Google AI to add recipes to Mealie


# Project structure
Flask app that accepts image from IOS
Class for vertex interaction
Class for mealie interaction


# Installation instructions
Create a .env file containing the following secrets:
```
MEALIE_SERVER_IP=YOUR_SERVER_IP #http://10.0.1.1 or https://10.0.1.1
MEALIE_SERVER_PORT=9925 #default, change if needed
MEALIE_API_KEY=YOUR_MEALIE_API_KEY
GEMINI_PROJECT_ID=YOUR_GEMINI_PROJECT_ID
```

Download the Google Vertex AI service account for your project.
See instructions:
- https://googleapis.dev/python/google-api-core/latest/auth.html
- https://cloud.google.com/iam/docs/service-accounts-create#creating

Make sure it is placed in the gemini folder: `./gemini/service_account.json`


# TODO
- Build IOS shortcut to send image, based on existing shortcut
- Add 'auto import' label in Mealie
- Clean requirements