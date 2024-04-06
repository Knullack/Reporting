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
from datetime import datetime
from datetime import datetime, timedelta
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, StaleElementReferenceException,  ElementClickInterceptedException, UnexpectedAlertPresentException, NoAlertPresentException
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
        class sideline_app:
            input = '/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div[1]/div/div/div[1]/input'
            change_container = '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div/div/div[3]/button/div/span'
            confirmation_yes = '/html/body/div[4]/div/div/div/div[3]/div/div[4]/button/div/span'
            source_container = '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div/div/div[2]/span'
            confirmed = '/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/div[2]/div/div/span'
            confirmation_div_overlay = '/html/body/div[4]/div/div/div'
            main_panel = '/html/body/div[1]/div/div/div[2]/div/div[1]'
        class counts:
            time_span = '/html/body/div[2]/nav/div[2]/ul[2]/li[3]/a'
            iframe = '/html/body/div/iframe'
            absolute = '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[1]/ul/li[3]/a'
            time_from = '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[2]/div/div/form/div[1]/div[1]/input'
            time_to = '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[2]/div/div/form/div[2]/div[1]/input'
            go = '/html/body/div[2]/config/div/div[1]/kbn-timepicker/div/div/div[1]/div/div[2]/div/div/form/div[3]/div/button'
            okay = '/html/body/div[4]/div/div/div[2]/button[2]'

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
                reason_statement  = '/html/body/div[1]/div[4]/div/div[1]/div/dl[3]/dd'
                sweeping_out = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/div[1]/fieldset/div[1]/div/div/label/span'
                enter = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/span[1]/span/input'
            class confirm:
                enter = '/html/body/div[1]/div[4]/div/div[2]/div[1]/form/span[1]/span/span/input'

        class fcmenu:
            input_badge = '//*[@id="badgeBarcodeId"]'
            inbound = '/html/body/div[3]/div/div[2]/ul[1]/li[1]/a'
            outbound = '/html/body/div[3]/div/div[2]/ul[1]/li[2]/a'
            picking = '/html/body/div[3]/div/div[2]/ul[1]/li[1]/a'
            move_container_145 = '/html/body/div[3]/div/div[2]/ul[2]/li[3]/a'
            individually_workflow = '/html/body/div/div/div/ul/li[2]'
            problem_solve = '/html/body/div[3]/div/div[2]/ul[2]/li[5]/a'
            sideline_app = '/html/body/div[3]/div/div[2]/ul[1]/li[1]/a'

            class move_container:
                input = '/html/body/div/div[7]/div/input'
                error_msg = '/html/body/div/div[4]/div[2]/div[1]'
            class peculiar_inventory:
                table_body = '/html/body/div[1]/div[3]/div/div[1]/div/div[1]/table/tbody'

            class fcresearch:
                asin = '/html/body/div[2]/div/div[1]/div/div[6]/div/div[2]/div/div/div[1]/div[2]/table/tbody/tr/td[2]/a'

            class pick:
                no_batch = '/html/body/div[1]/div[5]/ul/li[2]/a'
                input = '/html/body/div[1]/div[5]/form/input[6]'
                commit = '/html/body/div[1]/div[5]/form/input[7]'
                class vehicle:
                    input = '/html/body/div[1]/div[5]/form/input[6]'
                    title = '/html/body/div[1]/div[5]/p[1]/b'
                
                class cage:
                    title = '/html/body/div[1]/div[5]/div[1]'
                
                class scan_bin:
                    case = '/html/body/div[1]/div[5]/div[3]/div[1]/span[2]'
                    input = '/html/body/div[1]/div[5]/form[1]/input[9]'
                    commit = '/html/body/div[1]/div[5]/form[1]/input[10]'
                    P1 = '/html/body/div[1]/div[5]/div[1]/div[2]/div/span[1]'
                    P2 = '/html/body/div[1]/div[5]/div[1]/div[2]/div/span[2]'
                    P3 = '/html/body/div[1]/div[5]/div[1]/div[2]/div/span[3]'
                
                class scan_case:
                    input = '/html/body/div[1]/div[5]/form/input[10]'
                    commit = '/html/body/div[1]/div[5]/form/input[11]'

                    

        class picking_console:
            error_msg = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[1]/div/span/awsui-flashbar/div/awsui-flash/div/div[2]/div/div/span/span/span'
            table = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[3]/div/div/awsui-table/div/div[3]'

        class fc_andons:
            error_msg = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-flash/div/div[2]/div/div'

    class class_name:
        class delete:
            enter = 'a-button-input'

        class counts:
            spinner = 'spinner.large'

        class sideline_app:
            step = 'text text--bold'
            trans_out = 'text text--size-xl text--variant-white'

