from transformers import pipeline

model = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

# image_to_text("https://eksmo.ru/upload/iblock/ebd/bladerunner_l_min.jpg")


def image2text(*_, img_url: str):
    return model(img_url)[0]['generated_text']

