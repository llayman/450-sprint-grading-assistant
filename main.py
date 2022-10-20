from datetime import datetime
from zoneinfo import ZoneInfo
import json

from collections import namedtuple
from github import Github

Sprint = namedtuple('Sprint', 'start end')
SPRINT_1 = Sprint(datetime(2022, 10, 7, tzinfo=ZoneInfo('US/Eastern')),
                  datetime(2022, 10, 20, tzinfo=ZoneInfo('US/Eastern')))

ORG = "UNCW-CSC-450"
if __name__ == "__main__":

    with open("token.json", "r") as token_file:
        token = json.load(token_file)
    g = Github(token['token'])

    org = g.get_organization(ORG)
    repos = [
        'csc450fa22-project-group-4',
        'csc450fa22-project-group-7',
        'csc450fa22-project-group-8',
        'csc450fa22-project-group-6',
        'csc450fa22-project-team-1-1',
        'csc450fa22-project-team-2',
        'csc450fa22-project-team-3',
        'csc450fa22-project-team-5'
    ]

    for repo in repos:
        r = org.get_repo(repo)
        print(r.full_name)

        member_commits = {}
        for c in r.get_commits(since=SPRINT_1.start, until=SPRINT_1.end):
            if c.author.login not in member_commits:
                member_commits[c.author.login] = []
            member_commits[c.author.login].append(c)

        # TODO: Count pull requests

        for author, commits in member_commits.items():
            print(f"\n\n{author} - {len(commits)} commits")
            total = 0
            for c in commits:
                # the commit's last_modified is when it was merged into main
                # the commitStats last_modified is when the source files were last worked on
                # format is Mon, 10 Oct 2022 21:33:08 GMT
                # last_mod = c.stats.last_modified
                # formatted = datetime.strptime(last_mod, "%a, %d %b %Y %X %Z")
                print(f"\t{c.stats.last_modified} {len(c.files)} files, total:{c.stats.total} adds:{c.stats.additions} "
                      f"deletes:{c.stats.deletions} https://github.com/{r.full_name}/commit/{c.url.split('/')[-1]}")
        exit()
