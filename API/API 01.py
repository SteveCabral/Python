import requests

def get_posts():
    url = 'https://jsonplaceholder.typicode.com/posts'
    response = requests.get(url)

    if response.status_code == 200:
        posts = response.json()
        return posts
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

if __name__ == "__main__":
    posts = get_posts()

    if posts:
        print("Posts:")
        for post in posts:
            print(f"Title: {post['title']}")
            print(f"Body: {post['body']}")
            print("------")
    else:
        print("Failed to get posts from the JSONPlaceholder API.")
