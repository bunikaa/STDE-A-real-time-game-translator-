# Создание файла main.py


import capture
import time
import tkinter as tk
from ocr import recognize_text

window = tk.Tk()
window.overrideredirect(True)         # убрать рамку и заголовок
window.attributes("-topmost", True)   # всегда поверх других окон
window.attributes("-alpha", 0.85)     # прозрачность: 0 = невидимо, 1 = непрозрачно
window.geometry("900x250+250+600")
label = tk.Label(window, text="hely", font=("Arial",20),
fg="white", bg="black", wraplength=880, justify="left")
label.pack()
while True:

    capture.capture_screen()
    text = recognize_text("capture.png")
    label.config(text=text)
    window.update()
    time.sleep(0.5)

