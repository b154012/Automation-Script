# Created By  : Zulmi Yahya
# Created Date: 27/01/2023

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import pandas as pd
import time
import sys

def launchBrowser():
    
    try:   
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
            
        website = 'https://www.adamchoi.co.uk/overs/detailed'
        path = "/Users/User/Documents/'Auto Scripts'/Chrome Driver"
        driver = webdriver.Chrome(path, options=chrome_options)
        driver.get(website)
            
        all_matches_button = driver.find_element(By.XPATH, "//label[@analytics-event='All matches']")
        all_matches_button.click()

        select_id = driver.find_element(By.ID, 'country')
        dropdown = Select(select_id)
        dropdown.select_by_visible_text('Spain')

        time.sleep(2)

        matches = driver.find_elements(By.TAG_NAME, "tr")

        date = []
        home_team = []
        score = []
        away_team = []

        for match in matches:
            date.append(match.find_element(By.XPATH, "./td[1]").text)
            home_team.append(match.find_element(By.XPATH, "./td[2]").text)
            score.append(match.find_element(By.XPATH, "./td[3]").text)
            away_team.append(match.find_element(By.XPATH, "./td[4]").text)
            
        df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
        df.to_csv('football_data.csv', index=False)
        
    except Exception as err:
        print(err)
    finally:
        driver.quit()

if __name__ == '__main__':
    launchBrowser()