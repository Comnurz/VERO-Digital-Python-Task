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
        res = requests.post(
            self.BASE_URL.format("login"),
            json={"username": self.USERNAME, "password": self.PASSWORD},
            headers=headers
        )
        res.raise_for_status()
        self.TOKEN = res.json()['oauth']["access_token"]

    def _request(self, method, url, **kwargs):
        res = requests.request(method, url, **kwargs)
        if res.status_code == 401:
            self._authenticate()
            return self._request(method, url, **kwargs)
        res.raise_for_status()
        return res.json()


    def get_vehicles(self):
        res = self._request("GET",
            self.BASE_URL.format("v1/vehicles/select/active"),
            headers={"Authorization": f"Bearer {self.TOKEN}"}
        )
        return res

    def get_colors(self, label_id: int):
        res = self._request("GET",
            self.BASE_URL.format(f"v1/labels/{label_id}"),
            headers={"Authorization": f"Bearer {self.TOKEN}"}
        )
        return res[0]["colorCode"]
