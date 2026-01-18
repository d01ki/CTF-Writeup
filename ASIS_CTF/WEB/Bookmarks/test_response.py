#!/usr/bin/env python3
"""
Test what the actual HTTP response looks like
"""

import requests

TARGET = "http://65.109.202.184"

# Login with one of our CRLF users
session = requests.Session()

# Try to login with the last user we created
usernames = [
    "exp87520139",
    "hax2520946", 
    "pwn2520946"
]

for username in usernames:
    print(f"\n[*] Trying to login as: {username}")
    r = session.post(f"{TARGET}/login", data={
        "username": username,
        "password": f"pass{username[3:]}" if username.startswith("exp") else f"pass{username[3:]}"
    })
    
    if "dashboard" in r.text.lower():
        print(f"[+] Logged in!")
        
        # Get dashboard
        print("\n[*] Fetching /dashboard...")
        r = session.get(f"{TARGET}/dashboard")
        
        print(f"[+] Status: {r.status_code}")
        print(f"[+] All headers:")
        for k, v in r.headers.items():
            print(f"    {k}: {v}")
        
        print(f"\n[+] Raw response (first 1000 bytes):")
        print(r.text[:1000])
        
        print(f"\n[+] Looking for script tag...")
        if "<script>" in r.text.lower():
            print("[+] Script tag found!")
            # Find and print the script
            start = r.text.lower().find("<script>")
            end = r.text.lower().find("</script>", start)
            if start > -1 and end > -1:
                print(r.text[start:end+9])
        else:
            print("[!] No script tag found")
        
        break
