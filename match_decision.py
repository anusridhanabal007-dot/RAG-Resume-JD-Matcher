def get_match_result(score):

    if score >= 80:
        return "Strong Match"

    elif score >= 60:
        return "Good Match"

    elif score >= 40:
        return "Partial Match"

    else:
        return "Low Match"


score = 64.21

result = get_match_result(score)

print("Overall Match Score:", score, "%")
print("Recommendation:", result)