"""
Этап 2: OCR — распознавание текста на картинке.
Читает capture.png и печатает найденный текст в консоль.
Использует встроенный в Windows движок распознавания (нейросеть).
"""

import winocr            # обёртка над встроенным в Windows движком OCR
from PIL import Image, ImageOps  # открывает картинку из файла (PIL = библиотека pillow)

LANG = "en"  # какой язык распознаём. Позже сделаем сменяемым.


def recognize_text(path):
    """Открывает картинку по пути path и возвращает найденный текст."""
    image = Image.open(path)  # открываем файл картинки в память
    image = preprocess(image)
    # отдаём картинку движку OCR. Он возвращает словарь, где значение
    # под ключом "text" — найденный текст одной строкой.
    result = winocr.recognize_pil_sync(image, LANG)

    return result["text"]

def preprocess(image):
    width, height = image.size
    new_width = width*2
    new_height = height*2
    image = image.resize((new_width, new_height))
    image = image.convert("L")
    image = ImageOps.invert(image)
    return image

if __name__ == "__main__":
    text = recognize_text("capture.png")
    print("Распознано:")
    print(text)
