from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


#get data ticker
def test_get_data_with_ticker():
    response = client.get("ticker/data/?ticker=BTCUSD")
    assert response.status_code == 200

def test_get_data_with_unidentified_ticker():
    response = client.get("ticker/data/?ticker=SOMEWRONGUSD")
    assert response.status_code == 404

#get latest price ticker
def test_get_latest_price_ticker():
    response = client.get("/ticker/latest_price/?ticker=ETHUSD")
    assert response.status_code == 200

def test_get_latest_price_unidentified_ticker():
    response = client.get("/ticker/latest_price/?ticker=SOMEWRONGUSD")
    assert response.status_code == 404


# filtered
def test_get_price_ticker_filtered():
    response = client.get("/ticker/prices/filtered/?ticker=BTCUSD&date_from=2026-01-27&date_to=2026-01-27")
    assert response.status_code == 200

def test_get_price_ticker_filtered_nothing():
    response = client.get("/ticker/prices/filtered/?ticker=BTCUSD")
    assert response.status_code == 200

def test_get_price_ticker_filtered_date_from():
    response = client.get("/ticker/prices/filtered/?ticker=BTCUSD&date_from=2026-01-27")
    assert response.status_code == 200

def test_get_price_ticker_filtered_date_to():
    response = client.get("/ticker/prices/filtered/?ticker=BTCUSD&date_to=2026-01-27")
    assert response.status_code == 200

def test_get_price_ticker_filtered_value_error():
    response = client.get("/ticker/prices/filtered/?ticker=BTCUSD&date_to=2026.01.27")
    assert response.status_code == 400
    assert "detail" in response.json()
