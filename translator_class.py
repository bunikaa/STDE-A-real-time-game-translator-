""" Клас для перекладу тексту """

import json
from transformers import MarianMTModel, MarianTokenizer, AutoTokenizer, AutoModelForSeq2SeqLM
from glossary import normalize

MODEL_NAME = "facebook/nllb-200-distilled-600M"  # англійська → українська

class Translator:
    def __init__(self):
        # виконуэться раз при створенні об'єкта класу
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        try:
            with open("cache.json", "r", encoding="utf-8") as f:
                self.cache = json.load(f)
        except FileNotFoundError:
            self.cache = {}

    def translate(self, text):
        #Перекладає текст використовує кеш
        text = text.lstrip(". ")
        text = normalize(text) 
        if text in self.cache:
            result = self.cache[text]
        else:
                self.tokenizer.src_lang = "eng_Latn" # встановлюємо мову джерела
                inputs = self.tokenizer(text, return_tensors="pt") # текст → числа (тензори)
                target_id = self.tokenizer.convert_tokens_to_ids("ukr_Cyrl") # встановлюємо мову перекладу
                outputs = self.model.generate(**inputs, forced_bos_token_id=target_id) # модель перекладає
                result = self.tokenizer.decode(outputs[0], skip_special_tokens=True) # числа → текст
                self.cache[text] = result
                with open("cache.json", "w", encoding="utf-8")as f:
                    json.dump(self.cache, f, ensure_ascii=False) 
        return result


