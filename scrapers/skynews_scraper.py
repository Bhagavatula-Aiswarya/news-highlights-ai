import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

SKY_SECTIONS = {
    "finance": ["https://www.skynews.com.au/business/finance"],
    "sports": ["https://www.skynews.com.au/australia-news/sport"],
    "lifestyle": [
        "https://www.skynews.com.au/lifestyle/health",
        "https://www.skynews.com.au/lifestyle/trending",
        "https://www.skynews.com.au/lifestyle/celebrity-life"
    ],
    "music": ["https://www.skynews.com.au/lifestyle/arts-and-culture"]
}

def get_article_links(section_url):
    try:
        res = requests.get(section_url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"Failed to load section: {section_url} — {e}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select("a[href*='/news-story/']")
    return list({urljoin("https://www.skynews.com.au", a["href"]) for a in links})

def extract_article_data(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.select_one("h1#story-headline")
    author_tag = soup.select_one("span.author_name a")
    paragraphs = soup.select("div#story-primary p")

    return {
        "title": title.text.strip() if title else "Unknown",
        "author": author_tag.text.strip() if author_tag else "Unknown",
        "url": url,
        "content": "\n".join([p.text.strip() for p in paragraphs]) if paragraphs else "",
        "source": "SKY News",
    }

def scrape_skynews_articles():
    all_articles = []
    for category, urls in SKY_SECTIONS.items():
        print(f"\n Scraping category: {category}")
        for section_url in urls:
            print(f" Section URL: {section_url}")
            links = get_article_links(section_url)
            for link in links:
                if not link.startswith("http"):
                    continue
                article = extract_article_data(link)
                if article:
                    article["category"] = category
                    all_articles.append(article)
                time.sleep(1)
    return all_articles
