"""Basic HTTP server to handle digit from html page and query MSE deplyed App."""
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

import requests

PORT = 8080
HOST = "127.0.0.1"


class RequestHandler(SimpleHTTPRequestHandler):
    """Handler for HTTP requests."""

    def end_headers(self):
        """Set headers to handle CORS."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        return super().end_headers()

    def do_OPTIONS(self):
        """Handle POST requests."""
        self.send_response(200, "ok")
        self.end_headers()

    def do_POST(self):
        """Handle GET requests."""
        content_len = int(self.headers.get("Content-Length"))
        bytes_body = self.rfile.read(content_len)
        json_body = json.loads(bytes_body.decode("utf-8"))
        url = json_body["domain_name"]
        data = json_body["data"]
        response = requests.post(f"https://{url}/", json={"data": data}, verify=False)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.content)


if __name__ == "__main__":
    webServer = HTTPServer((HOST, PORT), RequestHandler)
    print(f"Server started http://{HOST}:{PORT}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
