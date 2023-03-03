"""Tests for sentiment analysis app"""
import requests


def test_recognition(url, certificate):
    """Test analysis"""
    response = requests.post(
        f"{url}/", json={"data": "long and boring"}, verify=certificate
    )
    assert response.status_code == 200
    assert response.json() == {"label": "NEGATIVE", "score": 0.9924578666687012}

    response = requests.post(
        f"{url}/", json={"data": "wonderful movie"}, verify=certificate
    )
    assert response.status_code == 200
    assert response.json() == {"label": "POSITIVE", "score": 0.9942570328712463}


def test_recognition_error(url, certificate):
    """Test error on post route if no data"""
    response = requests.post(f"{url}/", verify=certificate)
    assert response.status_code == 422


def test_health(url, certificate):
    """Test health check route"""
    response = requests.get(f"{url}/health", verify=certificate)
    assert response.status_code == 200
