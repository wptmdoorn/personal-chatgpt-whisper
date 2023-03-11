from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from db import init_db, get_messages, insert_message
import os, requests
import openai

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)

client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))


def query_gpt3(text: str, history: list[tuple]) -> str:
    _messages = [{"role": h[2], "content": h[3]} for h in history]
    _messages.insert(
        0,
        {
            "role": "system",
            "content": """You are replying to a SMS message from a friend. 
                          Please keep the conversation friendly and polite.
                          Try to reply in the same language as your friend.""",
        },
    )
    _messages.append({"role": "user", "content": text})

    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=_messages,
        max_tokens=1000,
    )["choices"][0]["message"]["content"]


@app.route("/sms", methods=["GET", "POST"])
def chatgpt():
    in_msg = request.form["Body"].lower()
    out_msg = query_gpt3(in_msg, get_messages(request.form["From"]))

    insert_message(request.form["From"], "user", in_msg)
    insert_message(request.form["From"], "assistant", out_msg)

    resp = MessagingResponse()
    resp.message(out_msg)

    return str(resp)


@app.route("/inbound/voice/call", methods=["POST"])
def incoming_voice_call():
    response = VoiceResponse(action="/recording/callback", method="POST")
    response.record(
        recording_status_callback="/recording/callback",
        recording_status_callback_event="completed",
    )

    return str(response)


@app.route("/recording/callback", methods=["GET", "POST"])
def upload_recording():
    call_object = client.calls(request.form["CallSid"]).fetch()

    recording_url = f"{request.values['RecordingUrl']}.mp3"
    filename = f"{request.values['RecordingSid']}.mp3"

    with open(f"audio/{filename}", "wb") as f:
        f.write(requests.get(recording_url).content)

    in_msg = openai.Audio.transcribe("whisper-1", open(f"audio/{filename}", "rb"))[
        "text"
    ]
    out_msg = query_gpt3(in_msg, get_messages(call_object.from_formatted))

    insert_message(call_object.from_formatted, "user", in_msg)
    insert_message(call_object.from_formatted, "assistant", out_msg)

    client.messages.create(
        body=out_msg,
        from_=call_object.to_formatted,
        to=call_object.from_formatted,
    )

    return Response(status=200)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
