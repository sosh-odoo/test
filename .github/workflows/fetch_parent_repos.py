import os, requests

# Constants
GITHUB_API_URL = "https://api.github.com"
ACCESS_TOKEN = os.environ["GITHUB_TOKEN"]
SUBMODULE_REPO = "test"

def search_repositories(query):
    """Search GitHub repositories using a query."""
    print("os", os.environ)
    url = f"https://api.github.com/search/repositories?q={query}"
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["items"]
    else:
        print(f"Failed to search repositories: {response.status_code} - {response.text}")
        return []

def main():
    # Replace this query with an appropriate one for finding repositories
    query = f'"{SUBMODULE_REPO}"'
    repos = search_repositories(query)
    
    with open('parent_repos.txt', 'w') as file:
        for repo in repos:
            file.write(f"{repo['full_name']}\n")

if __name__ == "__main__":
    main()
