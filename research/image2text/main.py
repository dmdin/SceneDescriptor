from transformers import pipeline

image2text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

# image_to_text("https://eksmo.ru/upload/iblock/ebd/bladerunner_l_min.jpg")