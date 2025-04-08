import requests
import settings
from urllib.parse import urlencode

def get_summoner_info(summoner_name=NONE, region=settings.DEFAULT_REGION_CODE):
    '''
    Wrapper for SUMMONER-V4 API PORTAL
    '''
    if not summoner_name:
        summoner_name=input("Summoner Name:")
    params = {
        'api_key': settings.API_KEY
    }
    api_url=f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    try:
        response=requests.get(api_url,params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'issue getting data bruh:{e}')
        return None



    