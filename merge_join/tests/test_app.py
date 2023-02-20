import requests


def test_merge_join(url, certificate):
    response = requests.delete(f"{url}/", verify=certificate)
    assert response.status_code == 200

    files = {'file': open('./client/data/A.csv', 'rb')}
    response = requests.post(f"{url}/", files=files, verify=certificate)
    assert response.status_code == 200

    files = {'file': open('./client/data/B.csv', 'rb')}
    response = requests.post(f"{url}/", files=files, verify=certificate)
    assert response.status_code == 200

    response = requests.get(f"{url}/", verify=certificate)
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.csv'
    assert 66000 <= len(response.content) <= 70000

    response = requests.delete(f"{url}/", verify=certificate)
    assert response.status_code == 200

    response = requests.get(f"{url}/", verify=certificate)
    assert response.status_code == 422


def test_merge_join_error(url, certificate):
    requests.delete(f"{url}/", verify=certificate)

    response = requests.post(f"{url}/", verify=certificate)
    assert response.status_code == 422

    files = {'file': open('./tests/data.json', 'rb')}
    response = requests.post(f"{url}/", files=files, verify=certificate)
    assert response.status_code == 422

    files = {'file': open('./client/data/A.csv', 'rb')}
    response = requests.post(f"{url}/", files=files, verify=certificate)
    response = requests.get(f"{url}/", verify=certificate)
    assert response.status_code == 422


def test_health(url, certificate):
    response = requests.get(f"{url}/health", verify=certificate)
    assert response.status_code == 200
