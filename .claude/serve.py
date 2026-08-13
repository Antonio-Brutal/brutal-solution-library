#!/usr/bin/env python3
"""Minimal static file server for the article preview (avoids http.server's __main__ argparse,
which calls os.getcwd() at import time and trips the sandbox)."""
import functools, os, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8747


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map,
                      ".svg": "image/svg+xml", ".mp4": "video/mp4", ".jpg": "image/jpeg"}

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    handler = functools.partial(Handler, directory=ROOT)
    print(f"serving {ROOT} on http://localhost:{PORT}/preview.html", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), handler).serve_forever()
