
import os
from os import getenv
from datetime import datetime
import pandas as pd
import spacy
from transformers import pipeline
from dotenv import load_dotenv
import torch
from datetime import datetime
import sys
sys.path.insert(0, '/app') 
from solidliquidity_etl.solidliquidity.reddit_scraper.scraper import RedditScraper
from solidliquidity_etl.solidliquidity.ticker_context.helpers import get_exchange_from_ticker
from solidliquidity_etl.solidliquidity.sentiment_analysis.analyser import extract_stocks_and_sentiment
from solidliquidity_etl.solidliquidity.news_scraper.helpers import get_recent_news, get_relevant_news
from solidliquidity_etl.solidliquidity.financial_analysis.helpers import get_market_cap
from solidliquidity_etl.solidliquidity.ticker_context.context import get_tickers_from_stocks

# Initialize environment variables
load_dotenv()

client_id = "1-AhmBlIhsWK2JgDZopeug"
client_secret = "Jq-ca_BmnaPuOJHFnE2AuwT-csnEDQ"
user_agent = "stock_scraper/1.0 by qwertytr575422" 

device = 0 if torch.cuda.is_available() else -1

# Airflow DAG definition
def get_tickers_from_subreddit(name):
    redditscraper = RedditScraper(client_id=client_id,
                                    client_secret=client_secret,
                                    user_agent=user_agent,
                                    subreddit_name=name)
    posts_df = redditscraper.fetch_posts()
    post_permalink = posts_df.iloc[0]['Permalink']
    comments_df = redditscraper.fetch_comments(post_permalink)

    nlp = spacy.load("en_core_web_sm")
    sentiment_analyser = pipeline("sentiment-analysis",
                                    model="cardiffnlp/twitter-roberta-base-sentiment",
                                    tokenizer="cardiffnlp/twitter-roberta-base-sentiment",
                                    truncation=True,
                                    max_length=512,
                                    device=device)

    comments_df["Analysis"] = comments_df["Comment Body"].apply(lambda x: extract_stocks_and_sentiment(x, nlp, sentiment_analyser))
    comments_df["Stocks"] = comments_df["Analysis"].apply(lambda x: x["Stocks"])
    comments_df["Sentiment"] = comments_df["Analysis"].apply(lambda x: x["Sentiment"])
    comments_df["Score"] = comments_df["Analysis"].apply(lambda x: x["Score"])
    filtered_comments_df = comments_df[comments_df['Stocks'].apply(lambda x: len(x) > 0)]
    positive_df = filtered_comments_df[filtered_comments_df['Sentiment'] == 'LABEL_2']
    final_df = positive_df[['Comment Body', 'Stocks', 'Sentiment', 'Score']].reset_index(drop=True)
    flat_list = list(set([ticker for sublist in list(final_df['Stocks']) for ticker in sublist]))
    df = get_tickers_from_stocks(flat_list).dropna()
    df['community'] = name
    df['timeframe'] = datetime.now()
    return df[['Ticker Symbol']].rename(columns={'Ticker Symbol': 'ticker'})

def save_to_db(df):
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

    DATABASE_URI = "postgresql+psycopg2://postgres:Limehousecut!1@35.246.116.71:5432/trading_alerts"
    
    # Create a SQLAlchemy engine
    engine = create_engine(DATABASE_URI)

    # Use the engine directly with pandas.to_sql()
    df.to_sql('tickers', con=engine, if_exists='append', index=False)

    print('saved to db')

def download_tickers_from_subreddit(name):
    df = get_tickers_from_subreddit(name)
    save_to_db(df)
    return df

for community in ['wallstreetbets', 'stocks', 'investing', 'stockmarket', 'valueinvesting']:
    try: 
        download_tickers_from_subreddit(community)
    except Exception as e:
        print(f"Error downloading tickers from {community}: {e}")
