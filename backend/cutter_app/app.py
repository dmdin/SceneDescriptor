import os
import pathlib
import requests
from yarl import URL
import json
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from silent_scenes.main import get_scenes_frames

DUBBING_APP_URL = 'http://localhost:8000'
PROJECTS_DIR = 'static/videos'
BASE_URL = URL('http://localhost:8001')


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/projects", StaticFiles(directory=PROJECTS_DIR), name="projects")


class VideoId(BaseModel):
    id: str


def get_dubbing(frame_path):
    # TODO
    # res = requests.post(f'{DUBBING_APP_URL}/image_to_voice', json={'url': frame_path})
    # return res.text
    return ''


@app.post('/generate_description')
def generate_description_by_id(body: VideoId):
    project_dir = pathlib.Path(PROJECTS_DIR) / body.id
    (project_dir / 'frames').mkdir(parents=True, exist_ok=True)

    scenes_frames = get_scenes_frames(f'{PROJECTS_DIR}/{body.id}/video.mp4', 4, 4, 3,
                                      f'{PROJECTS_DIR}/{body.id}/frames')

    descriptions = []

    for scene_info in scenes_frames:
        dubbing_path = get_dubbing(scene_info['frame'])
        descriptions.append({
            'scene': scene_info['scene'],
            'dubbing': '',
            'description': '',
            'frame': str(BASE_URL / scene_info['frame'])})

    with open(f'{PROJECTS_DIR}/{body.id}/description.json', 'w') as file:
        json.dump(descriptions, file)

    return descriptions


@app.get('/description')
def get_description_by_id(video_id: int):
    with open(f'{PROJECTS_DIR}/{video_id}/description.json', 'r') as file:
        data = json.load(file)

    return data


@app.get('/get_all_projects')
def get_all_projects():
    projects = os.listdir(PROJECTS_DIR)

    res = []
    for project_name in projects:
        project_url = BASE_URL / 'projects' / project_name

        res.append({
            'video': str(project_url / 'video.mp4'),
            'description': str(project_url / 'description.json'),
            'preview': str(project_url / 'frames' / 'frame_0.jpg'),
            'audio': str(project_url / 'video.wav')
        })
    return res


if __name__ == '__main__':
    uvicorn.run('app:app', use_colors=True, reload=True, port=8001)
