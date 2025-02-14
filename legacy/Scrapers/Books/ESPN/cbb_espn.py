import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import fasteners
import os

import requests
import undetected_chromedriver as uc
import time
import threading
import pandas as pd
from time import process_time
import json

league = 'CBB'
book = 'ESPN'

with open('../../../Dictionary/College/CBB.json', 'r') as file:
    team_mappings = json.load(file)

def encode_bet_table_id(matchup_id, book_name):
    """
    Generates a unique identifier for a betting table based on the matchup ID and the book name.

    Parameters:
    - matchup_id (str): The unique identifier for the matchup.
    - book_name (str): The name of the bookmaker.

    Returns:
    - str: A string that combines the book name and the matchup ID, separated by an underscore.
          Returns "Unknown" if either the matchup_id or book_name is missing.
    """
    if matchup_id and book_name:
        return f'{book_name}_{matchup_id}'
    return "Unknown" 

def encode_matchup_id(away_id, home_id, league):
    """
    Generates a unique identifier for a matchup based on the IDs of the away and home teams, and the league.

    Parameters:
    - away_id (str): The unique identifier for the away team.
    - home_id (str): The unique identifier for the home team.
    - league (str): The name of the league in which the matchup is taking place.

    Returns:
    - str: A string that combines the away team ID, home team ID, and league, separated by underscores.
          Returns "Unknown" if either the away_id or home_id is missing.
    """
    if away_id and home_id:
        return f'{away_id}_{home_id}_{league}'
    return "Unknown"

def find_team_id(team_name):
    """
    Searches for a team's ID based on its name.

    This function iterates through a predefined list of team mappings (team_mappings) to find a team's ID using its name. The search is based on the "ESPNBet" key in each mapping, which should match the provided team name.

    Parameters:
    - team_name (str): The name of the team for which the ID is being searched.

    Returns:
    - str: The ID of the team if found, otherwise returns "Unknown".
    """
    for team_mapping in team_mappings:
        if team_mapping["ESPNBet"] == team_name:
            return team_mapping["TeamID"]
    return "Unknown"  # Return a default value if not found

def find_team_rank_name(dk_team_name):
    """
    Searches for a team's ranking name based on its name used in DraftKings (DK).

    This function iterates through a predefined list of team mappings (team_mappings) to find a team's ranking name using its DraftKings name. The search is based on the "ESPNBet" key in each mapping, which should match the provided team name from DraftKings. If a match is found, the function returns the team's ranking name as listed in "Team Rankings Name".

    Parameters:
    - dk_team_name (str): The name of the team as used in DraftKings.

    Returns:
    - str: The ranking name of the team if found, otherwise returns "Unknown".
    """
    for team_mapping in team_mappings:
        if team_mapping["ESPNBet"] == dk_team_name:
            return team_mapping["Team Rankings Name"]
    return "Unknown"  # Return a default value if not found  # Return a default value if not found


match = {}

def clean_team(raw_team: str) -> str:
    """
    Clean a team name from the raw team name.

    Parameters:
    raw_team (str): The raw team name.

    Returns:
    str: The cleaned team name.
    """
    team = raw_team.split(" ")
    team = team[1].upper()
    if team == 'TRAIL':
        team = 'TRAILBLAZERS'
    return team

def generate_game_id(away_team, home_team):
    """
    Generates a unique game identifier using MD5 hashing.

    This function takes the names of the away and home teams, concatenates them, and then applies MD5 hashing to generate a unique identifier for a game. This identifier can be used to distinguish games in databases or logs where unique identification of games is required.

    Parameters:
    - away_team (str): The name of the away team.
    - home_team (str): The name of the home team.

    Returns:
    - str: A hexadecimal string representing the MD5 hash of the concatenated team names.
    """
    combined_string = away_team + home_team
    hash_object = hashlib.md5(combined_string.encode())
    return hash_object.hexdigest()

