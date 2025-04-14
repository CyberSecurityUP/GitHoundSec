# backend/run_trufflehog_single.py

import subprocess
import os

def run_trufflehog_generic(target: str, output_path: str):
    """
    Roda TruffleHog em uma organização (--org=) ou repositório git diretamente.
    Detecta se é URL ou nome de org.
    """
    is_repo = target.startswith("http") or target.endswith(".git")
    cmd = ["trufflehog"]
    cmd += ["git", target] if is_repo else ["github", f"--org={target}"]
    cmd += ["--json", "--no-update"]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as outfile:
        result = subprocess.run(cmd, stdout=outfile, stderr=subprocess.PIPE, text=True)
        if result.stderr:
            print("[TruffleHog STDERR]", result.stderr)
    return output_path
