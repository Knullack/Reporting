import importlib
import logging
import subprocess
import sys
import os
import glob
import time
import pandas as pd
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome


logging.basicConfig(level=logging.ERROR)

SITE = "https://peculiar-inventory-na.aka.corp.amazon.com/HDC3/overview"
LOGIN_URL = "https://fcmenu-iad-regionalized.corp.amazon.com/login"

class chromeSession():
    def __init__(self, badge: int):
        """Badge for FC Menu login"""
        self.driver = None
        self.badge = str(badge)
        self.file_prefixes = ["Pick All types", "Bin Item Defects All types"]

    def delete_cookie_by_name(self, cookie_name):
        """Deletes a cookie by name in the Chrome settings."""
        # Open Chrome settings
        self.driver.get("chrome://settings/content/all")

        # Wait for the cookies to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(('xpath', "/html/body/settings-ui//div[2]/settings-main//settings-basic-page//div[1]/settings-section[5]/settings-privacy-page//settings-animated-pages/settings-subpage/all-sites//div[6]/iron-list/site-entry[1]//div/div/div[2]/cr-icon-button")))

        # Find all cookies
        cookies = self.driver.find_element('xpath', "/html/body/settings-ui//div[2]/settings-main//settings-basic-page//div[1]/settings-section[5]/settings-privacy-page//settings-animated-pages/settings-subpage/all-sites//div[6]/iron-list/site-entry[1]//div/div/div[2]/cr-icon-button")

        # Iterate over cookies to find the one with the specified name
        for cookie in cookies:
            # Check if the cookie name matches
            if cookie.find_element(By.CSS_SELECTOR, ".settings-cookie-name").text == cookie_name:
                # Click on the corresponding trash button
                trash_button = cookie.find_element(By.CSS_SELECTOR, ".settings-cookie-remove")
                trash_button.click()

                # Find and click the "Delete site data and permissions" link
                delete_link = self.driver.find_element(By.XPATH, '//button[@title="Delete site data and permissions for a2z.com"]')
                delete_link.click()
                break

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

    def launch_chrome_with_remote_debugging(self, port):
        import subprocess
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([chrome_path, f"--remote-debugging-port={port}"])

    def start(self) -> object:
        """Starts a Chrome browser session"""
        self.install_module('selenium')
        self.port = 9200
        self.launch_chrome_with_remote_debugging(self.port)
        optionals = ChromeOptions()
        optionals.add_argument('--log-level=3')
        optionals.add_argument('--force-device-scale-factor=0.7')
        optionals.add_argument('--disable-blink-features=AutomationControlled')
        optionals.add_argument('--disable-notifications')
        optionals.add_argument('--disable-infobars')
        optionals.add_argument('--disable-extensions')
        optionals.add_argument('--disable-dev-shm-usage')
        optionals.add_argument('--disable-gpu')
        optionals.add_argument('--disable-browser-side-navigation')
        optionals.add_argument('--disable-features=VizDisplayCompositor')
        optionals.add_argument('--no-sandbox')
        optionals.add_argument('--disable-logging')
        optionals.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.port}")

        self.driver = Chrome(options=optionals)
        self.driver.implicitly_wait(10)
        # self.delete_cookie_by_name('a2z.com')
        self.FCMenu_login(self.driver, self.badge)
        
        self.driver.refresh()
    
    def get_text(self, site: str, xpath: str) -> str:
        """Retrieves the text at the given -xpath from the given -site"""
        actions = ActionChains(self.driver)
        try:
            if self.driver.current_url != site:
                self.navigate(self.driver, site, 2)

            element = self.driver.find_element(By.XPATH, xpath)
            actions.move_to_element(element).perform()
            return element.text
        except WebDriverException as WDE:
            if "ERR_NAME_NOT_RESOLVED" in WDE.msg:
                logging.error("Error: DNS resolution failed.")
            else:
                logging.error(f"Element not found for site '{site}' with XPath '{xpath}': {WDE}")
            return None
    
    def download_csv(self, url: str, button_xpath: str, download_dir: str, pick_andon: bool = False) -> int | float:
        self.navigate(self.driver, url, 5)
        
        # Wait for the download button to become clickable
        download_button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        download_button.click()

        time.sleep(5)

        # Search for the latest downloaded CSV file with the matching prefix
        csv_files = []
        if pick_andon:
            csv_files.extend(glob.glob(os.path.join(download_dir, f"Pick All types*.csv")))
        else:
            csv_files.extend(glob.glob(os.path.join(download_dir, f"Bin Item Defects All types*.csv")))
        print("CSV files found:", csv_files)  # Print the list of CSV files
        if not csv_files:
            print("No CSV files found in the download directory.")
            return None

        latest_file = max(csv_files, key=os.path.getmtime)

        # Use Pandas to open and read the CSV file
        if os.path.exists(latest_file):
            df = pd.read_csv(latest_file, header=0)
            # Count the number of rows excluding the header
            num_rows = df.shape[0]
            return num_rows
        else:
            print("CSV file not found in the download directory.")

    def close(self) -> None:
        """Quit the Chrome driver & terminate processes"""
        if self.driver:
            self.driver.quit()
            self.close_chrome_processes()
        else:
            return logging.INFO('No session active')
    
    def SBC_accuracy(self, site: str, download_anchor_xPath: str) -> float:
        actions = ActionChains(self.driver)
        self.navigate(self.driver, site, 5)

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(('xpath', "/html/body/div[2]/nav/div[2]/ul[2]/li[3]/a")))
        time_span = self.driver.find_element(By.XPATH, '/html/body/div[2]/nav/div[2]/ul[2]/li[3]/a')
        time_span.click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(('xpath', '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[1]/ul/li[1]/a')))
        quick = self.driver.find_element(By.XPATH, '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[1]/ul/li[1]/a')
        quick.click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(('xpath', '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[2]/div/div/div[1]/ul/li[2]/a')))
        this_week = self.driver.find_element(By.XPATH, '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[2]/div/div/div[1]/ul/li[2]/a')
        this_week.click()

        csv = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/dashboard-grid/ul/li[6]/dashboard-panel/div/visualize/div[2]/div/div/kbn-agg-table-group/table/tbody/tr/td/kbn-agg-table-group/table/tbody/tr/td/kbn-agg-table/paginated-table/paginate/div[2]/div/a')
        csv.click()

    def close_chrome_processes(self):
        try:
            # Find all running processes with name chrome.exe
            chrome_processes = os.popen('tasklist /FI "IMAGENAME eq chrome.exe"').read()

            # Check if any chrome.exe processes are running
            if "chrome.exe" in chrome_processes:
                # Redirect output to os.devnull to suppress termination messages
                os.system('taskkill /F /IM chrome.exe > nul 2>&1')
                print("Chrome processes terminated successfully.")
            else:
                print("No Chrome processes found.")
        except Exception as e:
            print(f"Error occurred while terminating Chrome processes: {e}")