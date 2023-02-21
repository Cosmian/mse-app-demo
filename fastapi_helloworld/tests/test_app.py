import requests


def test_hello(url, certificate):
    response = requests.get(url, verify=certificate)
    assert response.status_code == 200
    assert b"Hello world" in response.content


def test_health(url, certificate):
    if url.endswith("/"):
        url = url[:-1]
    response = requests.get(f"{url}/health", verify=certificate)
    assert response.status_code == 200
