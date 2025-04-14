import requests
import subprocess
from typing import List

def find_git_directories(domain: str) -> List[str]:
    subdomains = set()
    results = []

    try:
        # Use subfinder if available
        subfinder = subprocess.run(["subfinder", "-d", domain, "-silent"], capture_output=True, text=True)
        for line in subfinder.stdout.splitlines():
            subdomains.add(line.strip())
    except Exception:
        results.append("⚠️ subfinder not found or failed. Falling back to root domain only.")
        subdomains.add(domain)

    for sub in subdomains:
        url = f"http://{sub}/.git/config"
        try:
            r = requests.get(url, timeout=4)
            if r.status_code == 200 and "[core]" in r.text:
                results.append(f"✅ Found exposed .git on: {url}")
            else:
                results.append(f"❌ Not found or forbidden on: {url}")
        except Exception:
            results.append(f"⚠️ Failed to connect: {url}")

    if not results:
        results.append("No subdomains or .git folders found.")

    return results
