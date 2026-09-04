import os

import requests
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TextBee SMS API")


TEXTBEE_API_KEY = os.getenv("TEXTBEE_API_KEY")
TEXTBEE_DEVICE_ID = os.getenv("TEXTBEE_DEVICE_ID")
TEXTBEE_URL = os.getenv("TEXTBEE_API_URL", "https://api.textbee.dev/api/v1/gateway/send-sms")


class SMSRequest(BaseModel):
    recipient: str
    message: str


@app.get("/")
def home():
    return {"message": "TextBee SMS API is running"}


@app.post("/send-sms")
def send_sms(data: SMSRequest):

    response = requests.post(
        TEXTBEE_URL,
        headers={"x-api-key": TEXTBEE_API_KEY},
        json={
            "deviceId": TEXTBEE_DEVICE_ID,
            "recipients": [data.recipient],
            "message": data.message,
        },
    )

    return response.json()
