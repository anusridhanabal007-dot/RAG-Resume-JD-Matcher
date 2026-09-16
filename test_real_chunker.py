from parser.pdf_parser import extract_text_from_pdf
from cleaner.text_cleaner import clean_text
from chunker.text_chunker import chunk_text

resume_path = "data/resume/Anusri_resume.pdf"

# Step 1: Extract PDF
resume_text = extract_text_from_pdf(resume_path)

# Step 2: Clean text
cleaned_text = clean_text(resume_text)

# Step 3: Create chunks
chunks = chunk_text(cleaned_text, chunk_size=50)

print("NUMBER OF CHUNKS:", len(chunks))

for i, chunk in enumerate(chunks, 1):
    print(f"\nChunk {i}:")
    print(chunk)