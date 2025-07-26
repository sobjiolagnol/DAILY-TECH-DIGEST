import requests
from bs4 import BeautifulSoup
import os
import datetime
import json

JOURNAUX = {
    "BBC News": {
        "url": "https://www.bbc.com/news",
        "selector": "h3.gs-c-promo-heading__title"
    },
    "Le Monde": {
        "url": "https://www.lemonde.fr",
        "selector": "a.teaser__link"
    },
    "CNN": {
        "url": "https://edition.cnn.com",
        "selector": "h3.cd__headline a"
    }
}

def fetch_headlines(name, url, selector):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        elements = soup.select(selector)
        headlines = []
        for el in elements[:5]:  # Limite à 5 titres par site
            text = el.get_text(strip=True)
            link = el.get("href")
            if link and not link.startswith("http"):
                link = url.rstrip("/") + "/" + link.lstrip("/")
            headlines.append({"title": text, "url": link})
        return headlines
    except Exception as e:
        print(f"[{name}] Erreur : {e}")
        return []

def save_to_json(data):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    os.makedirs("headlines", exist_ok=True)
    filename = f"headlines/{today}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Titres enregistrés dans {filename}")

def main():
    all_headlines = {}
    for name, info in JOURNAUX.items():
        print(f"Scraping {name}...")
        headlines = fetch_headlines(name, info["url"], info["selector"])
        all_headlines[name] = headlines
    save_to_json(all_headlines)

if __name__ == "__main__":
    main()
