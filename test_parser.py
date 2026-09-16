from parser.pdf_parser import extract_text_from_pdf

resume_text = extract_text_from_pdf(
    "data/resume/Anusri_resume.pdf"
)

print(resume_text)