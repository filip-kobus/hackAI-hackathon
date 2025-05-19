import pickle
import chromedriver_autoinstaller
from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

load_dotenv()

class Xpaths:
    userid = "//input[@id='userID']"
    password = "//input[@id='pass']"
    login_button = "//button[@id='submitButton']"
    sms_indicator = "//label[@id='label-editbox-sms-code']"
    sms_field = "//input[@id='sms-code']"
    sms_button = "//button[@id='editbox-confirm-btn']"

class CSS_SELECTORS:
    sms_field = "input#sms-code"
    sms_button = "button#editbox-confirm-btn"
    authorization_component = "mbank-auth-v5"
    diaog_component = "dialog-component"

class Login:
    URL = "https://urev.online.mbank.pl/pl/Login"
    WAIT_TIME = 45

    def __init__(self):
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome()
        self.xpaths = Xpaths
        self.css_selectors = CSS_SELECTORS
        self.userId = os.getenv("USER_ID")
        self.password = os.getenv("PASSWORD")
        self.sms_code = os.getenv("SMS_CODE")

    def open_page(self):
        self.driver.get(self.URL)
        self.driver.maximize_window()

    def login(self):
        wait = WebDriverWait(self.driver, self.WAIT_TIME)
        wait.until(EC.presence_of_element_located((By.XPATH, self.xpaths.userid))).send_keys(self.userId)
        wait.until(EC.presence_of_element_located((By.XPATH, self.xpaths.password))).send_keys(self.password)
        wait.until(EC.element_to_be_clickable((By.XPATH, self.xpaths.login_button))).click()

    def get_shadow_root(self, element):
        return self.driver.execute_script('return arguments[0].shadowRoot', element)

    def confirm_sms(self):
        wait = WebDriverWait(self.driver, self.WAIT_TIME)
        wait.until(EC.presence_of_element_located((By.XPATH, self.xpaths.sms_indicator)))
        shadow_host = self.driver.find_element(By.CSS_SELECTOR, self.css_selectors.authorization_component)
        shadow_root = self.get_shadow_root(shadow_host)
        sms_input = shadow_root.find_element(By.CSS_SELECTOR, self.css_selectors.sms_field)
        sms_input.send_keys(self.sms_code)
        shadow_root.find_element(By.CSS_SELECTOR, self.css_selectors.sms_button).click()

if __name__ == "__main__":
    session = Login()
    session.open_page()
    session.login()
    session.confirm_sms()
    input()

