def generate_explanation(
    semantic_similarity,
    matched_skills,
    missing_skills,
    skill_score,
    overall_score,
    recommendation
):

    # --------------------------------------------------
    # Strengths
    # --------------------------------------------------

    strengths = []

    if semantic_similarity >= 70:
        strengths.append(
            "The resume has strong semantic relevance to the job description."
        )

    elif semantic_similarity >= 50:
        strengths.append(
            "The resume has moderate semantic relevance to the job description."
        )

    else:
        strengths.append(
            "The resume has limited semantic relevance to the job description."
        )

    if matched_skills:
        strengths.append(
            "The candidate has relevant skills: "
            + ", ".join(matched_skills)
            + "."
        )

    if skill_score >= 75:
        strengths.append(
            "The candidate matches most of the required technical skills."
        )

    elif skill_score >= 50:
        strengths.append(
            "The candidate matches several of the required technical skills."
        )

    # --------------------------------------------------
    # Areas to improve
    # --------------------------------------------------

    improvements = []

    if missing_skills:

        improvements.append(
            "Consider adding or developing these skills: "
            + ", ".join(missing_skills)
            + "."
        )

    if semantic_similarity < 50:

        improvements.append(
            "The resume could better highlight experience that directly "
            "relates to the responsibilities in the job description."
        )

    if skill_score < 50:

        improvements.append(
            "The resume is missing several important skills required by "
            "the job description."
        )

    if not improvements:

        improvements.append(
            "The resume has good alignment with the job description. "
            "Continue highlighting relevant projects and achievements."
        )

    # --------------------------------------------------
    # Recommended skills
    # --------------------------------------------------

    recommended_skills = missing_skills.copy()

    # --------------------------------------------------
    # Recruiter summary
    # --------------------------------------------------

    if overall_score >= 75:

        summary = (
            "The candidate appears to be a strong match for this role. "
            "The resume demonstrates strong alignment with the job "
            "requirements and contains several relevant skills."
        )

    elif overall_score >= 50:

        summary = (
            "The candidate appears to be a partial match for this role. "
            "The resume contains relevant skills and experience, but "
            "some requirements may need improvement."
        )

    else:

        summary = (
            "The candidate currently has a low match with this role. "
            "The resume may need additional relevant skills, experience, "
            "or better alignment with the job requirements."
        )

    # --------------------------------------------------
    # Return explanation
    # --------------------------------------------------

    return {
        "strengths": strengths,
        "improvements": improvements,
        "recommended_skills": recommended_skills,
        "summary": summary
    }