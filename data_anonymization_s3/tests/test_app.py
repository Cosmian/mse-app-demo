from io import StringIO
from pathlib import Path

import pandas as pd
import requests


def test_send_read_data(url, certificate):
    cwd_path: Path = Path(__file__).parent.resolve()
    files = {"files": open(cwd_path.parent / "files/data.csv", "rb")}

    send_response: requests.Response = requests.post(
        f"{url}/test_customer",
        files=files,
        headers={
            "Authorization": "Bearer os8BWtTEiygBGksHNwMjgcsqsaPqJvmn83YzXEN16c0="
        },
        verify=certificate,
    )
    assert send_response.status_code == 200
    assert b"status: Success" in send_response.content

    get_response = requests.get(
        f"{url}/test_customer",
        headers={
            "Authorization": "Bearer Yt3qdlRXfSpkfc17DmzSSiNsw64ca3TLOAKX6DJWsxA="
        },
        verify=certificate,
    )

    assert get_response.status_code == 200

    df = pd.read_csv(StringIO(get_response.text))
    assert len(df) == 100


def test_read_wrong_customer(url, certificate):
    response = requests.get(
        f"{url}/wrong_customer_id",
        headers={
            "Authorization": "Bearer Yt3qdlRXfSpkfc17DmzSSiNsw64ca3TLOAKX6DJWsxA="
        },
        verify=certificate,
    )
    assert response.status_code == 400
    assert b"No file found for customer_id:" in response.content


def test_read_wrong_token(url, certificate):
    response = requests.get(
        f"{url}/wrong_customer_id",
        headers={"Authorization": "Bearer WRONG_TOKEN"},
        verify=certificate,
    )
    assert response.status_code == 401
    assert b"Invalid token!" in response.content


def test_health(url, certificate):
    response = requests.get(f"{url}/health", verify=certificate)
    assert response.status_code == 200
