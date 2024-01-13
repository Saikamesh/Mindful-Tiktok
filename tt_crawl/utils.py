
def generate_request_query(query:dict, start_date:str, start_month:str, start_year:str, end_date:str, end_month:str, end_year:str )-> dict:
    """
    Returns a dictionary of the request query.
    """

    start_date = generate_date_string(start_date, start_month, start_year) 
    end_date = generate_date_string(end_date, end_month, end_year)

    request_query = {
        'query': query.get('query'),
        "max_count": 100,
        "cursor": 0,
	    "search_id": '',
        "start_date": start_date,
        "end_date": end_date
    }
    return request_query


def generate_date_string(date:int, month:int, year:int) -> str:
    date_str = str(year) + str(month).zfill(2) + str(date).zfill(2)
    return date_str