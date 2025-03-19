from datetime import datetime, timedelta
import feedparser
from .constants import EXCHANGES
from sentence_transformers import util

class NewsScraper:
    def __init__(self, stock_ticker, exchange):
        self.stock_ticker = stock_ticker
        self.exchange = exchange
        self.close_time = None
        self.open_time = None

    def set_exchange_times(self, now):
        """
        Calculate and set yesterday's close and today's open times for the exchange.
        """
        close_hour, close_minute = EXCHANGES[self.exchange]["close_time"]
        open_hour, open_minute = EXCHANGES[self.exchange]["open_time"]

        # Calculate yesterday's close
        close_time = (now - timedelta(days=1)).replace(
            hour=close_hour, minute=close_minute, second=0, microsecond=0
        )

        # Calculate today's open
        open_time = now.replace(
            hour=open_hour, minute=open_minute, second=0, microsecond=0
        )

        # Adjust if the current time is before today's open
        if now < open_time:
            # Move close time to the day before yesterday
            close_time -= timedelta(days=1)

        # Set the instance attributes
        self.close_time = close_time
        self.open_time = open_time

    def get_news_rss(self):
        """
        Fetch news for the stock ticker of the instance from Google News RSS.
        """
        url = f"https://news.google.com/rss/search?q={self.stock_ticker}"
        feed = feedparser.parse(url)
        return [
            {"Title": entry["title"], "Link": entry["link"],
                "Published": datetime(*entry["published_parsed"][:6])}
            for entry in feed["entries"]
        ]

    def filter_news_during_closed_hours(self, news):
        """
        Filter news published during the last closed hours.
        """
        if self.close_time is None or self.open_time is None:
            raise ValueError(
                "close_time and open_time must be set before filtering news.")
        return [article for article in news if self.close_time <=
                article["Published"] < self.open_time]

    def filter_headline(self, headline, ticker_context, model, threshold=0.3):
        """
        Filters a single headline based on relevance to a ticker context.

        Args:
            headline (str): The headline to filter.
            ticker_context (dict): Dictionary where keys are tickers and values are lists of context keywords.
            model (SentenceTransformer): Pre-trained SentenceTransformer model for semantic similarity.
            threshold (float): Similarity threshold to consider a headline relevant.

        Returns:
            str: The ticker if the headline is relevant, otherwise None.
        """
        for ticker, context_keywords in ticker_context.items():
            # Encode the headline
            headline_embedding = model.encode(headline)

            # Encode each context keyword and calculate similarity scores
            keyword_embeddings = model.encode(context_keywords)
            similarities = util.cos_sim(headline_embedding, keyword_embeddings)

            # Check if any similarity exceeds the threshold
            if similarities.max().item() > threshold:
                return headline  # Return the relevant ticker
        return None  # Return None if no match found
