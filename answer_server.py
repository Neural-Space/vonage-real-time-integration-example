from threading import Thread
import uuid
import requests
import os
import websocket as wsclient
import numpy as np
from scipy.io import wavfile
import json
from fastapi import FastAPI, Request, WebSocket


app = FastAPI()
ngrok_url = os.environ["NGROK_URL"]
ngrok_url = ngrok_url.replace("https://", '')
assert ngrok_url is not None, "NGROK_URL not set."

BASE = "https://voice.neuralspace.ai/api/v1/languages?type=stream"
API_KEY = os.environ["NS_API_KEY"]
assert API_KEY is not None, "NS_API_KEY not set."
headers = {
    "Authorization": API_KEY
}
TOKEN = ''
LANGUAGE = "en"
ncco_example = [
    {
        "action": "connect",
        "endpoint": [
            {
                "type": "websocket",
                "uri": f"wss://{ngrok_url}/socket",
                "content-type": "audio/l16;rate=16000",
                "headers": {"language": "en-IN", "caller-id": "Shubham"},
            }
        ],
    },
    {"action": "talk", "text": "Hello!"},
    {
        "action": "talk",
        "text": "Please tell us, how can we help you today?",
        "bargeIn": True,
    },
    {
        "eventUrl": [f"https://{ngrok_url}/speech"],
        "eventMethod": "POST",
        "action": "input",
        "type": ["speech"],
        "speech": {
            "language": "en-gb",
            "context": ["support", "buy", "credit", "account"],
            "endOnSilence": 5,
            "saveAudio": True,
            "sensitivity": "90",
        },
    },
]

@app.on_event("startup")
def startup():
    global TOKEN, LANGUAGE
    DURATION = 600
    TOKEN_URL = f"https://voice.neuralspace.ai/api/v1/token?duration={DURATION}"
    response = requests.get(TOKEN_URL, headers=headers)
    assert response.status_code == 200
    TOKEN = response.json()['data']['token']
    LANGUAGE = "en"
    print("GOT STREAM TOKEN")

@app.get("/answer")
async def answer(req: Request):
    # print(req.headers)
    # print(await req.body())
    # print(list(req.items()))
    print(req.query_params)
    return ncco_example


@app.post("/speech")
async def speech(req: Request):
    print(list(req.items()))
    print(await req.body())
    return [{"action": "talk", "text": "Received your speech data."}]


@app.websocket("/socket")
async def socket(websocket: WebSocket):
    await websocket.accept()
    total_bytes = b""
    session_id = uuid.uuid4()
    stream_url = f"wss://voice.neuralspace.ai/voice/stream/live/transcribe/{LANGUAGE}/{TOKEN}/{session_id}"
    print(stream_url)
    ws = wsclient.create_connection(stream_url)
    print("WEBSOCKET CONNECTION MADE")
    def print_thread():
        print("listening")
        while True:
            data = ws.recv()
            resp = json.loads(data)
            if resp["full"]:
                print(f"{resp['text']}")
    back_recieve_thread = Thread(target=print_thread, daemon=True)
    back_recieve_thread.start()
    print("after background thread.")
    buffer = b''
    try:
        while True:
            data = await websocket.receive()
            audio_bytes = data.get("bytes")
            if audio_bytes:
                if len(buffer) > 8000:
                    ws.send_binary(buffer)
                    buffer = b''
                else:
                    buffer += audio_bytes
                total_bytes += audio_bytes
    except Exception as e:
        print(e)
        np_data = np.frombuffer(total_bytes, dtype=np.int16)
        wavfile.write("tempfile.wav", 16000, np_data)