import re
from collections import Counter


# ============================================================
# 1. ACTION VERBS
# ============================================================

ACTION_VERBS = [
    "developed",
    "created",
    "built",
    "designed",
    "implemented",
    "analyzed",
    "managed",
    "improved",
    "optimized",
    "automated",
    "tested",
    "deployed",
    "configured",
    "integrated",
    "processed",
    "visualized",
    "engineered",
    "led",
    "organized",
    "develop",
    "create",
    "build",
    "design",
    "implement",
    "analyze",
    "manage",
    "improve",
    "optimize",
    "automate",
    "test",
    "deploy",
    "configure",
    "integrate",
    "process",
    "visualize",
    "engineer",
    "lead",
    "organize",
    "conducted",
    "performed",
    "generated",
    "prepared",
    "presented",
    "maintained",
    "collaborated",
    "coordinated",
    "researched",
    "evaluated",
    "identified",
    "solved",
    "delivered",
]


# ============================================================
# 2. GENERIC / WEAK PHRASES
# ============================================================

GENERIC_PHRASES = [
    "hardworking",
    "team player",
    "passionate",
    "highly motivated",
    "quick learner",
    "self motivated",
    "self-motivated",
    "detail oriented",
    "detail-oriented",
    "strong communication skills",
    "excellent communication skills",
    "results driven",
    "results-driven",
    "dedicated professional",
    "responsible individual",
    "positive attitude",
    "good communication",
    "good leadership",
    "strong leadership",
    "strong interpersonal skills",
    "ability to work under pressure",
    "works well under pressure",
    "willingness to learn",
    "fast learner",
]


# ============================================================
# 3. AI-LIKE PHRASES
# ============================================================

AI_LIKE_PHRASES = [
    "passionate about leveraging",
    "proven track record",
    "dynamic professional",
    "results-driven professional",
    "highly motivated individual",
    "strong foundation in",
    "demonstrated ability to",
    "seeking to leverage",
    "committed to delivering",
    "driving meaningful impact",
    "leverage my skills",
    "utilize my skills",
    "cutting-edge technologies",
    "innovative solutions",
    "transformative solutions",
    "strategic thinker",
    "forward-thinking",
    "make a meaningful contribution",
]


# ============================================================
# 4. COMMON RESUME SECTIONS
# ============================================================

SECTION_PATTERNS = {
    "contact": [
        "contact",
        "phone",
        "mobile",
        "email",
        "linkedin",
        "github",
    ],
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "career objective",
        "objective",
    ],
    "education": [
        "education",
        "academic background",
        "academic qualifications",
        "qualification",
        "qualifications",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "technical expertise",
        "skills & technologies",
        "technologies",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship",
        "internships",
    ],
    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "project experience",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "licenses",
        "courses",
    ],
    "achievements": [
        "achievements",
        "awards",
        "honors",
        "accomplishments",
    ],
}


# ============================================================
# 5. CONTACT PATTERNS
# ============================================================

EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

PHONE_PATTERN = (
    r"(?<!\d)"
    r"(?:\+91[\s-]?)?"
    r"[6-9]\d{9}"
    r"(?!\d)"
)

LINKEDIN_PATTERN = r"(linkedin\.com|linkedin)"

GITHUB_PATTERN = r"(github\.com|github)"


