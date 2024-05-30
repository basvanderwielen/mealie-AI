# mealie-AI
Use Google AI to add recipes to Mealie.

After finding a very nice community guide on importing recipes from IOS to Mealie, I was quickly disappointed that Gemini API is not available in Europe.
Instead of mocking, I used my frustration to create this small docker app that interfaces with Vertex AI instead.
I opted to use a docker app since authentication from the IOS shortcut was not possible. Moving the interfacing to docker from IOS also enables non-IOS devices to use this functionality.

**During the days that I was working on this project. Google AI studio became available in Europe...**
Still, I like the setup of this project, since it allows for expanding of functionality, such as adding scaling to recipes, adding images, etc...


# Project overview
Simple Flask app running in a docker container that accepts an image. After the image is uploaded, it can be processed using the Vertex AI platform by Google.
Uploading an image and requesting processing is automated in an IOS shortcut. Can be downloaded here: `https://www.icloud.com/shortcuts/b628cc2c1afd435a8eddaa07fd5a3849`


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

# Credits
The idea and parts of the IOS shortcut are based on this Mealie community guide: https://docs.mealie.io/documentation/community-guide/ios/ and the shortcut by https://github.com/zippyy.


# TODO
- Add 'auto import' label in Mealie
- Clean requirements