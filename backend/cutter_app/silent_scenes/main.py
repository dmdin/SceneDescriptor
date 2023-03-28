from scenedetect import detect, ContentDetector, AdaptiveDetector
from pyannote.audio import Pipeline
from dotenv import load_dotenv
import moviepy.editor as mp
import subprocess
import datetime
import time
import cv2
import os

load_dotenv()
AUTH_TOKEN = os.environ['AUTH_TOKEN']
SAVING_FRAMES_PER_SECOND = 10


def get_time_seconds(time_str):
    date_time = datetime.datetime.strptime(time_str, "%H:%M:%S.%f")
    return (date_time - datetime.datetime(1900, 1, 1)).total_seconds()


def get_scenes(filepath, thr):
    output = detect(filepath, AdaptiveDetector())

    scenes = []
    for scene in output:
        start = get_time_seconds(scene[0].get_timecode())
        end = get_time_seconds(scene[1].get_timecode())

        if end - start > thr:
            scenes.append((start, end))
    return scenes


def get_movie_audio(filepath, output_ext='wav'):
    filename, ext = os.path.splitext(filepath)
    audio_filepath = f"{filename}.{output_ext}"
    video = mp.VideoFileClip(filepath)
    video.audio.write_audiofile(audio_filepath)
    return audio_filepath


def get_silence_spans(filepath, span_thr):
    audio_filepath = get_movie_audio(filepath, 'wav')
    print('converted to audio')
    pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection",
                                        use_auth_token=AUTH_TOKEN)
    speeches = pipeline(audio_filepath).get_timeline().support()

    silence_spans = []
    for speech_ind in range(1, len(speeches)):
        if speeches[speech_ind].start - speeches[speech_ind - 1].end > span_thr:
            silence_spans.append((speeches[speech_ind - 1].end, speeches[speech_ind].start))

    return silence_spans


def get_scenes_with_silence(filepath, scene_thr, span_thr, voice_thr):
    scenes = get_scenes(filepath, scene_thr)
    print('got scenes')
    silence_spans = get_silence_spans(filepath, span_thr)
    print('got_spans')
    scenes_with_silence = []
    for span in silence_spans:
        for scene_ind in range(len(scenes)):
            current_scene = scenes[scene_ind]
            if current_scene[1] - span[0] >= voice_thr and current_scene[1] < span[1] or \
                    span[1] - current_scene[0] >= voice_thr and current_scene[0] > span[0]:
                scenes_with_silence.append((max(current_scene[0], span[0]), min(current_scene[1], span[1])))
    return scenes_with_silence


def get_scenes_frames(filepath, scene_thr, span_thr, voice_thr, timeline_dir, frames_dir='./data/frames'):
    scenes = get_scenes_with_silence(filepath, scene_thr, span_thr, voice_thr)
    print('got scenes with silence')

    cap = cv2.VideoCapture(filepath)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    current_scene_ind = 0
    timeline_frame_ind = 1
    frame_ind = 0
    timeline = []
    scenes_info = []
    while True:
        is_read, frame = cap.read()
        if not is_read:
            break

        if frame_ind == timeline_frame_ind * frames_number // 11:
            cv2.imwrite(f'{timeline_dir}/frame_{timeline_frame_ind}.jpg', frame)
            timeline.append(f'{timeline_dir}/frame_{timeline_frame_ind}.jpg')
            timeline_frame_ind += 1

        frame_time = frame_ind / fps
        if current_scene_ind < len(scenes) and frame_time >= scenes[current_scene_ind][0]:
            cv2.imwrite(f'{frames_dir}/frame_{current_scene_ind}.jpg', frame)
            print(f'frame for scene {current_scene_ind} saved as {frames_dir}/frame_{current_scene_ind}.jpg')
            scenes_info.append({'scene': scenes[current_scene_ind], 'frame': f'{frames_dir}/frame_{current_scene_ind}.jpg'})

            current_scene_ind += 1
        frame_ind += 1

    return scenes_info, timeline


# print(get_scenes_frames('./data/matrix.mp4', 4, 4, 3))
