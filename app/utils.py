import pandas as pd

def load_highlights(path="data/daily_news_highlights.csv"):
    return pd.read_csv(path)
