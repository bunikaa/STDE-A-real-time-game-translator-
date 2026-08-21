""" Оцінка якості нашого перекладу за допомоги використання моделі"""


import time

from translator import translate


test_set = [
    ("We once tamed it in what became one of the strangest, "
   "most wonderful journeys of our lives...", "Колись ми приборкали це в тому, що стало однією з найдивніших,"
    " найпрекрасніших подорожей у нашому житті.."),
    ("...back then, when we were young and unafraid.",
     "...тоді, коли ми були молодими і нічого не боялися"),
    ("Summer was coming to an end when Polly and Scott planned a road trip.", 
     "Літо наближалося до завершення, коли Поллі та Скотт планували автомобільну подорож."),
    ("The whole thing was bound to go off rails; this was the Prank Masterz, after all:",
     "Усе це мало піти не так; зрештою, це були Prank Masterz:")]

for english, reference in test_set:
    result = translate(english)
    print("вхідний текст: ", english,
           "\nпереклад: ", result, "\nеталон: ", reference)
    