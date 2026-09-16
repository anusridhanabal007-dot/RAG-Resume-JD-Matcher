import re


# Skills that your Resume Matcher supports
SKILLS = [
    "python",
    "sql",
    "java",
    "c++",
    "c",
    "javascript",
    "html",
    "css",
    "flask",
    "django",
    "react",
    "machine learning",
    "deep learning",
    "data analysis",
    "data analytics",
    "data preprocessing",
    "data visualization",
    "power bi",
    "tableau",
    "mongodb",
    "mysql",
    "git",
    "docker",
    "aws",
    "kubernetes",
]


# Related terms / aliases
SKILL_ALIASES = {
    "data analytics": "data analysis",
    "data analyst": "data analysis",
    "data analysis": "data analysis",
    "exploratory analysis": "data analysis",
    "exploratory data analysis": "data analysis",
    "eda": "data analysis",

    "powerbi": "power bi",
    "machine-learning": "machine learning",

    "js": "javascript",
    "reactjs": "react",
}


def normalize_text(text):
    """
    Convert text into lowercase and normalize spaces.
    """
    text = text.lower()
    text = re.sub(r"[\n\r\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text


def find_skills(text):
    """
    Extract skills from text.
    """

    text = normalize_text(text)

    found_skills = set()

    for skill in SKILLS:

        # Special handling for C
        if skill == "c":
            pattern = r"\bc\b"

        else:
            pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.add(skill)

    # Check aliases
    for alias, standard_skill in SKILL_ALIASES.items():

        if re.search(
            r"\b" + re.escape(alias) + r"\b",
            text
        ):
            found_skills.add(standard_skill)

    return found_skills


def match_skills(jd_text, resume_text):

    jd_skills = find_skills(jd_text)
    resume_skills = find_skills(resume_text)

    matched_skills = sorted(
        jd_skills.intersection(resume_skills)
    )

    missing_skills = sorted(
        jd_skills - resume_skills
    )

    if len(jd_skills) > 0:
        skill_score = (
            len(matched_skills) /
            len(jd_skills)
        ) * 100

    else:
        skill_score = 0

    return (
        matched_skills,
        missing_skills,
        skill_score
    )