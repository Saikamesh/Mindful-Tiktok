import requests


class TikTokAuth:
    OAUTH_URL = "https://open.tiktokapis.com/v2/oauth/token/"

    OAUTH_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

    def auth_research_api(
        self, client_key: str, client_secret: str, grant_type: str
    ) -> str:
        """
        Authenticate TikTok Research API.

        Args:
            client_key (str): The client key for the TikTok API.
            client_secret (str): The client secret for the TikTok API.
            grant_type (str): The grant type for the TikTok API.
        """
        response = requests.post(
            self.OAUTH_URL,
            headers=self.OAUTH_HEADERS,
            data={
                "client_key": client_key,
                "client_secret": client_secret,
                "grant_type": grant_type,
            },
        )
        if response.status_code == 200 and "error" in response.json():
            err = {
                "error": response.json()["error"],
                "error_description": response.json()["error_description"],
                # "log_id": response.json()['log_id']
            }
            raise ValueError(err)
        else:
            return response.json()["access_token"]
