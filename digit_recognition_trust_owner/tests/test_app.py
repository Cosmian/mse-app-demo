import requests


def test_recognition(url, certificate, data):
    response = requests.post(f'{url}/', json={"data": data}, verify=certificate)
    assert response.status_code == 200
    assert response.json() == {"number": "3"}


def test_recognition_error(url, certificate):
    response = requests.post(f'{url}/', verify=certificate)
    assert response.status_code == 422

    response = requests.post(f'{url}/', json={"data": "str"}, verify=certificate)
    assert response.status_code == 422


def test_health(url, certificate):
    response = requests.get(f"{url}/health", verify=certificate)
    assert response.status_code == 200
