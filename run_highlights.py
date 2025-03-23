import pandas as pd
from src.loader import load_data
from src.similarity import compute_similarity
from src.scorer import score_articles
from src.highlights import generate_highlights
from src.summarizer import summarize_articles

def main():
    df = load_data("data/raw_scraped_data.csv")
    similar_df = compute_similarity(df, threshold=0.5)
    cross_source_freq, duplicate_groups = score_articles(df, similar_df)
    top_news = generate_highlights(df, cross_source_freq, duplicate_groups, top_n=5)
    top_news = summarize_articles(top_news, df)
    top_news.to_csv("data/daily_news_highlights.csv", index=False)
    print("✅ Highlights generated and saved.")

if __name__ == "__main__":
    main()
