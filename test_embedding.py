from embedder.embedding_model import create_embedding

text = "Python developer with machine learning experience"

embedding = create_embedding(text)

print("Embedding:")
print(embedding)

print("\nNumber of values:", len(embedding))