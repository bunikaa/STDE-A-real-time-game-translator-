"""
Етап 2: OCR — розпізнавання тексту на зображенні.
Читає capture.png і друкує знайдений текст у консоль.
Використовує вбудований у Windows рушій розпізнавання (нейромережа).
"""

import winocr            # обгортка над вбудованим у Windows рушієм OCR
from PIL import Image, ImageOps  # відкриває зображення з файлу (PIL = бібліотека pillow)

LANG = "en"  # яку мову розпізнаємо. Пізніше зробимо змінною.


def recognize_text(path):
    """Відкриває зображення за шляхом path і повертає знайдений текст."""
    image = Image.open(path)  # відкриваємо файл зображення в пам'ять
    image = preprocess(image)
    # віддаємо зображення рушію OCR. Він повертає словник, де значення
    # під ключем "text" — знайдений текст одним рядком.
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
    print("Розпізнано:")
    print(text)
