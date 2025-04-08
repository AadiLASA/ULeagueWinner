#imports
import requests
import json
import time
import csv
from time import sleep
#constants/prog begin
start_time = time.time()
APIKEY="RGAPI-44f1b1b3-9c6a-4914-b2aa-c0314461b825"
START = "INSERT PUUID HERE"
REGION = "na1"
HEADERS = {"X-Riot-Token":APIKEY}
ROUTING = "americas"
headers = {
    "X-Riot-Token": APIKEY
}
seen_matches = set() #tracking matches already seen
seen_puuid = set() #tracking players already crept
data_rows = [] #list of rows to be written to csv

#functions

def get_chall_players(): #obtaining the matchIDs of the players in the Chall/GM queue in NA1
    url_chall = f"https://{REGION}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
    resp = requests.get(url_chall,headers=HEADERS)
    if resp.status_code != 200:
        print("Error:", resp.status_code)
        return []
    data=resp.json()
    url_gm = f"https://{REGION}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5"
    resp_gm = requests.get(url_gm,headers=HEADERS)
    data.update(resp_gm.json())
    return data["entries"]

def write_csv_players(chall_players,file_name): #writing players to CSV
    csv_file = f'{file_name}.csv'
    with open(csv_file, mode='w', newline='') as file:
        fieldnames = ['summonerId', 'puuid', 'leaguePoints', 'rank', 'wins', 'losses', 'veteran', 'inactive', 'freshBlood', 'hotStreak']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in chall_players:
            writer.writerow(entry)

def write_csv_matches(chall_players, file_name): #writing matchIDs to CSV
    csv_file = f'{file_name}.csv'
    with open(csv_file, mode='w', newline='') as file:
        fieldnames = ['match_id']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for match_id in chall_players:
            writer.writerow({'match_id': match_id}) 

def get_match_data(match_id): #obtaining match data
    url = f"https://{ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=headers)
    return response.json()

def read_csv_for_match_ids(csv_filename): #reading matchIDs from CSV
    match_ids = []
    with open(csv_filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            match_ids.append(row[0]) 
    return match_ids

# def extract_team_data(match_json): #extracting team data from match data
#     # if "info" not in match_json:
#     #     print("Warning: 'info' key missing in match data. Skipping this match.")
#     #     #return [] 
#     info = match_json["info"]
#     participants = info["participants"]
#     teams = info["teams"]

#     team_data = {
#         "blue": {"total_gold": 0, "total_xp": 0, "objectives": {}, "win": False},
#         "red": {"total_gold": 0, "total_xp": 0, "objectives": {}, "win": False}
#     }

#     for p in participants:
#         team = "blue" if p["teamId"] == 100 else "red"
#         team_data[team]["total_gold"] += p["goldEarned"]
#         team_data[team]["total_xp"] += p["champExperience"]

#     for t in teams:
#         team = "blue" if t["teamId"] == 100 else "red"
#         team_data[team]["win"] = t["win"]
#         for obj_type, obj_data in t["objectives"].items():
#             team_data[team]["objectives"][obj_type] = obj_data["kills"]

#     return team_data


# def flatten_team_data(match):
#     # Flatten the team data
#     row = {
#         # Blue team data
#         "blue_gold": match["blue"]["total_gold"],
#         "blue_xp": match["blue"]["total_xp"],
#         "blue_dragons": match["blue"]["objectives"].get("dragon", 0),
#         "blue_barons": match["blue"]["objectives"].get("baron", 0),
#         "blue_towers": match["blue"]["objectives"].get("tower", 0),
#         "blue_inhibitors": match["blue"]["objectives"].get("inhibitor", 0),
#         "blue_riftHeralds": match["blue"]["objectives"].get("riftHerald", 0),
#         "blue_atakhans": match["blue"]["objectives"].get("atakhan", 0),
#         "blue_champions": match["blue"]["objectives"].get("champion", 0),
#         "blue_hordes": match["blue"]["objectives"].get("horde", 0),

#         # Red team data
#         "red_gold": match["red"]["total_gold"],
#         "red_xp": match["red"]["total_xp"],
#         "red_dragons": match["red"]["objectives"].get("dragon", 0),
#         "red_barons": match["red"]["objectives"].get("baron", 0),
#         "red_towers": match["red"]["objectives"].get("tower", 0),
#         "red_inhibitors": match["red"]["objectives"].get("inhibitor", 0),
#         "red_riftHeralds": match["red"]["objectives"].get("riftHerald", 0),
#         "red_atakhans": match["red"]["objectives"].get("atakhan", 0),
#         "red_champions": match["red"]["objectives"].get("champion", 0),
#         "red_hordes": match["red"]["objectives"].get("horde", 0),

#         # Label: 1 = blue win, 0 = red win
#         "label": 1 if match["blue"]["win"] else 0
#     }
#     return row

def get_match_features(match_id):
    endpoint = f"https://{ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    try:
        res = requests.get(endpoint, headers=headers)
        if res.status_code != 200:
            print(f"Match {match_id} fetch failed: {res.status_code}")
            return None

        data = res.json()
        info = data.get("info")
        if not info:
            print(f"Match {match_id} missing 'info' field.")
            return None

        participants = info.get("participants", [])
        teams = info.get("teams", [])

        if len(participants) != 10 or len(teams) != 2:
            print(f"Match {match_id} has incomplete participants or teams.")
            return None

        # Group player stats by team ID
        stats = {100: {"gold": 0, "xp": 0}, 200: {"gold": 0, "xp": 0}}
        for p in participants:
            tid = p["teamId"]
            stats[tid]["gold"] += p["goldEarned"]
            stats[tid]["xp"] += p["champExperience"]

        # Get objective stats + win
        features = {}
        for t in teams:
            tid = t["teamId"]
            prefix = "blue" if tid == 100 else "red"
            obj = t.get("objectives", {})
            features[f"{prefix}_win"] = t.get("win", False)
            features[f"{prefix}_gold"] = stats[tid]["gold"]
            features[f"{prefix}_xp"] = stats[tid]["xp"]
            for key in ["baron", "dragon", "tower", "inhibitor", "riftHerald", "champion", "atakhan", "horde"]:
                features[f"{prefix}_{key}s"] = obj.get(key, {}).get("kills", 0)

        # Create model label: 1 = blue win, 0 = red win
        features["label"] = int(features["blue_win"])
        del features["blue_win"]
        del features["red_win"]

        return features

    except Exception as e:
        print(f"Unexpected error fetching match {match_id}: {e}")
        return None


# def write_csv_matchdata(data, file_name): #writing match data to CSV
#     csv_file = f'{file_name}.csv'
#     rows = [flatten_team_data(m) for m in data]
#     fieldnames = list(rows[0].keys())
#     with open(csv_file, "w", newline="") as f:
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(rows)

def write_csv_matchdata(data, file_name):
    if not data:
        print("No data to write.")
        return
    csv_file = f'{file_name}.csv'
    fieldnames = list(data[0].keys())
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)



