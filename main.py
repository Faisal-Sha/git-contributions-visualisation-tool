import os
from datetime import datetime, timedelta
from git import Repo, GitCommandError
from collections import defaultdict

def find_git_repositories(root_dir):
    """
    Finds all Git repositories in the given directory.

    Args:
        root_dir (str): The path to the root directory to search.

    Returns:
        list: A list of paths to directories containing Git repositories.
    """
    git_repos = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '.git' in dirnames:
            git_repos.append(dirpath)

    return git_repos

def get_repo_stats(repo_path, days):
    """
    Gathers statistics for a given Git repository.

    Args:
        repo_path (str): The path to the Git repository.
        days (int): The number of days to look back.

    Returns:
        dict: Statistics including total commits, contributors, and commit counts per contributor.
    """
    stats = {
        "total_commits": 0,
        "contributors": defaultdict(int),
    }

    try:
        repo = Repo(repo_path)
        if repo.bare:
            print(f"Repository at {repo_path} is bare.")
            return stats

        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        commits = list(repo.iter_commits(since=since_date))

        for commit in commits:
            stats["total_commits"] += 1
            stats["contributors"][commit.author.email] += 1

        return stats

    except GitCommandError as e:
        print(f"Error processing repository at {repo_path}: {e}")
        return stats

def main():
    root_directory = input("Enter the root directory to search for Git repositories: ").strip()

    if not os.path.isdir(root_directory):
        print("The specified path is not a valid directory.")
        return

    try:
        days = int(input("Enter the number of days to look back for stats: ").strip())
        if days <= 0:
            print("Please enter a positive number of days.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number of days.")
        return

    git_repositories = find_git_repositories(root_directory)

    if git_repositories:
        print("\nRepository Statistics:\n")
        for repo in git_repositories:
            stats = get_repo_stats(repo, days)
            print(f"Repository: {repo}")
            print(f"  Total Commits: {stats['total_commits']}")
            print("  Contributors:")
            for contributor, count in stats["contributors"].items():
                print(f"    {contributor}: {count} commits")
            print()

    else:
        print("No Git repositories found in the specified directory.")

if __name__ == "__main__":
    main()
