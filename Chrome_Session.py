import importlib
import logging
import subprocess
import sys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome


logging.basicConfig(level=logging.ERROR)

SITE = "https://peculiar-inventory-na.aka.corp.amazon.com/HDC3/overview"
LOGIN_URL = "https://fcmenu-iad-regionalized.corp.amazon.com/login"

class chromeSession():
    """(1) Start a session\n
    (2) Call get_text()
    """
    def __init__(self, badge: int):
        """Badge for FC Menu login"""
        self.driver = None
        self.badge = str(badge)

    def install_module(self, module_name: str) -> None:
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError:
            logging.info(f"{module_name} not found. Installing it now...")
            try:
                subprocess.run([sys.executable, '-m', 'pip',
                            'install', module_name], check=True)
            except subprocess.CalledProcessError as e:
                logging.error(f"Error installing {module_name}: {e}")
                sys.exit(1)

    def FCMenu_login(self, driver: Chrome, badge: str) -> None:
        """Logs into FCMenu with given BADGE"""
        self.navigate(driver, LOGIN_URL, 5)
        driver.get(LOGIN_URL)
        loginBadge = badge
        input_element = driver.find_element('xpath', '//*[@id="badgeBarcodeId"]')
        self.HELPER_type_and_click(input_element,loginBadge)

    def HELPER_type_and_click(self, element: object, text_to_type: str) -> None:
        element.send_keys(text_to_type)
        element.send_keys(Keys.ENTER)
        
    def navigate(self, driver: Chrome, url: str, max_attempts: int) -> None:
        """Navigate to give URL"""
        exception_count = 0
        while exception_count < max_attempts:
            try:
                driver.get(url)
                return
            except WebDriverException as se:
                exception_count += 1
                # logging.error(f'WebDriverException #{exception_count}:\n Error in loading URL:: {se.msg}\n')

    def start(self) -> object:
        """Starts a Chrome browser session"""
        self.install_module('selenium')
        
        optionals = ChromeOptions()
        optionals.add_argument('--log-level=3')
        optionals.add_argument('--force-device-scale-factor=0.7')
        optionals.add_argument('--disable-blink-features=AutomationControlled')
        optionals.add_argument('--disable-notifications')
        optionals.add_experimental_option('excludeSwitches', ['enable-automation'])
        optionals.add_experimental_option('useAutomationExtension', False)
        optionals.add_argument('--disable-infobars')
        optionals.add_argument('--disable-logging')

        self.driver = Chrome(options=optionals)
        self.driver.implicitly_wait(10)
    
    def get_text(self, site: str, xpath: str) -> str:
        """Retrieves the text at the given -xpath from the given -site"""
        actions = ActionChains(self.driver)
        try:
            self.FCMenu_login(self.driver, self.badge)
            self.navigate(self.driver, site, 2)
            actions.move_to_element(By.XPATH, xpath)
            element = self.driver.find_element(By.XPATH, xpath)
            return element.text
        except WebDriverException as WDE:
            if "ERR_NAME_NOT_RESOLVED" in WDE.msg:
                logging.error("Error: DNS resolution failed.")
            else:
                logging.error(f"Element not found for site '{site}' with XPath '{xpath}': {WDE}")
            return None
        
    def close(self) -> None:
        """Quit the Chrome driver"""
        if self.driver:
             self.driver.quit()
        else:
            return logging.error('No session active')
            