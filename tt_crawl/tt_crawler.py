import requests
import json
import csv
import os
from . import utils as ut

class TikTokCrawler:
    
    OAUTH_URL = 'https://open.tiktokapis.com/v2/oauth/token/'
    API_URL = 'https://open.tiktokapis.com/v2/research/video/query/'

    _client_key: str=''
    _client_secret: str=''
    _grant_type: str=''
    _auth_token: str=''

    FIELDS = 'id,video_description,create_time,region_code,share_count,view_count,like_count,comment_count,music_id,hashtag_names,username,effect_ids,playlist_id,voice_to_text'

    OAUTH_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded"
    }

    
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
        self._auth_token = self._generate_auth_token(self._client_key, self._client_secret, self._grant_type)
        # if not self._auth_token:
        #     print(self._auth_token)


    def _generate_auth_token(self, client_key, client_secret, grant_type) -> str:
        """
        Generate the auth token to interact with TikTok API.
        """
        response = requests.post(self.OAUTH_URL, headers= self.OAUTH_HEADERS ,data = {'client_key': client_key, 'client_secret': client_secret, 'grant_type':grant_type})
        if response.status_code == 200 and 'error' in response.json():
            err = {
                "error": response.json()['error'],
                "error_description": response.json()['error_description'],
                # "log_id": response.json()['log_id']
            }
            return err    
        else:
            auth_token = response.json()['access_token']
            return auth_token 
    

    def query_videos(self, query: dict, start_date:int, start_month:int, start_year:int, end_date:int, end_month:int, end_year:int) -> dict:
        """
        Returns a list of videos based on the search criteria.
        """

        QUERY_HEADERS = {
            "Authorization": "Bearer " + self._auth_token ,
            "Content-Type": "application/json"
        }
        req = ut.generate_request_query(query, start_date, start_month, start_year, end_date, end_month, end_year)
        req_json = json.dumps(req)
        
        response = requests.post(self.API_URL + "?fields=" + self.FIELDS, headers=QUERY_HEADERS, data=req_json)
        if response.status_code != 200:
            err = {
                'error':response.json()["error"]['code'],
                'description':response.json()['error']['message'],
                # 'log_id':response.json()['error']['log_id']
            }
            return err
        else:
            return response.json()
                            

    def make_csv(self, file_name: str, data: dict) -> None:
        """
        Makes a csv file from given data.
        """
        file_path = os.path.join(os.getcwd(), file_name)
        video_data = data['data']['videos']

        if video_data:            
            for d in video_data:
                for field in self.FIELDS.split(','):
                    if field not in d:
                        d[field] = None

            with open(file_path, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDS.split(','))
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerows(video_data)
        else:
            print("No data to write to csv file")
            print(data)