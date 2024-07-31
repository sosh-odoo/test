import os, requests
from github import Github

# Constants
GITHUB_API_URL = "https://api.github.com"
SUBMODULE_REPO = "test"

def search_repositories(token, query):
    """Search GitHub repositories using a query."""
    url = f"{GITHUB_API_URL}/search/repositories?q={query}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repos =  response.json()["items"]
        return repos
    else:
        print(f"Failed to search repositories: {response.status_code} - {response.text}")
        return []

def search_submodule(github_token, repo_owner, repo_name, submodule_name):
    g = Github(github_token)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    contents = repo.get_contents("")
    submodule_found = False

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
                            submodule_found = True
                            break

    return submodule_found

def main():
    query = f'"{SUBMODULE_REPO}"'
    token = os.environ["GITHUB_TOKEN"]
    repos = search_repositories(token, query)
    print(os.environ)
    submodule_name = os.environ["GITHUB_REPOSITORY"].split("/")[-1].replace(".git", "")

    with open('parent_repos.txt', 'w') as file:
        for repo in repos:
            repo_owner, repo_name = repo["full_name"].split("/")
            if search_submodule(token, repo_owner, repo_name, submodule_name):
                file.write(f"{repo['full_name']}\n")

if __name__ == "__main__":
    main()
