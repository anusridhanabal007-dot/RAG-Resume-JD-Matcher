import re

from skill_matcher import find_skills


def analyze_job_description(jd_text):

    text = jd_text.strip()

    # -----------------------------
    # Job Role
    # -----------------------------
    role = "Not specified"

    role_patterns = [
        r"(?:job title|role|position)\s*[:\-]\s*([^\n]+)",
        r"(?:looking for|seeking)\s+(?:a|an)?\s*([A-Za-z ]+(?:analyst|developer|engineer|scientist|manager))"
    ]

    for pattern in role_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            role = match.group(1).strip()
            break

    # -----------------------------
    # Required Skills
    # -----------------------------
    skills = sorted(find_skills(text))

    # -----------------------------
    # Experience
    # -----------------------------
    experience = "Not specified"

    experience_patterns = [
        r"\b\d+\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)",
        r"\b(?:experience|exp)[^.\n]{0,80}"
    ]

    for pattern in experience_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            experience = match.group(0).strip()
            break

    # -----------------------------
    # Education
    # -----------------------------
    education = "Not specified"

    education_patterns = [
        r"(?:bachelor'?s|b\.?tech|b\.?e\.?|degree)[^.\n]{0,100}",
        r"(?:master'?s|m\.?tech|m\.?e\.?|mba)[^.\n]{0,100}"
    ]

    for pattern in education_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            education = match.group(0).strip()
            break

    # -----------------------------
    # Responsibilities
    # -----------------------------
    responsibilities = []

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if (
            line.startswith("-")
            or line.startswith("•")
            or re.match(r"^\d+[\.\)]", line)
        ):
            responsibility = re.sub(
                r"^[-•\d\.\)]+\s*",
                "",
                line
            ).strip()

            if len(responsibility) > 10:
                responsibilities.append(responsibility)

    # Limit displayed responsibilities
    responsibilities = responsibilities[:8]

    return {
        "role": role,
        "skills": skills,
        "experience": experience,
        "education": education,
        "responsibilities": responsibilities
    }