import json
from github import Github

with open("token.json", "r") as token_file:
    token = json.load(token_file)
_g = Github(token['token'])
org = _g.get_organization("UNCW-CSC-450")



REPOS = [
    {'name': 'csc450-sp23-project-team1'},
    {'name': 'csc450-sp23-project-team-2'},
    {'name': 'csc450-sp23-project-team-3'},
    {'name': 'csc450-sp23-project-team-4'},
    {'name': 'csc450-sp23-project-team-5'},
    {'name': 'csc450-sp23-project-team6'},
    {'name': 'csc450-sp23-project-team7'},
    {'name': 'csc450-sp23-project-team-8', 'branch': 'jonahMerge'},
    {'name': 'csc450-sp23-project-team-9'},
]
