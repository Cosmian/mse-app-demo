import requests


def test_read_write(url, certificate):
    response = requests.get(
        url,
        headers={
            "Authorization": "Bearer bAyJhel6vwzrvNcy7ux2nULRwpP6BviE34KSiZRGixo="
        },
        verify=certificate,
    )
    assert response.status_code == 404
    assert b"You should write before read" in response.content

    response = requests.post(
        url,
        headers={
            "Authorization": "Bearer 6fMvPktkMwZj5UJwxasOIj7sO37H4DfZZo05Nn1fFYw="
        },
        verify=certificate,
    )
    assert response.status_code == 200

    response = requests.get(
        url,
        headers={
            "Authorization": "Bearer bAyJhel6vwzrvNcy7ux2nULRwpP6BviE34KSiZRGixo="
        },
        verify=certificate,
    )
    assert response.status_code == 200


def test_health(url, certificate):
    response = requests.get(f"{url}/health", verify=certificate)
    assert response.status_code == 200
