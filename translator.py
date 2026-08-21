
"""
Етап 7: переклад. Локальна модель Helsinki-NLP/opus-mt-en-uk.
Поки просто перевіряємо, що переклад працює.
"""
import json
from transformers import MarianMTModel, MarianTokenizer

MODEL_NAME = "Helsinki-NLP/opus-mt-en-uk"  # англійська → українська

# Завантажуємо токенізатор і модель.
# Перший раз модель завантажиться з інтернету (~300 МБ) і збережеться локально.
tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
model = MarianMTModel.from_pretrained(MODEL_NAME)

try:
    with open("cache.json","r", encoding="utf-8") as f:
        cache=json.load(f)
except FileNotFoundError: 
    cache ={}

def translate(text):
    """Перекладає англійський текст українською."""
    text = text.lstrip(". ")
    if text in cache:
        result = cache[text]
    else:
        tokens = tokenizer(text, return_tensors="pt")   # текст → числа (тензори)
        output = model.generate(**tokens)                # модель перекладає
    # числа → текст; skip_special_tokens прибирає службові токени
        result = tokenizer.decode(output[0], skip_special_tokens=True)
        cache[text] = result
        with open("cache.json", "w", encoding="utf-8")as f:
            json.dump(cache, f, ensure_ascii=False) 
    return result


if __name__ == "__main__":
    print(translate("Back then we were young and unafraid."))
    print(translate("Back then we were young and unafraid."))
