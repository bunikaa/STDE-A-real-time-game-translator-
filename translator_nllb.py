""" Налаштування для моделі NLLB  """

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
MODEL_NAME = "facebook/nllb-200-distilled-600M" # англійська → українська

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def translate_nllb(text):
    """Перекладає англійський текст українською за допомогою моделі NLLB."""
    tokenizer.src_lang = "eng_Latn" # встановлюємо мову джерела
    inputs = tokenizer(text, return_tensors="pt") # текст → числа (тензори)
    target_id = tokenizer.convert_tokens_to_ids("ukr_Cyrl") # встановлюємо мову перекладу
    outputs = model.generate(**inputs, forced_bos_token_id=target_id) # модель перекладає
    result = tokenizer.decode(outputs[0], skip_special_tokens=True) # числа → текст
    return result

if __name__ == "__main__":
    print(translate_nllb("Back then we were young and unafraid."))