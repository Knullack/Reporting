import importlib
import logging
import subprocess
import sys
import os
import csv
import io
from PIL import Image
import time
import glob
import time
import pandas as pd
from datetime import datetime, timedelta
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, StaleElementReferenceException,  ElementClickInterceptedException
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
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ARGUMENTS = ['--log-level=3','--force-device-scale-factor=0.7','--disable-blink-features=AutomationControlled','--disable-notifications','--disable-infobars','--disable-extensions','--disable-dev-shm-usage','--disable-gpu','--disable-browser-side-navigation','--disable-features=VizDisplayCompositor','--no-sandbox','--disable-logging']

class locator:
    body = '/html/body'
    nav = '/html/body/nav'
    class xpath:

        class counts:
            time_span = '/html/body/div[2]/nav/div[2]/ul[2]/li[3]/a'
            iframe = '/html/body/div/iframe'
            absolute = '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[1]/ul/li[3]/a'
            time_from = '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[2]/div/div/form/div[1]/div[1]/input'
            time_to = '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[2]/div/div/form/div[2]/div[1]/input'
            go = '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[2]/div/div/form/div[3]/div/button'
            okay = '/html/body/div[4]/div/div/div[2]/button[2]'
       
        class peculiar_inventory:
            table_body = '/html/body/div[1]/div[3]/div/div[1]/div/div[1]/table/tbody'
 
        class delete:
            H1_header = '/html/body/div[1]/div[4]/div/div[2]/div[1]/div/div/h1'
            restart = '/html/body/div[1]/div[2]/div/div[2]/ul/li[2]/span/span/a'
            btn_restart = '/html/body/div[4]/div/div/div/div[1]/div[1]/span[2]/div/div/div/div[1]/h1'
            
            class scan:
                input = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/div/input'
                enter = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/span/span/input'
            class select:
                enter = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/span[1]/span/input'
                container_empty = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/div[2]/div/div'
            class reason:
                enter = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/span[1]/span/input'
            class confirm:
                enter = '/html/body/div[1]/div[4]/div/div[2]/div[1]/form/span[1]/span/span/input'
 
        class fcmenu:
            input_badge = '//*[@id="badgeBarcodeId"]'
            inbound = '/html/body/div[3]/div/div[2]/ul[1]/li[1]/a'
            move_container_145 = '/html/body/div[3]/div/div[2]/ul[2]/li[3]/a'
            individually_workflow = '/html/body/div/div/div/ul/li[2]'
            class move_container:
                input = '/html/body/div/div[7]/div/input'
                input_box = '/html/body/div/div[7]'
                label_scan_destination = '/html/body/div/div[3]/div[2]/div[1]/div/div/h3'

        class picking_console:
            error_msg = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[1]/div/span/awsui-flashbar/div/awsui-flash/div/div[2]/div/div/span/span/span'
            table = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[3]/div/div/awsui-table/div/div[3]'
        
        class fc_andons:
            error_msg = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-flash/div/div[2]/div/div'

    class class_name:
        class delete:
            enter = 'a-button-input'
        
        class cc_completion:
            spinner = 'spinner.large'

class header:
    SCAN = 'Scan container'
    SELECT = 'Select item to delete'
    REASON = ['Select reason to delete','Select deletion reason']
    CONFIRM = 'Confirm Deletion'

