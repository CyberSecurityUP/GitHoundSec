import subprocess
import os
from backend.github_collector import collect_repos

def run_trufflehog(repo_url: str, output_path: str):
    """Executa TruffleHog em repositório remoto."""
    cmd = [
        "trufflehog", "git", repo_url,
        "--json",
        "--no-update"
    ]
    with open(output_path, "w") as outfile:
        result = subprocess.run(cmd, stdout=outfile, stderr=subprocess.PIPE, text=True)
        if result.stderr:
            print("[TruffleHog STDERR]", result.stderr)

def run_trufflehog_org(org_name: str, output_path: str):
    import subprocess, os
    env = os.environ.copy()
    cmd = [
        "trufflehog",
        "github",
        f"--org={org_name}",
        "--json",
        "--no-update"
    ]
    with open(output_path, "w") as outfile:
        subprocess.run(cmd, stdout=outfile, stderr=subprocess.PIPE, text=True, env=env)
    return output_path


def run_gitleaks(repo_path: str, output_path: str):
    """Executa Gitleaks localmente após clone do repositório."""
    cmd = [
        "gitleaks", "git",
        "--repo-path", repo_path,
        "--report-format", "json",
        "--report-path", output_path,
        "--no-banner"
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.stderr:
        print("[Gitleaks STDERR]", result.stderr)

# backend/gitleaks_runner.py

import subprocess
import uuid
import os

def run_gitleaks_scan(repo_name: str, use_token=False, token=None, config_enabled=False, config_path=None):
    repo_path = os.path.join("temp_repos", repo_name)
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"Repositório não encontrado em {repo_path}")

    os.makedirs("outputs", exist_ok=True)
    report_id = str(uuid.uuid4())[:8]
    report_path = os.path.join("outputs", f"gitleaks-report-{report_id}.json")

    cmd = [
        "gitleaks", "detect",
        "--source", repo_path,
        "--report-format", "json",
        "--report-path", report_path,
        "-v"
    ]

    if config_enabled and config_path:
        cmd += ["--config", config_path]

    env = os.environ.copy()
    if use_token and token:
        env["GITHUB_TOKEN"] = token

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "report": report_path
    }

def clone_repo(repo_url: str, dest_folder: str):
    if os.path.exists(dest_folder):
        return
    subprocess.run(["git", "clone", repo_url, dest_folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def scan_organization_secrets(token: str, org: str, base_output_path: str):
    os.makedirs("temp_repos", exist_ok=True)
    os.makedirs(base_output_path, exist_ok=True)

    all_repos = collect_repos(token, org)
    results = []

    for repo in all_repos:
        repo_url = f"https://github.com/{repo}"
        repo_name = repo.split("/")[-1]
        print(f"[+] Escaneando: {repo_url}")

        # TruffleHog remoto
        trufflehog_output = os.path.join(base_output_path, f"{repo_name}_trufflehog.json")
        run_trufflehog(repo_url, trufflehog_output)

        # Gitleaks local
        local_path = os.path.join("temp_repos", repo_name)
        clone_repo(repo_url, local_path)
        gitleaks_output = os.path.join(base_output_path, f"{repo_name}_gitleaks.json")
        run_gitleaks(local_path, gitleaks_output)

        results.append({
            "repo": repo,
            "trufflehog": trufflehog_output,
            "gitleaks": gitleaks_output
        })

    return results
