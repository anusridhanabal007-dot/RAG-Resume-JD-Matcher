from skill_extractor import extract_skills


jd = """
We are looking for a Data Analyst with strong Python
and SQL skills. The candidate should have experience
in Power BI, Machine Learning and Flask.
"""

skills = extract_skills(jd)

print("Extracted Skills:")

for skill in skills:
    print("✓", skill)