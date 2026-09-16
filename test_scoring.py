from scoring import calculate_overall_score, get_recommendation


semantic_similarity = 50
skill_match = 80

overall_score = calculate_overall_score(
    semantic_similarity,
    skill_match
)

recommendation = get_recommendation(overall_score)

print("Semantic Similarity:", semantic_similarity, "%")
print("Skill Match:", skill_match, "%")
print("Overall Match Score:", overall_score, "%")
print("Recommendation:", recommendation)