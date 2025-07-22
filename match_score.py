def calculate_match(resume_skills, job_titles):
    results = []
    for title in job_titles:
        score = sum(skill.lower() in title.lower() for skill in resume_skills)
        percent = (score / len(resume_skills)) * 100 if resume_skills else 0
        results.append({"job": title, "match_score": round(percent, 2)})
    return results

def calculate_resume_score(parsed_data, job_titles):
    score = 0

    # Skills (match to job titles)
    skills = parsed_data.get("skills", [])
    matched_keywords = sum(1 for skill in skills for title in job_titles if skill.lower() in title.lower())
    skill_score = min((matched_keywords / len(job_titles)) * 40, 40) if job_titles else 0

    # Experience (based on internships or experience_roles)
    experience_count = len(parsed_data.get("experience", [])) + len(parsed_data.get("experience_roles", []))
    exp_score = min(experience_count * 10, 20)

    # Education (bachelor/master/phd)
    edu = parsed_data.get("education", [])
    edu_score = min(len(edu) * 10, 20)

    # Projects
    projects = parsed_data.get("projects", [])
    project_score = min(len(projects) * 10, 20)

    total = skill_score + exp_score + edu_score + project_score

    return round(total), {
        "Skills": skill_score,
        "Experience": exp_score,
        "Education": edu_score,
        "Projects": project_score
    }
