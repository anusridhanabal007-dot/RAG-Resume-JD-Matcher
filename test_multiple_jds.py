from skill_matcher import match_skills


resume_text = """
Third-year B.Tech student specializing in Artificial Intelligence
and Data Science with strong foundational knowledge in Python,
SQL, Java, data analytics, data preprocessing, Power BI,
data visualization and web technologies.

Experienced in data preprocessing, exploratory analysis,
Power BI dashboards and database management.
"""


jds = {

    "Data Analyst": """
    We are looking for a Data Analyst with strong Python and SQL
    skills. The candidate should have experience in data
    preprocessing, data analysis, Power BI dashboards and
    data visualization.
    """,

    "Python Developer": """
    We are looking for a Python Developer with Python, Flask,
    Django, REST API and SQL experience.
    """,

    "Machine Learning Engineer": """
    We are looking for a Machine Learning Engineer with Python,
    machine learning, deep learning, TensorFlow and AWS experience.
    """
}


for job_title, jd_text in jds.items():

    matched, missing, score = match_skills(
        jd_text,
        resume_text
    )

    print("\n")
    print("=" * 60)
    print(job_title)
    print("=" * 60)

    print("\nMatched Skills:")

    for skill in matched:
        print("✓", skill)

    if not matched:
        print("None")

    print("\nMissing Skills:")

    for skill in missing:
        print("✗", skill)

    if not missing:
        print("None")

    print(f"\nSkill Match: {score:.2f}%")