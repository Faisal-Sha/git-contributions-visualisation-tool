import os
from datetime import datetime, timedelta
from git import Repo, GitCommandError

def find_git_repositories(root_dir):
    """
    Finds all Git repositories in the given directory.

    Args:
        root_dir (str): The path to the root directory to search.

    Returns:
        list: A list of paths to directories containing Git repositories.
    """
    git_repos = []

    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if .git exists in the current directory
        if '.git' in dirnames:
            git_repos.append(dirpath)

    return git_repos

def count_commits_in_last_days(repo_path, days):
    """
    Counts the number of commits made by the current user in the last given number of days.

    Args:
        repo_path (str): The path to the Git repository.
        days (int): The number of days to look back.

    Returns:
        int: The number of commits in the specified time frame.
    """
    try:
        repo = Repo(repo_path)
        if repo.bare:
            print(f"Repository at {repo_path} is bare.")
            return 0

        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        current_user = repo.config_reader().get_value("user", "email")
        commits = list(repo.iter_commits(since=since_date))

        user_commits = [commit for commit in commits if commit.author.email == current_user]
        return len(user_commits)

    except GitCommandError as e:
        print(f"Error processing repository at {repo_path}: {e}")
        return 0

def main():
    root_directory = input("Enter the root directory to search for Git repositories: ").strip()

    if not os.path.isdir(root_directory):
        print("The specified path is not a valid directory.")
        return

    try:
        days = int(input("Enter the number of days to look back for commits: ").strip())
        if days <= 0:
            print("Please enter a positive number of days.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number of days.")
        return

    git_repositories = find_git_repositories(root_directory)

    if git_repositories:
        print("\nFound Git repositories:")
        for repo in git_repositories:
            print(f"- {repo}")

        print(f"\nCommit analysis for the last {days} days:")
        for repo in git_repositories:
            commit_count = count_commits_in_last_days(repo, days)
            print(f"{repo}: {commit_count} commits in the last {days} days by the current user.")

    else:
        print("No Git repositories found in the specified directory.")

if __name__ == "__main__":
    main()
