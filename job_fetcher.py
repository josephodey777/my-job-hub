import requests
import os
from dotenv import load_dotenv

# This loads the hidden keys from your .env file
load_dotenv()

def fetch_adzuna_jobs(keyword, location="Canada"):
    # Securely grab the keys from the environment variables
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    
    # Adzuna's Canadian search URL
    url = f"https://api.adzuna.com/v1/api/jobs/ca/search/1"
    
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": 5, 
        "what": keyword,       
        "where": location      
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() 
        data = response.json()
        
        # We will extract just the info we care about for now
        formatted_jobs = []
        for job in data.get("results", []):
            formatted_jobs.append({
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name", "Unknown Company"),
                "location": job.get("location", {}).get("display_name", "Unknown Location"),
                "description": job.get("description", ""),
                "url": job.get("redirect_url")
            })
            
        return formatted_jobs
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs: {e}")
        return []