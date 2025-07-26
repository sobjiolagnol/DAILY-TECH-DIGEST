import requests
import datetime
import os
import json

API_KEY = "TA_CLE_API_ICI"
NEWS_URL = "https://newsapi.org/v2/top-headlines"

# Liste de pays ou langues (tu peux étendre)
COUNTRIES = ["us", "gb", "fr", "de", "jp"]  # USA, UK, France, Germany, Japan

def fetch_headlines(country: str):
    try:
        response = requests.get(NEWS_URL, params={
            "apiKey": API_KEY,
            "country": country,
            "pageSize": 5  # Nombre de titres à récupérer
        })
        data = response.json()
        return data.get("articles", [])
    except Exception as e:
        print(f"Erreur pour {country}: {e}")
        return []

def save_headlines(headlines: dict):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    os.makedirs("headlines", exist_ok=True)
    filename = f"headlines/{today}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(headlines, f, ensure_ascii=False, indent=2)
    print(f"Titres enregistrés dans {filename}")

def main():
    all_headlines = {}
    for country in COUNTRIES:
        articles = fetch_headlines(country)
        all_headlines[country] = [
            {"title": article["title"], "source": article["source"]["name"], "url": article["url"]}
            for article in articles
        ]
    save_headlines(all_headlines)

if __name__ == "__main__":
    main()
