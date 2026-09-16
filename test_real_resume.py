from parser.pdf_parser import extract_text_from_pdf

resume_path = "data/resume/Anusri_resume.pdf"

resume_text = extract_text_from_pdf(resume_path)

print("RESUME TEXT:")
print(resume_text)