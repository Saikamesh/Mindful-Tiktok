import requests
import json
import time
from .auth import TikTokAuth
from . import helper as hl
from typing import Literal


class TikResearchAPI:
    API_URL = "https://open.tiktokapis.com/v2/research/video/query/"

    _auth_token: str = ""

    FIELDS = "id,video_description,create_time,region_code,share_count,view_count,like_count,comment_count,music_id,hashtag_names,username,effect_ids,playlist_id,voice_to_text"

    def __init__(self, client_key: str, client_secret: str, grant_type: str) -> None:
        """Initialize the TikTokCrawler with the necessary authentication parameters.

        Args:
            client_key (str): The client key for the TikTok API.
            client_secret (str): The client secret for the TikTok API.
            grant_type (str): The grant type for the TikTok API.
        """
        if not client_key or not client_secret or not grant_type:
            raise ValueError(
                "One or more of the required parameters are missing. \nRequired: client_key, client_secret, grant_type"
            )

        self._auth_token = TikTokAuth().auth_research_api(
            client_key, client_secret, grant_type
        )

    def query_videos(
        self,
        field: Literal["keyword", "hashtag_name"],
        search_key: str,
        max_count: int = 100,
        start_date: str = None,
        end_date: str = None,
    ) -> dict:
        """
        Returns a list of videos based on the search key.

        Args:
            field (Literal["keyword", "hashtag_name"]): The field to search by.
            search_key (str): The term to search for.
            max_count (int, optional): The maximum number of videos to return. Defaults to 100.
            start_date (str, optional): The start date for the search. Expected in YYYYDDMM format. Defaults to last 30 days.
            end_date (str, optional): The end date for the search. Expected in YYYYDDMM format. Defaults to Current date.
        """

        if field not in ["keyword", "hashtag_name"]:
            raise ValueError(
                "Invalid field. Must be either 'keyword' or 'hashtag_name'"
            )

        if not start_date or not end_date:
            start_date = time.strftime(
                "%Y%m%d", time.gmtime(time.time() - 30 * 24 * 60 * 60)
            )
            end_date = time.strftime("%Y%m%d")

        QUERY_HEADERS = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._auth_token}",
        }

        request_body = {
            "query": {
                "and": [
                    {
                        "operation": "IN",
                        "field_name": "region_code",
                        "field_values": ["JP", "US"],
                    },
                    {
                        "operation": "EQ",
                        "field_name": field,
                        "field_values": [search_key],
                    },
                ]
            },
            "max_count": max_count,
            "cursor": 0,
            "start_date": start_date,
            "end_date": end_date,
        }

        req_json = json.dumps(request_body)
        response = requests.post(
            self.API_URL + "?fields=" + self.FIELDS,
            headers=QUERY_HEADERS,
            data=req_json,
        )
        if response.status_code != 200:
            err = {
                "error": response.json()["error"]["code"],
                "description": response.json()["error"]["message"],
                # 'log_id':response.json()['error']['log_id']
            }
            raise RuntimeError(err)
        else:
            response_json = response.json()
            res_json = hl.validate_urls(response_json)
            return res_json