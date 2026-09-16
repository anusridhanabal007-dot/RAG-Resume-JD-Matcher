from resume_matcher import match_resume

resume_text = """
Python developer with machine learning experience.
Experience with Python, SQL and Power BI.
"""

jd_text = """
We are looking for a Data Analyst with strong Python and SQL skills.
The candidate should have experience in data preprocessing,
data analysis, Power BI dashboards and data visualization.
"""

result = match_resume(
    resume_text,
    jd_text
)

print("\n")
print("=" * 50)
print("TEST MATCHING RESULT")
print("=" * 50)

print(
    f"\nSemantic Similarity: "
    f"{result['semantic_similarity']:.2f}%"
)

print("\nMatched Skills:")
for skill in result["matched_skills"]:
    print(f"✓ {skill}")

print("\nMissing Skills:")
for skill in result["missing_skills"]:
    print(f"✗ {skill}")

print(
    f"\nSkill Match: "
    f"{result['skill_score']:.2f}%"
)

print(
    f"\nOverall Match Score: "
    f"{result['overall_score']:.2f}%"
)

print(
    f"Recommendation: "
    f"{result['recommendation']}"
)

print("=" * 50)