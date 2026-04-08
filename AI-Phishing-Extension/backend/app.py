from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from datetime import datetime
import requests
import whois
from urllib.parse import urlparse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

EXCEL_FILE = "user_checked_links.xlsx"

# 🔥 Adjust threshold to reduce false positives
THRESHOLD = 0.75

# 🔐 Add your Google Safe Browsing API Key
GOOGLE_API_KEY = ""


class URLRequest(BaseModel):
    url: str


# -------------------------------
# DOMAIN AGE CHECK
# -------------------------------
def get_domain_age(url):
    try:
        domain = urlparse(url).netloc
        domain_info = whois.whois(domain)

        creation_date = domain_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date is None:
            return None

        age_days = (datetime.now() - creation_date).days
        return age_days

    except:
        return None


# -------------------------------
# GOOGLE SAFE BROWSING CHECK
# -------------------------------
def check_google_safe_browsing(url):

    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"

    body = {
        "client": {
            "clientId": "phishing-extension",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        response = requests.post(endpoint, json=body)
        result = response.json()
        return "matches" in result
    except:
        return False


# -------------------------------
# SAVE TO EXCEL (NO DUPLICATES)
# -------------------------------
def save_to_excel(url, prediction, probability, domain_age):

    label = "phishing" if prediction == 1 else "legitimate"

    new_row = {
        "url": url,
        "prediction": label,
        "probability": probability,
        "domain_age_days": domain_age,
        "timestamp": datetime.now()
    }

    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)

        if url in df["url"].values:
            return

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_excel(EXCEL_FILE, index=False)


# -------------------------------
# MAIN CHECK ENDPOINT
# -------------------------------
@app.post("/check")
def check_url(request: URLRequest):

    url = request.url

    # ML Prediction
    X = vectorizer.transform([url])
    ml_probability = model.predict_proba(X)[0][1]

    # Domain Age
    domain_age = get_domain_age(url)

    domain_risk = 0
    if domain_age is not None and domain_age < 90:
        domain_risk = 0.20  # boost risk for new domains

    # Google Safe Browsing
    google_flag = check_google_safe_browsing(url)

    google_risk = 0.30 if google_flag else 0

    # Final Score
    final_score = ml_probability + domain_risk + google_risk
    final_score = min(final_score, 1.0)

    prediction = 1 if final_score >= THRESHOLD else 0

    save_to_excel(url, prediction, float(final_score), domain_age)

    return {
        "status": prediction,
        "final_score": float(final_score),
        "ml_probability": float(ml_probability),
        "domain_age_days": domain_age,
        "google_flagged": google_flag
    }