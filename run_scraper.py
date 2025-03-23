import pandas as pd
from scrapers.abc_scraper import scrape_abc_articles
from scrapers.skynews_scraper import scrape_skynews_articles


def clean_articles(df):
    # df = pd.DataFrame(articles)
    df = df[df['content'].str.strip().str.len() > 50]  # Filter short/empty content
    df = df.drop_duplicates(subset=["url"])
    return df


def main():
    print("Scraping Sky News...")
    skynews_data = pd.DataFrame(scrape_skynews_articles())
    # skynews_data.to_csv("sky.csv")

    print("Scraping ABC News...")
    abc_data = pd.DataFrame(scrape_abc_articles())
    # abc_data.to_csv('abc.csv')

    print("Cleaning & Merging...")
    combined = pd.concat([skynews_data, abc_data], ignore_index=True)
    cleaned_df = clean_articles(combined)
    cleaned_df.to_csv("data/raw_scraped_data.csv", index=False)
    print(f"Saved {len(cleaned_df)} cleaned articles to raw_scraped_data.csv")


if __name__ == "__main__":
    main()