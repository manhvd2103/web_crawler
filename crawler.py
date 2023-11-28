import time
import os
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():

    driver_path = "D:\Works\web_crawler\chromedriver.exe" 
    service = Service(executable_path=driver_path)
    options = Options()
    options.add_argument("--hessless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-using")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--disable-infobars")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-content-security-policy")
    options.add_argument("--disable-proxy-certificate-handler")
    options.add_argument("--allow-running-insecure-content")
    
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    prefs = {"download.default_directory": rf"D:\Works\web_crawler\midi"}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=service, options=options)
            
    driver.get(f"https://musescore.com")
    wait = WebDriverWait(driver, 10)
    
    email = "info@qsent.vn"
    password = "joker2018"
    
    # Login button driver
    login_button = driver.find_element(By.XPATH, "//header/nav[1]/div[4]/section[1]/button[2]")
    login_button.click()
    time.sleep(10)
    
    # Redirect to google click
    google_redirect = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='google']")))
    google_redirect.click()
    time.sleep(10)
    # Login google box
    loginBox = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='identifierId']")))
    loginBox.send_keys(email)
    time.sleep(15)
    nextButton = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id ="identifierNext"]')))
    nextButton.click()
    
    # Password google box
    passWordBox = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id ="password"]/div[1]/div / div[1]/input')))
    passWordBox.send_keys(password)
    time.sleep(15)
    nextButton = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id ="passwordNext"]')))
    nextButton.click()
    print("Login successfully!")
    time.sleep(10)
    
    # Redirect to browse
    browse_element = wait.until(EC.presence_of_element_located((By.XPATH, "//header/nav[1]/div[3]/section[1]/a[1]")))
    browse_element.click()
    time.sleep(10)
    page = len(os.listdir("midi")) // 10
    for i in range(page, page + 2, 1):
        logger.info(f"Crawl data in page: {i + 1} wait some second to download all file...")
        if i > 0:
            driver.get(f"https://musescore.com/sheetmusic?page={i + 1}")
        for j in range(20):
            # Go to midi pages
            article_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "c9ju0")))
            article_elements[j].click()
            time.sleep(5)
            
            try:
                # Download file
                download_button_element = wait.until(EC.element_to_be_clickable((By.NAME, "download")))
                # driver.execute_script("arguments[0].click()", download_button_element)
                download_button_element.click()
                time.sleep(5)
                
                midi_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body/article[1]/section[1]/section[1]/div[1]/section[1]/section[1]/div[4]/div[1]/div[1]/h3[1]/button[1]")))
                midi_element.click()
                time.sleep(5)
            except:
                print("Next file")
                continue
            
            # Back to browse
            try:
                close_element = wait.until(EC.presence_of_element_located((By.XPATH, "//body/article[1]/section[1]/button[1]")))
                close_element.click()
            except Exception as e:
                print(e)
                print("No close button")
            if i > 0:
                driver.get(f"https://musescore.com/sheetmusic?page={i + 1}")
            else:
                browse_element = wait.until(EC.presence_of_element_located((By.XPATH, "//header/nav[1]/div[3]/section[1]/a[1]")))
                browse_element.click()
        logger.info(f"Crawl page {i + 1} done go to next page.")

    driver.close()
    
if __name__ == "__main__":
    main()
