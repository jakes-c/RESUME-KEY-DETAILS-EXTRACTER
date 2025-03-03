import streamlit as st
import PyPDF2
import docx
import re
import io  # For handling uploaded files

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    with io.BytesIO(uploaded_file.read()) as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Function to extract text from DOCX
def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Function to extract email
def extract_email(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    matches = re.findall(email_pattern, text)
    return matches if matches else ["Not found"]

# Function to extract phone numbers
def extract_phone(text):
    phone_pattern = r"\b\d{10,13}\b"
    matches = re.findall(phone_pattern, text)
    return matches if matches else ["Not found"]

# Function to extract skills
def extract_skills(text):
    skill_keywords = ["Python", "Java", "JavaScript", "C++", "SQL", "Machine Learning", "Deep Learning", "React", "Django", "Flask"]
    skills_found = [skill for skill in skill_keywords if skill.lower() in text.lower()]
    return skills_found if skills_found else ["Not found"]

# Function to extract certifications
def extract_certifications(text):
    cert_patterns = [
        r"(?i)certifications?\s*[:\n]", 
        r"(?i)(\bAWS\b|\bGoogle Cloud\b|\bAzure\b|\bPMP\b|\bCisco\b).*certified"
    ]
    for pattern in cert_patterns:
        match = re.search(pattern, text)
        if match:
            cert_text = text[match.end():].strip()
            return [cert_text.split("\n")[0]]
    return ["Not found"]

# Function to extract projects
def extract_projects(text):
    project_patterns = [
        r"(?i)(?:projects?|project details)\s*[:\n]",  
        r"(?i)(?:academic project|major project|minor project)\s*[:\n]"
    ]
    for pattern in project_patterns:
        match = re.search(pattern, text)
        if match:
            project_text = text[match.end():].strip()
            project_text = re.split(r"\n\n|\n\s*\n", project_text)[0]  
            bullets = re.findall(r"[-•]\s*(.+)", project_text)
            return bullets if bullets else [project_text]
    return ["Not found"]

# Streamlit UI
st.title("📄 Resume Keyword Extractor")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]

    # Read text from the uploaded file
    if file_type == "pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        text = extract_text_from_docx(uploaded_file)

    # Extract information
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    projects = extract_projects(text)
    certifications = extract_certifications(text)

    # Display results
    st.subheader("📧 Extracted Email:")
    st.write(", ".join(email))

    st.subheader("📞 Extracted Phone Number:")
    st.write(", ".join(phone))

    st.subheader("🛠 Extracted Skills:")
    st.write(", ".join(skills))

    st.subheader("📜 Extracted Certifications:")
    st.write(", ".join(certifications))

    st.subheader("💼 Extracted Projects:")
    for project in projects:
        st.write(f"- {project}")
