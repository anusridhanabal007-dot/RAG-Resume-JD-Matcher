import chromadb
from sentence_transformers import SentenceTransformer

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

# Get resume collection
collection = client.get_collection(name="resume_collection")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Job Description
jd = """
We are looking for a Python developer with
machine learning and Flask experience.
"""

# Convert JD into embedding
jd_embedding = model.encode(jd).tolist()

# Search resume embeddings
results = collection.query(
    query_embeddings=[jd_embedding],
    n_results=3
)

print("\nJOB DESCRIPTION:")
print(jd)

print("\nMATCHING RESUME CHUNKS:")

for i, document in enumerate(results["documents"][0], 1):
    distance = results["distances"][0][i - 1]

    print(f"\nResult {i}:")
    print("Resume Chunk:", document)
    print("Distance:", distance)