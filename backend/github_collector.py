# backend/github_collector.py
from github import Github

def collect_repos(token: str, org_name: str):
    g = Github(token)
    try:
        org = g.get_organization(org_name)
    except:
        org = g.get_user(org_name)
    
    repos = org.get_repos()
    return [repo.full_name for repo in repos]
