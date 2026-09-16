from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="resume_collection"
)

# Real resume chunks
chunks = [
    "ANUSRI D Third-year B.Tech student specializing in Artificial Intelligence and Data Science with strong foundational knowledge in Python, SQL, Java, and web technologies.",
    
    "Education Sri Sairam Institute of Technology B.Tech Artificial Intelligence and Data Science CGPA 9.20.",
    
    "Data Analyst Intern experience involving data preprocessing, cleaning, summarization, Google Colab and Power BI dashboards.",
    
    "MindfulAI Technologies Data Analyst Intern. Conducted data preprocessing and exploratory analysis and designed Power BI dashboards.",
    
    "Full Stack Intern. Worked on Visitor Management System using database structures, UML diagrams, ER diagrams and web application development.",
    
    "Skills: Python, SQL, C, Java, HTML, CSS, Git, VS Code, Power BI, Google Colab."
]

# Generate embeddings
embeddings = model.encode(chunks).tolist()

print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))
print("Embedding size:", len(embeddings[0]))

# Store in ChromaDB
collection.add(
    ids=[f"resume_chunk_{i+1}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings
)

print("\nResume embeddings stored successfully!")

# Check stored data
data = collection.get()

print("\nStored IDs:")
print(data["ids"])

print("\nStored documents:")
for doc in data["documents"]:
    print("-", doc)