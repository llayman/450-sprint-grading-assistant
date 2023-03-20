import json
from github import Github

with open("token.json", "r") as token_file:
    token = json.load(token_file)
_g = Github(token['token'])
org = _g.get_organization("UNCW-CSC-450")
REPOS = [
    'csc450-sp23-project-team1',
    'csc450-sp23-project-team-2',
    'csc450-sp23-project-team-3',
    'csc450-sp23-project-team-4',
    'csc450-sp23-project-team-5',
    'csc450-sp23-project-team6',
    'csc450-sp23-project-team7',
    'csc450-sp23-project-team-8',
    'csc450-sp23-project-team-9',
]
