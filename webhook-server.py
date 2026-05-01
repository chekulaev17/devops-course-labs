#!/usr/bin/env python3
import json
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

APP_DIR = "/home/anm/DevOps/website-example"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)

        event = self.headers.get('X-GitHub-Event')

        if event == "push":
            subprocess.run(["bash", "deploy.sh"], cwd=APP_DIR)

        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
