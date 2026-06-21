import simplemma

LANGUAGES = ('ru', 'en', 'de', 'lt')

def lemmatize_text(text):
    """
    Multilingual lemmatizer supporting Russian (ru), English (en),
    German (de), and Lithuanian (lt).
    """
    if not isinstance(text, str):
        return ""
    # Extract lemmas from text
    tokens = simplemma.text_lemmatizer(text, lang=LANGUAGES)
    return " ".join(tokens)
