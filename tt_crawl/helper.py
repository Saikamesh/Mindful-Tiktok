import requests
import pandas as pd


def validate_urls(response_json: dict) -> dict:
    """
    Removes all the photo posts from the data.

    Args:
        response_json (dict): The response object from the TikTok API.
    """

    EMBED_URL = "https://www.tiktok.com/embed/"

    for video in response_json["data"]["videos"]:
        url = EMBED_URL + str(video["id"])
        res = requests.get(url)

        if not res.ok:
            response_json["data"]["videos"].remove(video)

    return response_json


def remove_duplicate_rows(file) -> None:
    """
    Removes duplicate rows from a CSV file.

    Args:
        file (string): The path of the file with name.
    """
    df = pd.read_csv(file)
    duplicate_data = df[df.id.duplicated()]
    if duplicate_data.empty:
        return
    df.drop_duplicates(subset="id", keep="first", inplace=True)
    df.to_csv(file, index=False)
