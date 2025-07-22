import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_sections
from linkedin_scraper import scrape_jobs
from match_score import calculate_match
import pandas as pd

st.set_page_config(page_title="JobFit Analyzer", layout="wide", page_icon="📄")

# 🌙 Theme Toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Apply Theme
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            background-color: #121212 !important;
            color: #e0e0e0 !important;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #f0f0f0;
        }
        a {
            color: #00f2fe !important;
        }
        .info-box {
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 0 10px rgba(0,255,255,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            background-color: #f7f9fb !important;
            color: #1f1f1f !important;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
        }
        a {
            color: #0073b1 !important;
        }
        .info-box {
            background-color: #ffffff;
            border-left: 5px solid #2980b9;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
        }
        </style>
    """, unsafe_allow_html=True)

# Theme Toggle Button
st.sidebar.button("🌗 Toggle Dark Mode", on_click=toggle_theme)

# Assistant Sidebar
st.sidebar.markdown("#### 🤖 JobFit Assistant Guide")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/10290/10290594.png", width=80)
st.sidebar.markdown("""
📄 **Upload your resume** in PDF or DOCX format.  
🔍 **Our system will extract your skills, experience, education, and projects.**  
🎯 Click "Find Matching Jobs" to see job roles tailored to your resume.  
📥 Download a full report or apply directly.

💡 *Tips:*  
- Use common tech terms (e.g., Python, SQL, React).  
- Mention real projects and internships.
""")

st.markdown("""
<h1 style='text-align:center;'>📄 JobFit Analyzer</h1>
<p style='text-align:center;'>💼 AI-Powered Resume & Job Matching Assistant for Students and Recruiters 🚀</p>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("✨ Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("🔍 Extracting resume details..."):
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_docx(uploaded_file)

        parsed_data = extract_sections(text)

    st.markdown("""
        <div class='info-box'>
            <h4>🧠 Extracted Resume Details</h4>
        </div>
    """, unsafe_allow_html=True)
    st.json(parsed_data)

    if st.button("🚀 Find Matching Jobs in India"):
        with st.spinner("🔗 Connecting to job database & analyzing your profile..."):
            job_df = scrape_jobs(parsed_data)

        if job_df.empty:
            st.warning("😕 No jobs found. Try updating your resume or use broader skills.")
        else:
            st.success(f"🎯 Found {len(job_df)} curated jobs matching your resume skills!")

            # Match scoring
            match_scores = calculate_match(parsed_data["skills"], job_df["title"])
            match_df = pd.DataFrame(match_scores)
            job_df["Match Score (%)"] = match_df["match_score"]

            # Theme-aware job card styling
            if st.session_state.dark_mode:
                card_style = """
                    background-color: rgba(40, 40, 40, 0.8);
                    color: #f0f0f0;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                """
            else:
                card_style = """
                    background-color: #ffffff;
                    color: #000;
                    border: 1px solid #e0e0e0;
                """

            for _, row in job_df.iterrows():
                st.markdown(f"""
                    <div style='{card_style} padding:15px; margin:10px 0; border-radius:12px;
                                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); transition: all 0.3s ease;'>
                        <h4 style='margin-bottom:5px;'>💼 {row['title']}</h4>
                        <p><b>🏢 Company:</b> {row['company']} | <b>📍 Location:</b> {row['location']} | 
                        <b>📊 Match:</b> {row['Match Score (%)']}%</p>
                        <a href='{row['job_link']}' target='_blank'>🔗 Apply Now</a>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("""
                <div class='info-box'>
                    <h4>📥 Download Full Job Match Report</h4>
                </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label="Download as CSV",
                data=job_df.to_csv(index=False),
                file_name="job_matches.csv",
                mime="text/csv"
            )
else:
    st.info("👈 Upload your resume to get started and discover opportunities designed for your skills.")
