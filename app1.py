import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_sections
from linkedin_scraper import scrape_jobs
from match_score import calculate_match, calculate_resume_score
import pandas as pd

st.set_page_config(page_title="JobFit Analyzer", layout="wide", page_icon="📄")

# 🌙 Theme Toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Apply Theme Styles
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            background-color: #121212 !important;
            color: #f5f5f5 !important;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff;
        }
        a { color: #00f2fe !important; }
        .info-box, .job-card {
            background-color: #1e1e1e !important;
            color: #f0f0f0;
            border: 1px solid #333;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            box-shadow: 0px 4px 12px rgba(0, 255, 255, 0.05);
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            background-color: #ffffff !important;
            color: #2c3e50 !important;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
        }
        a { color: #0073b1 !important; }
        .info-box, .job-card {
            background-color: #f9f9f9;
            color: #222;
            border: 1px solid #eaeaea;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.03);
        }
        </style>
    """, unsafe_allow_html=True)

# Sidebar Assistant
st.sidebar.button("🌗 Toggle Dark Mode", on_click=toggle_theme)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/10290/10290594.png", width=70)
st.sidebar.markdown("### 🤖 JobFit Assistant")
st.sidebar.markdown("""
**Step 1**: Upload your resume (PDF/DOCX)  
**Step 2**: We extract your skills, experience, projects  
**Step 3**: Click **Find Jobs** to match your profile  
**Step 4**: Download a full report or apply directly  
---
💡 *Tips:*  
- Include real-world projects or internships  
- Add key skills like SQL, Excel, Python, etc.
""")

# Title & Description
st.markdown("<h1 style='text-align:center;'>📄 JobFit Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>💼 Smart Resume Matcher & Job Finder for Students and Recruiters</p>", unsafe_allow_html=True)

# Upload Resume
uploaded_file = st.file_uploader("✨ Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("🔍 Parsing your resume..."):
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_docx(uploaded_file)
        parsed_data = extract_sections(text)

    st.markdown("<div class='info-box'><h4>🧠 Extracted Resume Details</h4></div>", unsafe_allow_html=True)
    st.json(parsed_data)

    if st.button("🚀 Find Matching Jobs in India"):
        with st.spinner("🔗 Searching job listings..."):
            job_df = scrape_jobs(parsed_data)

        if job_df.empty:
            st.warning("😕 No jobs found. Try a more complete resume.")
        else:
            st.success(f"🎯 {len(job_df)} matching job(s) found for your resume!")

            # Add match score per job
            match_scores = calculate_match(parsed_data["skills"], job_df["title"])
            match_df = pd.DataFrame(match_scores)
            job_df["Match Score (%)"] = match_df["match_score"]

            # Resume rating out of 100
            rating, breakdown = calculate_resume_score(parsed_data, job_df["title"])
            st.markdown(f"<div class='info-box'><h4>📊 Resume Rating: {rating} / 100</h4></div>", unsafe_allow_html=True)

            with st.expander("🔍 See rating breakdown"):
                for k, v in breakdown.items():
                    st.markdown(f"- **{k}**: {int(v)} / {100 if k == 'Skills' else 20}")

            # Show job cards
            for _, row in job_df.iterrows():
                st.markdown(f"""
                    <div class='job-card'>
                        <h4>💼 {row['title']}</h4>
                        <p><b>🏢 Company:</b> {row['company']}<br>
                        <b>📍 Location:</b> {row['location']}<br>
                        <b>📊 Match:</b> {row['Match Score (%)']}%</p>
                        <a href="{row['job_link']}" target="_blank">🔗 Apply Now</a>
                    </div>
                """, unsafe_allow_html=True)

            # Download CSV
            st.markdown("<div class='info-box'><h4>📥 Download Job Match Report</h4></div>", unsafe_allow_html=True)
            st.download_button(
                label="Download as CSV",
                data=job_df.to_csv(index=False),
                file_name="job_matches.csv",
                mime="text/csv"
            )
else:
    st.info("👈 Upload your resume to begin your job-matching journey.")
