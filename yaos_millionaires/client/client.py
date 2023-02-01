"""Simple Python client for float_average microservice.

```console
$ pip install requests intel-sgx-ra
$ python client.py http://127.0.0.1:5000  # for local testing
```

Replace with HTTPS URL if you want to test with MSE.

"""

import socket
import ssl
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from intel_sgx_ra.quote import Quote
from intel_sgx_ra.ratls import ratls_verification


def reset(session: requests.Session, url: str) -> None:
    response: requests.Response = session.delete(url)

    if response.status_code != 200:
        raise Exception(f"Bad response: {response.status_code}")


def push(session: requests.Session, url: str, n: float) -> None:
    response: requests.Response = session.post(url=url, json={"n": n})

    if response.status_code != 200:
        raise Exception(f"Bad response: {response.status_code}")


def max(session: requests.Session, url: str) -> Dict[str, Any]:
    response: requests.Response = session.get(url)

    if response.status_code != 200:
        raise Exception(f"Bad response: {response.status_code}")

    return response.json()


def main() -> int:
    if (len(sys.argv) < 2):
        print("No argument URL found")
        return 1

    url: str = sys.argv[1]
    hostname, port = ((url.split("https://")[-1], 443) if "https" in url
                      else (url.split("http://")[-1], 80))
    session: requests.Session = requests.Session()

    if port == 443:
        cert_path: Path = Path(tempfile.gettempdir()) / "cert.pem"

        if not cert_path.exists():
            # get server certificate
            cert: Optional[str] = None
            with socket.create_connection((hostname, port)) as sock:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS)
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

    numbers: List[float] = [110_000.0, 25_000.0, 55_000.0]

    reset(session, url)

    for n in numbers:
        push(session, url, n)

    print(max(session, url))

    return 0


if __name__ == "__main__":
    main()
