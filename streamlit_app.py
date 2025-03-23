import streamlit as st

# Set layout first
st.set_page_config(page_title="News Highlights AI", layout="wide")

from app.rag_chatbot import rag_answer
from app.ui import display_highlights

def main():
    # Show main highlights view
    display_highlights()

    # Sidebar chatbot always visible
    st.sidebar.title("🧠 Ask the News Bot")
    query = st.sidebar.text_input("Ask something about today's news:")
    if query:
        with st.sidebar:
            with st.spinner("Thinking..."):
                answer, docs = rag_answer(query)
            st.markdown("**Answer:**")
            st.markdown(answer)
            st.markdown("---")
            st.markdown("**Context used:**")
            for doc in docs:
                st.markdown(f"- {doc}")

if __name__ == "__main__":
    main()
