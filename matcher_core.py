def match_resume(resume_text, jd_text):

    print("Resume received by matcher")
    print("JD received by matcher")

    print("\nResume length:", len(resume_text))
    print("JD length:", len(jd_text))

    return {
        "semantic_similarity": 0,
        "matched_skills": [],
        "missing_skills": [],
        "skill_match": 0,
        "overall_score": 0,
        "recommendation": "TESTING"
    }