# Mindful-Tiktok


The project is currently in alpha stage and is available on TestPyPi

Here is the link to the respositoy on TestPyPi -  [tt-crawl](https://test.pypi.org/project/tt-crawl/)

- Use the below command to install 

``` 
pip install -i https://test.pypi.org/simple/ tt-crawl
```

# Requirements
 
 You need access to [TikTok Research API](https://developers.tiktok.com/products/research-api/) to use this package. 


# Instructions

To learn how to construct your own query, use the [tiktok documentation](https://developers.tiktok.com/doc/research-api-specs-query-videos/)


Perform a query


```
from tt_crawl import TikTokCrawler

test_crawler = TikTokCrawler(client_key, client_secret, grant_type)

request_body = {
    "query": {
        "and": [
            {"operation": "IN", "field_name": "region_code", "field_values": ["JP", "US"]},
            {"operation": "EQ", "field_name": "hashtag_name", "field_values": ["Valorant"]},
        ],
        "or": [
            {"operation": "EQ", "field_name": "video_length", "field_values": ["MID"]},
            {"operation": "EQ", "field_name": "video_length", "field_values": ["LONG"]},
        ],
        "not": [
            {"operation": "EQ", "field_name": "video_length", "field_values": ["SHORT"]}
        ],
    }
}

result = test_crawler.query_videos(request_body, 1, 11, 2021, 1, 1, 2022)

```

To save the result in a csv file

```
test_crawler.make_csv(result)
```

To merge all the csv files

```
test_crawler.merge_all_data()
```

# Issues

If you encounter any problems, please [file an issue](https://github.com/Saikamesh/Mindful-Tiktok/issues) along with a detailed description.


# License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.