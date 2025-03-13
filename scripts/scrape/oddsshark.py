import requests
import json
import time 
import pandas as pd

# url = "https://www.oddsshark.com/api/scores/nba/2025-02-13?_format=json"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
# }
# response = requests.get(url, headers=headers)
# time.sleep(15)
# if response.status_code == 200:
#     data = response.json()
#     print(data)
#     print("Successfully fetched the page")
#     with open("data.json", "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4)
# else:
#     print(f"Failed to fetch page, status code: {response.status_code}")

def save_page(date: pd.to_datetime, league: str):
    
    url = 'https://www.oddsshark.com/api/scores/nba/{date}?format=json'
    headers = {
        "User-Agent": 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    if league == 'ncaab':
        league = 'ncb'
    response = requests.get(url, headers=headers)
    time.sleep(60)
    if response.status_code == 200:
        data = response.json()
        print("Successfully fetched the page")
        with open(f"../../data/raw/{league.upper()}/{date}/data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    else:
        print(f"Failed to fetch page, status code: {response.status_code}")
        
date = (pd.Timestamp.today() - pd.Timedelta(days=2)).date()
save_page(date, 'nba')
