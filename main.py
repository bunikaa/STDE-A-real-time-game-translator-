"""
Етап 5–6: потоки, черга і детект змін.
Повільну роботу (захоплення + OCR) виносимо в окремий потік-працівник,
а вікно живе в головному потоці й більше не підвисає.
Розпізнаємо ЛИШЕ коли кадр змінився (етап 6), а не без зупину.
"""

import hashlib      # для "відбитка" кадру — порівняти, чи він змінився
import queue        # черга — безпечна стрічка між потоками
import threading    # потоки — незалежні лінії виконання
import time         # для пауз (sleep)
import tkinter as tk

# ВАЖЛИВО: translator (torch) імпортуємо ПЕРШИМ серед бібліотек — інакше
# конфлікт системних DLL із winocr (в ocr) і аварійне падіння на Windows.
from translator import translate
import capture
from ocr import recognize_text

# --- Стрічка між потоками ---
# Працівник кладе сюди розпізнаний текст, вікно забирає.
text_queue = queue.Queue()


def frame_hash():
    """Короткий "відбиток" поточного знімка. Однакові кадри → однаковий відбиток."""
    with open("capture.png", "rb") as f:      # "rb" = читаємо файл як байти
        return hashlib.md5(f.read()).hexdigest()


def worker():
    """Потік-працівник: знімає по колу, але розпізнає ЛИШЕ коли кадр змінився."""
    last_hash = None   # відбиток останнього РОЗПІЗНАНОГО кадру
    while True:
        capture.capture_screen()
        current_hash = frame_hash()   # відбиток нового кадру
        if current_hash != last_hash:
            text = recognize_text("capture.png")
            text = translate(text) 
            text_queue.put(text)
            last_hash = current_hash
        time.sleep(0.2)   # маленька пауза, щоб не вантажити процесор даремно



def update_label():
    """Головний потік: заглядає на стрічку й оновлює напис, якщо є нове."""
    try:
        text = text_queue.get_nowait()   # взяти, ЯКЩО є; інакше не чекати
        label.config(text=text)          # показати новий текст
    except queue.Empty:
        pass                             # стрічка порожня — лишаємо попередній текст

    window.after(100, update_label)      # зазирнути на стрічку знову через 100 мс


# --- Вікно (головний потік) ---
window = tk.Tk()
window.overrideredirect(True)
window.attributes("-topmost", True)
window.attributes("-alpha", 0.85)
window.geometry("900x250+250+440")
label = tk.Label(window, text="чекаю текст...", font=("Arial", 20),
                 fg="white", bg="black", wraplength=880, justify="left")
label.pack()

# закрити вікно по кліку (хрестика немає)
window.bind("<Button-1>", lambda event: window.destroy())

# --- Запуск ---
# daemon=True: фоновий потік, помре разом із програмою (не триматиме її живою)
threading.Thread(target=worker, daemon=True).start()  # запустити працівника у фоні
update_label()      # запустити регулярну перевірку стрічки
window.mainloop()   # головний цикл вікна — тепер вікно чутливе
