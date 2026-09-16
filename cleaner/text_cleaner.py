import re


def clean_text(text):

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove unwanted characters
    text = re.sub(r'[^a-zA-Z0-9\s.,@+-]', '', text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text