## Tiktok research API

How to structure a request body?

Below is the example of a request body.

```json

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

```

The request body is a query object which is used to get the information from the api.

Every Query object has 3 children `and`, `or` , `not` . Each of which is a list of conditions.

The `and` conditions specify that all the conditions in the list must be met

The `or` conditions specify that at least one of the conditions in the list must be met

The `not` conditions specify that none of the conditions in the list must be met

A valid query must contain at least one non-empty `and`, `or` or `not` condition lists.

A condition is an object that specifies the field name, the operation, and the field values to restrict the query.

### operation:

---

**Possible values**: "EQ", "IN", "GT", "GTE", "LT", "LTE”

**Value Descriptions:**

**EQ**: equal to

**IN**: in

**GT**: greater than

**LT**: less than

**GTE**: greater than or equal to

**LTE**: less than or equal to

### field_name & field_value:

---

Depending on the field_name you’ve choose, use the corresponding field_values which are related to the field name.

Refer to the below table

| Field Name   | Description                                                                       | Example                              |
| ------------ | --------------------------------------------------------------------------------- | ------------------------------------ |
| create_date  | The video creation date in UTC, presented in the format YYYYMMDD                  | 20220910                             |
| username     | The username of the video creator                                                 | "cookie_love_122"                    |
| region_code  | A two digit code for the country where the video creator registered their account | ‘US’,’UK’,’IN’,’JP’ …                |
| video_id     | The unique identifier of the video                                                | 6978662169214864645                  |
| hashtag_name | The hashtag associated with the video                                             | "arianagrande", "celebrity"          |
| keyword      | The keyword in the video description                                              | "tiktok"                             |
| music_id     | The music ID of the video.                                                        | 8978345345214861235                  |
| effect_id    | The effect ID of the video.                                                       | 3957392342148643476                  |
| video_length | The duration of the video                                                         | "SHORT", "MID", "LONG", "EXTRA_LONG" |

`SHORT: <15s, 
MID: 15s~1min, 
LONG: 1~5min, 
EXTRA_LONG: >5min`

---

### Example

Below is an example on how to write query object based on the requirements

Let’s say, you want to get data about videos which contain the hashtag #nfl from region US, And you do not want any videos which are less than 15s. Below is how you write the query for it

```json

request_body = {
     "query": {
         "and": [
             {"operation": "IN", "field_name": "region_code","field_values": ["US"]},
             {"operation": "EQ", "field_name": "hashtag_name", "field_values": ["nfl"]},
         ],
         "or": [],
         "not": [
             {"operation": "EQ", "field_name": "video_length", "field_values": ["SHORT"]}
         ],
     }
}

```

We have left the `or` condition empty as there is no need for it.

consider for a moment that we need to get the data from either US or Japan, below is how we’d structure our query object,

```json

request_body = {
     "query": {
         "and": [
             {"operation": "EQ", "field_name": "hashtag_name", "field_values": ["nfl"]},
         ],
         "or": [
				{"operation": "IN", "field_name": "region_code","field_values": ["US"]},
				{"operation": "IN", "field_name": "region_code","field_values": ["JP"]}
			],
         "not": [
             {"operation": "EQ", "field_name": "video_length", "field_values": ["SHORT"]}
         ],
     }
}

```