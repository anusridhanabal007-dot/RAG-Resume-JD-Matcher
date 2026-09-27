import uuid
import chromadb
from sentence_transformers import SentenceTransformer

from skill_matcher import match_skills
from scoring import calculate_overall_score, get_recommendation
from explanation import generate_explanation
from resume_writing_analyzer import analyze_resume_writing
from jd_analyzer import analyze_job_description


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="./chroma_db"
)


# --------------------------------------------------
# Main Resume Matching Function
# --------------------------------------------------

def match_resume(resume_text, jd_text):

    # --------------------------------------------------
    # Create temporary Chroma collection
    # --------------------------------------------------

    collection_name = "resume_" + str(uuid.uuid4()).replace("-", "")

    collection = client.create_collection(
        name=collection_name
    )

    # --------------------------------------------------
    # Split resume into chunks
    # --------------------------------------------------

    words = resume_text.split()

    chunks = []

    chunk_size = 100

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        chunks.append(chunk)

    # --------------------------------------------------
    # Create embeddings for resume chunks
    # --------------------------------------------------

    resume_embeddings = model.encode(
        chunks
    ).tolist()

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=resume_embeddings
    )

    # --------------------------------------------------
    # Create JD embedding
    # --------------------------------------------------

    jd_embedding = model.encode(
        [jd_text]
    ).tolist()[0]

    # --------------------------------------------------
    # Retrieve most relevant resume sections
    # --------------------------------------------------

    results = collection.query(
        query_embeddings=[jd_embedding],
        n_results=min(5, len(chunks))
    )

    documents = results["documents"][0]

    distances = results["distances"][0]

    # --------------------------------------------------
    # Convert distances to similarity
    # --------------------------------------------------

    similarities = [
        1 - distance
        for distance in distances
    ]

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

    semantic_similarity = round(
        best_similarity * 100,
        2
    )

    # --------------------------------------------------
    # Skill Matching
    # --------------------------------------------------

    matched_skills, missing_skills, skill_score = match_skills(
        jd_text,
        resume_text
    )

    skill_score = round(
        skill_score,
        2
    )

    # --------------------------------------------------
    # Overall Score
    # --------------------------------------------------

    overall_score = calculate_overall_score(
        semantic_similarity,
        skill_score
    )

    # Make sure score is numeric
    overall_score = float(
        overall_score
    )

    # --------------------------------------------------
    # Recommendation
    # --------------------------------------------------

    recommendation = get_recommendation(
        overall_score
    )

    # --------------------------------------------------
    # Explanation
    # --------------------------------------------------

    explanation = generate_explanation(
        semantic_similarity,
        matched_skills,
        missing_skills,
        skill_score,
        overall_score,
        recommendation
    )

    # --------------------------------------------------
    # Resume Writing Analysis
    # --------------------------------------------------

    writing_analysis = analyze_resume_writing(
        resume_text
    )

    # --------------------------------------------------
    # Job Description Analysis
    # --------------------------------------------------

    jd_analysis = analyze_job_description(
        jd_text
    )

    # --------------------------------------------------
    # Delete temporary Chroma collection
    # --------------------------------------------------

    try:

        client.delete_collection(
            name=collection_name
        )

    except Exception:

        pass

    # --------------------------------------------------
    # Return Results
    # --------------------------------------------------

    return {

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

        "retrieved_documents":
            documents,

        "distances":
            distances,

        "best_chunk":
            best_chunk,

        "strengths":
            explanation["strengths"],

        "improvements":
            explanation["improvements"],

        "recommended_skills":
            explanation["recommended_skills"],

        "summary":
            explanation["summary"],

        "writing_analysis":
            writing_analysis,

        "jd_analysis":
            jd_analysis
    }