from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

def scrape_jobs(resume_data):
    query_terms = []

    query_terms += resume_data.get("skills", [])
    query_terms += [r for r in resume_data.get("experience_roles", [])]
    query_terms += [p.replace("project", "").strip() for p in resume_data.get("projects", [])]

    query_terms = list(set([q.strip().lower() for q in query_terms if len(q.strip()) > 2]))

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    all_jobs = []

    for keyword in query_terms:
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location=India"
        driver.get(search_url)
        time.sleep(5)

        job_cards = driver.find_elements(By.CLASS_NAME, 'base-card')

        for card in job_cards[:5]:
            try:
                title = card.find_element(By.CLASS_NAME, 'base-search-card__title').text
                company = card.find_element(By.CLASS_NAME, 'base-search-card__subtitle').text
                location = card.find_element(By.CLASS_NAME, 'job-search-card__location').text
                job_url = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
                all_jobs.append({
                    "keyword": keyword,
                    "title": title,
                    "company": company,
                    "location": location,
                    "job_link": job_url
                })
            except Exception as e:
                continue

    driver.quit()
    job_df = pd.DataFrame(all_jobs).drop_duplicates(subset=["title", "company", "job_link"])
    return job_df.reset_index(drop=True)
