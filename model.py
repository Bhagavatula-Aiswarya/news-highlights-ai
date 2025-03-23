# Saving locally for Streamlit to access

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
model.save('./models/all-MiniLM-L6-v2')
