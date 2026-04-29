import os
import requests
from requests.auth import HTTPBasicAuth

DOMAIN = os.environ.get("WP_DOMAIN", "https://mipony.in")
USERNAME = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")

BASE_URL = f"{DOMAIN}/wp-json/wp/v2"
AUTH = HTTPBasicAuth(USERNAME, APP_PASSWORD)


def list_posts(per_page=10):
    url = f"{BASE_URL}/posts"
    response = requests.get(url, params={"per_page": per_page}, auth=AUTH)
    print(f"Status: {response.status_code}")
    for post in response.json():
        print(f"  ID: {post['id']}  |  Title: {post['title']['rendered']}  |  Status: {post['status']}")
    return response.json()


def create_post(title, content, status="draft"):
    url = f"{BASE_URL}/posts"
    payload = {"title": title, "content": content, "status": status}
    response = requests.post(url, json=payload, auth=AUTH)
    print(f"Create post status: {response.status_code}")
    data = response.json()
    print(f"  Post ID: {data.get('id')}  |  Status: {data.get('status')}")
    return data


def update_post(post_id, title=None, content=None, status=None):
    url = f"{BASE_URL}/posts/{post_id}"
    payload = {}
    if title:
        payload["title"] = title
    if content:
        payload["content"] = content
    if status:
        payload["status"] = status
    response = requests.post(url, json=payload, auth=AUTH)
    print(f"Update post {post_id} status: {response.status_code}")
    return response.json()


def publish_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    payload = {"status": "publish"}
    response = requests.patch(url, json=payload, auth=AUTH)
    print(f"Publish post {post_id} status: {response.status_code}")
    return response.json()


def delete_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.delete(url, params={"force": True}, auth=AUTH)
    print(f"Delete post {post_id} status: {response.status_code}")
    return response.json()


def list_users():
    url = f"{BASE_URL}/users"
    response = requests.get(url, auth=AUTH)
    print(f"Status: {response.status_code}")
    for user in response.json():
        print(f"  ID: {user['id']}  |  Username: {user['slug']}  |  Email: {user.get('email', 'N/A')}")
    return response.json()


def create_user(username, email, password, role="subscriber"):
    url = f"{BASE_URL}/users"
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "roles": [role],
    }
    response = requests.post(url, json=payload, auth=AUTH)
    print(f"Create user status: {response.status_code}")
    data = response.json()
    print(f"  User ID: {data.get('id')}  |  Username: {data.get('slug')}")
    return data
