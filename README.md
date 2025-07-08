# AI Cover Letter Agent ✉️🤖

Generate professional cover letters from your CV and a job description using Google Gemini.

## 🌟 Features
- Upload your CV (PDF)
- Paste job description
- Get an AI-generated cover letter
- Gemini 1.5 Pro API support
- Clean Streamlit UI

## 🚀 How to Use
1. Click "Upload CV" and upload your PDF.
2. Paste the job description in the textarea.
3. Let Gemini generate your custom cover letter.
4. Download and use it instantly!

## 📦 Deployment
This app is deployable on [Streamlit Cloud](https://streamlit.io/cloud).
Make sure to add your `GEMINI_API_KEY` to the Secrets tab in Streamlit settings.

## 🔐 Secrets Configuration
In your Streamlit Cloud settings, go to **Secrets** and add:
```
GEMINI_API_KEY = "your-key-here"
```

## 📁 Project Structure
- `streamlit_app.py`: main Streamlit application
- `requirements.txt`: dependencies
- `runtime.txt`: sets Python version for Streamlit Cloud
