import requests
import os
import base64
def scan_org_actions_permissions(org: str, token: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}"
    }

    repos_url = f"https://api.github.com/orgs/{org}/repos?per_page=100"
    response = requests.get(repos_url, headers=headers)
    repos = response.json()
    if not isinstance(repos, list):
        raise Exception(f"GitHub API error: {repos.get('message', 'unknown error')}")

    findings = {}

    for repo in repos:
        repo_name = repo['name']
        workflows_url = f"https://api.github.com/repos/{org}/{repo_name}/contents/.github/workflows"
        wf_resp = requests.get(workflows_url, headers=headers)

        if wf_resp.status_code != 200:
            continue  # No workflows

        files = wf_resp.json()
        repo_findings = []

        for file in files:
            if not file['name'].endswith(".yml") and not file['name'].endswith(".yaml"):
                continue

            file_content_url = file['download_url']
            if not file_content_url:
                continue

            file_text = requests.get(file_content_url, headers=headers).text
            lines = file_text.splitlines()

            for i, line in enumerate(lines):
                if 'uses:' in line and '@' not in line:
                    repo_findings.append(f"[!] Unpinned Action: {line.strip()} (line {i+1})")
                if 'run:' in line and ('curl' in line or 'wget' in line or 'bash' in line):
                    repo_findings.append(f"[!] Dangerous run detected: {line.strip()} (line {i+1})")
                if 'permissions:' in line and ("write" in line or "id-token" in line):
                    repo_findings.append(f"[!] Elevated permission: {line.strip()} (line {i+1})")

        if repo_findings:
            findings[repo_name] = repo_findings

    return findings
