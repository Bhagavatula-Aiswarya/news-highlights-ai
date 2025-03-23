import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df['text_combined'] = df['title'].fillna('') + " " + df['content'].fillna('')
    return df
