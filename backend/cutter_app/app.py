import os
import pathlib
import requests
from yarl import URL
import json
import uvicorn
from typing import List
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


class Project(BaseModel):
    video_id: str
    name: str


class Frame(BaseModel):
    scene: str
    dubbing: str
    description: str
    frame: str


class VideoDescription(BaseModel):
    id: str
    name: str
    scenes_info: List[Frame]


@app.post('/generate_description')
def generate_description_by_id(body: Project):
    project_dir = pathlib.Path(PROJECTS_DIR) / body.video_id
    (project_dir / 'frames').mkdir(parents=True, exist_ok=True)

    scenes_frames = get_scenes_frames(f'{PROJECTS_DIR}/{body.video_id}/video.mp4', 4, 4, 3,
                                      f'{PROJECTS_DIR}/{body.video_id}/frames')

    description = {'id': body.video_id, 'name': body.name, 'scenes_info': []}

    for scene_info in scenes_frames:
        description['scenes_info'].append({
            'scene': scene_info['scene'],
            'dubbing': '',
            'description': '',
            'frame': str(BASE_URL / scene_info['frame'])})

    with open(f'{PROJECTS_DIR}/{body.video_id}/description.json', 'w') as file:
        json.dump(description, file)

    return description


@app.get('/description/{video_id}')
def get_description_by_id(video_id: int):
    with open(f'{PROJECTS_DIR}/{video_id}/description.json', 'r') as file:
        data = json.load(file)

    return data


@app.put('/description/{video_id}')
def update_description(video_id: int, new_description: VideoDescription):
    print(video_id)
    with open(f'{PROJECTS_DIR}/{video_id}/description.json', 'w') as file:
        json.dump(new_description.dict(), file)

    return new_description


@app.get('/get_all_projects')
def get_all_projects():
    projects = os.listdir(PROJECTS_DIR)

    res = []
    for project_id in projects:
        project_url = BASE_URL / 'projects' / project_id

        with open(f'{PROJECTS_DIR}/{project_id}/description.json', 'r') as file:
            description = json.load(file)

        res.append({
            'video': str(project_url / 'video.mp4'),
            'description': str(project_url / 'description.json'),
            'preview': str(project_url / 'frames' / 'frame_0.jpg'),
            'audio': str(project_url / 'video.wav')
        })
    return res


if __name__ == '__main__':
    uvicorn.run('app:app', use_colors=True, reload=True, port=8001)
