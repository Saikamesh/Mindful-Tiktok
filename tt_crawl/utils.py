
def generate_request_query(query:dict, start_date:str, start_month:str, start_year:str, end_date:str, end_month:str, end_year:str )-> dict:
    """
    Returns a dictionary of the request query.
    """
    start_date = start_year + start_month + start_date
    end_date = end_year + end_month + end_date

    request_query = {
        'query': query.get('query'),
        "max_count": 100,
        "cursor": 0,
	    "search_id": '',
        "start_date": start_date,
        "end_date": end_date
    }
    return request_query
