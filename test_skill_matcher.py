from skill_matcher import match_skills


jd = """
We are looking for a Data Analyst with strong Python
and SQL skills. The candidate should have experience
in Power BI, Machine Learning and Flask.
"""

resume = """
Third-year B.Tech student with strong knowledge
of Python, SQL, Java and Power BI.
"""

matched, missing, score = match_skills(jd, resume)


print("Matched Skills:")

for skill in matched:
    print("✓", skill)


print("\nMissing Skills:")

for skill in missing:
    print("✗", skill)


print("\nSkill Match:", score, "%")