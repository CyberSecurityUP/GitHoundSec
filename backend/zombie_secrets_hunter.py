import subprocess
import os
from typing import List

def zombie_secrets_scan(repo_path: str) -> List[str]:
    if not os.path.exists(repo_path):
        return ["❌ Repository path does not exist."]

    findings = []
    try:
        # Get all commit hashes
        commits = subprocess.check_output(["git", "rev-list", "--all"], cwd=repo_path, text=True).splitlines()
        for commit in commits:
            try:
                diff = subprocess.check_output(["git", "show", commit], cwd=repo_path, text=True, stderr=subprocess.DEVNULL)
                if any(keyword in diff.lower() for keyword in ["apikey", "token", "secret", "password"]):
                    findings.append(f"🔑 Potential secret in commit {commit}")
            except subprocess.CalledProcessError:
                continue

        if not findings:
            findings.append("✅ No zombie secrets found in commit history.")
        return findings
    except Exception as e:
        return [f"❌ Error during scan: {str(e)}"]