class chromeSession(): 
    def __init__(self, badge: int):
        """Badge for FC Menu login"""
        self.driver = None
        self.badge = str(badge)
        self.file_prefixes = ["Pick All types", "Bin Item Defects All types"]
        
    def delete_cookie_by_name(self, cookie_name) -> None:
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
        input_element = driver.find_element('xpath', locator.xpath.fcmenu.input_badge)
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

    def launch_chrome_with_remote_debugging(self, port) -> None:
        import subprocess
        chrome_path = CHROME_PATH
        subprocess.Popen([chrome_path, f"--remote-debugging-port={port}"])

    def start(self) -> object:
        """Starts a Chrome browser session"""
        self.install_module('selenium')
        self.port = 9200
        self.launch_chrome_with_remote_debugging(self.port)
        optionals = ChromeOptions()
        for arg in ARGUMENTS:
            optionals.add_argument(arg)
        optionals.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.port}")

        self.driver = Chrome(options=optionals)
        self.driver.implicitly_wait(10)
        self.actions = ActionChains(self.driver)
        self.FCMenu_login(self.driver, self.badge)
            
    def get_text(self, site: str, xpath: str) -> str:
        """Retrieves the text at the given -xpath from the given -site"""
        table = None
        actions = ActionChains(self.driver)
        siteERR = None
        attempt = 0
        while attempt < 2:
            try:
                self.driver.execute_script('location.reload();') if attempt == 1 else None
                if self.driver.current_url != site:
                    self.navigate(self.driver, site, 2)
                    WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, locator.body)))
                    if "picking-console" in site:
                        try:
                            siteERR = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, locator.xpath.picking_console.error_msg)))
                            siteERR = True
                        except TimeoutException:
                            siteERR = False
                            table = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.picking_console.table)))
                    if "fc-andons" in site:
                        try:
                            siteERR = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fc_andons.error_msg)))
                            siteERR = True
                        except TimeoutException:
                            siteERR = False
                if not siteERR:
                    if table:
                        actions.move_to_element(table)
                    WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath)))
                    element = self.driver.find_element(By.XPATH, xpath)
                    actions.move_to_element(element).perform()
                    return element.text
                else:
                    attempt += 1
            except WebDriverException as WDE:
                # return f"Element not found for site '{site}' with XPath '{xpath}'"
                raise NoSuchElementException
    
    def download_csv(self, url: str, button_xpath: str, download_dir: str, pick_andon: bool = False) -> int | float:
        self.navigate(self.driver, url, 5)
        
        # Wait for the download button to become clickable
        download_button = WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
        download_button.click()
        time.sleep(5)
        csv_files = []
        if pick_andon:
            csv_files.extend(glob.glob(os.path.join(download_dir, f"Pick All types*.csv")))
        else:
            csv_files.extend(glob.glob(os.path.join(download_dir, f"Bin Item Defects All types*.csv")))
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
    
    def SBC_accuracy(self, site: str, download_anchor_xPath: str, download_dir: str) -> float:
        # navigation
        self.navigate(self.driver, site, 5)
        iframe = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, locator.xpath.counts.iframe)))
        self.driver.switch_to.frame(iframe)
        tFrom, tTo = self.timeline()

        # actions
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/nav/div[2]/ul[2]/li[3]/a")))
        time_span = self.driver.find_element(By.XPATH, locator.xpath.counts.time_span)
        time_span.click()

        absolute = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, locator.xpath.counts.absolute)))
        absolute.click()

        eleFrom = self.driver.find_element(By.XPATH, locator.xpath.counts.time_from)
        eleFrom.clear()
        eleFrom.send_keys(tFrom)

        eleTo = self.driver.find_element(By.XPATH, locator.xpath.counts.time_to)
        eleTo.clear()
        eleTo.send_keys(tTo)
        btn_GO = self.driver.find_element(By.XPATH, locator.xpath.counts.go)
        btn_GO.click()
        # download
        try:
            csv = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, download_anchor_xPath)))
            csv.click()
            time.sleep(3)
            WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located((By.CLASS_NAME, "spinner.large"))) # website loading effect element
            csv_files = []
            csv_files.extend(glob.glob(os.path.join(download_dir, f"table_*.csv")))
            if not csv_files:
                print("No CSV files found in the download directory.")
                return None

            latest_file = max(csv_files, key=os.path.getmtime)
            print(f'Accuracy File: {str(latest_file).split(r"\\")[-1]}')
            # Use Pandas to open and read the CSV file
            if os.path.exists(latest_file):
                return self.calculate_average(latest_file, 5, 1)
            else:
                print("CSV file not found in the download directory.")


        except TimeoutException:
            return "SBC_Accuracy: Element not found"
    
    def CC_Completion(self, site: str, download_anchor_xPath: str, download_dir: str) -> tuple:
        attempt = 0
        while attempt < 2:
            ERR_OOPS = False
            self.driver.execute_script('location.reload();') if attempt == 1 else self.navigate(self.driver, site, 5)
            # navigation
            iframe = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, locator.xpath.counts.iframe)))
            self.driver.switch_to.frame(iframe)
            tFrom, tTo = self.timeline()
            try: 
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.nav)))
                ERR_OOPS = True
            except TimeoutException:
                ERR_OOPS = False
            
            if not ERR_OOPS:
                try:
                    # actions
                    WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/nav/div[2]/ul[2]/li[3]/a')))
                    time_span = self.driver.find_element(By.XPATH, locator.xpath.counts.time_span)
                    time_span.click()
                    
                    WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[1]/ul/li[3]/a')))
                    absolute = self.driver.find_element(By.XPATH, locator.xpath.counts.absolute)
                    absolute.click()
                    
                    eleFrom = self.driver.find_element(By.XPATH, locator.xpath.counts.time_from)
                    eleFrom.clear()
                    eleFrom.send_keys(tFrom)

                    eleTo = self.driver.find_element(By.XPATH, locator.xpath.counts.time_to)
                    eleTo.clear()
                    eleTo.send_keys(tTo)

                    btn_GO1 = self.driver.find_element(By.XPATH, locator.xpath.counts.go)
                    btn_GO1.click()
                    WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, locator.class_name.cc_completion.spinner)))
                    WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, locator.class_name.cc_completion.spinner)))
                except TimeoutException:
                    attempt += 1
                try:
                    csv = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, download_anchor_xPath)))
                    csv.click()

                    btn_ok = self.driver.find_element(By.XPATH, locator.xpath.counts.okay)
                    btn_ok.click()
                    start_time = time.time()
                    # can take quite a few seconds to download file (60s max)
                    WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located((By.CLASS_NAME, locator.class_name.cc_completion.spinner)))
                    csv_files = []
                    csv_files.extend(glob.glob(os.path.join(download_dir, f"export_*.csv")))
                    if not csv_files:
                        print("No CSV files found in the download directory.")
                        return None

                    latest_file = max(csv_files, key=os.path.getmtime)
                    print(f"completion file: {str(latest_file).split(r"\\")[-1]}")
                    # Use Pandas to open and read the CSV file
                    if os.path.exists(latest_file):
                        elapsed_time = time.time() - start_time
                        print(f"time to download count_completion: {elapsed_time}")
                        return self.calculate_counts(latest_file)
                        
                except TimeoutException:
                    return "CC_Completion: Element not found"
            else:
                attempt += 1

    def timeline(self) -> tuple:
        """returns (current week's start of week (sunday) date & default time (07:00), current day date & default time (18:00))"""
        dFrom =f"{datetime.now().date() + timedelta(self.subtract_by(datetime.now().weekday()))} 07:00:00.000"
        dNow = f"{datetime.now().date()} 18:00:00.000"
        return (dFrom, dNow)

    def subtract_by(self, day: int) -> int:
        # sunday = 6, monday = 1,... saturday = 5
        match day:
            case 0: # monday
                return -1
            case 1: # tuesday
                return -2
            case 2: # wednesday
                return -3
            case 3: # thursday
                return -4
            case 4: # friday
                return -5
            case 5: # saturday
                return -6
            case 6: # sunday
                return 0
                
    def calculate_average(self, csv_file: str, column_index: int, start_row: int) -> float:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row
            for _ in range(start_row - 1):
                next(reader, None)  # Skip rows until reaching the start_row
            data = [row[column_index] for row in reader]  # Extract data from the specified column
            numeric_data = [float(value) for value in data if value]  # Convert data to float, ignoring empty values
            average = sum(numeric_data) / len(numeric_data) if numeric_data else 0  # Calculate average
            return f"{str(round(average, 2))}%"
    
    def calculate_counts(self, csv_file: str) -> tuple:
        cycle_count = 0
        simple_count = 0
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['work_type'] == 'CYCLE_COUNT':
                    cycle_count += 1
                elif row['work_type'] == 'SIMPLE_BIN_COUNT':
                    simple_count += 1
        if type(cycle_count) != int and type(simple_count) != int:
            raise ValueError(f"Cycle Count Type: {type(cycle_count)}::: value: {cycle_count}\nSimple Count Type: {type(simple_count)}::: value: {simple_count}")
        else:
            return cycle_count, simple_count

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
    
    def delete_get_container(self, tr):
        container = self.get_text('https://peculiar-inventory-na.aka.corp.amazon.com/HDC3/report/Inbound?timeWindow=MoreThanFiveDay&containerType=DROP_ZONE_PRIME&containerLevel=PARENT_CONTAINER', f'/html/body/div[1]/div[3]/div/div[1]/div/div[1]/table/tbody/tr[{tr}]/td[3]/a')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.peculiar_inventory.table_body)))
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]')))
        # self.move_container(container, 'TRASH')
        asin = self.get_text(f'https://fcresearch-na.aka.amazon.com/HDC3/results?s={container}','/html/body/div[2]/div/div[1]/div/div[6]/div/div[2]/div/div/div[1]/div[2]/table/tbody/tr/td[2]/a')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.body)))
        if "B00" in asin or 'X00' in asin:
            return container

    def deleteItem(self, container, container_count: int):
        def start_over() -> None:
            try:
                restart = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.restart)))
                restart.click()
                #start over element
                # wait for popup content
                time.sleep(.5)
                element = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.btn_restart)))
                coord = element.location_once_scrolled_into_view
                self.actions.move_by_offset(coord['x'], coord['y']).click().perform()
                # scan container header
                time.sleep(.5)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.H1_header)))
                element = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.btn_restart)))
                coord = element.location_once_scrolled_into_view
                self.actions.move_by_offset(coord['x'], coord['y']).click().perform()
                _ = 0
            except TimeoutException:
                pass
        
        def enter_container() -> None:
            self.navigate(self.driver, 'https://aft-qt-na.aka.amazon.com/app/deleteitems?experience=Desktop', 5)
            input_container = self.driver.find_element(By.XPATH, locator.xpath.delete.scan.input_container)
            input_container.click()

            input_container.send_keys(f'{container}')
            container_enter = self.driver.find_element(By.XPATH, locator.xpath.delete.scan.enter)
            container_enter.submit()

        def select_item() -> bool:
            #"select item to delete"
            H1_header =  WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.H1_header))).text
            if header.REASON[0] in H1_header or header.REASON[1] in H1_header:
                continue_enter = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.select.enter))) # continue [enter]
                continue_enter.submit()
                time.sleep(1)
                return True
            # container empty message
            else:
                cnt_empty_message = WebDriverWait(self.driver, .5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.select.container_empty)))
                if f"Container {container} is empty." in cnt_empty_message.text:
                    return False
                   
        def select_reason() -> None:
            reason_continue_enter = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.reason.enter)))
            reason_continue_enter.submit()

        def confirm_deletion() -> None:
            #wait for  "confirm the deletion H1"
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.H1_header)))
            confirm_delete_enter = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.confirm.enter)))
            confirm_delete_enter.send_keys(Keys.ENTER)

        def get_header_text() -> str:
            return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.H1_header))).text

        for _ in range(1):
            current_state = header.SCAN
            start_over() if get_header_text() != header.SCAN else None
            while current_state != 'end':
                if current_state == header.SCAN:
                    try:
                        enter_container()
                        current_state = get_header_text()
                        
                    except NoSuchElementException:
                        start_over()

                    except StaleElementReferenceException:
                        retries = 3
                        for _ in range(retries):
                            try:
                                confirm_enter = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, locator.class_name.delete.enter)))
                                confirm_enter.click()

                                #wait for "Scan container" H1
                                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.H1_header)))
                                break
                            except StaleElementReferenceException:
                                continue
                        else:
                            print("All attempts failed.")
                            start_over()
                    
                    except TimeoutException:
                        start_over()

                    except ElementClickInterceptedException:
                        start_over()

                elif current_state == header.SELECT:
                    if not select_item():
                        current_state = 'end'
                    else:
                        current_state = get_header_text()

                elif current_state in header.REASON:
                    select_reason()
                    current_state = get_header_text()

                elif current_state == header.CONFIRM:
                    confirm_deletion()
                    print(f"{container} DELETED\n{'-' * 47}")
                    current_state = 'end'            
            
    def move_container(self, container: str, destination: str) -> None:
        move_URL = 'https://aft-moveapp-iad-iad.iad.proxy.amazon.com/move-container?jobId=200'
        # self.FCMenu_login(self.driver, 12730876)
        self.navigate(self.driver, move_URL, 5)
        if self.driver.current_url != move_URL:
            # Lands at FC Menu - does not navigate - reason unknown
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.inbound))).click() # inbound
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container_145))).click() # move container (145)
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.individually_workflow))).click() # move container individually
        ready_to_move = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container.input)))
        if ready_to_move:
                input_box = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.move_container.input_box)
                self.driver.send_keys()
                self.driver.execute_script("arguments[0].setAttribute('style', 'display: block;')", input_box)
                # ready_to_move.send_keys('t')
                # textbox = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[7]/div/input'))) # scan container
                textbox = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.move_container.input)
                self.driver.execute_script(f"arguments[0].value = '{container}';", textbox)
                textbox.send_keys(Keys.ENTER)
                textbox.send_keys(Keys.ENTER)
                ready_to_send = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container.label_scan_destination))) # Scan destination container
                ready_to_send.send_keys('t')

                ready_to_send.send_keys(destination)
                ready_to_send.send_keys(Keys.ENTER)
    
    def screenshot(self, site, xpath):
        self.driver.maximize_window()
        self.navigate(site)
        try:
            self.actions.move_to_element(self.driver.find_element('xpath', xpath)).perform()
            image_binary  = self.driver.find_element('xpath', xpath).screenshot_as_png
            img = Image.open(io.BytesIO(image_binary))
            t = time.time()
            img.save(f"image-{t}.png")
        except NoSuchElementException as e:
            logging.error(f"Element not found for site '{site}' with XPath '{xpath}': {e}")