class header:  
    SCAN = 'Scan container'
    SELECT = 'Select item to delete'
    REASON = ['Select reason to delete','Select deletion reason']
    CONFIRM = 'Confirm the deletion'

class chromeSession():
    def __init__(self, badge: int):
        """Badge for FC Menu login"""
        self.step = int
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

    def FCMenu_login(self, badge: str) -> None:
        """Logs into FCMenu with given BADGE"""
        self.navigate(LOGIN_URL)
        loginBadge = badge
        input_element = self.driver.find_element('xpath', locator.xpath.fcmenu.input_badge)
        self.HELPER_type_and_click(input_element, loginBadge)

    def HELPER_type_and_click(self, element: object, text_to_type: str) -> None:
        element.send_keys(text_to_type)
        element.send_keys(Keys.ENTER)

    def navigate(self, url: str, max_attempts: int = 5) -> None:
        """Navigate to give URL"""
        exception_count = 0
        while exception_count < max_attempts:
            try:
                self.driver.get(url)
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
        self.FCMenu_login(self.badge)

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
                    self.navigate(site)
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
        self.navigate(url)

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
        def close_chrome_processes():
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

        """Quit the Chrome driver & terminate processes"""
        if self.driver:
            self.driver.quit()
            close_chrome_processes()
        else:
            return logging.INFO('No session active')

    def SBC_accuracy(self, site: str, download_anchor_xPath: str, download_dir: str) -> float:
        """Gets and calculates % average"""
        def calculate_average(csv_file: str, column_index: int, start_row: int) -> float:
            """Calculates average % from file"""
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header row
                for _ in range(start_row - 1):
                    next(reader, None)  # Skip rows until reaching the start_row
                data = [row[column_index] for row in reader]  # Extract data from the specified column
                numeric_data = [float(value) for value in data if value]  # Convert data to float, ignoring empty values
                average = sum(numeric_data) / len(numeric_data) if numeric_data else 0  # Calculate average
            return f"{str(round(average, 2))}%"

        # navigation
        self.navigate(site)
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
            WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located((By.CLASS_NAME, locator.class_name.counts.spinner))) # website loading effect element
            csv_files = []
            csv_files.extend(glob.glob(os.path.join(download_dir, f"table_*.csv")))
            if not csv_files:
                print("No CSV files found in the download directory.")
                return None

            latest_file = max(csv_files, key=os.path.getmtime)
            print(f'Accuracy File: {str(latest_file).split(r"\\")[-1]}')
            # Use Pandas to open and read the CSV file
            if os.path.exists(latest_file):
                return calculate_average(latest_file, 5, 1)
            else:
                print("CSV file not found in the download directory.")


        except TimeoutException:
            return "SBC_Accuracy: Element not found"

    def CC_Completion(self, site: str, download_anchor_xPath: str, download_dir: str) -> tuple:
        """Gets and calculates work_type sum"""
        def calculate_counts(csv_file: str) -> tuple:
            """Counts sum each work_type column from given file"""
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

        attempt = 0
        while attempt < 2:
            ERR_OOPS = False
            self.driver.execute_script('location.reload();') if attempt == 1 else self.navigate(site)
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
                    WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, locator.class_name.counts.spinner)))
                    WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, locator.class_name.counts.spinner)))
                except TimeoutException:
                    attempt += 1
                try:
                    csv = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, download_anchor_xPath)))
                    csv.click()

                    btn_ok = self.driver.find_element(By.XPATH, locator.xpath.counts.okay)
                    btn_ok.click()
                    start_time = time.time()
                    # can take quite a few seconds to download file (60s max)
                    WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located((By.CLASS_NAME, locator.class_name.counts.spinner)))
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
                        return calculate_counts(latest_file)

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
        """Returns int to subtract by to get current date's Sunday datetime"""
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

    def deleteItem(self, container: str):
        """Uses DeleteItemsApp to 'delete' the container"""
        self.navigate('https://aft-qt-na.aka.amazon.com/app/deleteitems?experience=Desktop')if self.driver.current_url != 'https://aft-qt-na.aka.amazon.com/app/deleteitems?experience=Desktop' else None
        def get_container(tr):
            """Gets the container from the peculiar inventory site"""
            cnt = self.get_text('https://peculiar-inventory-na.aka.corp.amazon.com/HDC3/report/Inbound?timeWindow=MoreThanFiveDay&containerType=DROP_ZONE_PRIME&containerLevel=PARENT_CONTAINER', f'/html/body/div[1]/div[3]/div/div[1]/div/div[1]/table/tbody/tr[{tr}]/td[3]/a')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.peculiar_inventory.table_body)))
            # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]')))
            # self.move_container(container, 'TRASH')
            asin = self.get_text(f'https://fcresearch-na.aka.amazon.com/HDC3/results?s={cnt}', locator.xpath.fcmenu.fcresearch.asin)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.body)))
            if "B00" in asin or 'X00' in asin:
                return cnt
    
        def start_over() -> None:
            """Perform the 'start over' action in the 'Menu (m)' selection of the site"""
            head = get_header_text()
            try:
                if head != header.SCAN:
                    restart = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.restart)))
                    restart.click()
                    #start over element
                    # wait for popup content
                    time.sleep(.5)
                    element = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.btn_restart)))
                    coord = element.location_once_scrolled_into_view
                    self.actions.move_by_offset(coord['x'], coord['y']).click().perform()
                    # scan container header
                    _ = 0
                else:
                    pass
            except TimeoutException:
                pass

        def enter_container(cont) -> None:
            """Types in the given container in the input field"""
            self.navigate('https://aft-qt-na.aka.amazon.com/app/deleteitems?experience=Desktop')
            input_container = self.driver.find_element(By.XPATH, locator.xpath.delete.scan.input)
            input_container.click()

            input_container.send_keys(f'{cont}')
            container_enter = self.driver.find_element(By.XPATH, locator.xpath.delete.scan.enter)
            container_enter.submit()
            

        def select_item() -> bool:
            """Determines whether the given container entered has inventory (passes to the next step)-> True or doesn't and site returns an message -> False"""
            #"select item to delete"
            time.sleep(1.5)
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
                    print(f'{container}: {cnt_empty_message.text}')
                    return False
                
        def select_reason() -> None:
            """Reason already selected, function simulates form submit"""
            # wait for selection to be present
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.reason.sweeping_out)))
            reason_continue_enter = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.reason.enter)))
            reason_continue_enter.submit()

        def confirm_deletion() -> None:
            """Peforms final step in deletion process"""
            #wait for  "confirm the deletion H1"
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.reason.reason_statement)))
            confirm_delete_enter = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.confirm.enter)))
            confirm_delete_enter.send_keys(Keys.ENTER)
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, locator.xpath.delete.H1_header), header.SCAN))

        def get_header_text() -> str:
            """Gets the text of the header element to derive what step of the process the app is on"""
            return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.H1_header))).text

        for _ in range(1):
            current_state = ''
            time.sleep(.5)
            start_over() if get_header_text() != header.SCAN else None
            while current_state != 'end':
                current_state = get_header_text()
                if current_state == header.SCAN:
                    try:
                        enter_container(container)
                        if not select_item():
                            current_state = 'end'
                        else:
                            continue


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
                        continue

                elif current_state in header.REASON:
                    select_reason()

                elif current_state == header.CONFIRM:
                    confirm_deletion()
                    print(f"{container} DELETED\n{'-' * 47}")
                    current_state = 'end'


    def sideline_delete(self, container):
        STEP = str
        url_sideline = 'https://aft-poirot-website-iad.iad.proxy.amazon.com/'
        self.navigate(url_sideline) if self.driver.current_url != url_sideline else None
        if self.driver.current_url != url_sideline:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.problem_solve))).click()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.sideline_app))).click()

        def get_step():
            text =  WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.sideline_app.source_container))).text
            if text == "":
                return 'scan container'
            elif text == container:
                text = 'item'
            return text
        
        def start_over():
            self.driver.refresh()

        def enter_container(csX):
            if self.step == 0:
                input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.sideline_app.input)))
                input.send_keys(csX)
                input.send_keys(Keys.ENTER)
                main_panel = self.driver.find_element(By.XPATH, locator.xpath.sideline_app.main_panel)
                time.sleep(.2)
                if 'cannot be used because it contains an item bound to Transshipment' in main_panel.text:
                    self.step = -1
                else:
                    self.step = 1
                
            else: pass
        def change_container():
            if self.step == 1:
                button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.sideline_app.change_container)))
                button.click()
                self.step = 2
            else: pass
        def confirm():
            if self.step == 3:
                try:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.sideline_app.confirmation_yes))).click()
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.sideline_app.confirmed)))
                    return 'end'
                except TimeoutException:
                    self.step = 2
            else: pass
        STEP = str
        start_over()
        self.step = 0
        while STEP != 'end':
            time.sleep(.1)
            if self.step == -1:
                break
            try:
                if self.step == 2:
                    pass
                else:
                    STEP = get_step()
                if STEP == 'scan container':
                    enter_container(container)
                    time.sleep(.2)
                elif STEP == 'item' or self.step == 2:
                    change_container()
                    time.sleep(.2)
                    self.step = 3
                    if self.step == 3:
                        overlay = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.sideline_app.confirmation_div_overlay)))
                        if overlay:
                            STEP = confirm()
                        else: self.step = 2
                    else: self.step = 2
            except TimeoutException:
                start_over()
                self.step = 0

    def pickUI(self, vehicle: str, cage: str) -> str:
        vehicle_dropoff = 'dz-F-OB-10'
        self.FCMenu_login(self.badge) if self.driver.current_url == 'http://pickui-hdc3.aka.amazon.com/pick/pick' else None
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.outbound))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.picking))).click()
        
        def scan(input, container):
            self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", input, container)

        def select_no_batch():
            time.sleep(1)
            no_batch = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pick.no_batch)))
            no_batch.click()

        def scan_vehicle(ve):
            time.sleep(1.5)
            # wait for "Scan Your Vehicle"
            WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, locator.xpath.fcmenu.pick.vehicle.title),'Scan Your Vehicle'))
            input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pick.input)))
            scan(input, ve)
            # commit input
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pick.commit))).submit()

        def check_vehicle() -> str:
            try:
                error_div = WebDriverWait(self.driver, .8).until(EC.presence_of_element_located((By.ID, "error")))
                if 'dirty' in error_div.text:
                    return 'dirty'
                elif error_div.text == 'No more work: Unable to get job for picker':
                    return 'no work'
                elif error_div.text == '':
                    return 'clean'
            except TimeoutException:
                return 'clean'

        def scan_cage(paX):
            time.sleep(1)
            # wait for "Scan New Cage"
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, locator.xpath.fcmenu.pick.cage.title),'Scan New Cage'))
            input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pick.input)))
            scan(input, paX)
            # commit input
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pick.commit))).submit()

        def new_tab():
            self.driver.execute_script("window.open('about:blank', '_blank');")
            time.sleep(.5)
            self.driver.switch_to.window(self.driver.window_handles[-1])

        def close_tab(tab: int):
            switch_to_tab
            self.driver.close()
        
        def switch_to_tab(tab: int):
            self.driver.switch_to.window(self.driver.window_handles[tab])
        
        def check_if_pallet():
            P2 = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pick.scan_bin.P2).text
            time.sleep(1)
            while 'P' in P2:
                if 'P' in P2:
                    body = self.driver.find_element(By.XPATH, locator.body)
                    body.send_keys('m')
                    time.sleep(3)
                    body.send_keys('s')
                    body.send_keys('s')
                    time.sleep(1)
                    body.send_keys(Keys.ENTER)
                P2 = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pick.scan_bin.P2)))


        status = bool | str
        select_no_batch()
        scan_vehicle(vehicle)
        status = check_vehicle()
        if status == 'no work':
            # self.move_container()
            print("No work")
            sys.exit(0)
        elif status == 'clean':
            pass
        elif status == 'dirty':
            new_tab()
            self.move_container(300, vehicle, vehicle_dropoff)
            close_tab()

            # Switch back to the main tab
            self.driver.switch_to.window(self.driver.window_handles[0])                
            status = 'clean'
        
        if status == 'clean':
            if len(self.driver.window_handles) != 3:
                new_tab()
                new_tab()
            else: pass
            switch_to_tab(0)
            scan_cage(cage)
            check_if_pallet()
            case = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pick.scan_bin.case))).text
            switch_to_tab(1)
            self.deleteItem(case)
            switch_to_tab(2)
            self.move_container(200, case, 'TRASH')
            switch_to_tab(0)
            P1 = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pick.scan_bin.P1).text
            P2 = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pick.scan_bin.P2).text
            P3 = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pick.scan_bin.P3).text
            
            bin = P1 + '-' + P2 + P3

            scan(self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pick.scan_bin.input), bin)
            self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pick.scan_bin.commit).submit()
            
            scan(self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pick.scan_case.input), case)
            self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pick.scan_case.commit).submit()
            return case
            # print(f'{datetime.now()} // {case} // Deleted')
            

        

    def move_container(self, workflow: int, container: str, destination: str) -> None:
        """Moves container with Move Container App"""
        move_fails = ['Move was unsuccessful']
        move_URL = f'https://aft-moveapp-iad-iad.iad.proxy.amazon.com/move-container?jobId={workflow}'
        self.navigate(move_URL)
        if self.driver.current_url != move_URL:
            # Lands at FC Menu - does not navigate - reason unknown
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.inbound))).click() # inbound
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container_145))).click() # move container (145)
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.individually_workflow))).click() # move container individually
        ready_to_move = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container.input)))

        def enter_container(container_):
            
            try:
                time.sleep(1)
                body = self.driver.find_element(By.XPATH, locator.body)
            except UnexpectedAlertPresentException:
                try:
                    alert = self.driver.switch_to.alert
                    alert.accept()
                except NoAlertPresentException:
                    self.driver.refresh()
                    try:
                        body = self.driver.find_element(By.XPATH, locator.body)
                    except UnexpectedAlertPresentException:
                        try:
                            alert = self.driver.switch_to.alert
                            alert.accept()
                        except NoAlertPresentException:
                            pass
            self.driver.find_element(By.XPATH, locator.body).send_keys('t')
            input = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.move_container.input)
            input.clear()
            input.click()
            input.send_keys(container_)
            input.send_keys(Keys.ENTER)

        if ready_to_move:
            if workflow == 200:
                self.navigate(move_URL)
                enter_container(container)
                time.sleep(1.2)
                enter_container(destination)
                msg = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.move_container.error_msg).text
                if msg in move_fails:
                    for i in range(2):
                        input = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.move_container.input)
                        input.send_keys(Keys.ENTER)
                        print(f'{container} TRASHED\n')
                    time.sleep(2)
            elif workflow == 300:
                enter_container(container)
                for i in range(2):
                    time.sleep(.5)
                    enter_container(destination)
                time.sleep(1.5)
        time.sleep(2)
    def screenshot(self, site, xpath):
        """Screenshot given element at given site"""
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
