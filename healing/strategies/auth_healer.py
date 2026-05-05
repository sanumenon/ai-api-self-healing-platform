import requests

class AuthHealer:

    def __init__(self, config):
        self.cfg = config["auth"]["auth0"]

    def get_token(self, user_email):

        payload = {
            "grant_type": self.cfg["grant_type"],
            "client_id": self.cfg["client_id"],
            "username": user_email,
            "password": self.cfg["password"],
            "audience": self.cfg["audience"],
            "scope": self.cfg["scope"]
        }

        response = requests.post(
            self.cfg["token_url"],
            data=payload,  # ⚠️ important: urlencoded
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code != 200:
            print("Token fetch failed:", response.text)
            return None

        return response.json().get("access_token")