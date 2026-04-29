from wordpress import list_posts, create_post, update_post, publish_post, delete_post, list_users, create_user

print("=== List Posts ===")
posts = list_posts(per_page=5)

print("\n=== Create Post ===")
new_post = create_post(
    title="Hello from Python",
    content="This post was created using the WordPress REST API and Python requests library.",
    status="draft",
)

if new_post.get("id"):
    post_id = new_post["id"]

    print(f"\n=== Update Post {post_id} ===")
    update_post(post_id, title="Hello from Python - Updated")

    print(f"\n=== Publish Post {post_id} ===")
    publish_post(post_id)

    print(f"\n=== Delete Post {post_id} ===")
    delete_post(post_id)

print("\n=== List Users ===")
list_users()

print("\n=== Create User ===")
create_user(
    username="testuser_adi",
    email="testadi@example.com",
    password="StrongPass@123",
    role="subscriber",
)
