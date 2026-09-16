from sentence_transformers import SentenceTransformer
import chromadb
import uuid

from skill_matcher import match_skills
from scoring import calculate_overall_score, get_recommendation
from explanation import generate_explanation
from resume_writing_analyzer import analyze_resume_writing


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="./chroma_db"
)


def match_resume(resume_text, jd_text):

    # ---------------------------------------------------------
    # 1. CREATE A TEMPORARY CHROMADB COLLECTION
    # ---------------------------------------------------------

    collection_name = (
        "resume_" + uuid.uuid4().hex[:8]
    )

    collection = client.create_collection(
        name=collection_name,
        metadata={
            "hnsw:space": "cosine"
        }
    )

    # ---------------------------------------------------------
    # 2. CHUNK RESUME
    # ---------------------------------------------------------

    words = resume_text.split()

    chunk_size = 100

    resume_chunks = []

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = " ".join(
            words[
                i:i + chunk_size
            ]
        )

        if chunk.strip():

            resume_chunks.append(
                chunk
            )

    print(
        "\nResume chunks created:",
        len(resume_chunks)
    )

    # ---------------------------------------------------------
    # 3. CREATE RESUME EMBEDDINGS
    # ---------------------------------------------------------

    if resume_chunks:

        embeddings = model.encode(
            resume_chunks
        ).tolist()

        ids = [
            f"chunk_{i}"
            for i in range(
                len(resume_chunks)
            )
        ]

        collection.add(
            ids=ids,
            documents=resume_chunks,
            embeddings=embeddings
        )

    print(
        "Resume chunks stored:",
        len(resume_chunks)
    )

    # ---------------------------------------------------------
    # 4. CREATE JD EMBEDDING
    # ---------------------------------------------------------

    jd_embedding = model.encode(
        jd_text
    ).tolist()

    print(
        "JD embedding size:",
        len(jd_embedding)
    )

    # ---------------------------------------------------------
    # 5. RETRIEVE MOST RELEVANT RESUME CHUNKS
    # ---------------------------------------------------------

    if resume_chunks:

        n_results = min(
            5,
            len(resume_chunks)
        )

        results = collection.query(
            query_embeddings=[
                jd_embedding
            ],
            n_results=n_results,
            include=[
                "documents",
                "distances"
            ]
        )

        documents = results[
            "documents"
        ][0]

        distances = results[
            "distances"
        ][0]

    else:

        documents = []
        distances = []

    print(
        "\nMOST RELEVANT RESUME CHUNKS:"
    )

    print(
        "-" * 60
    )

    similarities = []

    for i, (
        document,
        distance
    ) in enumerate(
        zip(
            documents,
            distances
        ),
        start=1
    ):

        similarity = 1 - distance

        similarity = max(
            0,
            min(
                1,
                similarity
            )
        )

        similarities.append(
            similarity
        )

        print(
            f"\nResult {i}"
        )

        print(
            "Resume Chunk:",
            document
        )

        print(
            f"Distance: {distance:.4f}"
        )

        print(
            f"Similarity: {similarity:.4f}"
        )

    # ---------------------------------------------------------
    # 6. FIND BEST SEMANTIC MATCH
    # ---------------------------------------------------------

    if similarities:

        best_similarity = max(
            similarities
        )

        best_index = similarities.index(
            best_similarity
        )

        best_chunk = documents[
            best_index
        ]

    else:

        best_similarity = 0

        best_chunk = ""

    print(
        "-" * 60
    )

    if best_chunk:

        print(
            "\nBEST MATCHING RESUME SECTION:"
        )

        print(
            best_chunk
        )

    semantic_similarity = (
        best_similarity * 100
    )

    semantic_similarity = round(
        semantic_similarity,
        2
    )

    print(
        f"\nSemantic Similarity: "
        f"{semantic_similarity}%"
    )

    # ---------------------------------------------------------
    # 7. SKILL MATCHING
    # ---------------------------------------------------------

    matched_skills, missing_skills, skill_score = match_skills(
        jd_text,
        resume_text
    )

    skill_score = round(
        skill_score,
        2
    )

    print(
        "\nMatched Skills:"
    )

    for skill in matched_skills:

        print(
            f"✓ {skill}"
        )

    print(
        "\nMissing Skills:"
    )

    for skill in missing_skills:

        print(
            f"✗ {skill}"
        )

    print(
        f"\nSkill Match: "
        f"{skill_score}%"
    )

    # ---------------------------------------------------------
    # 8. OVERALL JD MATCH SCORE
    # ---------------------------------------------------------

    overall_score = calculate_overall_score(
        semantic_similarity,
        skill_score
    )

    print(
        f"\nOverall Match Score: "
        f"{overall_score}%"
    )

    recommendation = get_recommendation(
        overall_score
    )

    print(
        f"Recommendation: "
        f"{recommendation}"
    )

    # ---------------------------------------------------------
    # 9. EXISTING MATCH EXPLANATION
    # ---------------------------------------------------------

    explanation = generate_explanation(
        semantic_similarity,
        matched_skills,
        missing_skills,
        skill_score,
        overall_score,
        recommendation
    )

    # ---------------------------------------------------------
    # 10. RESUME WRITING ANALYSIS
    # ---------------------------------------------------------

    print(
        "\nRESUME WRITING ANALYSIS"
    )

    print(
        "-" * 60
    )

    writing_analysis = analyze_resume_writing(
        resume_text
    )

    print(
        "Specificity Score:",
        writing_analysis[
            "specificity_score"
        ]
    )

    print(
        "AI-Writing Indicators:",
        writing_analysis[
            "ai_indicator_score"
        ]
    )

    print(
        "Human-Writing Indicators:",
        writing_analysis[
            "human_indicator_score"
        ]
    )

    print(
        "Writing Style:",
        writing_analysis[
            "writing_style"
        ]
    )

    print(
        "AI Indicator Level:",
        writing_analysis[
            "ai_indicator_level"
        ]
    )

    print(
        "Human Indicator Level:",
        writing_analysis[
            "human_indicator_level"
        ]
    )

    print(
        "Numbers Found:",
        writing_analysis[
            "number_count"
        ]
    )

    print(
        "Action Verbs:",
        writing_analysis[
            "action_verb_count"
        ]
    )

    # ---------------------------------------------------------
    # 11. RETURN ALL RESULTS
    # ---------------------------------------------------------

    return {

        # JD MATCHING
        "semantic_similarity":
            semantic_similarity,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "skill_score":
            skill_score,

        "overall_score":
            overall_score,

        "recommendation":
            recommendation,

        # RETRIEVAL
        "retrieved_documents":
            documents,

        "distances":
            distances,

        "best_chunk":
            best_chunk,

        # EXISTING EXPLANATION
        "strengths":
            explanation[
                "strengths"
            ],

        "improvements":
            explanation[
                "improvements"
            ],

        "recommended_skills":
            explanation[
                "recommended_skills"
            ],

        "summary":
            explanation[
                "summary"
            ],

        # RESUME WRITING ANALYSIS
        "writing_analysis":
            writing_analysis
    }