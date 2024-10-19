from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver_path = r'path\chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)


driver.get("https://twitter.com/")
time.sleep(30)

last_height = driver.execute_script("return document.body.scrollHeight")
collected_tweets = set()

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    tweets = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')

    for tweet in tweets:
        try:
            tweet_text = tweet.find_element(By.XPATH, './/span').text
            if tweet_text and tweet_text not in collected_tweets:  
                collected_tweets.add(tweet_text)
                print(tweet_text)
        except Exception as e:
            print("Hata:", e)
            
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
with open('tweets.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Tweet Metni"]) 
    print("Toplanan Tweet Sayısı:", len(collected_tweets))
    for tweet_text in collected_tweets:
        writer.writerow([tweet_text])
        print("Yazılan Tweet:", tweet_text)

driver.quit()
