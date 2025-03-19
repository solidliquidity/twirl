def calculate_earnings_per_share(financials):
    """
    Calculate Earnings Per Share (EPS).
    EPS = (Net Income - Preferred Dividends) / Common Shares Outstanding
    """
    try:
        return (financials['Net Income'] - financials.get(
            'Preferred Stock Dividends', 0)) / financials['Basic Average Shares']
    except (KeyError, ZeroDivisionError) as e:
        return f"Error: {e}"


def calculate_return_on_equity(financials):
    """
    Calculate Return on Equity (ROE).
    ROE = Net Income / Average Equity
    """
    try:
        average_equity = (
            financials['Common Stock Equity'][0] + financials['Common Stock Equity'][1]) / 2
        return financials['Net Income'] / average_equity
    except (KeyError, ZeroDivisionError) as e:
        return f"Error: {e}"


def calculate_current_ratio(financials):
    """
    Calculate Current Ratio.
    Current Ratio = Current Assets / Current Liabilities
    """
    try:
        return financials['Current Assets'] / financials['Current Liabilities']
    except (KeyError, ZeroDivisionError) as e:
        return f"Error: {e}"


def calculate_debt_to_equity(financials):
    """
    Calculate Debt-to-Equity Ratio.
    Debt-to-Equity = Total Debt / Total Equity
    """
    try:
        return financials['Total Debt'] / financials['Stockholders Equity']
    except (KeyError, ZeroDivisionError) as e:
        return f"Error: {e}"
