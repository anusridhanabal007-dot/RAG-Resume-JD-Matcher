def calculate_final_score(similarity, skill_match):
    final_score = (similarity * 0.40) + (skill_match * 0.60)

    return round(final_score, 2)


semantic_similarity = 40.52
skill_match = 80.00

final_score = calculate_final_score(
    semantic_similarity,
    skill_match
)

print("Semantic Similarity:", semantic_similarity, "%")
print("Skill Match:", skill_match, "%")
print("Overall Match Score:", final_score, "%")