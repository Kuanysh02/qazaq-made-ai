from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class TextToSpeechResponse(BaseModel):
    audio: str

class TTSRequest(BaseModel):
    input: str

GOOGLE_TTS_API_URL = "https://texttospeech.googleapis.com/v1beta1/text:synthesize"
API_KEY = os.getenv("API_KEY")

@app.post("/text-to-speech", response_model=TextToSpeechResponse)
async def text_to_speech(tts_request: TTSRequest):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "x-goog-user-project": "qazaqmadeapi",
        "Content-Type": "application/json"
    }

    data = {
        "input": {"text": tts_request.input},
        "voice": {
            "languageCode": "en-US",
            "name": "en-US-Journey-F"
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "effectsProfileId": ["small-bluetooth-speaker-class-device"],
            "pitch": 0,
            "speakingRate": 1
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_TTS_API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()

    audio_content = response_data["audioContent"]
    return {"audio": audio_content}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
