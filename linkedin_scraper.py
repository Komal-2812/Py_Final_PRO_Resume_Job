import pandas as pd

def scrape_jobs(parsed_resume):
    skills = parsed_resume.get('skills', [])

    # Sample job list
    job_db = [
        {"title": "Python Developer", "company": "Infosys", "location": "Bangalore", "job_link": "https://linkedin.com/jobs/1"},
        {"title": "Data Analyst", "company": "TCS", "location": "Mumbai", "job_link": "https://linkedin.com/jobs/2"},
        {"title": "React Intern", "company": "StartupX", "location": "Remote", "job_link": "https://linkedin.com/jobs/3"},
        {"title": "Flask Developer", "company": "Cognizant", "location": "Hyderabad", "job_link": "https://linkedin.com/jobs/4"},
        {"title": "Full Stack Intern", "company": "TechNova", "location": "Delhi", "job_link": "https://linkedin.com/jobs/5"},
    ]

    job_df = pd.DataFrame(job_db)

    # Simple filter: include job if any resume skill appears in job title
    matches = []
    for _, row in job_df.iterrows():
        if any(skill.lower() in row['title'].lower() for skill in skills):
            matches.append(row)

    return pd.DataFrame(matches)