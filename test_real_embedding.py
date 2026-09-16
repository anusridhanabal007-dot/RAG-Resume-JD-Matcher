from parser.pdf_parser import extract_text_from_pdf
from cleaner.text_cleaner import clean_text
from chunker.text_chunker import chunk_text
from sentence_transformers import SentenceTransformer

# Resume path
resume_path = "data/resume/Anusri_resume.pdf"

# Step 1: Extract
resume_text = extract_text_from_pdf(resume_path)

# Step 2: Clean
cleaned_text = clean_text(resume_text)

# Step 3: Chunk
chunks = chunk_text(cleaned_text, chunk_size=50)

# Step 4: Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 5: Convert chunks into embeddings
embeddings = model.encode(chunks)

print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))

# Display first embedding
print("\nFirst chunk:")
print(chunks[0])

print("\nFirst embedding:")
print(embeddings[0])

print("\nEmbedding size:")
print(len(embeddings[0]))