import streamlit as st
import pandas as pd


def display_highlights():
    # st.set_page_config(page_title="Daily News Highlights", layout="wide")
    st.title("🗞️ Daily News Highlights")
    st.caption("Curated & summarized news from multiple Australian News sites.")

    # Load processed data
    df = pd.read_csv("data/daily_news_highlights.csv")

    # Ensure frequency exists
    if "frequency" not in df.columns:
        df["frequency"] = 1

    categories = ["finance", "sports", "lifestyle", "music"]

    # Show categories as buttons in columns
    st.markdown("### 🔍 Choose a category")
    col1, col2, col3, col4 = st.columns(4)
    category_selected = None

    with col1:
        if st.button("💰 Finance"):
            category_selected = "finance"
    with col2:
        if st.button("🏅 Sports"):
            category_selected = "sports"
    with col3:
        if st.button("🧘 Lifestyle"):
            category_selected = "lifestyle"
    with col4:
        if st.button("🎵 Music"):
            category_selected = "music"

    if category_selected:
        filtered = df[df["category"] == category_selected]
        st.markdown(f"## 🔥  Top Stories in {category_selected.capitalize()}")

        for _, row in filtered.iterrows():
            with st.container():
                st.markdown(f"### {row['title']}")
                st.markdown(
                    f"👤 **Author:** {row.get('author', 'Unknown')} &nbsp;&nbsp; "
                    f"📡 **Source:** {row.get('source', 'N/A')} &nbsp;&nbsp; "
                    f"🔁 **Frequency:** `{row.get('frequency', 1)}`"
                )
                st.markdown(f"[🔗 Read Full Article]({row['url']})")

                MAX_SUMMARY_LENGTH = 600  # character limit
                with st.expander("🔎 Show Summary"):
                    summary_text = row.get("summary", "Summary not available.")
                    if isinstance(summary_text, str) and len(summary_text) > MAX_SUMMARY_LENGTH:
                        summary_text = summary_text[:MAX_SUMMARY_LENGTH].rsplit(" ", 1)[0] + "..."
                    st.markdown(summary_text)

                st.markdown("---")
    else:
        st.info("Please select a category to view today's top stories.")
