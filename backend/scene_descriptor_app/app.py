from silent_scenes.main import get_scenes_frames

import requests
from yarl import URL
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json

DUBBING_APP_URL = 'http://localhost:8000'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VideoId(BaseModel):
    id: int


def get_dubbing(frame_path):
    # TODO
    # res = requests.post(f'{DUBBING_APP_URL}/image_to_voice', json={'url': frame_path})
    # return res.text
    return ''


@app.post('/generate_description')
def generate_description_by_id(body: VideoId):
    scenes_frames = get_scenes_frames(f'./static/videos/{body.id}/video.mp4', 4, 4, 3, f'./static/videos/{body.id}/frames')

    descriptions = []
    for scene_info in scenes_frames:
        dubbing_path = get_dubbing(scene_info['frame'])
        descriptions.append({'scene': scene_info['scene'], 'dubbing': dubbing_path})

    with open(f'./static/videos/{body.id}/description.txt', 'w') as file:
        json.dump(descriptions, file)

    return descriptions


@app.get('/description')
def get_description_by_id(video_id: int):
    with open(f'./static/videos/{video_id}/description.txt', 'r') as file:
        data = json.load(file)

    return data


