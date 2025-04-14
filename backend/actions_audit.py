# backend/actions_audit.py

import os
import glob
import yaml
import re

def list_workflows(repo_path: str):
    workflows_path = os.path.join(repo_path, ".github", "workflows")
    if not os.path.exists(workflows_path):
        return []
    return glob.glob(os.path.join(workflows_path, "*.yml"))

def audit_workflow(file_path: str):
    risks = []
    with open(file_path, "r") as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            return [f"Erro ao parsear YAML: {e}"]

    if not data:
        return ["Workflow vazio ou inválido"]

    jobs = data.get("jobs", {})
    for job_name, job_data in jobs.items():
        steps = job_data.get("steps", [])
        for step in steps:
            if "run" in step:
                cmd = step["run"]
                if re.search(r"(curl|wget).*(bash|sh)", cmd):
                    risks.append(f"[{file_path}] Uso de download + execução: `{cmd}`")
                if "sudo" in cmd or "chmod 777" in cmd:
                    risks.append(f"[{file_path}] Comando potencialmente inseguro: `{cmd}`")

            if "uses" in step:
                uses = step["uses"]
                if "@" not in uses:
                    risks.append(f"[{file_path}] Action sem versionamento: `{uses}`")
                elif "@master" in uses or "@main" in uses:
                    risks.append(f"[{file_path}] Action referenciando branch: `{uses}`")
    return risks

def audit_repo_actions(repo_path: str):
    result = []
    for wf in list_workflows(repo_path):
        result.extend(audit_workflow(wf))
    return result
