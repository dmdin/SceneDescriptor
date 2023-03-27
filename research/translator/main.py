from transformers import AutoTokenizer, AutoModel, AutoModelForSeq2SeqLM

translation_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
translator = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-ru")


def translate(source: str) -> str:
    input_ids = translation_tokenizer(
        source, return_tensors="pt"
    ).input_ids  # Batch size 1
    outputs = translator.generate(input_ids)
    return translation_tokenizer.decode(outputs[0], skip_special_tokens=True)