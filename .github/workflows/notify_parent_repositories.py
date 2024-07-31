import os
import json
import subprocess
import sys
import requests

# Import PyGithub library
import github

# Authenticate with GitHub
g = github.Github(os.environ["GITHUB_TOKEN"])

# Get the authenticated user
user = g.get_user(login=True)
print(user)

# Loop through each repository and trigger a dispatch event
for repo in user.get_repos():
    # Check if the repository contains the submodule
    submodule_response = requests.get(
        f"https://api.github.com/repos/{repo.full_name}/contents/.gitmodules",
        headers={
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        },
    )

    if submodule_response.status_code == 200:
        submodule_content = json.loads(submodule_response.text)
        if "test" in submodule_content[0]["content"]:
            # Trigger repository_dispatch event
            dispatch_response = requests.post(
                f"https://api.github.com/repos/{repo.full_name}/dispatches",
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({"event_type": "submodule-updated"}),
            )

            if dispatch_response.status_code == 201:
                print(f"Successfully triggered dispatch event for {repo.full_name}")
            else:
                print(f"Failed to trigger dispatch event for {repo.full_name}")
                print(dispatch_response.text)
        else:
            print(f"Submodule 'test' not found in {repo.full_name}")
    else:
        print(f"Failed to get submodule content for {repo.full_name}")
        print(submodule_response.text)
