import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_sections
from linkedin_scraper import scrape_jobs
from match_score import calculate_match
import pandas as pd

# Page setup
st.set_page_config(page_title="JobFit Analyzer", layout="wide", page_icon="📄")

# Custom white theme styling
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #ffffff;
        color: #2c3e50;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .info-box {
        background-color: #f9f9f9;
        border-left: 5px solid #0073b1;
        padding: 20px;
        border-radius: 12px;
        margin: 25px 0;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.04);
    }
    .job-card {
        background-color: #ffffff;
        border: 1px solid #eaeaea;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        transition: transform 0.2s ease-in-out;
    }
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    a {
        color: #0073b1 !important;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Guide
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/10290/10290594.png", width=80)
st.sidebar.markdown("#### 🤖 JobFit Assistant Guide")
st.sidebar.markdown("""
📄 **Step 1:** Upload your resume (PDF or DOCX)  
🔍 **Step 2:** We extract your skills, projects, experience  
🚀 **Step 3:** Click **Find Jobs** to see matching roles  
📥 **Step 4:** Download the full ATS-ready report

💡 *Tips:*  
- Use clear role titles & keywords (e.g., Python, Excel, Analyst)  
- Include internships or projects with outcomes
""")

# Title
st.markdown("<h1 style='text-align:center;'>📄 JobFit Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>💼 Resume Intelligence & Job Matching for Students & Recruiters</p>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("✨ Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("🔍 Extracting resume details..."):
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_docx(uploaded_file)
        parsed_data = extract_sections(text)

    st.markdown("<div class='info-box'><h4>🧠 Extracted Resume Details</h4></div>", unsafe_allow_html=True)
    st.json(parsed_data)

    if st.button("🚀 Find Matching Jobs in India"):
        with st.spinner("🔗 Searching job database for matches..."):
            job_df = scrape_jobs(parsed_data)

        if job_df.empty:
            st.warning("😕 No jobs found. Try updating your resume or use broader skills.")
        else:
            st.success(f"🎯 Found {len(job_df)} matching jobs for your resume!")

            # Score calculation
            match_scores = calculate_match(parsed_data["skills"], job_df["title"])
            match_df = pd.DataFrame(match_scores)
            job_df["Match Score (%)"] = match_df["match_score"]

            # Job cards
            for _, row in job_df.iterrows():
                st.markdown(f"""
                    <div class='job-card'>
                        <h4>💼 {row['title']}</h4>
                        <p><b>🏢 Company:</b> {row['company']}<br>
                        <b>📍 Location:</b> {row['location']}<br>
                        <b>📊 Match Score:</b> {row['Match Score (%)']}%</p>
                        <a href='{row['job_link']}' target='_blank'>🔗 Apply Now</a>
                    </div>
                """, unsafe_allow_html=True)

            # Download button
            st.markdown("<div class='info-box'><h4>📥 Download Job Match Report</h4></div>", unsafe_allow_html=True)
            st.download_button(
                label="Download as CSV",
                data=job_df.to_csv(index=False),
                file_name="job_matches.csv",
                mime="text/csv"
            )
else:
    st.info("👈 Upload your resume to start your JobFit analysis.")
