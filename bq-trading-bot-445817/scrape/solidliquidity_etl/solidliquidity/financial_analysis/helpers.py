import yfinance as yf


def get_financial_data(ticker):
    """
    Fetch financial data for a given ticker using yfinance.

    Args:
        ticker (str): Stock ticker symbol.

    Returns:
        dict: Financial data for the ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        financials = {
            "Net Income": stock.financials.loc['Net Income'][-1],
            "Total Debt": stock.balance_sheet.loc['Total Liab'][-1],
            "Stockholders Equity": stock.balance_sheet.loc['Total Stockholder Equity'][-1],
            "Current Assets": stock.balance_sheet.loc['Total Current Assets'][-1],
            "Current Liabilities": stock.balance_sheet.loc['Total Current Liabilities'][-1],
            "Market Price Per Share": stock.info['currentPrice'],
            "Basic Average Shares": stock.info['sharesOutstanding']
        }
        return financials
    except Exception as e:
        return {"Error": str(e)}


def classify_market_cap(market_cap):
    """
    Classify market capitalization into small-cap, mid-cap, or large-cap.

    Args:
        market_cap (float): Market capitalization.

    Returns:
        str: Market cap classification.
    """
    if market_cap < 2e9:
        return "Small-cap"
    elif market_cap < 10e9:
        return "Mid-cap"
    else:
        return "Large-cap"


def get_market_cap(ticker):
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get('currentPrice')
        shares_outstanding = stock.info.get('sharesOutstanding')

        if price and shares_outstanding:
            market_cap = price * shares_outstanding
            if market_cap < 2e9:
                return "Small-cap"
            elif market_cap < 10e9:
                return "Mid-cap"
            else:
                return "Large-cap"
        return None
    except Exception:
        return None
