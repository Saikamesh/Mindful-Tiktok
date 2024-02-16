import csv
import glob
import json
import os
import requests
import datetime
import re
from typing import Union
from . import utils as ut
from . import validation as vl

class TikTokCrawler:
    OAUTH_URL = "https://open.tiktokapis.com/v2/oauth/token/"
    API_URL = "https://open.tiktokapis.com/v2/research/video/query/"

    _client_key: str = ""

    _client_secret: str = ""

    _grant_type: str = ""

    _auth_token: str = ""

    FIELDS = "id,video_description,create_time,region_code,share_count,view_count,like_count,comment_count,music_id,hashtag_names,username,effect_ids,playlist_id,voice_to_text"

    OAUTH_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

    def __init__(self, client_key: str, client_secret: str, grant_type: str) -> None:
        """Initialize the TikTokCrawler with the necessary authentication parameters.

        Args:
            client_key (str): The client key for the TikTok API.
            client_secret (str): The client secret for the TikTok API.
            grant_type (str): The grant type for the TikTok API.
        """
        self._client_key = client_key
        self._client_secret = client_secret
        self._grant_type = grant_type
        self._auth_token = self._generate_auth_token(
            self._client_key, self._client_secret, self._grant_type
        )
        # if not self._auth_token:
        #     print(self._auth_token)

    def _generate_auth_token(self, client_key, client_secret, grant_type) -> str:
        """
        Generate the auth token to interact with TikTok API.

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
            return err
        else:
            auth_token = response.json()["access_token"]
            return auth_token

    def _process_request(
        self, request: dict, search_key: str, queried_date: str
    ) -> dict:
        """
        Makes a request to the TikTok API and returns the response.

        Args:
            request (dict): The request body.
            search_key (str): The search key.
            queried_date (str): The date on which the query was made.
        """
        QUERY_HEADERS = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self._auth_token,
        }

        req_json = json.dumps(request)
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
            print(err)
            print(response.status_code)
            return err
        else:
            response_json = response.json()
            res_json = vl.validate_urls(response_json)
            res_json["search_key"] = search_key
            res_json["queried_date"] = queried_date
            return res_json

    def query_videos(
        self,
        query: dict,
        start_day: int,
        start_month: int,
        start_year: int,
        end_day: int,
        end_month: int,
        end_year: int,
    ) -> dict:
        """
        Returns a list of videos based on the search criteria.

        Args:
            query (dict): The search query.
            start_day (int): The start day of the search.
            start_month (int): The start month of the search.
            start_year (int): The start year of the search.
            end_day (int): The end day of the search.
            end_month (int): The end month of the search.
            end_year (int): The end year of the search.
        """
        search_key = ut.generate_search_key(query)
        queried_date = datetime.datetime.now().strftime("%Y%m%d")
        start_date = ut.generate_date_string(start_day, start_month, start_year)
        end_date = ut.generate_date_string(end_day, end_month, end_year)
        date_range = ut.check_date_range(start_date, end_date)

        if not date_range:
            requests_list = ut.generate_request_queries(query, start_date, end_date)
            response_list = []

            for request in requests_list:
                response_json = self._process_request(request, search_key, queried_date)
                response_list.append(response_json)
            return response_list
        else:
            req = ut.generate_request_query(query, start_date, end_date)
            response_json = self._process_request(req, search_key, queried_date)
            return response_json

    def make_csv(
        self, data: Union[dict, list], file_name: str = None, data_dir: str = None
    ) -> None:
        """
        Makes a csv file from given data.

        Args:
            data (Union[dict, list]): The data to be converted to csv.
            file_name (str, optional): The name of the csv file. Defaults to a search key based on query.
            data_dir (str, optional): The directory in which the csv file is to be stored. Defaults to current working dir.
        """
        fields = self.FIELDS.split(",") + ["search_key", "queried_date"]

        if not data_dir:
            data_dir = os.path.join(os.getcwd(), "Data", "video_data")
            os.makedirs(data_dir, exist_ok=True)

        if not isinstance(data, list):
            search_key = data["search_key"]
            queried_date = data["queried_date"]
        else:
            search_key = data[0].get("search_key")
            queried_date = data[0].get("queried_date")

        if not file_name:
            search_key = re.sub(r"[^a-zA-Z\s]", "", search_key)
            file_name = (
                f"{search_key}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )

        file_path = os.path.join(data_dir, file_name)

        if isinstance(data, list):
            for item in data:
                ut.process_data(item, fields, search_key, queried_date, file_path)
        else:
            ut.process_data(data, fields, search_key, queried_date, file_path)

    def merge_all_data(self, data_dir: str = None, file_name: str = None) -> None:
        """
        Merges all the csv files in the Data folder.
        """
        if not data_dir:
            data_dir = os.path.join(os.getcwd(), "Data", "video_data")
        if not file_name:
            file_name = "video_list.csv"
            # file_name = (
            #     f"merged_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            # )

        all_files = glob.glob(os.path.join(data_dir, "*.csv"))
        file_path = os.path.join(os.getcwd(), "Data", file_name)

        with open(
            os.path.join(file_path), "a", newline="", encoding="utf-8"
        ) as fout:
            writer = csv.writer(fout)
            header_saved = False
            for filename in all_files:
                with open(filename, "r", newline="", encoding="utf-8") as fin:
                    reader = csv.reader(fin)
                    header = next(reader)
                    if not header_saved:
                        writer.writerow(header)
                        header_saved = True
                    for row in reader:
                        writer.writerow(row)
