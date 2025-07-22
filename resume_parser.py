import fitz  # pymupdf
import docx
import re
import spacy
import subprocess
import importlib.util

# Auto-install en_core_web_sm if not found
def load_spacy_model():
    model = "en_core_web_sm"
    if not importlib.util.find_spec(model):
        subprocess.run(["python", "-m", "spacy", "download", model])
    return spacy.load(model)

nlp = load_spacy_model()

# ✅ For PDF files uploaded via Streamlit
def extract_text_from_pdf(file):
    # Read PDF from stream
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# ✅ For DOCX files uploaded via Streamlit
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# ✅ NLP Extraction (Skills, Education, Experience)
def extract_sections(text):
    doc = nlp(text.lower())

    # 🔹 Common technology & skill keywords
    skill_keywords = [
        "python", "java", "c++", "c", "html", "css", "javascript", "react", "node", "express",
        "django", "flask", "mysql", "mongodb", "sqlite", "sql", "excel", "power bi", "tableau",
        "tensorflow", "pytorch", "machine learning", "deep learning", "nlp", "data analysis",
        "data science", "git", "github", "linux", "bash", "cloud", "aws", "azure", "google cloud",
        "rest api", "bootstrap", "kubernetes", "docker"
    ]

    # 🔹 Skill Extraction
    found_skills = []
    for token in doc:
        if token.text in skill_keywords:
            found_skills.append(token.text)

    # 🔹 Project Titles (look for “project” followed by colon or name)
    project_titles = re.findall(r"(project\s*[:\-]?\s*[a-zA-Z0-9 \-]+)", text, re.IGNORECASE)

    # 🔹 Internship/Experience (look for “intern at” or “internship” or “worked at”)
    internships = re.findall(r"(intern(?:ship)?\s*(?:at)?\s*[a-zA-Z &]+)", text, re.IGNORECASE)
    experiences = re.findall(r"(worked\s+at\s+[a-zA-Z &]+|experience\s+in\s+[a-zA-Z &]+)", text, re.IGNORECASE)

    # 🔹 Education (degrees, optional)
    education = re.findall(r"(b\.tech|b\.sc|m\.tech|msc|bachelor|master|phd)", text, re.IGNORECASE)

    # 🔹 Experience Duration (e.g., "2 years", "6 months")
    durations = re.findall(r"\d+\s+(years?|months?)", text, re.IGNORECASE)

    return {
        "skills": list(set(found_skills)),
        "projects": list(set(project_titles)),
        "internships": list(set(internships)),
        "experience_roles": list(set(experiences)),
        "experience_duration": list(set(durations)),
        "education": list(set(education)),
    }
