import json
import sys

def extract_relevant_data(file_path):
    """
    Extracts and reformats data from a JSON file containing game information.

    This function reads a JSON file specified by the file_path parameter, extracts
    information about each game, and reformats this information into a more
    accessible structure. The reformatted data includes details such as team names,
    spreads, and total points for each game, identified by a unique MatchupID.

    Parameters:
    - file_path (str): The path to the JSON file containing the original game data.

    Returns:
    - dict: A dictionary where each key is a MatchupID and each value is another
      dictionary containing reformatted game information, including home and away
      team names, home and away spreads, and total points.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    reformatted_games = {}
    for game_section in data:
        for game in game_section:
            matchup_info = game['Info Table']
            odds_info = game['Odds Table']
            matchup_id = game['MatchupID']
            reformatted_games[matchup_id] = {
                'Home Team': matchup_info['Home Team Rank Name'],
                'Away Team': matchup_info['Away Team Rank Name'],
                'Home Spread': odds_info['Home Spread'],
                'Away Spread': odds_info['Away Spread'],
                'Total Points': odds_info['Total']
            }
    return reformatted_games

def main(input_file, output_file):
    reformatted_data = extract_relevant_data(input_file)
    with open(output_file, 'w', encoding='utf-8') as new_file:
        json.dump(reformatted_data, new_file, indent=4)
    print(f"Reformatted JSON saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python master_dk_lite.py <input_file_path> <output_file_path>")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        main(input_path, output_path)