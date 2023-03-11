# Personal SMS and Call Assistant

<p align="center"><img src="https://user-images.githubusercontent.com/26939682/224476548-6e29835c-b85d-4f03-bbdd-ad0009b04411.PNG" width="25%"/> <img src="https://user-images.githubusercontent.com/26939682/224476640-699ac1e9-c742-4a94-bc04-bb3292a96974.PNG" width="25%"/> <img src="https://user-images.githubusercontent.com/26939682/224476641-69ed2a36-0012-436c-818e-2a3d059c7c0a.PNG" width="25%"/></p>

This project is a personal SMS and Call assistant that allows you to communicate through text messages and calls using speech-to-text technology. It uses Twilio to handle incoming SMS and calls, OpenAI to generate responses to incoming messages, Whisper to convert incoming calls to text, and Flask to create a web application. It uses a SQLite3 database to store messages for each number, hereby remembering previous conversations. 

## Installation

To install this project, you will need to have Python 3.x installed on your system. You will also need to create accounts with Twilio and OpenAI, and set up a virtual environment to manage the project dependencies.

1. Clone the repository to your local machine.
2. Create a virtual environment using `python3 -m venv venv`.
3. Activate the virtual environment using `source venv/bin/activate`.
4. Install the project dependencies using `pip install -r requirements.txt`.
5. Set up your Twilio and OpenAI accounts, and create a file named `.env` in the project root directory with the following environment variables: 
`
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
OPENAI_API_KEY=your_openai_api_key
`         

6. Install ngrok by following the instructions at https://ngrok.com/download.  
7. Run ngrok to create a secure tunnel to localhost using the command `./ngrok http 5000`. Note that you need the forwarding URL in steps 8 and 9.
8. In the Twilio console, set the webhook for incoming SMS messages to `https://<your-ngrok-url>/sms`.  
9. In the Twilio console, set the webhook for incoming calls to `https://<your-ngrok-url>/inbound/voice/call`.  
10. Run the application using `python bot.py`.

## Usage

Once the application is running and the webhooks are set up, you can communicate with the personal SMS and Call assistant using SMS and phone calls.

### SMS

To send a text message to the assistant, simply send a text message to the Twilio phone number associated with the application. The assistant will use OpenAI to generate a response and send it back to you.

### Calls

To initiate a phone call with the assistant, call the Twilio phone number associated with the application. The assistant will answer the call and use Whisper to convert your spoken words to text. It will then use OpenAI to generate a response and send it back to you as an SMS message.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

This project was created using the following technologies:

- [Twilio](https://www.twilio.com/)
- [OpenAI](https://openai.com/)
- [Whisper](https://whisper.ai/)
- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [ngrok](https://ngrok.com/)
