import json
import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler

import requests

serverPort = 8080
hostName = "127.0.0.1"

class RequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(RequestHandler, self).end_headers()


    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()


    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        bytes_body = self.rfile.read(content_len)
        json_body = json.loads(bytes_body.decode('utf-8'))
        url = json_body['domain_name']
        data = json_body['data']
        response = requests.post(f"https://{url}/", json={"data": data}, verify=False)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.content)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), RequestHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
