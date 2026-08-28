import easyocr
from ocr import recognize_text

reader = easyocr.Reader(['en'])  # Створюємо об'єкт easyocr.Reader для англійської 

def easy_ocr(path):
    """Відкриває зображення за шляхом path і повертає знайдений текст."""
    result = reader.readtext(path, detail=0)  # Розпізнаємо текст на зображенні
    return ' '.join(result)  # Об'єднуємо результати в один рядок

if __name__ == "__main__":
    print("Розпізнано за допомогою easyocr:")
    print(easy_ocr("capture.png"))
    print("Розпізнано за допомогою winocr:")
    print(recognize_text("capture.png"))
