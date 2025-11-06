import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

LEDGER_PATH = Path(__file__).resolve().parents[0] / "ledger.jsonl"
PORT = 8080

class AuditHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/ledger" or self.path == "/ledger/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            events = []
            if os.path.exists(LEDGER_PATH):
                try:
                    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                events.append(json.loads(line))
                except Exception as e:
                    self.send_error(500, f"Error reading ledger: {str(e)}")
                    return
            
            response = {
                "status": "ok",
                "count": len(events),
                "events": events
            }
            self.wfile.write(json.dumps(response, indent=2).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def log_message(self, format, *args):
        """Override to reduce log verbosity."""
        pass

def run_server(port=PORT):
    server_address = ("", port)
    with HTTPServer(server_address, AuditHandler) as httpd:
        print(f"Audit Trail API running at http://localhost:{port}/")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
