"""
Етап 2: OCR — розпізнавання тексту на зображенні.
Читає capture.png і друкує знайдений текст у консоль.
"""

import easyocr


LANG = "en"  # яку мову розпізнаємо. Пізніше зробимо змінною.
reader = easyocr.Reader([LANG])  # Створюємо об'єкт easyocr.Reader для англійської

def recognize_text(path):
    """Відкриває зображення за шляхом path і повертає знайдений текст."""
    result = reader.readtext(path, detail=0)  # Розпізнаємо текст на зображенні
    return ' '.join(result)  # Об'єднуємо результати в один рядок

if __name__ == "__main__":
    text = recognize_text("capture.png")
    print("Розпізнано:")
    print(text)
