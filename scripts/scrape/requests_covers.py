import csv
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    """Sets up and returns a basic Selenium WebDriver instance."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('log-level=3')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def fetch_articles_requests(url):
    """Attempts to fetch article data using requests (faster)."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Requests failed with status code {response.status_code}, falling back to Selenium...")
        return None  # Indicate failure to trigger Selenium fallback
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract dynamic hashed IDs (if any)
    articles = soup.find_all("article")
    parsed_data = []
    
    for article in articles:
        try:
            title_text = article.find("h1").text.strip()  # Adjust selector based on HTML structure
            away_team, home_team = title_text.split(" @ ")
            
            dynamic_text = article.find("div", {"class": "some-class"})  # Adjust based on actual structure
            if not dynamic_text:
                continue

            text_content = dynamic_text.text
            cover_team = text_content.split(' covered')[0].strip()
            spread_line = text_content.split('spread of ')[1].split('. The total')[0]
            actual_total = text_content.split('The total score of ')[1].split(' was')[0]
            total_line = text_content.strip().split()[-1]

            parsed_data.append([away_team, home_team, cover_team, spread_line, total_line, actual_total])

        except Exception as e:
            print(f"Error parsing article: {e}")

    return parsed_data

def fetch_articles_selenium(url):
    """Falls back to Selenium if requests fails."""
    driver = setup_driver()
    parsed_data = []
    
    try:
        driver.get(url)
        time.sleep(10)  # Adjust if needed

        articles = driver.find_elements("xpath", "//article")
        for article in articles:
            try:
                title = article.text.split("\n")[0]
                away_team, home_team = title.split(" @ ")

                dynamic_text = article.find_element("xpath", './div[3]').text
                cover_team = dynamic_text.split(' covered')[0].strip()
                spread_line = dynamic_text.split('spread of ')[1].split('. The total')[0]
                actual_total = dynamic_text.split('The total score of ')[1].split(' was')[0]
                total_line = dynamic_text.strip().split()[-1]

                parsed_data.append([away_team, home_team, cover_team, spread_line, total_line, actual_total])

            except Exception as e:
                print(f"Error processing article: {e}")
    
    finally:
        driver.quit()
    
    return parsed_data

def save_to_csv(data, output_csv):
    """Saves scraped data to a CSV file."""
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Away Team", "Home Team", "Cover Team", "Closing Spread", "Closing Total Line", "Actual Total Score"])
        writer.writerows(data)
    
    print(f"Saved {len(data)} articles to {output_csv}")

def main():
    """Main function to scrape articles."""
    league_list = ['NCB', 'NBA']
    
    for league in league_list:
        selected_date = date.today() - timedelta(days=1)
        selected_league = 'ncaab' if league == 'NCB' else league
        url = f"https://www.covers.com/sports/{selected_league}/matchups?selectedDate={selected_date}"
        output_csv = f"{selected_league}_matchups_{selected_date}.csv"
        
        print(f"Fetching data for {selected_league} on {selected_date}...")

        # Try requests first
        data = fetch_articles_requests(url)
        
        # If requests failed, use Selenium
        if data is None or len(data) == 0:
            print("Switching to Selenium...")
            data = fetch_articles_selenium(url)
        
        if data:
            save_to_csv(data, output_csv)
        else:
            print("No data found.")

if __name__ == '__main__':
    main()
