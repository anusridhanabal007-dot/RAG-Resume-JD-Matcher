# RAG Resume–JD Matcher

An AI-powered Resume–Job Description Matcher that uses **Retrieval-Augmented Generation (RAG)** concepts and semantic similarity to compare resumes with job descriptions.

## Project Overview

Traditional resume screening often relies heavily on keyword matching. This project uses **text embeddings and vector similarity** to identify meaningful relationships between a candidate's resume and a job description.

The system extracts resume text, cleans and chunks the content, converts the text into numerical embeddings, stores the embeddings in a vector database, and calculates semantic similarity between the resume and job description.

## Problem Statement

Keyword-based resume screening can miss relevant candidates when the resume and job description use different words to describe similar skills.

For example:

* Resume: `Data visualization using Power BI`
* Job Description: `Experience creating business intelligence dashboards`

Although the wording is different, the concepts are related.

This project aims to improve matching by using **semantic similarity instead of relying only on exact keywords**.

## Features

* PDF resume text extraction
* Text cleaning and preprocessing
* Text chunking
* Sentence-transformer embeddings
* ChromaDB vector storage
* Semantic similarity matching
* Resume–JD matching score
* Flask-based web application
* Interactive dashboard
* Easy-to-use interface

## RAG Architecture

```text
Resume PDF
    ↓
Text Extraction
    ↓
Text Cleaning
    ↓
Text Chunking
    ↓
Text Embeddings
    ↓
ChromaDB Vector Database
    ↓
Job Description
    ↓
Job Description Embedding
    ↓
Cosine / Vector Similarity
    ↓
Matching Score
    ↓
Dashboard
```

## Technology Stack

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| Python                | Core programming language |
| Flask                 | Web application backend   |
| pdfplumber / PyPDF2   | PDF text extraction       |
| Pandas                | Data processing           |
| Sentence Transformers | Text embeddings           |
| ChromaDB              | Vector database           |
| NumPy                 | Numerical operations      |
| HTML/CSS/JavaScript   | Frontend                  |
| Git/GitHub            | Version control           |

## Project Structure

```text
RAG_Resume_JD_Matcher/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── parser.py
│   ├── cleaner.py
│   ├── chunker.py
│   └── embedder.py
│
├── data/
│   ├── resumes/
│   └── jd/
│
└── chroma_db/
```

## How the System Works

### 1. Resume Parsing

The system extracts text from the uploaded PDF resume.

### 2. Text Cleaning

Unnecessary spaces, symbols, and formatting noise are removed to create cleaner text.

### 3. Chunking

The extracted resume text is divided into smaller sections called chunks.

Chunking helps the system process and retrieve relevant information more effectively.

### 4. Embedding Generation

Each text chunk is converted into a numerical vector using a sentence-transformer model.

These vectors represent the semantic meaning of the text.

### 5. Vector Storage

The generated embeddings are stored in ChromaDB.

ChromaDB allows the system to efficiently store and retrieve vector representations.

### 6. Job Description Matching

The job description is also converted into an embedding.

The system compares the resume information with the job description using vector similarity.

### 7. Matching Score

The similarity results are used to generate a resume–JD matching score.

A higher similarity indicates stronger semantic alignment between the resume and job description.

## Installation

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd RAG_Resume_JD_Matcher
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask application:

```bash
python app.py
```

Then open the local URL displayed in the terminal, usually:

```text
http://127.0.0.1:5000
```

## Sample Workflow

```text
Upload Resume
      ↓
Enter Job Description
      ↓
Extract Resume Text
      ↓
Process Resume
      ↓
Generate Embeddings
      ↓
Compare Semantic Similarity
      ↓
Display Matching Results
```

## Sample Output

The dashboard provides a resume–job description matching result based on semantic similarity.

Example:

```text
Resume: Data Analyst Resume

Job Description:
Looking for a Data Analyst with Python, SQL,
Power BI and data visualization skills.

Matching Score: XX%
```

> The score shown depends on the resume and job description used during testing.

## Screenshots

Add screenshots of the working application here.

Recommended screenshots:

1. Home page
2. Resume upload
3. Job description input
4. Matching dashboard
5. Final matching result

Example:

```markdown
![Dashboard](screenshots/dashboard.png)
```

## Future Enhancements

* Multiple resume comparison
* Skill gap analysis
* Resume improvement suggestions
* Job recommendation system
* LLM-based explanation of matching results
* Support for multiple resume formats
* Advanced candidate ranking
* Cloud deployment
* Authentication and user accounts

## Resume Project Description

**RAG Resume–JD Matcher** — Developed an AI-powered resume screening system using semantic embeddings and vector similarity to compare resumes with job descriptions. Implemented PDF text extraction, preprocessing, chunking, embeddings, ChromaDB vector storage, and a Flask-based dashboard for semantic resume–JD matching.

## Key Learning Outcomes

Through this project, I learned:

* Natural Language Processing fundamentals
* Text preprocessing
* Text chunking
* Semantic embeddings
* Vector databases
* Similarity search
* RAG architecture concepts
* Flask web development
* Git and GitHub project management

## Author

**Anusri D**

B.Tech Artificial Intelligence and Data Science

Sri Sairam Institute of Technology
