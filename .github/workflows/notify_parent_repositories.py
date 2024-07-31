import os
import json
from github import Github

def authenticate_with_github(token):
    return Github(token)

def get_repos_with_submodule(g, submodule_name):
    for repo in g.get_user().get_repos():
        submodule_content = repo.get_contents(".gitmodules")
        if submodule_content and submodule_name in submodule_content.decoded_content.decode("utf-8"):
            yield repo

def trigger_dispatch_event(repo, event_type):
    response = repo.create_dispatch(event_type=event_type)
    if response:
        print(f"Successfully triggered dispatch event for {repo.full_name}")
    else:
        print(f"Failed to trigger dispatch event for {repo.full_name}")

def main():
    g = authenticate_with_github(os.environ["GITHUB_TOKEN"])
    submodule_name = "test"
    event_type = "submodule-updated"

    for repo in get_repos_with_submodule(g, submodule_name):
        trigger_dispatch_event(repo, event_type)

if __name__ == "__main__":
    main()