def find_element_text_or_not_found(driver, xpath, wait_time=10):
    """
    Attempts to find an element on a web page by its XPath and return its text. If the element is not found within the specified wait time, returns 'N/A'.

    Parameters:
    - driver: The Selenium WebDriver instance used to interact with the web page.
    - xpath (str): The XPath string used to locate the element on the web page.
    - wait_time (int, optional): The maximum number of seconds to wait for the element to become visible. Defaults to 10 seconds.

    Returns:
    - str: The text of the found element, or 'N/A' if the element is not found or not visible within the wait time.
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return element.text
    except:
        return 'N/A'

#Espn has +100 odds set to 'Even'
def check_even(text):
    """
    Checks if the provided text represents an 'Even' betting odd and converts it to a standard numerical format.

    In betting terminology, 'Even' odds mean that the potential win is the same amount as the stake. This function converts the textual representation 'Even' to its numerical equivalent '+100', which is the standard format used in betting to represent even odds. If the text does not represent 'Even' odds, it is returned unchanged.

    Parameters:
    - text (str): The text to check for 'Even' odds.

    Returns:
    - str: Returns '+100' if the input text is 'Even', otherwise returns the original text.
    """
    if text == 'Even':
        return '+100'
    return text

def scrape(matchup_num):
    """
    Scrapes betting information for a specific matchup from a webpage.

    This function navigates to specific elements on a webpage using XPath to extract information about a sports matchup. It retrieves details such as team names, spread values, moneyline (ML) values, total points, and start times. It then uses helper functions to find additional information like team rankings and IDs based on the scraped team names. Finally, it compiles all the information into a structured dictionary.

    Parameters:
    - matchup_num (int): The number of the matchup on the webpage, used to construct the XPath for locating elements.

    Returns:
    - list: A list containing a single dictionary with detailed betting and matchup information, including team names, IDs, rankings, and betting odds.
    """
    # Scraping various pieces of information using XPath. Each piece corresponds to a specific betting or game detail.
    away_team_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[2]/div[1]/button/div/div/div[1]')
    home_team_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[3]/div[1]/button/div/div/div[1]')
    away_spread_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[2]/div[2]/button[1]/span[1]')
    away_spread_odds_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[2]/div[2]/button[1]/span[2]')
    total_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[2]/div[2]/button[2]/span[1]')
    over_total_odds_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[2]/div[2]/button[2]/span[2]')
    away_ml_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[2]/div[2]/button[3]/span[2]')
    home_spread_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[3]/div[2]/button[1]/span[1]')
    home_spread_odds_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[3]/div[2]/button[1]/span[2]')
    under_total_odds_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[3]/div[2]/button[2]/span[2]')
    home_ml_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[3]/div[2]/button[3]/span[2]')
    start_time_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[1]/button/span')
    
    # Using helper functions to find team rankings and IDs based on the scraped team names.
    away_team_rank_name = find_team_rank_name(away_team_text)  # Name from team rankings.com
    home_team_rank_name = find_team_rank_name(home_team_text)  # Name from team rankings.com
    away_team_id = find_team_id(away_team_text)  # Team
    home_team_id = find_team_id(home_team_text)  # Team
    
    # Generating unique identifiers for the matchup and the betting table.
    matchup_id = encode_matchup_id(away_team_id, home_team_id, league)
    bet_table_id = encode_bet_table_id(matchup_id, book)
    
    # Compiling all the scraped and generated information into a structured dictionary.
    info = [ 
        {
            'BetTableId': bet_table_id,
            'Odds Table': {
                'Book Name': book,
                'Away Spread': away_spread_text, 
                'Away Spread Odds': away_spread_odds_text,
                'Away ML': away_ml_text,
                'Home Spread': home_spread_text, 
                'Home Spread Odds': home_spread_odds_text,
                'Home ML': home_ml_text,
                'Total': total_text[3:], 
                'Over Total Odds': over_total_odds_text, 
                'Under Total Odds': under_total_odds_text,
            },
            'MatchupID': matchup_id,
            'Info Table': {                
                    'Away Team': away_team_text, 
                    'Away Team Rank Name': away_team_rank_name, 
                    'Away ID': away_team_id,
                    'Home Team': home_team_text, 
                    'Home Team Rank Name': home_team_rank_name,
                    'Home ID': home_team_id, 
                    'Start Time': start_time_text, 
                    'League': league
                }
            }
    ]
    
    # Printing the teams involved in the matchup for logging purposes.
    print(f'{away_team_text}, {home_team_text}')
    return info



def managed_webdriver(*args, **kwargs):
    """
    Context manager for managing the lifecycle of a Selenium WebDriver.

    This function initializes a Selenium WebDriver with the given arguments and keyword arguments,
    and ensures that the WebDriver is properly closed after use. It is designed to be used with
    a 'with' statement, which guarantees that the WebDriver is closed even if an error occurs
    during its use.

    Parameters:
    - *args: Variable length argument list to be passed to the WebDriver constructor.
    - **kwargs: Arbitrary keyword arguments to be passed to the WebDriver constructor.

    Yields:
    - driver: An instance of the initialized Selenium WebDriver.

    Example usage:
    ```
    with managed_webdriver(options=options) as driver:
        driver.get("https://example.com")
    ```
    """
    driver = webdriver.Chrome(*args, **kwargs)
    try:
        yield driver
    finally:
        driver.quit()
def read_games_count(game_type):
    """
    Reads the count of games for a specific game type from a JSON file.

    This function attempts to read a JSON file specified by the global variable `data_file_path`.
    It acquires an inter-process lock before accessing the file to ensure that no other process
    is writing to it at the same time. If the file exists and is not empty, it loads the JSON data
    and attempts to retrieve the count of games for the specified `game_type`. If the `game_type`
    is not found in the data, or if the file does not exist or is empty, the function returns None.

    Parameters:
    - game_type (str): The type of game for which the count is being requested. This should match
                       one of the keys in the JSON data.

    Returns:
    - int or None: The count of games for the specified `game_type` if found, otherwise None.
    """
    with lock:
        if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
            with open(data_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get(game_type)
        return None  # Or appropriate error handling/alternative return value


options = Options()
options.add_argument('--headless')
options.add_argument('log-level=3')

# Initialize the Service
service = Service(ChromeDriverManager().install())

# Initialize WebDriver without the 'desired_capabilities' argument
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://espnbet.com/sport/basketball/organization/united-states/competition/ncaab/featured-page")


time.sleep(10)  # Reduced sleep time after initial load
#specific_tbody = driver.find_element(By.CSS_SELECTOR, 'tbody.sportsbook-table__body')

#num_rows = len(specific_tbody.find_elements(By.TAG_NAME, 'tr'))
data_file_path = '../games_count.json'
lock_file_path = '../games_count.lock'
lock = fasteners.InterProcessLock(lock_file_path)


number_of_games = read_games_count('CBB')
all_matchups = []
for z in range(1, int(number_of_games)+1):
    print(f'{league} - {book}: {z}/{int(number_of_games)}')
    matchup = scrape(z)
    if matchup:
        all_matchups.append(matchup)

print(f'Total matchups scraped: {len(all_matchups)}')
driver.quit()


#Writes to JSON
try:
    with open('../../Data/ESPN/CBB.json', 'w', encoding='utf-8') as fp:
        json.dump(all_matchups, fp, indent=4)
except Exception as e:
    print(f"Error writing to file: {e}")


#TODO: Only Scrape todays matches
#TODO: Fix freeze bug
#TODO: Fix dictionary for ESPN
