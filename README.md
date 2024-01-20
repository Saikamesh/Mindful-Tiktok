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

# Privacy Policy

This privacy policy governs the use of the Mindful-Tiktok application.

## Information Collection and Use

This is a Python package developed for research and educational purposes only. It is designed to interact with the TikTok Research API. As such, it does not collect or store any kind of information related to the user.

## Data Security

We do not collect any personal information from users of the Mindful-Tiktok application. 

## Changes to This Privacy Policy

We may update our privacy policy from time to time. We will try our best to notify users of any changes to this privacy policy. However, users are responsible for regularly checking the GitHub project page to ensure they are aware of any updates.




# Terms of Service

By using the Mindful-Tiktok application, you agree to the following terms and conditions:

## Intellectual Property

All intellectual property rights of the Mindful-Tiktok application belong to the developers.

## Limitation of Liability

The developers of the Mindful-Tiktok application shall not be held liable for any damages or losses arising from the use or inability to use the application.

## Governing Law

These terms and conditions shall be governed by and construed in accordance with the laws of the jurisdiction in which the Mindful-Tiktok application is used.





# Issues

If you encounter any problems, please [file an issue](https://github.com/Saikamesh/Mindful-Tiktok/issues) along with a detailed description.


# License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.