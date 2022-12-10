from app.fx_calculate import fetch_exchange_data, calculate_new_currency
from pandas import DataFrame

def test_data_fetching():
    result = fetch_exchange_data("FX_DAILY","EUR","USD")
    assert isinstance(result, DataFrame)

    assert "timestamp" in result.columns
    assert "open" in result.columns
    assert "high" in result.columns
    assert "low" in result.columns
    assert "close" in result.columns

    assert len(result) >= 100

def test_calculation():
    assert calculate_new_currency(100,"0.9") == 90
    
