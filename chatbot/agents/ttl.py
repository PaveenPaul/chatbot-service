import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()


def ttl(text):
    url = "https://api.murf.ai/v1/speech/generate"
    key = os.getenv("MurfAPI")
    payload = json.dumps({
    "voiceId": "en-US-natalie",
    "style": "Promo",
    "text": f"{text}",
    "rate": 0,
    "pitch": 0,
    "sampleRate": 48000,
    "format": "MP3",
    "channelType": "MONO",
    "pronunciationDictionary": {},
    "encodeAsBase64": False,
    "variation": 1,
    "audioDuration": 0,
    "modelVersion": "GEN2",
    "multiNativeLocale": "en-US"
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'api-key': key
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("audioFile", "")  
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return ""
    