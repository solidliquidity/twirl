from datetime import datetime
from .scraper import NewsScraper

def get_recent_news(scraper):
    try:
        RSS_news = scraper.get_news_rss()
        return scraper.filter_news_during_closed_hours(RSS_news)
    except Exception:
        return []


def get_relevant_news(scraper, ticker_context, recent_news, model, threshold=0.3):
    try:
        relevant_news = [
            scraper.filter_headline(
                news['Title'], ticker_context, model, threshold)
            for news in recent_news
        ]
        return [news for news in relevant_news if news]
    except KeyError as e:
        print(e)
        return []
    
    
def clean_exchange_name(exchange):
    """
    Cleans the exchange name to standardize 'NASDAQ' variations.
    
    Args:
        exchange (str): The exchange name.

    Returns:
        str: The cleaned exchange name.
    """
    if exchange.startswith("NASDAQ"):
        return "NASDAQ"
    return exchange
