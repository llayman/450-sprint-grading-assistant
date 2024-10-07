import json
from github import Github

with open("token.json", "r") as token_file:
    token = json.load(token_file)
_g = Github(token['token'])
org = _g.get_organization("UNCW-CSC-450")



REPOS = [
    {'name': 'csc450-fa24-team1'},
    {'name': 'csc450-fa24-team2'},
    {'name': 'csc450-fa24-team3'},
    {'name': 'csc450-fa24-team4'},
    {'name': 'csc450-fa24-team5'},
]
