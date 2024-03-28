import json
from github import Github

with open("token.json", "r") as token_file:
    token = json.load(token_file)
_g = Github(token['token'])
org = _g.get_organization("UNCW-CSC-450")



REPOS = [
    {'name': 'csc450-sp24-project-team_1'},
    {'name': 'csc450-sp24-project-team2'},
    {'name': 'csc450-sp24-project-team-3'},
    {'name': 'csc450-sp24-project-team_4'},
    {'name': 'csc450-sp24-project-group-5'},
    {'name': 'csc450-sp24-project-team-6'},
    {'name': 'csc450-sp24-project-team-7'},
    {'name': 'csc450-sp24-project-team-8'},
    {'name': 'csc450-sp24-project-team-9'},
    {'name': 'csc450-sp24-project-team-10'},
    {'name': 'csc450-sp24-project-team-11'},
]
