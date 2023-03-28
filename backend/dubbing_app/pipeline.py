import functools
from image2text import image2text
from translator import translate
from text2speech import text2speech, Voice, setup_text2speech


# In: url to image
# Out: path to voice
t2s = setup_text2speech(out_dir='voices', speed=1.3, voice=Voice.Jane)


@functools.cache
def pipeline_img2spch(*_, img_url):
    en_text = image2text(img_url=img_url)
    ru_text = translate(en_text)
    return t2s(ru_text)


@functools.cache
def pipeline_img2txt(*_, img_url):
    en_text = image2text(img_url=img_url)
    ru_text = translate(en_text)
    return ru_text


@functools.cache
def pipeline_txt2spch(*_, ru_text):
    return t2s(ru_text)


if __name__ == '__main__':
    voice_path = pipeline(img_url='https://i.ytimg.com/vi/3s5zsFm3VgA/maxresdefault.jpg')
    print(voice_path)
