import requests
import datetime
import os
import csv
import zipfile
from typing import List, Dict, Optional

SOURCES = {
    "Hacker News": {
        "url": "https://hacker-news.firebaseio.com/v0/topstories.json",
        "processor": lambda: fetch_hn_article()
    },
    "TechCrunch": {
        "url": "https://techcrunch.com/wp-json/wp/v2/posts?per_page=1",
        "processor": lambda: fetch_techcrunch_article()
    },
    "Dev.to": {
        "url": "https://dev.to/api/articles?top=1&per_page=1",
        "processor": lambda: fetch_devto_article()
    }
}

# --- fetchers ---
def fetch_hn_article() -> Optional[Dict]:
    try:
        top_stories = requests.get(SOURCES["Hacker News"]["url"]).json()
        top_id = top_stories[0]
        story = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{top_id}.json").json()
        return {
            "title": story.get('title', 'No title'),
            "url": story.get('url', '#'),
            "source": "Hacker News"
        }
    except Exception as e:
        print(f"Error fetching Hacker News: {e}")
        return None

def fetch_techcrunch_article() -> Optional[Dict]:
    try:
        response = requests.get(SOURCES["TechCrunch"]["url"])
        article = response.json()[0]
        return {
            "title": article.get('title', {}).get('rendered', 'No title'),
            "url": article.get('link', '#'),
            "source": "TechCrunch"
        }
    except Exception as e:
        print(f"Error fetching TechCrunch: {e}")
        return None

def fetch_devto_article() -> Optional[Dict]:
    try:
        response = requests.get(SOURCES["Dev.to"]["url"])
        article = response.json()[0]
        return {
            "title": article.get('title', 'No title'),
            "url": article.get('url', '#'),
            "source": "Dev.to"
        }
    except Exception as e:
        print(f"Error fetching Dev.to: {e}")
        return None

# --- core ---
def fetch_articles() -> List[Dict]:
    articles = []
    for source in SOURCES.values():
        article = source["processor"]()
        if article:
            articles.append(article)
    return articles

def save_markdown(articles: List[Dict]) -> str:
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%H-%M")
    filename = f"articles/{today}_{timestamp}.md"
    os.makedirs("articles", exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Tech Digest - {today} {timestamp}\n\n")
        f.write("## Top Articles\n\n")
        
        for article in articles:
            f.write(f"### [{article['source']}]: {article['title']}\n")
            f.write(f"[Read more]({article['url']})\n\n")
        
        f.write("\n---\n")
        f.write(f"Generated at {datetime.datetime.now().strftime('%H:%M')}\n")

    return filename

# --- actions supplémentaires sans API ---
def save_csv(articles: List[Dict]):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"articles/{today}.csv"
    os.makedirs("articles", exist_ok=True)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "title", "url"])
        if f.tell() == 0:  # écrire l'entête si fichier vide
            writer.writeheader()
        writer.writerows(articles)

def log_to_file(articles: List[Dict]):
    filename = "articles/run.log"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.datetime.now()}] {len(articles)} articles récupérés\n")
        for article in articles:
            f.write(f"- {article['source']}: {article['title']} ({article['url']})\n")

def archive_day():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    zip_filename = f"articles/{today}.zip"
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for file in os.listdir("articles"):
            if file.startswith(today) and (file.endswith(".md") or file.endswith(".csv")):
                zipf.write(os.path.join("articles", file), file)

# --- scheduler ---
def main():
    now = datetime.datetime.now()
    weekday = now.strftime("%A")  # ex: "Monday", "Tuesday"
    hour = now.hour

    # Exemple: exécuter seulement du lundi au vendredi, 9h / 14h / 18h
    allowed_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    allowed_hours = [9, 14, 18]

    if weekday in allowed_days and hour in allowed_hours:
        articles = fetch_articles()
        if articles:
            filename = save_markdown(articles)
            print(f"✅ {len(articles)} articles enregistrés dans {filename}")

            # autres actions locales
            save_csv(articles)
            log_to_file(articles)
            archive_day()
        else:
            print("⚠️ Aucun article trouvé.")
    else:
        print(f"⏸ Non programmé pour {weekday} à {hour}h")

if __name__ == "__main__":
    main()
