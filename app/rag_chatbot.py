import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Load data
df = pd.read_csv("data/daily_news_highlights.csv")

# Prepare documents
documents = df["summary"].fillna("").tolist()
titles = df["title"].tolist()
metadata = df[["title", "url", "category", "source"]].to_dict("records")

# Encode with SentenceTransformer
embedder = SentenceTransformer("models/all-MiniLM-L6-v2")
doc_embeddings = embedder.encode(documents, convert_to_tensor=False)

# Build FAISS index
dimension = doc_embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(doc_embeddings))

# Load a lightweight T5 model
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# Format and safely truncate context
def format_context(docs, max_chars=1800):
    context = ""
    for doc in docs:
        if len(context) + len(doc) + 5 > max_chars:
            break
        context += f"• {doc.strip()}\n\n"
    return context.strip()

def rag_answer(query, top_k=3):
    # Embed and search
    query_vec = embedder.encode([query])[0]
    distances, indices = index.search(np.array([query_vec]), top_k)

    matched_docs = [documents[i] for i in indices[0]]
    matched_meta = [metadata[i] for i in indices[0]]

    # Truncate context to avoid model errors
    context = format_context(matched_docs)

    # Prompt with context
    prompt = (
        f"You are a helpful assistant summarizing Australian news for a curious user.\n"
        f"User asked: {query}\n\n"
        f"Relevant news summaries:\n{context}\n\n"
        f"Based on the above news, provide a helpful and concise answer:"
    )

    try:
        response = generator(prompt, max_new_tokens=200, do_sample=False)[0]['generated_text']
    except Exception as e:
        response = "Sorry, I couldn't generate a proper answer."

    return response.strip(), [meta["title"] for meta in matched_meta]
