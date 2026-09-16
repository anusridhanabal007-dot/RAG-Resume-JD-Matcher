from sentence_transformers import SentenceTransformer
import re

# -----------------------------
# 1. Resume and Job Description
# -----------------------------

resume = """
Python developer with machine learning experience.
Skills: Python, SQL, Machine Learning, Power BI
"""

jd = """
We are looking for a Python developer with
machine learning and Flask experience.
"""

# -----------------------------
# 2. Load embedding model
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# 3. Convert Resume and JD
#    into embeddings
# -----------------------------

resume_embedding = model.encode(resume)
jd_embedding = model.encode(jd)

# -----------------------------
# 4. Calculate cosine similarity
# -----------------------------

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(
    [resume_embedding],
    [jd_embedding]
)[0][0]

print("Semantic Similarity:", round(float(similarity), 4))

# -----------------------------
# 5. Skill Matching
# -----------------------------

required_skills = [
    "Python",
    "Machine Learning",
    "Flask",
    "SQL"
]

matched_skills = []
missing_skills = []

for skill in required_skills:

    if re.search(r"\b" + re.escape(skill) + r"\b", resume, re.IGNORECASE):
        matched_skills.append(skill)
    else:
        missing_skills.append(skill)

# -----------------------------
# 6. Calculate skill match
# -----------------------------

skill_percentage = (
    len(matched_skills) / len(required_skills)
) * 100

# -----------------------------
# 7. Threshold
# -----------------------------

threshold = 0.70

if similarity >= threshold:
    result = "MATCH"
else:
    result = "NOT MATCH"

# -----------------------------
# 8. Final Result
# -----------------------------

print("\nJOB MATCHING RESULT")
print("--------------------")

print("Result:", result)

print("\nMatched Skills:")
for skill in matched_skills:
    print("✓", skill)

print("\nMissing Skills:")
for skill in missing_skills:
    print("✗", skill)

print("\nSkill Match:", round(skill_percentage, 2), "%")