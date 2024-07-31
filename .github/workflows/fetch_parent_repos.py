import os
import requests
from github import Github

# Constants
GITHUB_API_URL = "https://api.github.com"
SUBMODULE_REPO = "test"

def get_parent_repositories(token, submodule_name):
    """Get parent repositories of a submodule."""
    query = f'"{submodule_name}"'
    repos = search_repositories(token, query)
    parent_repos = []

    for repo in repos:
        repo_owner, repo_name = repo["full_name"].split("/")
        if is_submodule(token, repo_owner, repo_name, submodule_name):
            parent_repos.append(repo["full_name"])

    return parent_repos

def search_repositories(token, query):
    """Search GitHub repositories using a query."""
    url = f"{GITHUB_API_URL}/search/repositories?q={query}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["items"]
    else:
        print(f"Failed to search repositories: {response.status_code} - {response.text}")
        return []

def is_submodule(github_token, repo_owner, repo_name, submodule_name):
    """Check if a repository contains a submodule."""
    g = Github(github_token)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    contents = repo.get_contents("")
    
    while contents:
        file_content = contents.pop(0)
        if file_content.type == 'dir':
            contents.extend(repo.get_contents(file_content.path))
        else:
            if file_content.size <= 100:
                if file_content.raw_data.get('type') == 'submodule':
                    if file_content.raw_data.get("submodule_git_url") is not None:
                        src = file_content.raw_data.get("submodule_git_url").split("/")[-1].replace(".git", "")
                        if src == submodule_name:
                            return True

    return False

def main():
    token = os.environ["GITHUB_TOKEN"]
    submodule_name = os.environ["GITHUB_REPOSITORY"].split("/")[-1].replace(".git", "")
    parent_repos = get_parent_repositories(token, submodule_name)

    with open('parent_repos.txt', 'w') as file:
        for repo in parent_repos:
            file.write(f"{repo}\n")

if __name__ == "__main__":
    main()
