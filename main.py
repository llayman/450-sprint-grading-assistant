from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from collections import namedtuple
from github import PullRequest, Commit, Issue
from typing import Dict, List

import config

Sprint = namedtuple('Sprint', 'start end')


class UserStats:

    def __init__(self, name: str = None):
        self.name = name
        self.pulls: List[PullRequest] = []
        self.commits: List[Commit] = []
        self.issues: List[Issue] = []


def get_stats_for_sprint(sprint: Sprint):
    for repo in config.REPOS:
        r = config.org.get_repo(repo)
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
                user_stats.setdefault(p.user.login, UserStats(p.user.login)).pulls.append(p)

        # Gather user-assigned issues
        for i in r.get_issues(state='all'):
            if i.assignees:
                for assignee in i.assignees:
                    user_stats.setdefault(assignee.login, UserStats(assignee.login)).issues.append(i)

        sprint_first_week_cutoff = sprint.start + timedelta(days=8)
        # Loop over user_stats dictionary to compute statistics on a per-user basis.
        for author, stats in user_stats.items():
            has_printed_cutoff = False
            print(
                f"\n\n{author} ({stats.name}) - {len(stats.commits)} commits, {len(stats.pulls)} PRs, {len(stats.issues)} issues assigned")

            # Show issues
            print(f'\tIssues: {len(stats.issues)}')
            for i in stats.issues:
                print(
                    f'\t\t{i.state.upper()} ({"" if i.milestone is None else i.milestone.title}) {i.title[:64]} https://github.com/{r.full_name}/issues/{i.number}')

            # Compute commit statistics
            print(f'\tCommits: {len(stats.commits)}')
            for c in stats.commits:
                # the commit's last_modified is when it was merged into main
                # the commitStats last_modified is when the source files were last worked on
                # format is Mon, 10 Oct 2022 21:33:08 GMT
                date_format = '%a, %d %b %Y %H:%M:%S %Z'
                commit_date = datetime.strptime(c.stats.last_modified, date_format).replace(tzinfo=timezone.utc)
                if commit_date < sprint_first_week_cutoff and not has_printed_cutoff:
                    print(f'\t\t----- FIRST WEEK END -----')
                    has_printed_cutoff = True


                # TODO: Figure a way to print the branch name
                # TODO: print commit comment
                print(
                    f"\t\t{c.stats.last_modified} {len(c.files)} files, total:{c.stats.total} adds:{c.stats.additions} "
                    f"deletes:{c.stats.deletions} https://github.com/{r.full_name}/commit/{c.url.split('/')[-1]}")

            if not has_printed_cutoff:
                print(f'\t\t----- FIRST WEEK END -----')

            # compute pull request statistics
            pr_stats = {}
            for p in stats.pulls:
                pr_stats[p.state] = pr_stats.get(p.state, 0) + 1

            print(f'\tPRs:{len(stats.pulls)}, {pr_stats}')
            for p in stats.pulls:
                print(f"\t\t{p.created_at} {p.html_url}")


if __name__ == "__main__":
    SPRINT_1 = Sprint(datetime(2023, 2, 23, tzinfo=ZoneInfo('US/Eastern')),
                      datetime(2023, 3, 14, tzinfo=ZoneInfo('US/Eastern')))
    SPRINT_2 = Sprint(datetime(year=2023, month=3, day=14, hour=14, tzinfo=ZoneInfo('US/Eastern')),
                      datetime(year=2023, month=3, day=27, hour=23, minute=59, tzinfo=ZoneInfo('US/Eastern')))

    SPRINT_3 = Sprint(datetime(year=2022, month=11, day=3, hour=14, minute=10, tzinfo=ZoneInfo('US/Eastern')),
                      datetime(year=2022, month=11, day=17, hour=14, minute=10, tzinfo=ZoneInfo('US/Eastern')))

    SPRINT_4 = Sprint(datetime(year=2022, month=11, day=17, hour=14, minute=11, tzinfo=ZoneInfo('US/Eastern')),
                      datetime(year=2022, month=12, day=6, hour=23, minute=59, tzinfo=ZoneInfo('US/Eastern')))

    get_stats_for_sprint(SPRINT_2)
