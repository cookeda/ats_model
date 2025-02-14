import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import pandas as pd
from time import process_time
import json

#with open('Dictionary/Pro/NBA.json', 'r') as file:
#    team_mappings = json.load(file)

#def find_team_rank_name(dk_team_name):
#    for team_mapping in team_mappings:
#        if team_mapping["DraftKings Name"] == dk_team_name:
#            return team_mapping["Team Rankings Name"]
#    return "Unknown"  # Return a default value if not found


match = {}

def clean_team(raw_team):
    team = raw_team.split(" ")
    team = team[1].upper()
    if team == 'TRAIL':
        team = 'TRAILBLAZERS'
    return team

def generate_game_id(away_team, home_team):
    combined_string = away_team + home_team
    hash_object = hashlib.md5(combined_string.encode())
    return hash_object.hexdigest()

def find_element_text_or_not_found(driver, xpath, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return element.text
    except:
        return 'N/A'

def scrape(matchup_num):
    matchup_num *= 2
    x = matchup_num - 1  # Indicates Away Team
    y = matchup_num      # Indicates Home Team

    away_team_text = find_element_text_or_not_found(driver, f'/html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[{matchup_num}]/div/div/div[1]/a/div[1]/div/div/div/div[2]/span')
    home_team_text = find_element_text_or_not_found(driver, f'/html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[{matchup_num}]/div/div/div[1]/a/div[3]/div/div/div/div[2]/span')
   #                                                           /html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[4]/div/div/div[1]/a/div[3]/div/div/div/div[2]
    away_spread_text = find_element_text_or_not_found(driver, f'/html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[{matchup_num}]/div/div/div[1]/div/div[1]/div[1]/span[1]')
    away_spread_odds_text = find_element_text_or_not_found(driver, f'/html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[{matchup_num}]/div/div/div[1]/div/div[1]/div[1]/span[2]')
    total_text = find_element_text_or_not_found(driver, f'/html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[{matchup_num}]/div/div/div[1]/div/div[1]/div[3]/span[1]')
    over_total_odds_text = find_element_text_or_not_found(driver, f'/html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[{matchup_num}]/div/div/div[1]/div/div[1]/div[3]/span[2]')
    away_ml_text = find_element_text_or_not_found(driver, f'/html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[{matchup_num}]/div/div/div[1]/div/div[1]/div[2]/span')
    home_spread_text = find_element_text_or_not_found(driver, f'/html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[{matchup_num}]/div/div/div[1]/div/div[2]/div[1]/span[1]')
    home_spread_odds_text = find_element_text_or_not_found(driver, f'/html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[{matchup_num}]/div/div/div[1]/div/div[2]/div[1]/span[2]')
    under_total_odds_text = find_element_text_or_not_found(driver, f'/html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[{matchup_num}]/div/div/div[1]/div/div[2]/div[3]/span[2]')
    home_ml_text = find_element_text_or_not_found(driver, f'/html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[{matchup_num}]/div/div/div[1]/div/div[2]/div[2]/span')
    start_time_text = find_element_text_or_not_found(driver, f'/html/body/div[1]/div/div/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[3]/ul/li[{matchup_num}]/div/div/div[2]/div[1]/time')
    # away_team_rank_name = find_team_rank_name(away_team_text) #Name from team rankings.com
    # home_team_rank_name = find_team_rank_name(home_team_text) #Name from team rankings.com

    matchup = {
        'Away Team': away_team_text, 
        # 'Away Team Rank Name': away_team_rank_name, 
         'FD Away Odds': {
             'Spread': away_spread_text, 
             'Spread Odds': away_spread_odds_text, 
             'Away ML': away_ml_text
         }, 
        'Home Team': home_team_text, 
        # 'Home Team Rank Name': home_team_rank_name, 
         'FD Home Odds': {
             'Spread': home_spread_text, 
             'Spread Odds': home_spread_odds_text, 
             'Home ML': home_ml_text
         },
         'Game': {
             'Start Time': start_time_text, 
             'Total': total_text, 
             'Over Total Odds': over_total_odds_text, 
             'Under Total Odds': under_total_odds_text,
             'League': 'NBA'
        }
    }

    print(f'{away_team_text}, {home_team_text}')
    return matchup

my_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'

options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument(f"user-agent={my_user_agent}")
driver = uc.Chrome(options=options)
driver.get("https://sportsbook.fanduel.com/navigation/nba")


time.sleep(10)  # Reduced sleep time after initial load
#specific_tbody = driver.find_element(By.CSS_SELECTOR, 'tbody.sportsbook-table__body')

#num_rows = len(specific_tbody.find_elements(By.TAG_NAME, 'tr'))
#number_of_games = num_rows/2
all_matchups = []
for z in range(3, 6+1):
    print(f'{z}/{(3)}')
    matchup = scrape(z)
    if matchup:
        all_matchups.append(matchup)

matchup = scrape(1)

#Writes to JSON
try:
    with open('Scrapers/Data/nbaFD.json', 'w') as fp:
        json.dump(matchup, fp, indent=4)
except Exception as e:
    print(f"Error writing to file: {e}")

driver.quit()

