import os
from datetime import datetime

import argparse
import requests
import enum

from dotenv import load_dotenv

load_dotenv()

IAM_TOKEN = os.environ['IAM_TOKEN']
FOLDER_ID = os.environ['FOLDER_ID']


class Voice(enum.Enum):
    Alena='alena'
    Filipp='filipp'
    Ermil='ermil'
    Jane='jane'
    Madirus='madirus'
    Omazh='omazh'
    Zahar='zahar'


def send_to_api(text, speed, voice):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + IAM_TOKEN,
    }

    data = {
        'text': text,
        'speed': speed,
        'voice': voice,
        'folderId': FOLDER_ID,
        'lang': 'ru-RU',
        'format': 'mp3'
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


def text2speech(text, *_, speed=3.0, voice=Voice.Filipp):
    out_path = datetime.now()

    with open(out_path, "wb") as f:
        for audio_content in send_to_api(text, speed, voice):
            f.write(audio_content)
    return out_path


def setup_text2speech(*, speed, voice: Voice):
    def wrap(text: str, out_path: str):
        return text2speech(text, speed=speed, voice=voice)
    return wrap
