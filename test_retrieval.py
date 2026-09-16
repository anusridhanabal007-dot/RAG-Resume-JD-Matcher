import chromadb
from sentence_transformers import SentenceTransformer

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

# Get the collection
collection = client.get_collection(name="resume_collection")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Job Description / Query
query = "Python developer with Flask experience"

# Convert query into embedding
query_embedding = model.encode(query).tolist()

# Search ChromaDB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print("\nQuery:")
print(query)

print("\nRetrieved chunks:")
print(results)