def calculate_overall_score(semantic_similarity, skill_match):
    overall_score = (
        semantic_similarity * 0.60
        + skill_match * 0.40
    )

    return round(overall_score, 2)


def get_recommendation(score):

    if score >= 75:
        return "STRONG MATCH"

    elif score >= 50:
        return "PARTIAL MATCH"

    else:
        return "LOW MATCH"