import json
from github import Github

with open("token.json", "r") as token_file:
    token = json.load(token_file)
_g = Github(token['token'])
org = _g.get_organization("UNCW-CSC-450")
REPOS = [
    'csc450fa22-project-team-1-1',
    'csc450fa22-project-team-2',
    'csc450fa22-project-team-3',
    'csc450fa22-project-group-4',
    'csc450fa22-project-team-5',
    'csc450fa22-project-group-6',
    'csc450fa22-project-group-7',
    'csc450fa22-project-group-8',
]
