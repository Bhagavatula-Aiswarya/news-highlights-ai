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

# Encode with SentenceTransformer
embedder = SentenceTransformer("models/all-MiniLM-L6-v2")
doc_embeddings = embedder.encode(documents, convert_to_tensor=False)

# Build FAISS index
dimension = doc_embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(doc_embeddings))

# Setup summarization and QA pipeline
qa_pipeline = pipeline("question-answering")

def rag_answer(query, top_k=3):
    query_vec = embedder.encode([query])[0]
    distances, indices = index.search(np.array([query_vec]), top_k)
    retrieved_docs = [documents[i] for i in indices[0]]

    # Use concatenated retrieved docs for QA
    context = " ".join(retrieved_docs)
    answer = qa_pipeline({
        "question": query,
        "context": context
    })
    return answer['answer'], retrieved_docs



