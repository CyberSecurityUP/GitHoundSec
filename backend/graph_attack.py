import requests
from pyvis.network import Network
import os
from typing import Optional

GITHUB_API = "https://api.github.com"


def build_graph_from_org(org_name: str, token: Optional[str] = None) -> str:
    headers = {
        "Accept": "application/vnd.github+json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    net = Network(height='800px', width='100%', bgcolor='#111111', font_color='white')
    net.force_atlas_2based()

    org_node_id = f"ORG::{org_name}"
    net.add_node(org_node_id, label=org_name, shape='ellipse', color='orange')

    repos_response = requests.get(f"{GITHUB_API}/orgs/{org_name}/repos?per_page=100", headers=headers)
    repos = repos_response.json()
    if not isinstance(repos, list):
        raise Exception(f"GitHub API error: {repos.get('message', 'unknown error')}")

    added_any_node = False

    for repo in repos:
        repo_name = repo['name']
        repo_node_id = f"REPO::{repo_name}"
        net.add_node(repo_node_id, label=repo_name, shape='box', color='deepskyblue')
        net.add_edge(org_node_id, repo_node_id)
        added_any_node = True

        # Tenta usar /collaborators se o token existir
        collabs = []
        if token:
            collabs_url = f"{GITHUB_API}/repos/{org_name}/{repo_name}/collaborators"
            collabs_response = requests.get(collabs_url, headers=headers)
            if collabs_response.status_code == 200:
                collabs = collabs_response.json()
        
        # Se não veio nada, tenta pegar contributors (público)
        if not collabs:
            contributors_url = f"{GITHUB_API}/repos/{org_name}/{repo_name}/contributors"
            contributors_response = requests.get(contributors_url, headers=headers)
            if contributors_response.status_code == 200:
                collabs = contributors_response.json()

        for user in collabs:
            login = user.get('login')
            if not login:
                continue
            permission = user.get('permissions', {}) if token else {}
            role = 'admin' if permission.get('admin') else 'write' if permission.get('push') else 'contrib'
            label = f"{login} [{role}]" if token else login
            user_id = f"USER::{login}"
            net.add_node(user_id, label=label, shape='dot', color='yellow')
            net.add_edge(repo_node_id, user_id)

    if not added_any_node:
        raise Exception("No public repositories or collaborators found. Try using a GitHub token.")

    os.makedirs("outputs", exist_ok=True)
    output_file = f"outputs/{org_name}_graph.html"
    net.show(output_file)
    return output_file