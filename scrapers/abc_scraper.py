import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import re

ABC_SECTIONS = {
    "finance": ["https://www.abc.net.au/news/business"],
    "sports": ["https://www.abc.net.au/news/sport"],
    "lifestyle": ["https://www.abc.net.au/news/lifestyle"],
    "music": ["https://www.abc.net.au/news/entertainment"]
}

def get_abc_links(section_url):
    try:
        res = requests.get(section_url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"Failed to load ABC section: {section_url} — {e}")
        return []
    
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select("a[href*='/news/']")
    article_urls = list({urljoin("https://www.abc.net.au", a["href"]) for a in links if a["href"].count('/') > 3 and "/news/" in a["href"]})
    return article_urls

def extract_abc_article(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"Failed to scrape ABC {url}: {e}")
        return None
    soup = BeautifulSoup(res.text, 'html.parser')
    title_tag = soup.find('h1', class_=lambda x: x and 'ArticleHeadlineTitle' in x)
    title = title_tag.text.strip() if title_tag else 'Unknown'

     # Extract author from <a> tag with profile link
    author_tag = soup.find('a', href=lambda x: x and '/news/' in x and re.search(r'/\d{7,}', x))
    author = author_tag.text.strip() if author_tag else None

    # Fallback: check for <p> starting with "By "
    if not author:
        p_tags = soup.find_all('p', class_=lambda x: x and 'CardTag_text' in x)
        for p in p_tags:
            match = re.match(r'^By (.+)$', p.text.strip())
            if match:
                author = match.group(1)
                break

    if not author:
        author = "Unknown"

    content_div = soup.find('div', class_=lambda x: x and 'ArticleRender_article' in x)
    paragraphs = content_div.find_all('p') if content_div else []
    content = '\n'.join([p.text.strip() for p in paragraphs])

    return {
        'title': title,
        'author': author,
        'url': url,
        'content': content,
        'source': 'ABC News'
    }

def scrape_abc_articles():
    all_articles = []
    for category, urls in ABC_SECTIONS.items():
        print(f"\n Scraping ABC category: {category}")
        for section_url in urls:
            print(f" Section URL: {section_url}")
            links = get_abc_links(section_url)
            for link in links:
                if not link.startswith("http"):
                    continue
                article = extract_abc_article(link)
                if article:
                    article["category"] = category
                    all_articles.append(article)
                time.sleep(1)
    return all_articles
