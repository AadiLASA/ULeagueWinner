from helpers import get_summoner_info
summoner_name="oscarblacklebron"
summoner=get_summoner_info(summoner_name)
print(summoner)
print(summoner['name'])
