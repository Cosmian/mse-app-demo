import argparse
import socket
import ssl
import tempfile
from io import StringIO
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import pandas as pd
import requests

FLASK_TOKEN = "Bearer Yt3qdlRXfSpkfc17DmzSSiNsw64ca3TLOAKX6DJWsxA="


def get_certificate(hostname: str, port: int) -> str:
    with socket.create_connection((hostname, port)) as sock:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            bin_cert = ssock.getpeercert(True)
            if not bin_cert:
                raise Exception("Can't get peer certificate")
            return ssl.DER_cert_to_PEM_cert(bin_cert)


def download_anonymized_data(
    customer_id: str, url: str, cert_path: Optional[Path] = None
):
    headers = {"Authorization": FLASK_TOKEN}

    try:
        response: requests.Response = requests.get(
            f"{url}/{customer_id}", headers=headers, verify=cert_path
        )
    except requests.exceptions.SSLError as e:
        raise Exception(
            "SSL certificate verification failed! \nRetry with `--ssl` option"
        )

    if response.status_code != 200:
        raise Exception(
            f"Bad response from server: {response.status_code} {response.text}"
        )

    print("Anonymized data received successfully:")

    df_anonymized = pd.read_csv(StringIO(response.text))

    print(df_anonymized.head())


def main(url: str, self_signed_ssl: bool = False):
    if not url.startswith("http"):
        print(f"WARNING: no scheme found in {url}. Continuing with HTTP.")
        url = f"http://{url}"
    parsed_url = urlparse(url)

    cert_path: Optional[Path] = None
    if self_signed_ssl and parsed_url.scheme == "https":
        hostname, port = parsed_url.hostname, 443

        cert_path = Path(tempfile.gettempdir()) / f"{hostname}.pem"
        if not cert_path.exists():
            cert_data = get_certificate(hostname, port)
            cert_path.write_bytes(cert_data.encode("utf-8"))

    download_anonymized_data("customerX", url, cert_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Data provider example.")
    parser.add_argument("url", type=str, help="URL of the secure API")
    parser.add_argument(
        "--ssl", action="store_true", help="Use a self signed ssl certificate"
    )

    try:
        args = parser.parse_args()
        main(args.url, args.ssl)
    except SystemExit:
        parser.print_help()
        raise
