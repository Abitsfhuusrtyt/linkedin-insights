import os
os.makedirs("app", exist_ok=True)
open("app/__init__.py", "w").close()
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
           # Entry point for API
open("app/scraper.py","w").close()
import requests
from bs4 import BeautifulSoup
def scrape_linkedin_page(page_id):
    url = f"https://www.linkedin.com/company/{page_id}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch LinkedIn page"}

    soup = BeautifulSoup(response.text, "html.parser")

    page_data = {
        "page_name": soup.title.string if soup.title else "Unknown",
        "page_url": url
    }
    return page_data
         # Scraper logic
          
open("app/db.py","w").close()     
from pymongo import MongoClient
try:
    client = MongoClient("mongodb://localhost:27017/")
db = client["linkedin_insights"]
pages_collection = db["pages"]
         # Database connection
os.makedirs("models", exist_ok=True)           # Data schema
os.makedirs("routes", exist_ok=True)  
from fastapi import APIRouter
from app.scraper import scrape_linkedin_page # type: ignore
from app.db import pages_collection # type: ignore

router = APIRouter()

@router.get("/scrape/{page_id}")
def scrape_page(page_id: str):
    data = scrape_linkedin_page(page_id)
    if "error" in data:
        return data
    
    pages_collection.insert_one(data)  # Save to database
    return {"message": "Data stored successfully", "data": data}

@router.get("/pages")
def get_pages():
    return list(pages_collection.find({}, {"_id": 0}))
         # API endpoints

os.makedirs("env", exist_ok=True)  # Virtual environment
open("requirements.txt", "w").close() # Dependencies
open("README.md", "w").close()             # Documentation
