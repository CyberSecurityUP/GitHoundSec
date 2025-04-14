from github import Github
from typing import List

def apt_recon(org_name: str, token: str = None) -> List[str]:
    g = Github(token) if token else Github()
    findings = []

    try:
        org = g.get_organization(org_name)
        repos = list(org.get_repos())
    except Exception as e:
        return [f"❌ Error fetching organization: {str(e)}"]

    for repo in repos:
        repo_info = f"📦 {repo.full_name} - ⭐ {repo.stargazers_count} | 👁️ {repo.watchers_count} | 🍴 {repo.forks_count}"
        findings.append(repo_info)

        try:
            contributors = repo.get_contributors()
            for user in contributors:
                user_info = f"   👤 {user.login} | 📝 {user.contributions} contributions"
                findings.append(user_info)
        except Exception:
            findings.append("   ⚠️ Could not fetch contributors.")

        try:
            issues = repo.get_issues(state="open")
            for issue in issues:
                findings.append(f"   ❗ Issue: {issue.title[:80]} [{issue.user.login}]")
        except Exception:
            findings.append("   ⚠️ Could not fetch issues.")

    return findings