def get_matchlist_by_puuid(data_total, count=20): #getting matchlist by puuid; currently parsing 20 matches per player
    counter = 0
    match_data = []
    seen_matches = []
    seen_puuid = []
    for entry in data_total:
        puuid = entry["puuid"]
        if puuid in seen_puuid:
            continue
        seen_puuid.append(puuid)
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
        resp = requests.get(url,headers=HEADERS)
        matches = resp.json() 
        for match in matches:
            if match not in seen_matches: 
                seen_matches.append(match) 
                match_data.append(match) 
            else:
                counter+=1
            
    
    print(counter)
    return match_data


# MAIN EXECUTION

#chall_players= get_chall_players()
#matches=get_matchlist_by_puuid(chall_players) -- get matchlist by puuid for each player TAKES A WHILE
matches=read_csv_for_match_ids("GCmatches.csv")
#print(chall_players) --prints out all players in the challenger game puuid
#print("Writing Chall Players to CSV") 
#sleep(2) 
##write_csv_players(chall_players,"chall_entries") --writing the players to a csv
#print("Writing matchlist to CSV") 
#sleep(2)
# print(matches)
#write_csv_matches(matches,"GCmatches")--writing their matches to csv

dataset = []
print(" Fetching matches...")
# for match_id in matches:
#     #print(f" Fetching match {match_id}...") @DEBUG
#     #match = get_match_data(match_id)
#     #match_data = extract_team_data(match)
#     #print(f"for match {match_id}, match data is {match_data}") @DEBUG
#     #dataset.append(match_data)
#     #time.sleep(1.2) TESTING NO SLEEP LOL
#     match = get_match_data(match_id)
#     if match:
#         #print(match)
#         print(f"Checking match {match_id}...")
#         match_data = extract_team_data(match)
#         #print(match_data)
#         if match_data:  # Only add valid data
#             dataset.append(match_data)
#             print(f"Match {match_id} data added.")
#         else:
#             print(f"Skipping match {match_id} due to missing 'info' data.")
#     else:
#         print(f"Error fetching data for match {match_id}.")
# for match_id in matches:
#     try:
#         match = get_match_data(match_id)
#         if match:
#             #print(f"Checking match {match_id}...")
#             match_data = extract_team_data(match)
#             if match_data:  # Only add valid data
#                 dataset.append(match_data)
#               #  print(f"Match {match_id} data added.")
#             else:
#                 print(f"Skipping match {match_id} due to missing 'info' data.")
#         else:
#             print(f"Error fetching data for match {match_id}.")
#     except Exception as e:
#         print(f"An error occurred while processing match {match_id}: {e}")
#         continue  # Skip this match and continue with the next

for match_id in matches:
    print(f"Checking match {match_id}...")
    features = get_match_features(match_id)
    if features:
        dataset.append(features)
        print(f"Match {match_id} data added.")
        time.sleep(1.3)  # minimum sleep to avoid rate limiting + 0.1 seconds safety
    else:
        print(f"Skipping match {match_id} due to invalid or missing data.")


print("Beginning CSV Matchdata write...")
sleep(2)
write_csv_matchdata(dataset,"TOTALmatchdata")
print("Program Complete.")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Script completed in {elapsed_time:.2f} seconds.")

