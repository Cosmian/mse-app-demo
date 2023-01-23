import requests


def test_read_write(url, certificate):
    response = requests.get(url, verify=certificate)
    assert response.status_code == 404
    assert b"You should write before read" in response.content

    response = requests.post(url, verify=certificate)
    assert response.status_code == 200

    response = requests.get(url, verify=certificate)
    assert response.status_code == 200


def test_health(url, certificate):
    response = requests.get(f"{url}/health", verify=certificate)
    assert response.status_code == 200


def test_login(url, certificate):
    response = requests.get(f"{url}/whoami", verify=certificate)
    assert response.status_code == 200
    assert b"username" in response.content
