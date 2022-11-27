from app.fx_report import fetch_exchange_data
from pandas import DataFrame

def test_data_fetching():
    result = fetch_exchange_data("EUR","USD")
    assert isinstance(result, DataFrame)

    assert "timestamp" in result.columns
    assert "open" in result.columns
    assert "high" in result.columns
    assert "low" in result.columns
    assert "close" in result.columns

    assert len(result) >= 100