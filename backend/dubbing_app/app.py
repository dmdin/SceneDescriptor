import os
import uvicorn
from yarl import URL
import pathlib
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from pipeline import pipeline_img2spch, pipeline_img2txt, pipeline_txt2spch
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
VOICE_DIR = "voices"
IMG_DIR = "images"
pathlib.Path(VOICE_DIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(IMG_DIR).mkdir(parents=True, exist_ok=True)

app.mount("/voices", StaticFiles(directory=VOICE_DIR), name="voices")
app.mount("/images", StaticFiles(directory=IMG_DIR), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ImageUrl(BaseModel):
    url: str


class UrlPath(BaseModel):
    url: str


class Text(BaseModel):
    text: str


BASE_URL = URL('http://localhost:8000')


@app.post('/image2speech', response_model=UrlPath)
def synth_voice_by_image(body: ImageUrl):
    voice_path = pipeline_img2spch(img_url=body.url)
    voice_url = BASE_URL / voice_path.as_posix()
    return UrlPath(url=str(voice_url))


@app.post('/image2text', response_model=Text)
def synth_text_by_image(body: ImageUrl):
    text = pipeline_img2txt(img_url=body.url)
    return Text(text=text)


@app.post('/text2speech', response_model=UrlPath)
def synth_voice_by_text(body: Text):
    voice_path = pipeline_txt2spch(ru_text=body.text)
    voice_url = BASE_URL / voice_path.as_posix()
    return UrlPath(url=str(voice_url))


@app.post('/text2speech', response_model=UrlPath)
def synth_voice_by_text(body: Text):
    voice_path = pipeline_txt2spch(ru_text=body.text)
    voice_url = BASE_URL / voice_path.as_posix()
    return UrlPath(url=str(voice_url))


@app.post('/upload_image')
def upload_image(file: UploadFile = File()):
    path = pathlib.Path(IMG_DIR) / file.filename
    with open(path, "wb+") as file_object:
        file_object.write(file.file.read())

    url = BASE_URL / path.as_posix()
    return UrlPath(url=url)


@app.post('/upload_voice')
def upload_image(file: UploadFile = File()):
    path = pathlib.Path(VOICE_DIR) / file.filename
    with open(path, "wb+") as file_object:
        file_object.write(file.file.read())

    url = BASE_URL / path.as_posix()
    return UrlPath(url=url)


if __name__ == '__main__':
    uvicorn.run('app:app', use_colors=True, reload=True)
