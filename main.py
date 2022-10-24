from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import json

from collections import namedtuple
from github import Github
from typing import Dict

Sprint = namedtuple('Sprint', 'start end')


class UserStats:

    def __init__(self, name: str = None):
        self.name = name
        self.pulls = []
        self.commits = []
        self.issues = []


def get_stats_for_sprint(sprint: Sprint):
    with open("token.json", "r") as token_file:
        token = json.load(token_file)
    g = Github(token['token'])
    org = g.get_organization("UNCW-CSC-450")
    repos = [
        'csc450fa22-project-team-1-1',
        'csc450fa22-project-team-2',
        'csc450fa22-project-team-3',
        'csc450fa22-project-group-4',
        'csc450fa22-project-team-5',
        'csc450fa22-project-group-6',
        'csc450fa22-project-group-7',
        'csc450fa22-project-group-8',
    ]

    for repo in repos:
        r = org.get_repo(repo)
        print('=' * 10)
        print(r.full_name)

        user_stats: Dict[str, UserStats] = {}

        # Gather commits authored by a user. This may be separate from the committer due to merging.
        for c in r.get_commits(since=sprint.start, until=sprint.end):
            # Commits can have no author for unknown reasons.
            if c.author is None:
                print(f"c.author is None: https://github.com/{r.full_name}/commit/{c.url.split('/')[-1]}")
                continue
            user_stats.setdefault(c.author.login, UserStats(c.author.name)).commits.append(c)

        # Gather user-initiated PRs
        for p in r.get_pulls(state="all"):
            if p.created_at.replace(tzinfo=timezone.utc) > sprint.start:
                user_stats[p.user.login].pulls.append(p)

        # Gather user-assigned issues
        for i in r.get_issues(state='all'):
            if i.assignees:
                for assignee in i.assignees:
                    user_stats.setdefault(assignee.login, UserStats(assignee.login)).issues.append(i)

        # Loop over user_stats dictionary to compute statistics on a per-user basis.
        for author, stats in user_stats.items():
            print(
                f"\n\n{author} ({stats.name}) - {len(stats.commits)} commits, {len(stats.pulls)} PRs, {len(stats.issues)} issues assigned")

            # Compute commit statistics
            print(f'\tCommits: {len(stats.commits)}')
            for c in stats.commits:
                # the commit's last_modified is when it was merged into main
                # the commitStats last_modified is when the source files were last worked on
                # format is Mon, 10 Oct 2022 21:33:08 GMT
                print(
                    f"\t\t{c.stats.last_modified} {len(c.files)} files, total:{c.stats.total} adds:{c.stats.additions} "
                    f"deletes:{c.stats.deletions} https://github.com/{r.full_name}/commit/{c.url.split('/')[-1]}")

            # compute pull request statistics
            pr_stats = {}
            for p in stats.pulls:
                pr_stats[p.state] = pr_stats.get(p.state, 0) + 1

            print(f'\tPRs:{len(stats.pulls)}, {pr_stats}')
            for p in stats.pulls:
                print(f"\t\t{p.created_at} {p.html_url}")


if __name__ == "__main__":
    SPRINT_1 = Sprint(datetime(2022, 10, 7, tzinfo=ZoneInfo('US/Eastern')),
                      datetime(2022, 10, 20, tzinfo=ZoneInfo('US/Eastern')))

    get_stats_for_sprint(SPRINT_1)
