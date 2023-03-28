import os
import uvicorn
from yarl import URL
import pathlib
from pydantic import BaseModel
from fastapi import FastAPI
from pipeline import pipeline
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
VOICE_DIR = "voices"
pathlib.Path(VOICE_DIR).mkdir(parents=True, exist_ok=True)

app.mount("/voices", StaticFiles(directory=VOICE_DIR), name="voices")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ImageUrl(BaseModel):
    url: str


class VoicePath(BaseModel):
    url: str


BASE_URL = URL('http://localhost:8000')


@app.post('/image_to_voice', response_model=VoicePath)
def synth_voice_by_image(body: ImageUrl):
    voice_path = pipeline(img_url=body.url)
    voice_url = BASE_URL / voice_path.as_posix()
    return VoicePath(url=str(voice_url))


if __name__ == '__main__':
    uvicorn.run('app:app', use_colors=True, reload=True)
