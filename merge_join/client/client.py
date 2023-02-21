"""Simple Python client for merge_join microservice.

```console
$ pip install requests intel-sgx-ra
$ python client.py http://127.0.0.1:5000  # for local testing
```

Replace with HTTPS URL if you want to test with MSE.

"""

from pathlib import Path
import socket
import ssl
import sys
import tempfile
from typing import List, Optional

from intel_sgx_ra.quote import Quote
from intel_sgx_ra.ratls import ratls_verification
import requests


def reset(session: requests.Session, url: str) -> None:
    response: requests.Response = session.delete(url)

    if response.status_code != 200:
        raise Exception(f"Bad response: {response.status_code}")


def push(session: requests.Session, url: str, path: Path) -> None:
    response: requests.Response = session.post(
        url=url,
        files={"file": (path.name, path.open("rb"), "text/csv", {"Expires": "0"})},
    )

    if response.status_code != 200:
        raise Exception(f"Bad response: {response.status_code}")


def merge(session: requests.Session, url: str, out_path: Path) -> None:
    response: requests.Response = session.get(url, stream=True)

    if "text/csv" not in response.headers.get("Content-Type", ""):
        raise Exception(f'Unexpected Content-Type: {response.headers["Content-Type"]}')

    if response.status_code != 200:
        raise Exception(f"Bad response: {response.status_code}")

    with out_path.open("wb") as fd:
        for chunk in response.iter_content(chunk_size=8192):
            fd.write(chunk)


def main() -> int:
    url: str = sys.argv[1]
    hostname, port = (
        (url.split("https://")[-1], 443)
        if "https" in url
        else (url.split("http://")[-1], 80)
    )
    session: requests.Session = requests.Session()

    if port == 443:
        cert_path: Path = Path(tempfile.gettempdir()) / "cert.pem"

        if not cert_path.exists():
            # get server certificate
            cert: Optional[str] = None
            with socket.create_connection((hostname, port), timeout=10) as sock:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    bin_cert = ssock.getpeercert(True)
                    if not bin_cert:
                        raise Exception("Can't get peer certificate")
                    cert = ssl.DER_cert_to_PEM_cert(bin_cert)
            if cert:
                # save it for future use
                cert_path.write_bytes(cert.encode("utf-8"))

        # verify quote in X.509 certificate
        quote: Quote = ratls_verification(cert_path)

        session.verify = f"{cert_path}"

    dir_path: Path = Path(__file__).resolve().parent / "data"
    csvs_path: List[Path] = [p.resolve() for p in dir_path.glob("*") if p.is_file()]

    reset(session, url)

    for csv_path in csvs_path:
        push(session, url, csv_path)

    result_path: Path = Path("result.csv")
    merge(session, url, result_path)
    print(f"Result saved: {result_path.resolve()}")

    return 0


if __name__ == "__main__":
    main()
