import streamlit as st
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------- Load API Key Securely -----------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API key not found. Please set it in .env file.")
    st.stop()
os.environ["GOOGLE_API_KEY"] = api_key

# ----------------- LLM Setup -----------------
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
template = """
Extract the following information from the resume.

1 Name
2 Address
3 Contact
4 List of Projects

Give output in exactly 4 lines like this:

Name:
Address:
Contact:
Projects:

Resume:
{resume}
"""
prompt = PromptTemplate(input_variables=["resume"], template=template)
parser = StrOutputParser()
chain = prompt | llm | parser

# ----------------- Page Config -----------------
st.set_page_config(page_title="Resume Lens", layout="wide", page_icon="🔍")

# ----------------- Sidebar -----------------
st.sidebar.title("🔍 Resume Lens ")
st.sidebar.info("Paste your resume and click Extract Info.\nProfessional AI-powered resume extractor.")
theme = st.sidebar.radio("Theme", ["Light", "Dark"])
st.sidebar.markdown("""
**Features:**
- AI-powered extraction
- Summary & Projects Tabs
- Collapsible Project Cards
- Copy & Download
- Dark/Light Theme
- Modern Dashboard Look
""")

# ----------------- Theme CSS (Fixed Text Visibility) -----------------
if theme == "Dark":
    bg_color = "#121212"
    text_color = "white"
    card_bg = "#1e1e1e"
    card_text = "white"
    card_shadow = "2px 2px 15px rgba(0,255,255,0.3)"
    button_bg = "#00bfa5"
    button_hover = "#008e76"
else:
    bg_color = "#f0f2f6"
    text_color = "#000000"
    card_bg = "#ffffff"
    card_text = "#000000"
    card_shadow = "2px 2px 15px rgba(0,0,0,0.1)"
    button_bg = "#00796b"
    button_hover = "#004d40"

st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
    color: {text_color};
    font-family: 'Segoe UI', sans-serif;
}}
.stButton>button {{
    background-color: {button_bg};
    color: white;
    font-weight: bold;
    border-radius: 10px;
}}
.stButton>button:hover {{
    background-color: {button_hover};
}}
.card {{
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 10px;
    background-color: {card_bg};
    color: {card_text};
    box-shadow: {card_shadow};
    transition: transform 0.2s;
}}
.card:hover {{
    transform: scale(1.03);
}}
.expander-content {{
    background-color: {card_bg};
    color: {card_text};
}}
code {{
    color: {card_text} !important;
    background-color: {card_bg} !important;
}}
</style>
""", unsafe_allow_html=True)
# ----------------- Header -----------------
st.markdown(f"<h1 style='text-align:center;color:{text_color}'>🔍 Resume Lens - AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;color:{text_color}'>Extract summaries and projects from any resume like a professional AI agent.</p>", unsafe_allow_html=True)

# ----------------- Columns Layout -----------------
col1, col2 = st.columns([1,2])

with col1:
    resume_text = st.text_area("Paste Your Resume Here:", height=400)
    extract_btn = st.button("Extract Information")

with col2:
    if extract_btn:
        if not resume_text.strip():
            st.warning("Please paste your resume first.")
        else:
            with st.spinner("🔍 Resume Lens is processing your resume..."):
                result = chain.invoke({"resume": resume_text})

            lines = [line.strip() for line in result.split("\n") if line.strip() != ""]
            info_dict = {}
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    info_dict[key.strip()] = value.strip()

            # ----------------- Tabs -----------------
            tab1, tab2 = st.tabs(["📋 Summary", "📝 Projects"])

            # ----------------- Summary Tab -----------------
            with tab1:
                st.subheader("✅ Extracted Summary")
                for key in ["Name","Address","Contact","Projects"]:
                    if key in info_dict:
                        st.markdown(f"<div class='card'><strong>{key}:</strong> {info_dict[key]}</div>", unsafe_allow_html=True)
                summary_text = "\n".join([f"{key}: {info_dict[key]}" for key in info_dict])
                st.code(summary_text, language="text")
                st.download_button("📥 Download Summary", summary_text, "resume_summary.txt")
                st.download_button(
                    label="📥 Download in JSON",
                    data=json.dumps(info_dict, indent=2),
                    file_name="resume_summary.txt",
                    mime="text/plain"
                )
            # ----------------- Projects Tab -----------------
            with tab2:
                st.subheader("📝 Projects")
                if "Projects" in info_dict:
                    projects = [proj.strip() for proj in info_dict["Projects"].split(",")]
                    for i, proj in enumerate(projects, 1):
                        with st.expander(f"Project {i} ✅"):
                            st.markdown(f"<div class='card'>{proj}</div>", unsafe_allow_html=True)
                            st.info("Add tools, technologies, or notes here.")
                else:
                    st.info("No projects found in the extracted data.")