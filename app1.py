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
            border-left: 5px solid #00f2fe;
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
            background-color: #eef3f7 !important;
            color: #222 !important;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
        }
        a {
            color: #0073b1 !important;
        }
        .info-box {
            background: linear-gradient(145deg, #f0f0f3, #d2d2d4);
            border-left: 5px solid #2980b9;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 4px 4px 12px rgba(0,0,0,0.05);
        }
        </style>
    """, unsafe_allow_html=True)

# Theme Toggle Button
st.sidebar.button("🌗 Toggle Dark Mode", on_click=toggle_theme)

# Assistant Sidebar
st.sidebar.markdown("#### 🤖 JobFit Assistant")
st.sidebar.info("✅ Upload a detailed resume to get better job matches\n\n📌 Add keywords like 'SQL', 'Excel', 'React', etc.\n\n💡 Use action verbs in your experience section!")

st.markdown("""<h1 style='text-align:center;'>📄 JobFit Analyzer</h1>""", unsafe_allow_html=True)
st.markdown("""<p style='text-align:center;'>AI-Powered Resume Parser & LinkedIn Job Matcher for Gen-Z Talent & Recruiters 🚀</p>""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("✨ Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("🔍 Extracting resume details..."):
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_docx(uploaded_file)

        parsed_data = extract_sections(text)

    st.markdown("""<div class='info-box'><b>✅ Extracted Resume Details</b></div>""", unsafe_allow_html=True)
    st.json(parsed_data)

    if st.button("🚀 Find Matching Jobs in India"):
        with st.spinner("Connecting with LinkedIn... Fetching best job matches for you 💼"):
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
                                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);'>
                        <h4 style='margin-bottom:5px;'>{row['title']}</h4>
                        <p><b>Company:</b> {row['company']} | <b>Location:</b> {row['location']} | 
                        <b>Match:</b> {row['Match Score (%)']}%</p>
                        <a href='{row['job_link']}' target='_blank'>🔗 Apply Now</a>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("""<div class='info-box'><b>📥 Download Full Job Match Report</b></div>""", unsafe_allow_html=True)
            st.download_button(
                label="Download as CSV",
                data=job_df.to_csv(index=False),
                file_name="job_matches.csv",
                mime="text/csv"
            )
else:
    st.info("👈 Upload your resume to get started and discover opportunities designed for your skills.")
