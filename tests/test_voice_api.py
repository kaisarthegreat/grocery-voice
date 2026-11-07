from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_voice_transcript_is_returned_for_review():
    response = client.post(
        "/api/voice/transcript",
        json={"text": "2 litres milk", "language": "en-IN"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "text": "2 litres milk",
        "language": "en-IN",
        "received": True,
    }


def test_blank_voice_transcript_is_rejected():
    response = client.post(
        "/api/voice/transcript",
        json={"text": "   ", "language": "en-IN"},
    )
    assert response.status_code == 422


def test_unsupported_recognition_language_is_rejected():
    response = client.post(
        "/api/voice/transcript",
        json={"text": "milk", "language": "fr-FR"},
    )
    assert response.status_code == 422
