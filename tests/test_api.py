import os
import sys

from fastapi.testclient import TestClient


# -------------------------------------------------
# Fix import path so pytest can import app.main
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from app.main import app  # noqa: E402


client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "status" in data


def test_predict():
    payload = {
        "product_id": "TEC-PH-10000000",
        "ship_mode": "Standard Class",
        "segment": "Consumer",
        "state": "California",
        "country": "United States",
        "market": "US",
        "region": "West",
        "category": "Technology",
        "sub_category": "Phones",
        "order_priority": "Medium",
        "quantity": 2,
        "discount": 0.1,
        "profit": 50.0,
        "shipping_cost": 10.0,
        "ship_days": 4,
        "order_month": 5,
        "order_year": 2014,
        "profit_margin": 0.2,
    }

    response = client.post("/ml/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)

    # Some projects return prediction directly,
    # some return {"prediction": {...}}
    prediction = data.get("prediction", data)

    assert "predicted_sales" in prediction
    assert (
        "predicted_sales_class" in prediction
        or "sales_class" in prediction
    )


def test_search_sales():
    response = client.get("/search/sales?category=Technology&limit=5")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, (dict, list))


def test_agent_chat():
    payload = {
        "message": "Explain demand forecasting and anomaly detection for retail sales."
    }

    response = client.post("/agent/chat", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)

    assert (
        "selected_agent" in data
        or "response" in data
        or "answer" in data
        or "message" in data
    )


def test_azure_status():
    response = client.get("/azure/status")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)

    assert (
        data.get("status") in ["Completed", "Configured", "Running", "Success"]
        or "azure_components_used" in data
        or "section" in data
    )


def test_pipeline_status():
    response = client.get("/pipeline/status")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)

    assert (
        data.get("status") in ["Completed", "Configured", "Running", "Success"]
        or "pipeline_flow" in data
        or "flow" in data
        or "section" in data
    )