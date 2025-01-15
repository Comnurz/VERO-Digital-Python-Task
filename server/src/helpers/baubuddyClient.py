import requests

base_url = "https://api.baubuddy.de/index.php/{}"
username, password = "365", "1"

def authenticate():
    headers = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }
    res = requests.post(
        base_url.format("login"),
        json={"username": username, "password": password},
        headers=headers
    )
    res.raise_for_status()
    return res.json()["oauth"]["access_token"]

def get_vehicles():
    res = requests.get(
        base_url.format("v1/vehicles/select/active"),
        headers={"Authorization": f"Bearer {authenticate()}"}
    )
    res.raise_for_status()
    return res.json()

def get_colors(label_id: int):
    res = requests.get(
        base_url.format(f"v1/labels/{label_id}"),
        headers={"Authorization": f"Bearer {authenticate()}"}
    )
    res.raise_for_status()
    return res.json()[0]["colorCode"]

