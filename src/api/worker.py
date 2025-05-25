"""
Selenium worker
"""


import chromedriver_autoinstaller
from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options

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
    chat_icon_button = 'button[data-test-id="chat:chat-icon"]'
    chat_tab_button = 'button[id="tab-1"]'
    chat_input_field = 'textarea[id="textbox"]'
    chat_send_button = 'chat-icon-button'
    bot_message = 'mbank-chat-message-bot'
    user_message = 'mbank-chat-message-customer'

class ShadowRoot_Routes:
    chat_icon_route = ["mbank-chat", "chat-minimized", "chat-icon-button"]
    chat_tab_route = ["mbank-chat", "mbank-tabs"]
    chat_input_route = ["mbank-chat", "chat-base", "mbank-chat-textbox"]
    chat_messages_route = ["mbank-chat", "chat-base", "mbank-chat-messages-container"]

class SeleniumWorker:
    URL = "https://urev.online.mbank.pl/pl/Login"
    WAIT_TIME = 150

    def __init__(self):
        chromedriver_autoinstaller.install()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.userId = os.getenv("USER_ID")
        self.password = os.getenv("PASSWORD")
        self.sms_code = os.getenv("SMS_CODE")
        self.bot_messages = []
        self.isReloading = True

    def open_page(self):
        self.driver.get(self.URL)

    def login(self):
        wait = WebDriverWait(self.driver, self.WAIT_TIME)
        wait.until(EC.presence_of_element_located((By.XPATH, Xpaths.userid))).send_keys(self.userId)
        wait.until(EC.presence_of_element_located((By.XPATH, Xpaths.password))).send_keys(self.password)
        wait.until(EC.element_to_be_clickable((By.XPATH, Xpaths.login_button))).click()

    def get_nested_shadow_root(self, route):
        wait = WebDriverWait(self.driver, self.WAIT_TIME)
        previous = None
        for element in route:
            if previous is None:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))
                shadow_host = self.driver.find_element(By.CSS_SELECTOR, element)
            else:
                shadow_host = previous.find_element(By.CSS_SELECTOR, element)
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', shadow_host)
            if shadow_root is None:
                raise Exception(f"Shadow root not found for {element}")
            previous = shadow_root
        return previous

    def get_shadow_root_element(self, element):
        shadow_host = self.driver.find_element(By.CSS_SELECTOR, element)
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', shadow_host)
        return shadow_root

    def confirm_sms(self):
        wait = WebDriverWait(self.driver, self.WAIT_TIME)
        wait.until(EC.presence_of_element_located((By.XPATH, Xpaths.sms_indicator)))
        shadow_root = self.get_shadow_root_element(CSS_SELECTORS.authorization_component)
        sms_input = shadow_root.find_element(By.CSS_SELECTOR, CSS_SELECTORS.sms_field)
        sms_input.send_keys(self.sms_code)
        shadow_root.find_element(By.CSS_SELECTOR, CSS_SELECTORS.sms_button).click()

    def click_chat_icon(self):
        shadow_root = self.get_nested_shadow_root(ShadowRoot_Routes.chat_icon_route)
        chat_button = shadow_root.find_element(By.CSS_SELECTOR, CSS_SELECTORS.chat_icon_button)
        sleep(1)
        chat_button.click()

    def click_chat_tab(self):
        shadow_root = self.get_nested_shadow_root(ShadowRoot_Routes.chat_tab_route)
        chat_tab = shadow_root.find_element(By.CSS_SELECTOR, CSS_SELECTORS.chat_tab_button)
        sleep(1)
        chat_tab.click()

    def send_message(self, message):
        shadow_root = self.get_nested_shadow_root(ShadowRoot_Routes.chat_input_route)
        chat_input = shadow_root.find_element(By.CSS_SELECTOR, CSS_SELECTORS.chat_input_field)
        try:
            chat_input.send_keys(message)
            chat_send_button = shadow_root.find_element(By.CSS_SELECTOR, CSS_SELECTORS.chat_send_button)
            chat_send_button.click()
        except Exception as e:
            print(f"Error while sending a message: {e}")
            self.isReloading = True

    def load_bot_messages(self):
        shadow_root = self.get_nested_shadow_root(ShadowRoot_Routes.chat_messages_route)
        wait = WebDriverWait(shadow_root, 10)
        self.bot_messages = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, CSS_SELECTORS.bot_message)))

    def initialize(self):
        self.login()
        self.confirm_sms()
        self.click_chat_icon()
        self.click_chat_tab()
        self.load_bot_messages()
        self.isReloading = False

    def load_response(self):
        shadow_root = self.get_nested_shadow_root(ShadowRoot_Routes.chat_messages_route)
        wait = WebDriverWait(shadow_root, 10)
        extracted_message = None

        try:
            current_bot_messages = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, CSS_SELECTORS.bot_message)))
            diff = len(current_bot_messages) - len(self.bot_messages)
            if diff > 0:
                latest = current_bot_messages[-1]
                if latest not in self.bot_messages:
                    self.bot_messages = current_bot_messages
                    message_root = self.driver.execute_script('return arguments[0].shadowRoot', latest)
                    extracted_message = message_root.find_element(By.CSS_SELECTOR, 'p[class="textContent"]').text

        except StaleElementReferenceException:
            print("StaleElementReferenceException occurred. Retrying...")
            return self.load_response()

        return extracted_message

    def is_chat_window_present(self):
        shadow_root = self.get_nested_shadow_root(ShadowRoot_Routes.chat_input_route)
        chat_input = shadow_root.find_element(By.CSS_SELECTOR, CSS_SELECTORS.chat_input_field)

    def check_for_response(self):
        response = None
        while response is None:
            response = self.load_response()
            if response is None:
                sleep(0.25)
        return response

    def kill_session(self):
        if self.driver:
            self.driver.quit()
            print("Selenium session terminated.")

if __name__ == "__main__":
    session = SeleniumWorker()
    session.open_page()
    session.initialize()

    while True:
        if not session.isReloading:
            print("Enter your message:")
            message = input()
            if message.lower() == "exit":
                break
            session.send_message(message)
            response = session.check_for_response()
            print(f"Response: {response}")
            sleep(0.1)
        else:
            session.initialize()