import os
import base64
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "curi-adi")

BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def list_repos(per_page=5, max_pages=3):
    all_repos = []
    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}/user/repos"
        response = requests.get(url, headers=HEADERS, params={"per_page": per_page, "page": page})
        print(f"Page {page} status: {response.status_code}")
        repos = response.json()
        if not repos:
            break
        for repo in repos:
            print(f"  {repo['name']}  |  Private: {repo['private']}")
        all_repos.extend(repos)
    return all_repos


def create_repo(name, description="", private=False):
    url = f"{BASE_URL}/user/repos"
    payload = {"name": name, "description": description, "private": private}
    response = requests.post(url, headers=HEADERS, json=payload)
    print(f"Create repo status: {response.status_code}")
    data = response.json()
    print(f"  Repo: {data.get('full_name')}  |  URL: {data.get('html_url')}")
    return data


def create_readme(repo_name, content_text, commit_message="Add README"):
    url = f"{BASE_URL}/repos/{GITHUB_USERNAME}/{repo_name}/contents/README.md"
    encoded = base64.b64encode(content_text.encode()).decode()
    payload = {"message": commit_message, "content": encoded}
    response = requests.put(url, headers=HEADERS, json=payload)
    print(f"Create README status: {response.status_code}")
    return response.json()


def delete_repo(repo_name):
    url = f"{BASE_URL}/repos/{GITHUB_USERNAME}/{repo_name}"
    response = requests.delete(url, headers=HEADERS)
    print(f"Delete repo {repo_name} status: {response.status_code}")
    return response.status_code
