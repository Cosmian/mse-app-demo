"""Tests for sentiment analysis app"""
import requests


def test_recognition(url, certificate):
    """Test analysis"""
    response = requests.post(
        f"{url}/", json={"data": "long and boring"}, verify=certificate
    )
    assert response.status_code == 200
    assert response.json() == {"sentiment": "NEGATIVE"}

    response = requests.post(
        f"{url}/", json={"data": "wonderfull movie"}, verify=certificate
    )
    assert response.status_code == 200
    assert response.json() == {"sentiment": "POSITIVE"}


def test_recognition_error(url, certificate):
    """Test error on post route if no data"""
    response = requests.post(f"{url}/", verify=certificate)
    assert response.status_code == 422


def test_health(url, certificate):
    """Test health check route"""
    response = requests.get(f"{url}/health", verify=certificate)
    assert response.status_code == 200
