from github import Github

# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = Auth.Token("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")

# First create a Github instance:

# Public Web Github
g = Github(auth=auth)

# Github Enterprise with custom hostname
# g = Github(base_url="https:///api/v3", auth=auth)

# Then play with your Github objects:
for repo in g.get_user().get_repos():
    print(repo.name)
