import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
from fpdf import FPDF
import os

# ---------- CONFIG ----------
st.set_page_config(page_title="SmartLetter AI", layout="centered")
st.title("🧠 SmartLetter AI - Cover Letter Generator")
st.markdown("Generate personalized cover letters based on your **CV** and **job description**.")

# ---------- LANGUAGE SELECTOR ----------
language = st.selectbox("🌍 Select Language", ["English", "French", "Arabic"])

# ---------- GEMINI CONFIG ----------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-pro")

# ---------- PDF TEXT EXTRACTION ----------
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ---------- GENERATE PROMPT ----------
def build_prompt(cv_text, job_desc, lang):
    base = {
        "English": "Write a professional, concise cover letter in English for this job description. Base it on the candidate's CV.",
        "French": "Rédigez une lettre de motivation professionnelle et concise en français, basée sur le CV du candidat et l'offre d'emploi.",
        "Arabic": "اكتب رسالة تحفيزية احترافية ومختصرة باللغة العربية بناءً على السيرة الذاتية والوصف الوظيفي."
    }
    return f"{base[lang]}\n\n---\n\n📄 CV:\n{cv_text}\n\n💼 Job Description:\n{job_desc}"

# ---------- PDF DOWNLOAD ----------
def export_to_pdf(content, filename="SmartLetterAI_CoverLetter.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    return filename

# ---------- MAIN UI ----------
uploaded_cv = st.file_uploader("📎 Upload your CV (PDF only)", type=["pdf"])
job_description = st.text_area("🧾 Paste the Job Description", height=200)

if st.button("🚀 Generate Cover Letter"):
    if not uploaded_cv or not job_description.strip():
        st.error("Please upload a CV and provide a job description.")
    else:
        with st.spinner("Generating..."):
            cv_text = extract_text_from_pdf(uploaded_cv)
            prompt = build_prompt(cv_text, job_description, language)
            try:
                response = model.generate_content(prompt)
                cover_letter = response.text
                st.success("✅ Cover Letter Generated!")
                st.text_area("📄 Your Cover Letter", value=cover_letter, height=300)

                pdf_path = export_to_pdf(cover_letter)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_file,
                        file_name="cover_letter.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"❌ Gemini API Error: {e}")
