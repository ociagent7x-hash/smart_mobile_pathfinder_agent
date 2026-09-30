import os
import http.server
import socketserver

PORT = 8000

# Ensure 'output' directory exists
os.makedirs("output", exist_ok=True)

# Change working directory to 'output' so SimpleHTTPRequestHandler serves dashboard.html directly
os.chdir("output")

Handler = http.server.SimpleHTTPRequestHandler

print(f"[+] Starting Agent Dashboard Server at: http://127.0.0.1:{PORT}/dashboard.html")
print("[*] Press Ctrl+C in your terminal to stop the server when finished.\n")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped.")