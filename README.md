# News Highlights AI + Chatbot

An AI-powered system that:
- Extracts and summarizes daily news from Australian outlets ( Sky News and ABC News at the moment, can be extended easily to add other sources in the future)
- Categorizes news by topic (Sports, Finance, Lifestyle, Music)
- Presents highlights in a Streamlit UI
- Includes a chatbot using Retrieval-Augmented Generation (RAG)

## Data Scraping and Processing

There are two data files that are cached on the repo.

1. raw_scraped_data.csv : This file is generated by run_scraper.py. It collects data from the News sites and creates dataset with information from the news articles. The dataset includes title,author,url,content,source,category of the article.

2. daily_news_highlights.csv: This file is generated by run_highlights.py. It loads the raw scraped data from above and performs additional analysis by grouping similar articles across multiple sources, deduplication, summarization of the content and creating highlights based on importance of the story.

## Instructions To Run Locally
1. Clone the repo  
2. Create and activate a venv 
3. Install dependencies using the requirements.txt
4. Run the app:

```bash
streamlit run streamlit_app.py
