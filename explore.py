"""
Дослідження конвеєра перекладу: текст → токени → числа → модель → текст.
Друкуємо проміжні значення, щоб побачити, що відбувається всередині.
"""

from translator import tokenizer, model

text = "Back then we were young and unafraid."
print("1. Вхідний текст:")
print("   ", text)

# Токенізація: текст → числа. Дивимось і на числа, і на самі токени.
tokens = tokenizer(text, return_tensors="pt")
ids = tokens["input_ids"][0].tolist()   # список чисел

print("\n2. Токени (шматочки, на які розбито текст):")
print("   ", tokenizer.convert_ids_to_tokens(ids))

print("\n3. Числа (ID кожного токена):")
print("   ", ids)

# Модель перекладає: числа на вході → числа на виході.
output = model.generate(**tokens)
print("\n4. Числа, які видала модель:")
print("   ", output[0].tolist())

# Декодування: числа → текст.
result = tokenizer.decode(output[0], skip_special_tokens=True)
print("\n5. Готовий переклад:")
print("   ", result)
