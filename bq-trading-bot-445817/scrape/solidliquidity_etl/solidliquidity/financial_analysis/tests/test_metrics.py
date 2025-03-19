import pytest
from financial_analysis.metrics import (
    calculate_earnings_per_share,
    calculate_return_on_equity,
    calculate_current_ratio,
    calculate_debt_to_equity
)


@pytest.fixture
def mock_financials():
    return {
        "Net Income": 1_000_000,
        "Preferred Stock Dividends": 50_000,
        "Basic Average Shares": 100_000,
        "Common Stock Equity": [2_000_000, 2_500_000],
        "Total Debt": 1_500_000,
        "Stockholders Equity": 2_500_000,
        "Current Assets": 800_000,
        "Current Liabilities": 400_000
    }


def test_calculate_earnings_per_share(mock_financials):
    eps = calculate_earnings_per_share(mock_financials)
    assert eps == 9.5


def test_calculate_return_on_equity(mock_financials):
    roe = calculate_return_on_equity(mock_financials)
    assert roe == pytest.approx(0.4, 0.01)


def test_calculate_current_ratio(mock_financials):
    current_ratio = calculate_current_ratio(mock_financials)
    assert current_ratio == 2.0


def test_calculate_debt_to_equity(mock_financials):
    debt_to_equity = calculate_debt_to_equity(mock_financials)
    assert debt_to_equity == 0.6
