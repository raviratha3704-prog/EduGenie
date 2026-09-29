from fastapi.testclient import TestClient

import main


client = TestClient(
    main.app
)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_empty_question():

    response = client.post(
        "/qa",
        json={
            "question": ""
        }
    )

    assert response.status_code == 422


def test_short_quiz_text():

    response = client.post(
        "/quiz",
        json={
            "text": "short"
        }
    )

    assert response.status_code == 422


def test_summary_validation():

    response = client.post(
        "/summarize",
        json={
            "text": "short"
        }
    )

    assert response.status_code == 422


def test_learning_validation():

    response = client.post(
        "/learn/recommendations",
        json={
            "topic": "",
            "level": "beginner",
            "hours_per_week": 5
        }
    )

    assert response.status_code == 422