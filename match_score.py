def calculate_match(resume_skills, job_titles):
    results = []
    for title in job_titles:
        score = sum(skill.lower() in title.lower() for skill in resume_skills)
        percent = (score / len(resume_skills)) * 100 if resume_skills else 0
        results.append({"job": title, "match_score": round(percent, 2)})
    return results
