from chunker.text_chunker import chunk_text

sample = """
Python SQL Java Machine Learning Power BI Excel Flask HTML CSS JavaScript
"""

chunks = chunk_text(sample, chunk_size=4)

for i, chunk in enumerate(chunks, 1):
    print(f"Chunk {i}:")
    print(chunk)
    print()