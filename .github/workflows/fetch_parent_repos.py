import os, requests

# Constants
GITHUB_API_URL = "https://api.github.com"
SUBMODULE_REPO = "test"

def search_repositories(token, query):
    """Search GitHub repositories using a query."""
    url = f"https://api.github.com/search/repositories?q={query}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repos =  response.json()["items"]
        print(repos)
        return repos
    else:
        print(f"Failed to search repositories: {response.status_code} - {response.text}")
        return []

def main():
    # Replace this query with an appropriate one for finding repositories
    query = f'"{SUBMODULE_REPO}"'
    token = os.environ["GITHUB_TOKEN"]
    repos = search_repositories(token, query)
    
    with open('parent_repos.txt', 'w') as file:
        for repo in repos:
            file.write(f"{repo['full_name']}\n")

if __name__ == "__main__":
    main()
