from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.respond(200, {"status": "alive"})

        elif self.path == "/readyz":
            self.respond(200, {"status": "ready"})

        elif self.path == "/":
            self.respond(
                200,
                {
                    "service": "friendly-neighborhood-watch",
                    "hero": "Spider-Man",
                    "status": "operational",
                    "version": os.getenv("APP_VERSION", "local"),
                    "incidents": 3,
                },
            )

        else:
            self.respond(404, {"error": "not found"})

    def respond(self, status, payload):
        body = json.dumps(payload).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("Friendly Neighborhood Watch listening on port 8080")
    server.serve_forever()

