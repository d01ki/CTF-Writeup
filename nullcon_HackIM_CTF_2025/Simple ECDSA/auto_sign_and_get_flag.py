#!/usr/bin/env python3
# auto_sign_and_get_flag.py
# Usage: python3 auto_sign_and_get_flag.py <host> <port>
# Example: python3 auto_sign_and_get_flag.py 10.0.0.5 1337

import sys
import socket
import re
import importlib.util
import pathlib
import sys as _sys
import time
from typing import Tuple

def load_chall_module(chall_path: pathlib.Path):
    if not chall_path.exists():
        raise FileNotFoundError(f"{chall_path} not found in current dir.")
    spec = importlib.util.spec_from_file_location("ctf_chal", str(chall_path))
    module = importlib.util.module_from_spec(spec)
    # ensure same directory on path so ec.py can be imported
    _sys.path.insert(0, str(chall_path.parent))
    spec.loader.exec_module(module)
    return module

def extract_challenge(text: str) -> str:
    # look for a 64-hex (32 bytes) or 32-hex (maybe 16 bytes) pattern
    m = re.search(r"\b([0-9a-fA-F]{64})\b", text)
    if m:
        return m.group(1)
    # fallback: 32-hex
    m = re.search(r"\b([0-9a-fA-F]{32})\b", text)
    if m:
        return m.group(1)
    # sometimes challenge is prefixed like 'challenge: 0x...'
    m = re.search(r"0x([0-9a-fA-F]{64})", text)
    if m:
        return m.group(1)
    return None

def communicate_and_get_flag(host: str, port: int, module) -> Tuple[str,str]:
    """Connects, reads banner/challenge, signs, sends, returns server response."""
    s = socket.create_connection((host, port), timeout=10)
    s_file = s.makefile('rwb', buffering=0)
    # Helper to recv until timeout or prompt-like behavior
    def recv_all(timeout=2.0):
        s.settimeout(timeout)
        data = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
                # short heuristic: stop if server ends with newline and pause
                if len(chunk) < 4096:
                    break
        except socket.timeout:
            pass
        return data

    # read initial banner
    banner = recv_all(2.0).decode(errors='ignore')
    print("----- server banner -----")
    print(banner)
    chal_hex = extract_challenge(banner)
    # If not found, try to read a bit more (server might wait)
    if not chal_hex:
        # wait for server to send challenge; sometimes need to send an initial newline
        more = recv_all(1.0).decode(errors='ignore')
        banner += more
        print("additional data:")
        print(more)
        chal_hex = extract_challenge(banner)
    if not chal_hex:
        # As last resort, prompt the user to paste the challenge if it didn't arrive automatically
        raise RuntimeError("Couldn't find challenge hex in server banner. Paste the banner here or run interactively.")
    print("Found challenge hex:", chal_hex)

    # sign using module.sign()
    if not hasattr(module, "sign"):
        raise RuntimeError("Loaded challenge module doesn't provide sign(challenge_bytes).")
    challenge_bytes = bytes.fromhex(chal_hex)
    r, s_val = module.sign(challenge_bytes)
    # prepare payload. Many challenges expect "r,s\n"
    payload = f"{r},{s_val}\n".encode()
    print("Sending signature:", payload.decode().strip())
    s.sendall(payload)

    # read response (flag)
    time.sleep(0.2)
    resp = recv_all(3.0).decode(errors='ignore')
    # maybe server expects newline-terminated; try reading again
    if not resp:
        resp = recv_all(1.0).decode(errors='ignore')
    s.close()
    return resp, payload.decode().strip()

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 auto_sign_and_get_flag.py <host> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])

    # locate challenge script in current dir. Adjust filename if necessary.
    chall_filenames = ["chall (2).py", "chall.py", "challenge.py"]
    base = pathlib.Path.cwd()
    found = None
    for fname in chall_filenames:
        p = base / fname
        if p.exists():
            found = p
            break
    if not found:
        print("No challenge script found in current directory. Put 'chall (2).py' or 'chall.py' next to this script.")
        sys.exit(1)

    print(f"Loading challenge script from {found}")
    module = load_chall_module(found)
    print("Module loaded. It has attributes:", [n for n in dir(module) if not n.startswith('_')][:50])

    try:
        resp, sent = communicate_and_get_flag(host, port, module)
    except Exception as e:
        print("Error during communicate:", e)
        sys.exit(1)

    print("----- sent signature -----")
    print(sent)
    print("----- server response -----")
    print(resp)

if __name__ == "__main__":
    main()
