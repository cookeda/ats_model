@echo off
:: Capture start time
set start_time0=%time%

:: Run History in Data Collecting Src
cd Data Collecting Src
python history.py

:: Scrape Adv League Data
cd ../OddsHistory
del NBA.json
del MLB.json
scrapy crawl NBA -o NBA.json
scrapy crawl MLB -o MLB.json

:: Scrape League Data
cd ../Data Collecting Src/
:: python MLBScrape.py
python NBAScrape.py
python CBBScrape.py
python script.py
python Sort.py
cd ../

:: Scrape Matchups
cd ./Scrapers/Books
python daily_refresh.py

:: Run Algorithms
cd ../../Data Collecting Src/

python alg.py > ../Results/alg_results.txt
python game.py > ../Results/game_results.txt

cd ../Results
python summary.py
cd ../

cd DegenBets
:: npx eas update --auto 
cd ../

:: Capture end time
set end_time0=%time%

:: Display start and end times
echo Start Time: %start_time0%
echo End Time: %end_time0%