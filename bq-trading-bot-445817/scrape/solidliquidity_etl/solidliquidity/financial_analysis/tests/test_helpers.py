from financial_analysis.helpers import get_financial_data, classify_market_cap


def test_get_financial_data():
    financials = get_financial_data("AAPL")
    assert "Net Income" in financials
    assert financials["Net Income"] > 0


def test_classify_market_cap():
    assert classify_market_cap(1_000_000_000) == "Small-cap"
    assert classify_market_cap(5_000_000_000) == "Mid-cap"
    assert classify_market_cap(20_000_000_000) == "Large-cap"
