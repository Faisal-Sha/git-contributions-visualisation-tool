import os

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

def main():
    root_directory = input("Enter the root directory to search for Git repositories: ").strip()

    if not os.path.isdir(root_directory):
        print("The specified path is not a valid directory.")
        return

    git_repositories = find_git_repositories(root_directory)

    if git_repositories:
        print("\nFound Git repositories:")
        for repo in git_repositories:
            print(f"- {repo}")
    else:
        print("No Git repositories found in the specified directory.")

if __name__ == "__main__":
    main()
