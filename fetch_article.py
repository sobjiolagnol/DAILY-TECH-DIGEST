
import requests
import datetime
import os
from typing import List, Dict, Optional
import json

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

def fetch_articles() -> List[Dict]:
    articles = []
    for source in SOURCES.values():
        article = source["processor"]()
        if article:
            articles.append(article)
    return articles

def save_markdown(articles: List[Dict]):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"articles/{today}.md"
    os.makedirs("articles", exist_ok=True)
    
    with open(filename, "w") as f:
        f.write(f"# Daily Tech Digest - {today}\n\n")
        f.write("## Top Articles from Around the Web\n\n")
        
        for article in articles:
            f.write(f"### [{article['source']}]: {article['title']}\n")
            f.write(f"[Read more]({article['url']})\n\n")
        
        f.write("\n---\n")
        f.write(f"Generated at {datetime.datetime.now().strftime('%H:%M')}\n")

def main():
    articles = fetch_articles()
    if articles:
        save_markdown(articles)
        print(f"Successfully saved {len(articles)} articles to markdown file.")
    else:
        print("No articles were fetched.")

if __name__ == "__main__":
    main()
