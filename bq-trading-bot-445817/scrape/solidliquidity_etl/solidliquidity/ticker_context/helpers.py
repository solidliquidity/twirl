from yahooquery import Ticker

def get_exchange_from_ticker(ticker_symbol):
    """
    Retrieves the exchange for a given ticker symbol using YahooQuery.

    Args:
        ticker_symbol (str): The ticker symbol.

    Returns:
        str or None: The exchange name if available, otherwise None.
    """
    try:
        ticker = Ticker(ticker_symbol)
        data = ticker.price.get(ticker_symbol, {})
        return data.get("exchangeName", None)
    except Exception as e:
        return None
