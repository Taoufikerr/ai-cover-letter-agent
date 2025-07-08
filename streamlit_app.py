import streamlit as st
import fitz  # PyMuPDF
import os
import requests

# Gemini
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(
    model_name='models/gemini-1.5-pro-latest',
    safety_settings=[
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUAL", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    ]
)

prompt = "Write a cover letter for a React/Node.js job based on my resume."

if not prompt.strip():
    st.error("⚠️ Prompt is empty.")
else:
    try:
        response = model.generate_content(prompt)
        st.write(response.text)
    except Exception as e:
        st.error(f"❌ Gemini error: {e}")

# ✅ Before calling generate_content
if not prompt.strip():
    st.error("⚠️ Prompt is empty. Please enter valid input.")
else:
    try:
        response = model.generate_content(prompt)
        st.success("✅ Cover Letter Generated")
        st.write(response.text)
    except Exception as e:
        st.error(f"❌ Error generating content: {e}")

# Page config
st.set_page_config(page_title="AI Cover Letter Generator", page_icon="📝")

st.title("📝 AI Cover Letter Generator")

# Upload CV
uploaded_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])
job_description = st.text_area("Paste the Job Description", height=200)

if uploaded_file and job_description:
    # Extract text from PDF
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        cv_text = ""
        for page in doc:
            cv_text += page.get_text()

    st.success("✅ CV content extracted!")

    # Prompt Gemini
    prompt = f"""
    You are an expert career assistant. Generate a professional cover letter based on the candidate's CV and the job description.

    CV:
    {cv_text}

    Job Description:
    {job_description}

    Write a concise, enthusiastic cover letter tailored to this job.
    """

    with st.spinner("Generating cover letter..."):
        response = model.generate_content(prompt)
        letter = response.text

    st.subheader("📄 Generated Cover Letter:")
    st.write(letter)

    st.download_button("📥 Download as .txt", data=letter, file_name="cover_letter.txt", mime="text/plain")
