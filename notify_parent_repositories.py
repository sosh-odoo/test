import os
import requests
import json

# Fetch GitHub token from environment variable
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable not set")

# Fetch repositories
def fetch_repositories():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get("https://api.github.com/users/sosh-odoo/repos", headers=headers)
    response.raise_for_status()
    repos = [repo['full_name'] for repo in response.json()]
    return repos

# Check if a repository has a specific submodule
def has_submodule(repo):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }
    response = requests.get(f"https://raw.githubusercontent.com/{repo}/master/.gitmodules", headers=headers)
    if response.status_code == 200:
        content = response.text
        return 'submodule "test"' in content
    return False

# Trigger workflow dispatch
def trigger_dispatch(repo):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    # Get workflows
    response = requests.get(f"https://api.github.com/repos/{repo}/actions/workflows", headers=headers)
    response.raise_for_status()
    workflows = response.json().get('workflows', [])
    if not workflows:
        print(f"No workflows found in {repo}.")
        return

    workflow_id = workflows[0]['id']
    dispatch_url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow_id}/dispatches"
    data = {
        "ref": "master"
    }
    dispatch_response = requests.post(dispatch_url, headers=headers, data=json.dumps(data))
    if dispatch_response.status_code == 204:
        print(f"Dispatched workflow for {repo}")
    else:
        print(f"Failed to dispatch workflow for {repo}: {dispatch_response.text}")

def main():
    repos = fetch_repositories()
    for repo in repos:
        if has_submodule(repo):
            print(f"Submodule 'test' present in .gitmodules of {repo}")
            trigger_dispatch(repo)
        else:
            print(f"Submodule 'test' not found in {repo}.gitmodules.")

if __name__ == "__main__":
    main()
