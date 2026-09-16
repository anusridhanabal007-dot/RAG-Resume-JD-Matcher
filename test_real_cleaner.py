from parser.pdf_parser import extract_text_from_pdf
from cleaner.text_cleaner import clean_text

resume_path = "data/resume/Anusri_resume.pdf"

# Extract text from PDF
resume_text = extract_text_from_pdf(resume_path)

# Clean extracted text
cleaned_text = clean_text(resume_text)

print("CLEANED RESUME:")
print(cleaned_text)