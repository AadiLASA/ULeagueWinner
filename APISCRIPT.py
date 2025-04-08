import requests
import time
import json
from requests.exceptions import HTTPError

RIOT_API_KEY = "your-api-key-here"
BASE_URL = "https://na1.api.riotgames.com/lol"
HEADERS = {"X-Riot-Token": RIOT_API_KEY}
CACHE = {}
RATE_LIMIT = {
    "limit": 100,  
    "interval": 120 
}
REQUEST_LOG = []


def rate_limited_request(url):
    """Handles Riot API rate limiting by queuing requests."""
    global REQUEST_LOG
    now = time.time()
    

    REQUEST_LOG = [t for t in REQUEST_LOG if now - t < RATE_LIMIT["interval"]]
    
    
    if len(REQUEST_LOG) >= RATE_LIMIT["limit"]:
        sleep_time = RATE_LIMIT["interval"] - (now - REQUEST_LOG[0])
        print(f"Rate limit exceeded. Sleeping for {sleep_time:.2f} seconds.")
        time.sleep(sleep_time)
        
 
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        REQUEST_LOG.append(time.time())
        return response.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None


def get_summoner_by_name(summoner_name):
    """Retrieve summoner data by summoner name."""
    url = f"{BASE_URL}/summoner/v4/summoners/by-name/{summoner_name}"
    return rate_limited_request(url)


def get_matchlist_by_puuid(puuid, count=10):
    """Retrieve a list of recent matches by PUUID."""
    url = f"{BASE_URL}/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    return rate_limited_request(url)


def get_match_data(match_id):
    """Retrieve match data by match ID."""
    url = f"{BASE_URL}/match/v5/matches/{match_id}"
    return rate_limited_request(url)


def cache_data(key, data):
    """Store data in a local cache."""
    CACHE[key] = data
    with open("riot_cache.json", "w") as f:
        json.dump(CACHE, f)


def load_cache():
    """Load cached data from file."""
    global CACHE
    try:
        with open("riot_cache.json", "r") as f:
            CACHE = json.load(f)
    except FileNotFoundError:
        CACHE = {}


if __name__ == "__main__":
    load_cache()
    summoner_name = "oscarblacklebron"
    summoner_data = get_summoner_by_name(summoner_name)
    
    if summoner_data:
        puuid = summoner_data.get("puuid")
        match_list = get_matchlist_by_puuid(puuid, count=5)
        
        if match_list:
            for match_id in match_list:
                match_data = get_match_data(match_id)
                if match_data:
                    cache_data(match_id, match_data)
                    print(f"Cached data for match {match_id}")
