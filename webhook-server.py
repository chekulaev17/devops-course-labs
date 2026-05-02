#!/usr/bin/env python3
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

APP_DIR = "/home/chekulaev17/catty-reminders-app"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        self.rfile.read(length)

        event = self.headers.get('X-GitHub-Event')

        if event == "push":
            subprocess.run(["bash", "deploy.sh"], cwd=APP_DIR)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