# ============================================================
# 6. NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    text = text.lower()

    text = re.sub(
        r"[\n\r\t]+",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# 7. COUNT NUMBERS
# ============================================================

def count_numbers(text):

    return len(
        re.findall(
            r"\b\d+(?:\.\d+)?%?\b",
            text
        )
    )


# ============================================================
# 8. COUNT ACTION VERBS
# ============================================================

def count_action_verbs(text):

    text = normalize_text(text)

    count = 0

    for verb in ACTION_VERBS:

        pattern = (
            r"\b"
            + re.escape(verb)
            + r"\b"
        )

        count += len(
            re.findall(
                pattern,
                text
            )
        )

    return count


# ============================================================
# 9. FIND GENERIC PHRASES
# ============================================================

def find_generic_phrases(text):

    text = normalize_text(text)

    found = []

    for phrase in GENERIC_PHRASES:

        if phrase in text:

            found.append(
                phrase
            )

    return sorted(
        set(found)
    )


# ============================================================
# 10. FIND AI-LIKE PHRASES
# ============================================================

def find_ai_like_phrases(text):

    text = normalize_text(text)

    found = []

    for phrase in AI_LIKE_PHRASES:

        if phrase in text:

            found.append(
                phrase
            )

    return sorted(
        set(found)
    )


# ============================================================
# 11. FIND REPEATED PHRASES
# ============================================================

def count_repeated_phrases(text):

    words = normalize_text(
        text
    ).split()

    if len(words) < 20:

        return []

    phrases = []

    for i in range(
        len(words) - 2
    ):

        phrase = " ".join(
            words[i:i + 3]
        )

        phrases.append(
            phrase
        )

    frequency = Counter(
        phrases
    )

    repeated = [
        phrase
        for phrase, count
        in frequency.items()
        if count >= 2
    ]

    return sorted(
        repeated,
        key=lambda x: frequency[x],
        reverse=True
    )[:10]


# ============================================================
# 12. CALCULATE SPECIFICITY SCORE
# ============================================================

def calculate_specificity_score(
    text,
    number_count,
    action_verb_count
):

    words = max(
        len(
            normalize_text(text).split()
        ),
        1
    )

    number_score = min(
        40,
        (
            number_count
            / max(words / 100, 1)
        ) * 10
    )

    action_score = min(
        60,
        (
            action_verb_count
            / max(words / 100, 1)
        ) * 10
    )

    score = (
        number_score
        + action_score
    )

    return round(
        min(100, score),
        2
    )


# ============================================================
# 13. DETECT RESUME SECTIONS
# ============================================================

def detect_sections(text):

    normalized = normalize_text(
        text
    )

    detected_sections = []

    for section, patterns in SECTION_PATTERNS.items():

        for pattern in patterns:

            if re.search(
                r"\b"
                + re.escape(pattern)
                + r"\b",
                normalized
            ):

                detected_sections.append(
                    section
                )

                break

    return sorted(
        set(detected_sections)
    )


# ============================================================
# 14. SECTION COMPLETENESS
# ============================================================

def calculate_section_completeness(
    detected_sections
):

    important_sections = [
        "education",
        "skills",
        "experience",
        "projects",
    ]

    optional_sections = [
        "summary",
        "certifications",
        "achievements",
    ]

    important_found = sum(
        1
        for section in important_sections
        if section in detected_sections
    )

    optional_found = sum(
        1
        for section in optional_sections
        if section in detected_sections
    )

    important_score = (
        important_found
        / len(important_sections)
    ) * 70

    optional_score = (
        optional_found
        / len(optional_sections)
    ) * 30

    score = (
        important_score
        + optional_score
    )

    return round(
        min(100, score),
        2
    )


# ============================================================
# 15. DETECT BULLET POINTS
# ============================================================

def extract_bullet_lines(text):

    lines = text.splitlines()

    bullets = []

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        if re.match(
            r"^[•●▪◦\-–—*]\s+",
            stripped
        ):

            bullets.append(
                stripped
            )

    return bullets


# ============================================================
# 16. BULLET QUALITY ANALYSIS
# ============================================================

def analyze_bullet_quality(
    text
):

    bullets = extract_bullet_lines(
        text
    )

    if not bullets:

        return {
            "bullet_count": 0,
            "quality_score": 50.0,
            "strong_bullets": 0,
            "weak_bullets": 0,
        }

    strong_bullets = 0
    weak_bullets = 0

    for bullet in bullets:

        cleaned = re.sub(
            r"^[•●▪◦\-–—*]\s+",
            "",
            bullet
        )

        words = cleaned.split()

        lower = cleaned.lower()

        starts_with_action = any(
            re.match(
                r"^"
                + re.escape(verb)
                + r"\b",
                lower
            )
            for verb in ACTION_VERBS
        )

        has_number = bool(
            re.search(
                r"\b\d+(?:\.\d+)?%?\b",
                cleaned
            )
        )

        enough_detail = (
            len(words) >= 8
        )

        if (
            starts_with_action
            and (
                has_number
                or enough_detail
            )
        ):

            strong_bullets += 1

        else:

            weak_bullets += 1

    quality_score = (
        strong_bullets
        / len(bullets)
    ) * 100

    return {
        "bullet_count": len(bullets),
        "quality_score": round(
            quality_score,
            2
        ),
        "strong_bullets": strong_bullets,
        "weak_bullets": weak_bullets,
    }


# ============================================================
# 17. CONTACT INFORMATION ANALYSIS
# ============================================================

def analyze_contact_information(
    text
):

    email_found = bool(
        re.search(
            EMAIL_PATTERN,
            text
        )
    )

    phone_found = bool(
        re.search(
            PHONE_PATTERN,
            text
        )
    )

    linkedin_found = bool(
        re.search(
            LINKEDIN_PATTERN,
            text,
            re.IGNORECASE
        )
    )

    github_found = bool(
        re.search(
            GITHUB_PATTERN,
            text,
            re.IGNORECASE
        )
    )

    found_items = sum([
        email_found,
        phone_found,
        linkedin_found,
        github_found,
    ])

    score = (
        found_items / 4
    ) * 100

    return {
        "email": email_found,
        "phone": phone_found,
        "linkedin": linkedin_found,
        "github": github_found,
        "score": round(
            score,
            2
        ),
    }


# ============================================================
# 18. ACHIEVEMENT / IMPACT ANALYSIS
# ============================================================

def analyze_achievement_evidence(
    text
):

    normalized = normalize_text(
        text
    )

    impact_words = [
        "increased",
        "decreased",
        "reduced",
        "improved",
        "achieved",
        "saved",
        "generated",
        "delivered",
        "accuracy",
        "performance",
        "efficiency",
        "growth",
        "result",
        "results",
        "success",
        "successfully",
        "score",
        "percentage",
        "users",
        "records",
        "dataset",
        "projects",
    ]

    found_impact_words = []

    for word in impact_words:

        if re.search(
            r"\b"
            + re.escape(word)
            + r"\b",
            normalized
        ):

            found_impact_words.append(
                word
            )

    number_count = count_numbers(
        normalized
    )

    evidence_score = (
        min(
            50,
            len(found_impact_words) * 5
        )
        + min(
            50,
            number_count * 5
        )
    )

    return {
        "impact_words": sorted(
            set(found_impact_words)
        ),
        "impact_word_count": len(
            set(found_impact_words)
        ),
        "quantified_evidence": number_count,
        "achievement_score": round(
            min(100, evidence_score),
            2
        ),
    }


# ============================================================
# 19. WEAK WORDING ANALYSIS
# ============================================================

def analyze_weak_wording(
    text
):

    normalized = normalize_text(
        text
    )

    found = []

    for phrase in GENERIC_PHRASES:

        if phrase in normalized:

            found.append(
                phrase
            )

    weak_word_penalty = min(
        40,
        len(found) * 5
    )

    return {
        "weak_phrases": sorted(
            set(found)
        ),
        "weak_phrase_count": len(
            set(found)
        ),
        "penalty": weak_word_penalty,
    }


# ============================================================
# 20. RESUME WRITING QUALITY SCORE
# ============================================================

def calculate_writing_quality_score(
    section_score,
    bullet_score,
    specificity_score,
    contact_score,
    achievement_score,
    weak_word_penalty
):

    base_score = (
        section_score * 0.20
        + bullet_score * 0.20
        + specificity_score * 0.20
        + contact_score * 0.10
        + achievement_score * 0.30
    )

    final_score = (
        base_score
        - weak_word_penalty * 0.25
    )

    return round(
        max(
            0,
            min(
                100,
                final_score
            )
        ),
        2
    )


# ============================================================
# 21. WRITING QUALITY LEVEL
# ============================================================

def get_writing_quality_level(
    score
):

    if score >= 85:

        return "Excellent"

    elif score >= 70:

        return "Strong"

    elif score >= 50:

        return "Moderate"

    else:

        return "Needs Improvement"


# ============================================================
# 22. GENERATE WRITING SUGGESTIONS
# ============================================================

def generate_writing_suggestions(
    section_score,
    bullet_score,
    specificity_score,
    contact_score,
    achievement_score,
    weak_phrases,
    detected_sections
):

    suggestions = []

    if section_score < 75:

        suggestions.append(
            "Consider adding or improving important resume sections such as Education, Skills, Experience, or Projects."
        )

    if bullet_score < 70:

        suggestions.append(
            "Rewrite bullet points using strong action verbs and provide specific details about your work."
        )

    if specificity_score < 60:

        suggestions.append(
            "Add measurable details such as percentages, project size, accuracy, time saved, or number of users."
        )

    if contact_score < 75:

        suggestions.append(
            "Complete your contact information by adding relevant professional links such as LinkedIn or GitHub."
        )

    if achievement_score < 50:

        suggestions.append(
            "Highlight achievements and measurable outcomes instead of only describing responsibilities."
        )

    if weak_phrases:

        suggestions.append(
            "Replace generic phrases such as "
            + ", ".join(weak_phrases[:4])
            + " with specific evidence or achievements."
        )

    if "projects" not in detected_sections:

        suggestions.append(
            "Add a Projects section to demonstrate practical technical experience."
        )

    if "experience" not in detected_sections:

        suggestions.append(
            "Add internship, work, or practical experience details when applicable."
        )

    if not suggestions:

        suggestions.append(
            "The resume demonstrates good writing quality. Continue using specific achievements, measurable results, and strong action verbs."
        )

    return suggestions


# ============================================================
# 23. MAIN ANALYZER
# ============================================================

def analyze_resume_writing(
    text
):

    normalized = normalize_text(
        text
    )

    words = normalized.split()

    word_count = len(
        words
    )

    # --------------------------------------------------------
    # Existing analysis
    # --------------------------------------------------------

    number_count = count_numbers(
        normalized
    )

    action_verb_count = count_action_verbs(
        normalized
    )

    generic_phrases = find_generic_phrases(
        normalized
    )

    ai_like_phrases = find_ai_like_phrases(
        normalized
    )

    repeated_phrases = count_repeated_phrases(
        normalized
    )

    specificity_score = calculate_specificity_score(
        normalized,
        number_count,
        action_verb_count
    )

    generic_penalty = min(
        30,
        len(generic_phrases) * 5
    )

    ai_phrase_penalty = min(
        30,
        len(ai_like_phrases) * 5
    )

    repetition_penalty = min(
        20,
        len(repeated_phrases) * 2
    )

    ai_indicator_score = round(
        min(
            100,
            generic_penalty
            + ai_phrase_penalty
            + repetition_penalty
        ),
        2
    )

    human_indicator_score = round(
        min(
            100,
            specificity_score
            + min(
                number_count * 3,
                30
            )
            + min(
                action_verb_count * 2,
                30
            )
        ),
        2
    )

    # --------------------------------------------------------
    # Writing style
    # --------------------------------------------------------

    if specificity_score >= 70:

        writing_style = (
            "Specific and evidence-based"
        )

    elif specificity_score >= 40:

        writing_style = (
            "Moderately specific"
        )

    else:

        writing_style = (
            "Generic and needs more detail"
        )

    # --------------------------------------------------------
    # AI indicator level
    # --------------------------------------------------------

    if ai_indicator_score >= 60:

        ai_indicator_level = "High"

    elif ai_indicator_score >= 30:

        ai_indicator_level = "Moderate"

    else:

        ai_indicator_level = "Low"

    # --------------------------------------------------------
    # Human indicator level
    # --------------------------------------------------------

    if human_indicator_score >= 70:

        human_indicator_level = "Strong"

    elif human_indicator_score >= 40:

        human_indicator_level = "Moderate"

    else:

        human_indicator_level = "Limited"

    # ========================================================
    # NEW DAY 46 ANALYSIS
    # ========================================================

    # --------------------------------------------------------
    # Section detection
    # --------------------------------------------------------

    detected_sections = detect_sections(
        text
    )

    section_score = calculate_section_completeness(
        detected_sections
    )

    # --------------------------------------------------------
    # Bullet analysis
    # --------------------------------------------------------

    bullet_analysis = analyze_bullet_quality(
        text
    )

    bullet_score = bullet_analysis[
        "quality_score"
    ]

    # --------------------------------------------------------
    # Contact analysis
    # --------------------------------------------------------

    contact_analysis = analyze_contact_information(
        text
    )

    contact_score = contact_analysis[
        "score"
    ]

    # --------------------------------------------------------
    # Achievement analysis
    # --------------------------------------------------------

    achievement_analysis = analyze_achievement_evidence(
        text
    )

    achievement_score = achievement_analysis[
        "achievement_score"
    ]

    # --------------------------------------------------------
    # Weak wording
    # --------------------------------------------------------

    weak_wording = analyze_weak_wording(
        text
    )

    weak_phrases = weak_wording[
        "weak_phrases"
    ]

    weak_word_penalty = weak_wording[
        "penalty"
    ]

    # --------------------------------------------------------
    # Overall writing quality
    # --------------------------------------------------------

    writing_quality_score = calculate_writing_quality_score(
        section_score,
        bullet_score,
        specificity_score,
        contact_score,
        achievement_score,
        weak_word_penalty
    )

    writing_quality_level = get_writing_quality_level(
        writing_quality_score
    )

    # --------------------------------------------------------
    # Suggestions
    # --------------------------------------------------------

    suggestions = generate_writing_suggestions(
        section_score,
        bullet_score,
        specificity_score,
        contact_score,
        achievement_score,
        weak_phrases,
        detected_sections
    )

    # ========================================================
    # RETURN ALL ANALYSIS
    # ========================================================

    return {

        # ----------------------------------------------------
        # Existing analysis
        # ----------------------------------------------------

        "word_count":
            word_count,

        "number_count":
            number_count,

        "action_verb_count":
            action_verb_count,

        "generic_phrases":
            generic_phrases,

        "ai_like_phrases":
            ai_like_phrases,

        "repeated_phrases":
            repeated_phrases,

        "specificity_score":
            specificity_score,

        "ai_indicator_score":
            ai_indicator_score,

        "human_indicator_score":
            human_indicator_score,

        "ai_indicator_level":
            ai_indicator_level,

        "human_indicator_level":
            human_indicator_level,

        "writing_style":
            writing_style,

        # ----------------------------------------------------
        # Day 46 — Section analysis
        # ----------------------------------------------------

        "detected_sections":
            detected_sections,

        "section_score":
            section_score,

        # ----------------------------------------------------
        # Day 46 — Bullet analysis
        # ----------------------------------------------------

        "bullet_count":
            bullet_analysis[
                "bullet_count"
            ],

        "strong_bullets":
            bullet_analysis[
                "strong_bullets"
            ],

        "weak_bullets":
            bullet_analysis[
                "weak_bullets"
            ],

        "bullet_quality_score":
            bullet_score,

        # ----------------------------------------------------
        # Day 46 — Contact analysis
        # ----------------------------------------------------

        "email_found":
            contact_analysis[
                "email"
            ],

        "phone_found":
            contact_analysis[
                "phone"
            ],

        "linkedin_found":
            contact_analysis[
                "linkedin"
            ],

        "github_found":
            contact_analysis[
                "github"
            ],

        "contact_completeness_score":
            contact_score,

        # ----------------------------------------------------
        # Day 46 — Achievement analysis
        # ----------------------------------------------------

        "impact_words":
            achievement_analysis[
                "impact_words"
            ],

        "impact_word_count":
            achievement_analysis[
                "impact_word_count"
            ],

        "quantified_evidence":
            achievement_analysis[
                "quantified_evidence"
            ],

        "achievement_score":
            achievement_score,

        # ----------------------------------------------------
        # Day 46 — Weak wording
        # ----------------------------------------------------

        "weak_phrases":
            weak_phrases,

        "weak_phrase_count":
            weak_wording[
                "weak_phrase_count"
            ],

        # ----------------------------------------------------
        # Day 46 — Final writing quality
        # ----------------------------------------------------

        "writing_quality_score":
            writing_quality_score,

        "writing_quality_level":
            writing_quality_level,

        "writing_suggestions":
            suggestions,
    }

