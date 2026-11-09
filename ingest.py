import os
import requests
from dotenv import load_dotenv
from database import SessionLocal
from models import Job
from sponsorship import analyze_sponsorship  # Import the new logic

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

def fetch_and_save_jobs():
    url = "https://api.adzuna.com/v1/api/jobs/ca/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 5,
        "what": "software engineer",
    }

    print("Fetching jobs from Adzuna...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        jobs = response.json().get("results", [])
        db = SessionLocal()
        
        saved_count = 0
        for job_data in jobs:
            existing_job = db.query(Job).filter(Job.external_id == str(job_data.get('id'))).first()
            
            if not existing_job:
                # Extract description
                desc = job_data.get('description', '')
                
                # Run the analysis
                analysis = analyze_sponsorship(desc)
                
                new_job = Job(
                    external_id=str(job_data.get('id')),
                    title=job_data.get('title'),
                    company_name=job_data.get('company', {}).get('display_name'),
                    location=job_data.get('location', {}).get('display_name'),
                    description=desc,
                    apply_url=job_data.get('redirect_url'),
                    # Save the analysis results
                    sponsorship_score=analysis["score"],
                    sponsorship_category=analysis["category"]
                )
                db.add(new_job)
                saved_count += 1
                
                print(f"Analyzed: {new_job.title} -> {analysis['category']} (Score: {analysis['score']})")
                
        db.commit()
        db.close()
        print(f"Successfully saved and analyzed {saved_count} new jobs.")
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    fetch_and_save_jobs()