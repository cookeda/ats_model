import pandas as pd
from datetime import datetime, timedelta, date

def add_home_cover(date):
    league_list = ['NCB', 'NBA']
    for league in league_list:    
        df = pd.read_csv(f'../../data/raw/{league}/{date}/game_results.csv') #TODO(Support CBB)
        df['Home Cover'] = df['Home Team'] == df['Cover Team']
        df = df.reset_index(drop=True)
        df.to_csv(f'../../data/raw/NCB/{date}/game_results.csv', index=False)

start_date = date(2024, 11, 10)
end_date = date.today()
delta = timedelta(days=1)
while start_date < end_date:
    # print(start_date.strftime("%Y-%m-%d"))
    try:
        add_home_cover(start_date)
    except:
        print("Error results processing", date)
    start_date += delta


