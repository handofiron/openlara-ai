#!/usr/bin/env python3
import io
import json
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DISPLAY = ":1"
BRIDGE_PORT = 8090

ACTION_KEYS = {
    "forward": "Up",
    "left": "Left",
    "right": "Right",
}

held_key = None


def run(command):
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def xdotool(*args):
    return run(["xdotool", "--display", DISPLAY, *args])


def release_held_key():
    global held_key

    if held_key:
        xdotool("keyup", held_key)
        held_key = None


def press_action(action):
    global held_key

    if action == "no-op":
        release_held_key()
        return {"action": action, "held_key": None}

    if action == "jump":
        release_held_key()
        result = xdotool("key", "--clearmodifiers", "Alt")
        return {
            "action": action,
            "held_key": None,
            "returncode": result.returncode,
            "stderr": result.stderr.decode(errors="replace"),
        }

    key = ACTION_KEYS.get(action)
    if key is None:
        raise ValueError(f"Unknown action: {action}")

    if held_key != key:
        release_held_key()
        result = xdotool("keydown", key)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode(errors="replace"))
        held_key = key

    return {"action": action, "held_key": held_key}


class BridgeHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        global held_key

        if self.path == "/health":
            self.send_json(200, {
                "status": "ok",
                "display": DISPLAY,
                "held_key": held_key,
            })
            return

        if self.path == "/frame":
            result = run([
                "import",
                "-display", DISPLAY,
                "-window", "root",
                "png:-",
            ])

            if result.returncode != 0 or not result.stdout:
                self.send_json(500, {
                    "error": "frame capture failed",
                    "stderr": result.stderr.decode(errors="replace"),
                })
                return

            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(result.stdout)))
            self.end_headers()
            self.wfile.write(result.stdout)
            return

        if self.path == "/windows":
            result = xdotool("search", "--onlyvisible", "--name", "")
            windows = result.stdout.decode(errors="replace").splitlines()
            self.send_json(200, {"windows": windows})
            return

        self.send_json(404, {"error": "not found"})

    def do_POST(self):
        global held_key

        if self.path != "/input":
            self.send_json(404, {"error": "not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            action = payload.get("action", "no-op")
            result = press_action(action)
            self.send_json(200, result)
        except Exception as exc:
            self.send_json(400, {"error": str(exc)})

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", BRIDGE_PORT), BridgeHandler)
    print(f"OpenLara diagnostic bridge listening on port {BRIDGE_PORT}", flush=True)
    server.serve_forever()
