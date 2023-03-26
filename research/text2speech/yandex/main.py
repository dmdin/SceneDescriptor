import os

import argparse
import requests
from dotenv import load_dotenv

load_dotenv()


def synthesize(folder_id, iam_token, text):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }

    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': 'filipp',
        'folderId': folder_id,
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--token", required=True, help="IAM token")
    # parser.add_argument("--folder_id", required=True, help="Folder id")
    parser.add_argument("--text", required=True, help="Text for synthesize")
    parser.add_argument("--output", required=True, help="Output file name")
    args = parser.parse_args()

    with open(args.output, "wb") as f:
        for audio_content in synthesize(os.environ['FOLDER_ID'], os.environ['IAM_TOKEN'], args.text):
            f.write(audio_content)
