from sentence_transformers import SentenceTransformer
import chromadb

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(
    name="resume_collection"
)

# Job Description
jd = """
We are looking for a Data Analyst with strong Python and SQL skills.
The candidate should have experience in data preprocessing,
data analysis, Power BI dashboards and data visualization.
"""

# Convert JD to embedding
jd_embedding = model.encode(jd).tolist()

# Retrieve top resume chunks
results = collection.query(
    query_embeddings=[jd_embedding],
    n_results=3
)

print("JOB DESCRIPTION:")
print(jd)

print("\nMATCHING RESULTS:\n")

for i in range(len(results["documents"][0])):

    distance = results["distances"][0][i]

    # For cosine distance
    similarity = 1 - distance

    print(f"Result {i + 1}")
    print("Resume Chunk:")
    print(results["documents"][0][i])

    print(f"Distance: {distance:.4f}")
    print(f"Similarity: {similarity:.4f}")

    print("-" * 50)