from pydub import AudioSegment
from pydub import effects


# Returns new path with higher speed
def speedup(path: str, by=1.3) -> str:
    sound = AudioSegment.from_file(path)
    so = sound.speedup(by, 150, 25)
    so.export(path[:-4] + f'x{by}.mp3', format='mp3')
