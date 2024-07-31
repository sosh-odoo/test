import os, requests
import json

def get_git_request(url,token):
    headers = {
        "Authorization": f"token {token}",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        reponse = response.json()
        print("Your data:")
        print("--------------")
        print(f"Response: {reponse}")
    else:
        print(f"Error: {response.status_code}")
    
def main():
    token = os.environ["GITHUB_TOKEN"]
    url = "https://api.github.com/user/repos"
    get_git_request(url, token)

if __name__ == "__main__":
    main()
