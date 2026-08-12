"""
Этап 5–6: потоки, очередь и детект изменений.
Медленную работу (захват + OCR) уносим в отдельный поток-работник,
а окно живёт в главном потоке и больше не подвисает.
Распознаём ТОЛЬКО когда кадр изменился (этап 6), а не без остановки.
"""

import hashlib      # для "отпечатка" кадра — сравнить, изменился ли он
import queue        # очередь — безопасная лента между потоками
import threading    # потоки — независимые линии выполнения
import time         # для пауз (sleep)
import tkinter as tk

import capture
from ocr import recognize_text

# --- Лента между потоками ---
# Работник кладёт сюда распознанный текст, окно забирает.
text_queue = queue.Queue()


def frame_hash():
    """Короткий "отпечаток" текущего снимка. Одинаковые кадры → одинаковый отпечаток."""
    with open("capture.png", "rb") as f:      # "rb" = читаем файл как байты
        return hashlib.md5(f.read()).hexdigest()


def worker():
    """Поток-работник: снимает по кругу, но распознаёт ТОЛЬКО когда кадр изменился."""
    last_hash = None   # отпечаток последнего РАСПОЗНАННОГО кадра
    while True:
        capture.capture_screen()
        current_hash = frame_hash()   # отпечаток нового кадра
        if current_hash != last_hash:
            text = recognize_text("capture.png")
            text_queue.put(text)
            last_hash = current_hash
        time.sleep(0.2)   # маленькая пауза, чтобы не грузить процессор впустую



def update_label():
    """Главный поток: заглядывает на ленту и обновляет надпись, если есть новое."""
    try:
        text = text_queue.get_nowait()   # взять, ЕСЛИ есть; иначе не ждать
        label.config(text=text)          # показать новый текст
    except queue.Empty:
        pass                             # лента пуста — оставляем прежний текст

    window.after(100, update_label)      # заглянуть на ленту снова через 100 мс


# --- Окно (главный поток) ---
window = tk.Tk()
window.overrideredirect(True)
window.attributes("-topmost", True)
window.attributes("-alpha", 0.85)
window.geometry("900x250+250+440")
label = tk.Label(window, text="жду текст...", font=("Arial", 20),
                 fg="white", bg="black", wraplength=880, justify="left")
label.pack()

# закрыть окно по клику (крестика нет)
window.bind("<Button-1>", lambda event: window.destroy())

# --- Запуск ---
# daemon=True: фоновый поток, умрёт вместе с программой (не будет держать её живой)
threading.Thread(target=worker, daemon=True).start()  # запустить работника в фоне
update_label()      # запустить регулярную проверку ленты
window.mainloop()   # главный цикл окна — теперь окно отзывчивое
