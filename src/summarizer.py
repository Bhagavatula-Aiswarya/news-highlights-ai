from transformers import pipeline
from tqdm import tqdm
tqdm.pandas()

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text, max_length=120, min_length=30):
    if not text or len(text.strip()) < 100:
        return text
    try:
        result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return result[0]['summary_text']
    except Exception:
        return text

def summarize_articles(highlights_df, full_df):
    title_to_content = full_df.set_index("title")["content"].to_dict()
    highlights_df["content"] = highlights_df["title"].map(title_to_content)
    highlights_df["summary"] = highlights_df["content"].progress_apply(summarize_text)
    return highlights_df
