import yfinance as yf
from yahooquery import search, Ticker
import pandas as pd
from transformers import AutoModel
from keybert import KeyBERT


def get_ticker_context_yfinance(stock_list):
    """
    Fetch financial context for a list of stock tickers using yfinance.

    Args:
        stock_list (list): List of stock tickers.

    Returns:
        dict: A dictionary containing industry, sector, and business summary for each ticker.
    """
    ticker_context = {}
    for stock in stock_list:
        try:
            ticker = yf.Ticker(stock)
            info = ticker.info
            ticker_context[stock] = {
                "Industry": info.get("industry", "Unknown"),
                "Sector": info.get("sector", "Unknown"),
                "Business Areas": info.get("longBusinessSummary", "No business summary available.")[:200] + "..."
            }
        except Exception as e:
            ticker_context[stock] = {"Error": str(e)}
    return ticker_context

def get_ticker_from_name(company_name):
    """
    Retrieve the ticker symbol for a given company name using YahooQuery.

    Args:
        company_name (str): Name of the company.

    Returns:
        str: Ticker symbol if found, otherwise None.
    """
    try:
        results = search(company_name)
        quotes = results.get("quotes", [])
        return quotes[0].get("symbol") if quotes else None
    except Exception as e:
        return None

def get_tickers_from_stocks(stocks): 
    stock_dictionary = {}
    for stock in stocks:
        ticker = get_ticker_from_name(stock)
        if ticker:
            stock_dictionary[stock] = ticker
        else:
            print(f"Could not find ticker for: {stock}")

    df = pd.DataFrame(stock_dictionary.items(), columns=['Company Name', 'Ticker Symbol'])
    return df


def generate_ticker_context_with_keybert(ticker):
    # Load KeyBERT model with FinBERT embeddings
    model = AutoModel.from_pretrained("yiyanghkust/finbert-pretrain")
    kw_model = KeyBERT(model=model)

    ticker_context = {}

    try:
        # Fetch company description
        company = yf.Ticker(ticker)
        business_summary = company.info.get("longBusinessSummary", "")

        # Extract keywords directly
        keywords = kw_model.extract_keywords(
            business_summary, keyphrase_ngram_range=(1, 2), top_n=4
        )
        ticker_context[ticker] = [kw[0] for kw in keywords]
    except Exception as e:
        ticker_context[ticker] = [f"Error: {str(e)}"]

    return ticker_context