import os
from dotenv import load_dotenv
import requests

def load_api_key() -> str:

    load_dotenv() # load env variables from the .env file

    api_key = os.getenv("MASSIVE_API_KEY")

    if not api_key:
        raise ValueError("API key not found in environment variable 'MASSIVE_API_KEY'.")
    
    return api_key

# returns the url that is part of the get request
def build_url(endpoint: str, **kwargs) -> str: 

    # build a base url for a single security that requires multiple path parameters or a 
    # url for multiple securities that requires a single path parameter

    base = "https://api.massive.com/"
    try: 
        if endpoint == "custom_bars":
            url = base + f"v2/aggs/ticker/{kwargs['ticker']}/range/{kwargs['multiplier']}/{kwargs['timespan']}/{kwargs['start_date']}/{kwargs['end_date']}"
        elif endpoint == "grouped_daily":
            url = base + f"v2/aggs/grouped/locale/us/market/stocks/{kwargs['date']}"
        else: 
            raise ValueError("Unsupported endpoint. Choose custom_bars or grouped_daily")
    except KeyError as e: 
        raise KeyError(f"KeyError: Missing required path parameter {e} for endpoint {endpoint}")

    return url

# returns the header for the get request
def build_headers(api_key: str) -> dict[str,str]:
    return {"Authorization" : f"Bearer {api_key}"}

# as of Nov.2026, these query parameters are adjusted (for stock splits) and sorted in ascending order
# a function call is keyWord="true", for example
def build_params(**kwargs: str) -> dict[str,str]: 
    return kwargs

# successfully construct and send a GET request
def get_request(url: str, params: dict[str, str], headers: dict[str, str],timeout: float = 10.0) -> requests.Response:

    try:
        # the GET request
        requestObject = requests.get(url, params=params, headers=headers,timeout=timeout)

    except requests.exceptions.ConnectionError as c:
        raise ConnectionError(f"Internet connection failed: {c}") from c
    except requests.exceptions.Timeout as t:
        raise TimeoutError(f"Request timed out: {t}") from t
    
    return requestObject



