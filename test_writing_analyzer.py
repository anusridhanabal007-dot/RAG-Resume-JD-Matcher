from resume_writing_analyzer import analyze_resume_writing


resume_text = """
Developed a Python data analysis project using Pandas and NumPy.
Analyzed 5000 customer records and improved data processing efficiency
by 25%.

Created a Power BI dashboard for sales analysis.
Implemented SQL queries using MySQL and visualized business trends.

I am a hardworking and passionate team player with strong communication
skills and a proven track record of success.
"""


result = analyze_resume_writing(resume_text)


print("\nRESUME WRITING ANALYSIS")
print("-" * 50)

print("Word Count:", result["word_count"])

print("Numbers:", result["number_count"])

print("Action Verbs:", result["action_verb_count"])

print("Specificity Score:", result["specificity_score"])

print(
    "AI-Writing Indicators:",
    result["ai_indicator_score"]
)

print(
    "Human-Writing Indicators:",
    result["human_indicator_score"]
)

print(
    "AI Indicator Level:",
    result["ai_indicator_level"]
)

print(
    "Human Indicator Level:",
    result["human_indicator_level"]
)

print(
    "Writing Style:",
    result["writing_style"]
)


print("\nGeneric Phrases:")

for phrase in result["generic_phrases"]:
    print(" -", phrase)


print("\nAI-Like Phrases:")

for phrase in result["ai_like_phrases"]:
    print(" -", phrase)


print("\nRepeated Phrases:")

for phrase in result["repeated_phrases"]:
    print(" -", phrase)