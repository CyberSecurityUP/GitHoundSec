# GitHoundSec

**GitHoundSec** is an advanced offensive security toolkit for auditing GitHub organizations, repositories, and developer activity. It offers modules for secrets detection, workflow abuse, access enumeration, attack simulation, and APT-style reconnaissance.

---

## 🚀 Features

- **Secrets Scanning:**
  - TruffleHog & Gitleaks support
  - Organization-wide or repo-specific
  - Support for external config files and tokens

- **GitHub Actions Auditing:**
  - Detect dangerous patterns and overly permissive workflows
  - Auto-analysis and reporting

- **Offensive Modules:**
  - Malicious PR simulation
  - Workflow backdoors (direct and via PR)
  - GitHub Token theft via CI
  - Phishing invitation generator
  - Typosquatting repo finder
  - Shadow repo hijack scanner

- **APT Recon Tools:**
  - Contributor graph analysis
  - GitHub apps & actions permissions scanner
  - Developer fingerprinting

- **.git Directory Finder:**
  - Find subdomains exposing `.git/config`

- **User-Friendly Interface:**
  - Built with `customtkinter`
  - Interactive tabs for each module
  - Output terminal and logs per action

---

## 🧠 Requirements

- Python 3.10+
- `customtkinter`
- `requests`, `subprocess`
- External binaries (optional):
  - `subfinder` (for subdomain enumeration)
  - `trufflehog`, `gitleaks`, `git`

---

## ⚙️ Setup

```bash
git clone https://github.com/YourOrg/GitHoundSec.git
cd GitHoundSec
pip install -r requirements.txt
python3 main.py
```

---

## 📦 Directory Structure

```
GitHoundSec/
├── backend/                  # Core logic for each module
├── frontend/                 # GUI using customtkinter
├── outputs/                  # Reports and results
├── temp_repos/              # Cloned repositories for analysis
└── main.py                   # Entry point
```

---

## 📌 Legal Disclaimer

This project is intended for educational and authorized security testing only. Unauthorized usage against systems you do not own or have explicit permission to test is illegal.

---

## 🧠 Author

Created by **Joas Antonio dos Santos** 
---

## 🔗 License

MIT License

