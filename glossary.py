""" Словник сленгу: нормалізуємо розмовну англійську перед перекладом. """

# розмовне → стандартне (nllb краще перекладає стандартну англійську)
SLANG = {
    "gonna": "going to",
    "wanna": "want to",
    "gotta": "got to",
    "kinda": "kind of",
    "gimme": "give me",
    "lemme": "let me",
    "dunno": "do not know",
    
}

def normalize(text):
    """Замінює сленгові слова на стандартні перед перекладом."""
    words = text.split()        
    result = []
    for word in words:
        word = word.lower()
        word = SLANG.get(word, word)
        result.append(word)
    return " ".join(result)      


if __name__ == "__main__":
    print(normalize("I'm gonna wanna eat, dunno kinda"))