import difflib
from github import Github

def detect_typosquat_repos(org_name: str, token: str = None, similarity_threshold: float = 0.75):
    g = Github(token) if token else Github()
    try:
        org = g.get_organization(org_name)
        repos = list(org.get_repos())
    except Exception as e:
        return [f"❌ Error fetching repositories: {str(e)}"]

    names = [repo.name for repo in repos]
    results = []
    checked_pairs = set()

    for i, name1 in enumerate(names):
        for j, name2 in enumerate(names):
            if i >= j:
                continue
            pair_key = tuple(sorted([name1, name2]))
            if pair_key in checked_pairs:
                continue
            ratio = difflib.SequenceMatcher(None, name1.lower(), name2.lower()).ratio()
            if ratio >= similarity_threshold:
                results.append(f"⚠️ Possible typosquat pair: '{name1}' <-> '{name2}' (Similarity: {round(ratio*100, 2)}%)")
            checked_pairs.add(pair_key)

    if not results:
        return ["✅ No suspicious typosquat repositories detected."]
    return results
