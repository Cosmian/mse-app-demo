import requests


def test_average(url, certificate):
    response = requests.delete(f'{url}/', verify=certificate)
    assert response.status_code == 200

    response = requests.get(f'{url}/', verify=certificate)
    assert response.status_code == 200
    assert response.json() == {"mean": None, "count": 0}

    response = requests.post(f'{url}/', json={"n": 100.0}, verify=certificate)
    assert response.status_code == 200

    response = requests.get(f'{url}/', verify=certificate)
    assert response.status_code == 200
    assert response.json() == {"mean": None, "count": 1}

    response = requests.post(f'{url}/', json={"n": 200.0}, verify=certificate)
    assert response.status_code == 200

    response = requests.get(f'{url}/', verify=certificate)
    assert response.status_code == 200
    assert response.json() == {"mean": 150, "count": 2}

    response = requests.delete(f'{url}/', verify=certificate)
    assert response.status_code == 200

    response = requests.get(f'{url}/', verify=certificate)
    assert response.status_code == 200
    assert response.json() == {"mean": None, "count": 0}


def test_average_error(url, certificate):
    response = requests.post(f'{url}/', verify=certificate)
    assert response.status_code == 422

    response = requests.post(f'{url}/', json={"n": "str"}, verify=certificate)
    assert response.status_code == 422


def test_health(url, certificate):
    response = requests.get(f"{url}/health", verify=certificate)
    assert response.status_code == 200
