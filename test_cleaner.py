from cleaner.text_cleaner import clean_text


sample_text = """
ANUSRI D


Python     SQL
Java
"""


cleaned_text = clean_text(sample_text)

print(cleaned_text)