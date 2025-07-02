import requests
import datetime
import os

def fetch_top_article():
    top_stories = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()
    top_id = top_stories[0]
    story = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{top_id}.json").json()
    return story['title'], story['url']

def save_markdown(title, url):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"articles/{today}.md"
    os.makedirs("articles", exist_ok=True)
    with open(filename, "w") as f:
        f.write(f"# {today}\n\n")
        f.write(f"## {title}\n\n")
        f.write(f"[Read more]({url})\n")

def main():
    title, url = fetch_top_article()
    save_markdown(title, url)

if __name__ == "__main__":
    main()
