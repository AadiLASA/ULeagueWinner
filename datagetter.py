import requests
import time
import csv

# CONFIGURATION
API_KEY = "RGAPI-c6479b11-c413-4d9e-bc45-a4bcc76e4c25"  # <-- Replace with your Riot API key
SUMMONER_NAME = "gatorniggilis"   # <-- Replace with any summoner name
REGION = "na1"            # API platform routing (e.g., na1, euw1, kr)
ROUTING = "americas"      # Match routing: na1 → americas, euw1 → europe, kr → asia
MATCH_COUNT = 10          # Number of matches to fetch

headers = {
    "X-Riot-Token": API_KEY
}

# --- API FUNCTIONS ---

def get_summoner_info(summoner_name):
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    response = requests.get(url, headers=headers)
    return response.json()

def get_match_ids(puuid, count=5):
    url = f"https://{ROUTING}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    response = requests.get(url, headers=headers)
    return response.json()

def get_match_data(match_id):
    url = f"https://{ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=headers)
    return response.json()

def extract_team_data(match_json):
    info = match_json["info"]
    participants = info["participants"]
    teams = info["teams"]

    team_data = {
        "blue": {"total_gold": 0, "total_xp": 0, "objectives": {}, "win": False},
        "red": {"total_gold": 0, "total_xp": 0, "objectives": {}, "win": False}
    }

    for p in participants:
        team = "blue" if p["teamId"] == 100 else "red"
        team_data[team]["total_gold"] += p["goldEarned"]
        team_data[team]["total_xp"] += p["champExperience"]

    for t in teams:
        team = "blue" if t["teamId"] == 100 else "red"
        team_data[team]["win"] = t["win"]
        for obj_type, obj_data in t["objectives"].items():
            team_data[team]["objectives"][obj_type] = obj_data["kills"]

    return team_data

# --- DATA FLATTENING AND EXPORT ---

def flatten_team_data(match):
    row = {
        "blue_gold": match["blue"]["total_gold"],
        "blue_xp": match["blue"]["total_xp"],
        "blue_dragons": match["blue"]["objectives"].get("dragon", 0),
        "blue_barons": match["blue"]["objectives"].get("baron", 0),
        "blue_towers": match["blue"]["objectives"].get("tower", 0),

        "red_gold": match["red"]["total_gold"],
        "red_xp": match["red"]["total_xp"],
        "red_dragons": match["red"]["objectives"].get("dragon", 0),
        "red_barons": match["red"]["objectives"].get("baron", 0),
        "red_towers": match["red"]["objectives"].get("tower", 0),

        # Label: 1 = blue win, 0 = red win
        "label": 1 if match["blue"]["win"] else 0
    }
    return row

def export_to_csv(data, filename="match_data.csv"):
    rows = [flatten_team_data(m) for m in data]
    fieldnames = list(rows[0].keys())

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Exported {len(rows)} matches to {filename}")

# --- MAIN FLOW ---

def main():
    # print(f"🔍 Looking up summoner '{SUMMONER_NAME}'...")
    # summoner = get_summoner_info(SUMMONER_NAME)
    # puuid = summoner.get("puuid")

    # if not puuid:
    #     print("❌ Could not find summoner.")
    #     return
    puuid = "QgZAOtEwS4aeaO7pdSPF5XhD73qZYvtzGl7a2Erxtwc6OtTKDI1VmS-eKOoHZLU4azSVRNiGgwRMJA"

    print(f"✅ Found summoner. Getting last {MATCH_COUNT} matches...")
    match_ids = get_match_ids(puuid, count=MATCH_COUNT)

    dataset = []
    for match_id in match_ids:
        print(f"📦 Fetching match {match_id}...")
        match = get_match_data(match_id)
        match_data = extract_team_data(match)
        dataset.append(match_data)
        time.sleep(1.2)  # Respect rate limit

    export_to_csv(dataset)

if __name__ == "__main__":
    main()
