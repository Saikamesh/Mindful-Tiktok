import requests


def validate_urls(response_json: dict) -> dict:
    EMBED_URL = "https://www.tiktok.com/embed/"

    for video in response_json["data"]["videos"]:
        url = EMBED_URL + str(video["id"])
        res = requests.get(url)
        if res.status_code == 400:
            response_json["data"]["videos"].remove(video)

    return response_json
