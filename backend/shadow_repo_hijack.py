from github import Github
from typing import List
import difflib

def detect_shadow_repo_candidates(org_name: str, token: str = None) -> List[str]:
    g = Github(token) if token else Github()
    messages = []

    try:
        org = g.get_organization(org_name)
        official_repos = [repo.name.lower() for repo in org.get_repos()]
    except Exception as e:
        return [f"❌ Failed to fetch organization: {str(e)}"]

    # Search popular names / typo-similarities globally
    try:
        for name in official_repos:
            query = f"{name} in:name"
            results = g.search_repositories(query=query)
            for repo in results:
                if repo.owner.login.lower() != org_name.lower():
                    similarity = difflib.SequenceMatcher(None, name, repo.name.lower()).ratio()
                    if similarity > 0.8:
                        messages.append(
                            f"⚠️ Possible Shadow Repo: {repo.full_name} | Similar to '{name}' | Similarity: {round(similarity*100,2)}%"
                        )
    except Exception as e:
        messages.append(f"❌ Error during search: {str(e)}")

    if not messages:
        messages.append("✅ No shadow repository candidates detected.")

    return messages
