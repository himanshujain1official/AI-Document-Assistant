import streamlit as st
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv


st.set_page_config(
    page_title="Smart AI Doc Assistant",
    page_icon="✨",
    layout="centered"
)

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


genai.configure(api_key=api_key)

st.markdown("""
<style>
    /* Gradient Header */
    .main-title {
        font-size: 3rem;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Subheader */
    .sub-title {
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }

    /* Custom Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 18px;
        border: none;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        width: 100%;
    }

    /* Button Hover Effect (Motion) */
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
        color: #fff;
    }

    /* Summary Card Styling */
    .summary-card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4ECDC4;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

def get_pdf_text(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_gemini_summary(text):
    model = genai.GenerativeModel("gemma-3-1b-it")
    prompt = f"""
    You are an expert document analyst. 
    Read the following text and provide a detailed summary in 5 bullet points.
    Make the output professional and easy to read.
    
    TEXT:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text


st.markdown('<div class="main-title">✨ AI Document Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Transform long PDFs into smart summaries in seconds.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📂 Upload your PDF file here", type=["pdf"])


if uploaded_file is not None:
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        
        process_btn = st.button("🚀 Analyze & Summarize", type="primary")

    if process_btn:
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("📖 Reading PDF...")
            progress_bar.progress(30)
            
            
            raw_text = get_pdf_text(uploaded_file)
            
            status_text.text("🤖 Consulting Gemini AI...")
            progress_bar.progress(70)
            
            
            summary_result = get_gemini_summary(raw_text)
            
            progress_bar.progress(100)
            status_text.empty() 
            progress_bar.empty() 
            
            
            st.toast("## 🎉 Analysis Complete!")

        
            st.markdown("### 📝 Smart Summary")
            st.markdown(f'<div class="summary-card">{summary_result}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")