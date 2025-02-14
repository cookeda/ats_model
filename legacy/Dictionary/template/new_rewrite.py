import json
import os

# Define the file paths
current_file_path = 'Dictionary/temp/cbb_teams.json'
old_file_path = '../college/cbb_old/cbb_teams.json'
output_file = 'Dictionary/Pro/test.json'

# Load the current data
with open(current_file_path, 'r') as current_file:
    current_data = json.load(current_file)

# Check if the old data file exists and load it if available
if os.path.exists(old_file_path):
    with open(old_file_path, 'r') as old_file:
        old_data = json.load(old_file)
else:
    old_data = []

# Convert old data to a dictionary for easier lookup by team name
old_data_dict = {team["Team Rankings Name"]: team for team in old_data}

# Create a list to hold the merged data
merged_list = []

# Populate the merged list with data from current and old sources
for team in current_data:
    if team in old_data_dict:
        merged_list.append(old_data_dict[team])
    else:
        merged_list.append({
            "Team Rankings Name": team,
            "DraftKings Name": "",
            "FanDuel Name": "",
            "BetMGM Name": "",
            "Pinnacle Name": "",
            "TeamID": ""
        })

# Save the merged list to the output file
with open(output_file, 'w') as output:
    json.dump(merged_list, output, indent=4)

print("JSON file created or updated successfully.")
