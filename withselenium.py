from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

import time


driver_path = r'path\chromedriver.exe'  # Buraya ChromeDriver yolunu ekleyin
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)
search_query = input("hashtag")
driver.get(f"https://twitter.com/search?q={search_query}&src=typed_query")
time.sleep(25)
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
tweets = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')

for tweet in tweets:
    tweet_text = tweet.find_element(By.XPATH, './/span').text  # İlk <span> öğesini al
    hashtags = tweet.find_elements(By.XPATH, './/a[@role="link"]')  # Tüm etiketleri al
    hashtags_list = [hashtag.text for hashtag in hashtags]
    print("Tweet Metni:", tweet_text)
    print("Hashtagler:", hashtags_list)
    print()
driver.quit()