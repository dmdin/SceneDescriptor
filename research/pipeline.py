from image2text import image2text
from translator import translate
from text2speech import text2speech, Voice

# In: url to image
# Out: path to voice
def pipeline(*_, img_url):
    en_text = image2text(img_url)
    ru_text = translate(en_text)
    # t2s = setup_text2speech(speed=3.0, voice=Voice.Jane)

    # return t2s(ru_text)


# pipeline("")


from datetime import datetime

print(datetime.now())