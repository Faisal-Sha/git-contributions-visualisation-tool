import os
from datetime import datetime, timedelta
from git import Repo
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def find_git_repositories(root_dir):
    """Finds all Git repositories in the given directory."""
    git_repos = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '.git' in dirnames:
            git_repos.append(dirpath)

    return git_repos

def get_commit_dates(repo_path, days):
    """Gathers commit dates for the last `days` from the given Git repository."""
    dates = []

    try:
        repo = Repo(repo_path)
        if repo.bare:
            return dates

        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        commits = list(repo.iter_commits(since=since_date))

        for commit in commits:
            dates.append(datetime.fromtimestamp(commit.committed_date).date())

    except Exception as e:
        print(f"Error processing repository at {repo_path}: {e}")

    return dates

def prepare_heatmap_data(dates, days):
    """Prepares data for the heatmap."""
    start_date = datetime.now().date() - timedelta(days=days)
    date_range = [start_date + timedelta(days=i) for i in range(days + 1)]
    data = defaultdict(int)

    for date in dates:
        data[date] += 1

    heatmap_data = [data[date] for date in date_range]
    return date_range, heatmap_data

def render_contribution_graph(date_range, heatmap_data):
    """Renders the contribution graph."""
    fig, ax = plt.subplots(figsize=(15, 2))
    cmap = plt.cm.get_cmap("Greens", max(heatmap_data) + 1)

    bars = ax.bar(date_range, heatmap_data, color=[cmap(val) for val in heatmap_data])
    ax.set_title("Contribution Graph")
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

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
    all_dates = []

    for repo in git_repositories:
        all_dates.extend(get_commit_dates(repo, days))

    if all_dates:
        date_range, heatmap_data = prepare_heatmap_data(all_dates, days)
        render_contribution_graph(date_range, heatmap_data)
    else:
        print("No contributions found in the specified time period.")

if __name__ == "__main__":
    main()
