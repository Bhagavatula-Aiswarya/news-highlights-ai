from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def compute_similarity(df, threshold=0.5):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(df['text_combined'])

    cosine_sim = cosine_similarity(tfidf_matrix)
    similar_pairs = []

    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            if cosine_sim[i, j] >= threshold:
                similar_pairs.append({
                    "index_1": i,
                    "index_2": j,
                    "title_1": df.iloc[i]['title'],
                    "title_2": df.iloc[j]['title'],
                    "source_1": df.iloc[i]['source'],
                    "source_2": df.iloc[j]['source'],
                    "similarity": cosine_sim[i, j],
                    "category": df.iloc[i]['category']
                })

    return pd.DataFrame(similar_pairs)
