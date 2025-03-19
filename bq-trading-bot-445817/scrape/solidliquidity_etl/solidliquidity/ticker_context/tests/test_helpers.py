from ticker_context.helpers import get_exchange_from_ticker

def test_get_exchange_from_ticker():
    exchange = get_exchange_from_ticker("AAPL")
    assert exchange == "NASDAQ"
