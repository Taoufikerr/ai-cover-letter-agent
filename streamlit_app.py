import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import os

# -------------------- SETUP --------------------
st.set_page_config(page_title="AI Cover Letter Generator", layout="wide")

st.title("📄 AI Cover Letter Generator with Gemini")
st.write("Upload your CV and paste a job description. Let Gemini write your tailored cover letter.")

# -------------------- GEMINI CONFIG --------------------
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("❌ Missing Gemini API key. Please set 'GEMINI_API_KEY' in Streamlit secrets.")
    st.stop()

# Load Gemini model
model = genai.GenerativeModel("models/gemini-1.5-pro")

# -------------------- FILE UPLOAD --------------------
uploaded_file = st.file_uploader("📎 Upload your CV (PDF)", type="pdf")

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

cv_text = ""
if uploaded_file:
    cv_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ CV text extracted successfully.")

# -------------------- JOB DESCRIPTION --------------------
job_description = st.text_area("💼 Paste the Job Description here", height=200)

# -------------------- GENERATE BUTTON --------------------
if st.button("🚀 Generate Cover Letter"):
    if not cv_text or not job_description:
        st.warning("⚠️ Please upload a CV and paste a job description.")
        st.stop()

    prompt = f"""
You are an expert career assistant. Based on the resume text and the job description below, write a personalized, professional, and concise cover letter tailored to the job.

Resume:
\"\"\"
{cv_text[:15000]}  # trimmed to avoid token limits
\"\"\"

Job Description:
\"\"\"
{job_description}
\"\"\"

Cover Letter:
"""

    try:
        response = model.generate_content(prompt)
        generated_letter = response.text
        st.subheader("📬 Generated Cover Letter")
        st.write(generated_letter)

        # Optional download button
        st.download_button("📩 Download as .txt", generated_letter, file_name="cover_letter.txt")

    except Exception as e:
        st.error(f"❌ Gemini API Error: {e}")

