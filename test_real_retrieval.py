from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Get existing collection
collection = client.get_collection(
    name="resume_collection"
)

# Job Description
jd = """
We are looking for a Data Analyst with strong Python and SQL skills.
The candidate should have experience in data preprocessing,
data analysis, Power BI dashboards and data visualization.
"""

print("JOB DESCRIPTION:")
print(jd)

# Convert JD into embedding
jd_embedding = model.encode(jd).tolist()

print("JD embedding size:", len(jd_embedding))

# Search ChromaDB
results = collection.query(
    query_embeddings=[jd_embedding],
    n_results=3
)

# Display results
print("\nMOST RELEVANT RESUME CHUNKS:\n")

for i in range(len(results["documents"][0])):

    print(f"Result {i + 1}:")
    print("Resume Chunk:")
    print(results["documents"][0][i])

    print("Distance:")
    print(results["distances"][0][i])

    print("-" * 50)