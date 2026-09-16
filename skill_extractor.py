SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "MySQL",
    "MongoDB",
    "Flask",
    "Django",
    "React",
    "HTML",
    "CSS",
    "JavaScript",
    "Bootstrap",
    "Power BI",
    "Tableau",
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "Data Science",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Git",
    "Docker",
    "AWS",
    "Azure",
    "Spring Boot"
]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills