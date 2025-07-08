
import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import tempfile

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Extract text from uploaded PDF
def extract_text_from_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        doc = fitz.open(tmp.name)
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()

# Extract keywords from job description (simple version)
def extract_keywords(text):
    words = text.lower().split()
    return list(set([w.strip(".,()") for w in words if len(w) > 3]))

# Generate the cover letter
def generate_cover_letter(cv_text, job_description, matched_keywords, tone="professional"):
    prompt = f"""
You are a career assistant.

Using the following user's CV and job description, write a personalized cover letter in a {tone} tone. 
Focus on these matched skills: {', '.join(matched_keywords)}.

### CV:
{cv_text}

### Job Description:
{job_description}

Start with "Dear Hiring Manager," and keep the letter under 250 words.
"""
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("📄 AI Cover Letter Generator")

uploaded_cv = st.file_uploader("Upload your CV (PDF only)", type="pdf")
job_description = st.text_area("Paste the job description here")
tone = st.selectbox("Select tone", ["professional", "confident", "enthusiastic"])

if uploaded_cv and job_description:
    with st.spinner("Reading CV..."):
        cv_text = extract_text_from_pdf(uploaded_cv)

    job_keywords = extract_keywords(job_description)
    matched_keywords = [word for word in job_keywords if word in cv_text.lower()]

    if st.button("Generate Cover Letter"):
        with st.spinner("Generating..."):
            cover_letter = generate_cover_letter(cv_text, job_description, matched_keywords, tone)
            st.success("✅ Done!")
            st.text_area("📄 Cover Letter Output", cover_letter, height=300)
