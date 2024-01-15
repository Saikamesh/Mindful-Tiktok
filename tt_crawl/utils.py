import datetime


def check_date_range(start_date: str, end_date: str) -> bool:
    """
    Returns True if the date range is valid.
    """
    start_datetime = datetime.datetime.strptime(start_date, "%Y%m%d")
    end_datetime = datetime.datetime.strptime(end_date, "%Y%m%d")
    delta = end_datetime - start_datetime

    if delta.days <= 30:
        return True
    else:
        return False


def generate_request_query(query: dict, start_date: str, end_date: str) -> dict:
    """
    Returns a dictionary of the request query.
    """
    request_query = {
        "query": query.get("query"),
        "max_count": 100,
        "cursor": 0,
        "search_id": "",
        "start_date": start_date,
        "end_date": end_date,
    }
    return request_query


def generate_request_queries(query: int, start_date: str, end_date: str) -> list:
    """
    Returns a list of the request queries.
    """
    start_datetime = datetime.datetime.strptime(start_date, "%Y%m%d")
    end_datetime = datetime.datetime.strptime(end_date, "%Y%m%d")
    
    delta = end_datetime - start_datetime
    query_ranges = delta.days // 30 + 1

    request_queries = []
    for i in range(query_ranges):
        range_start = start_datetime + datetime.timedelta(days=i*30)
        range_end = min(start_datetime + datetime.timedelta(days=(i+1)*30), end_datetime)
        
        request_query = generate_request_query(query, range_start.strftime("%Y%m%d"), range_end.strftime("%Y%m%d"))
        request_queries.append(request_query)
    
    return request_queries


def generate_search_key(query: dict) -> str:
    search_key = ""
    for operator in ["and", "or", "not"]:
        for item in query["query"][operator]:
            search_key += f"{item['operation']} {item['field_name']} {' '.join(item['field_values'])} "
        search_key = search_key.rstrip() + " | "
    search_key = search_key.rstrip(" | ")
    return search_key


def generate_date_string(day: int, month: int, year: int) -> str:
    date_str = str(year) + str(month).zfill(2) + str(day).zfill(2)
    return date_str
