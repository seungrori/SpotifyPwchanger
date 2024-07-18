from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

class Spotify:
    def __init__(self):
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
        self.loginurl = "https://accounts.spotify.com/ko/login?continue=https%3A%2F%2Fwww.spotify.com%2Fkr-ko%2Faccount%2Fchange-password%2F"

    async def changepw(self, id, pw, newpw):
        try:
            self.driver.get(self.loginurl)
            self.driver.find_element(By.XPATH, '//*[@id="login-username"]').send_keys(id)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="login-password"]').send_keys(pw)
            time.sleep(2)
            self.driver.find_element(By.CSS_SELECTOR,'#login-button').click()
            time.sleep(3.0)
            try:
                self.driver.find_element(By.CSS_SELECTOR, "#old_password")
            except Exception as e:
                print(e)
                return "loginerror"
            
            try:
                self.driver.find_element(By.CSS_SELECTOR, "#old_password").send_keys(pw)
            except:
                self.driver.find_element(By.XPATH, '//*[@id="old_password"]').send_keys(pw)

            try:
                self.driver.find_element(By.CSS_SELECTOR, "#new_password").send_keys(newpw)
            except:
                self.driver.find_element(By.XPATH, '//*[@id="new_password"]').send_keys(newpw)

            try:
                self.driver.find_element(By.CSS_SELECTOR, "#new_password_confirmation").send_keys(newpw)
            except:
                self.driver.find_element(By.XPATH, '//*[@id="new_password_confirmation"]').send_keys(newpw)
            try:
                self.driver.find_element(By.CSS_SELECTOR, "#__next > div.encore-layout-themes.encore-dark-theme > div > div.sc-85f631f4-0.ieLURn > div.sc-decd1ee7-0.hYa-doI > article > section > form > div.sc-55564d75-0.iETFCl > button").click()
            except:
                self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div/div[2]/div[2]/article/section/form/div[4]/button').click()
            
            self.driver.close()
            return "success"
        except Exception as e:
            print(e)
            return "exception"