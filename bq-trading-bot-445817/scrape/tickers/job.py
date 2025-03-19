import pandas as pd
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
from scrape.solidliquidity_etl.solidliquidity.reddit_scraper.scraper import RedditScraper
from scrape.solidliquidity_etl.solidliquidity.ticker_context.helpers import get_exchange_from_ticker
from scrape.solidliquidity_etl.solidliquidity.sentiment_analysis.analyser import extract_stocks_and_sentiment
from scrape.solidliquidity_etl.solidliquidity.news_scraper.helpers import get_recent_news, get_relevant_news
from scrape.solidliquidity_etl.solidliquidity.financial_analysis.helpers import get_market_cap
from scrape.solidliquidity_etl.solidliquidity.ticker_context.context import get_tickers_from_stocks

# Initialize environment variables
load_dotenv()

client_id = getenv('REDDIT_CLIENT_ID')
client_secret = getenv('REDDIT_CLIENT_SECRET')
user_agent = getenv('REDDIT_USER_AGENT')
device = 0 if torch.cuda.is_available() else -1

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

def download_tickers_from_subreddit(name):
    df = get_tickers_from_subreddit(name)
    return df

def job() -> pd.DataFrame:
    """Put your code here and return a pandas DataFrame"""
    return download_tickers_from_subreddit('valueinvesting')
