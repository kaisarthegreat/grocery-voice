from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_parse_endpoint_returns_structured_items():
    response = client.post(
        "/api/grocery/parse",
        json={"text": "2 litres milk and aadha kilo aloo", "language": "en-IN"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {"name": "Milk", "quantity": "2 L"},
            {"name": "Potatoes", "quantity": "1/2 kg"},
        ],
        "count": 2,
        "language": "en-IN",
    }


def test_parse_endpoint_rejects_blank_text():
    response = client.post("/api/grocery/parse", json={"text": "   "})
    assert response.status_code == 422


def test_parse_endpoint_rejects_unsupported_language():
    response = client.post(
        "/api/grocery/parse", json={"text": "milk", "language": "fr-FR"}
    )
    assert response.status_code == 422
