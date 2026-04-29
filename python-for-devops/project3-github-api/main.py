from github_api import list_repos, create_repo, create_readme, delete_repo

print("=== List My Repos ===")
list_repos(per_page=5, max_pages=2)

print("\n=== Create Repo ===")
repo = create_repo(
    name="jan26-bootcamp-python-demo",
    description="Python for DevOps assignment - created via GitHub API",
    private=False,
)

if repo.get("name"):
    repo_name = repo["name"]

    readme_content = """# Python for DevOps - GitHub API Demo

This repository was created programmatically using the **GitHub REST API** and Python.

## What this demonstrates
- Authenticating with GitHub API using a personal access token
- Creating a repository via API
- Creating files (this README) via API
- Listing repositories with pagination

## Tech used
- Python `requests` library
- GitHub REST API v3
- Environment variables for secure token storage

## Author
Aditya Shrivastava | DevOps Bootcamp - Jan 2026
"""
    print(f"\n=== Create README in {repo_name} ===")
    create_readme(repo_name, readme_content)

    print(f"\n=== List Repos (after creation) ===")
    list_repos(per_page=5, max_pages=1)
