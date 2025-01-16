import requests

class BaubuddyClient:
    TOKEN = ""
    BASE_URL = "https://api.baubuddy.de/index.php/{}"
    USERNAME, PASSWORD = "365", "1"

    def _authenticate(self):
        headers = {
            "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
            "Content-Type": "application/json"
        }
        res = requests.request(
            'POST',
            self.BASE_URL.format("login"),
            json={"username": self.USERNAME, "password": self.PASSWORD},
            headers=headers
        )
        res.raise_for_status()
        self.TOKEN = res.json()['oauth']["access_token"]

    def _request(self, method, url, **kwargs):
        res = requests.request(method, f'{self.BASE_URL}/{url}',
                               headers={"Authorization": f"Bearer {self.TOKEN}"},
                               **kwargs)
        if res.status_code == 401:
            self._authenticate()
            return self._request(method, url, **kwargs)
        res.raise_for_status()
        return res.json()


    def get_vehicles(self):
        res = self._request("GET",
            "v1/vehicles/select/active"
        )
        return res

    def get_colors(self, label_id: int):
        res = self._request("GET",
            f"v1/labels/{label_id}"
        )
        return res[0]["colorCode"]
