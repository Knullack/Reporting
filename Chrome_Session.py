try:
    import pyautogui as pyg
    import win32clipboard as wc
    import win32con
    import keyboard
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
    from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, StaleElementReferenceException,  ElementClickInterceptedException, UnexpectedAlertPresentException, NoAlertPresentException, NoSuchWindowException, ElementNotInteractableException, MoveTargetOutOfBoundsException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver import Chrome
    from selenium.webdriver.remote.webelement import WebElement
    from typing import Literal, Union
    from util.utilities import locator, header, constants, Container
except ImportError as e:
    missing_module = str(e).split("'")[1]
    print(f"Module '{missing_module}' is not installed. Installing...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', missing_module])
    print(f"Module '{missing_module}' has been installed. Please restart the script.")
    sys.exit(1)
logging.basicConfig(level=logging.ERROR)

LOGIN_URL = constants.LOGIN_URL
CHROME_PATH = constants.CHROME_PATH
ARGUMENTS = constants.ARGUMENTS

class chromeSession():
    def __init__(self, site: str, badge: int):
        """Sideline Shorting, DeleteItems App, PickUI and other ICQA related data scrapping. Use close() method to end chrome process"""
        self.step = int
        self.driver = None
        self.badge = str(badge)
        self.site = str(site).upper()
        self.file_prefixes = ["Pick All types", "Bin Item Defects All types"]
        self.start()

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
        self.actions = ActionChains(self.driver)
        self.FCMenu_login(self.badge)

    def FCMenu_login(self, badge: str) -> None:
        self.navigate(LOGIN_URL)
        loginBadge = badge
        input_element = self.driver.find_element('xpath', locator.xpath.fcmenu.input_badge)
        self.HELPER_type_and_click(input_element, loginBadge)

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

    def deleteItem(self, container: str, mode: Literal['container', 'single'], *arg, **title):
        """Uses DeleteItemsApp to 'delete' the container"""
        FcSKU_count = 0
        mode = mode.lower()
        self.navigate('https://aft-qt-na.aka.amazon.com/app/deleteitems?experience=Desktop')if self.driver.current_url != 'https://aft-qt-na.aka.amazon.com/app/deleteitems?experience=Desktop' else None
        def get_container(tr):
            """Gets the container from the peculiar inventory site"""
            cnt = self.get_text(f'https://peculiar-inventory-na.aka.corp.amazon.com/{self.site}/report/Inbound?timeWindow=MoreThanFiveDay&containerType=DROP_ZONE_PRIME&containerLevel=PARENT_CONTAINER', f'/html/body/div[1]/div[3]/div/div[1]/div/div[1]/table/tbody/tr[{tr}]/td[3]/a')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.peculiar_inventory.table_body)))
            # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]')))
            # self.move_container(container, 'TRASH')
            asin = self.get_text(f'https://fcresearch-na.aka.amazon.com/{self.site}/results?s={cnt}', locator.xpath.fcmenu.fcresearch.asin)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.body)))
            if "B00" in asin or 'X00' in asin:
                return cnt

        def wait_for_processing():
            try:
                WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element_attribute((By.XPATH, locator.xpath.delete.processing_element), 'class', locator.class_name.itemApps.processing_visible))
                WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element_attribute((By.XPATH, locator.xpath.delete.processing_element), 'class', locator.class_name.itemApps.processing_hidden))
            except TimeoutException:
                pass

        # def userMenu_is_displayed(expected_attribute: bool) -> bool:
        #     if expected_attribute:
        #         expected_attribute = 'true'
        #         return WebDriverWait(self.driver, 2).until(EC.text_to_be_present_in_element_attribute((By.ID, locator.ID.delete.user_menu), 'aria-hidden', expected_attribute))
        #     if not expected_attribute:
        #         expected_attribute = 'false'
        #         if WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.scan.enter))):
        #             return True


        def set_mode(mode):
            current_mode = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.modes.current_mode))).text.lower()
            
            def click_menu():
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.menu))).click()

            def click_change_mode():
                # if userMenu_is_displayed(True):
                time.sleep(1)
                change_mode = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.btn_change_mode)))
                coord = change_mode.location_once_scrolled_into_view
                self.actions.move_by_offset(coord['x'], coord['y']).click().perform()
            
            def click_mode(mode_):
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.modes.select_modes_banner)))
                if mode_ == 'single':
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.modes.single))).click()
                elif mode_ == 'container':
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.modes.container))).click()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.modes.continue_enter))).click()
            
            if current_mode == mode:
                pass
            else:
                click_menu()
                click_change_mode()
                click_mode(mode)

        def start_over() -> None:
            """Perform the 'start over' action in the 'Menu (m)' selection of the site"""
            head = get_header_text()
            try:
                if head not in header.SCAN[0]:
                    menu = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.menu)))
                    menu.click()
                    # if userMenu_is_displayed(True):
                    time.sleep(1)
                    try:
                        restart = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.btn_restart)))
                        coord = restart.location_once_scrolled_into_view
                        self.actions.move_by_offset(coord['x'], coord['y']).click().perform()
                    except MoveTargetOutOfBoundsException:
                        self.driver.find_element(By.XPATH, locator.body).send_keys('r')
                    wait_for_processing()
                    WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element((By.XPATH, locator.xpath.delete.H1_header), header.SCAN[0]))
                else:
                    pass
            except TimeoutException:
                pass

        def enter_container(cont) -> None:
            """Types in the given container in the input field"""
            input_container = self.driver.find_element(By.XPATH, locator.xpath.delete.scan.input)
            input_container.click()
            input_container.clear()
            input_container.send_keys(cont)
            container_enter = self.driver.find_element(By.XPATH, locator.xpath.delete.scan.enter)
            container_enter.submit()
            wait_for_processing()
            
        def enter_item(item) -> bool:
            input_item = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.scan.scan_item)))
            input_item.clear()
            input_item.send_keys(item)
            self.driver.find_element(By.XPATH, locator.xpath.delete.scan.enter).click()
            wait_for_processing()
            try: # container empty message
                cnt_empty_message = WebDriverWait(self.driver, 1, poll_frequency=.1).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.select.container_empty)))
                if "not in the container." in cnt_empty_message.text:
                    print(f'{container}: {cnt_empty_message.text}')
                    return False
                else:
                    if get_header_text in header.REASON:
                        print(f"Item: {arg[0]}\nFcSKUs: {FcSKU_count-1} | {datetime.now().time()}") 
                    return True
            except TimeoutException:
                if get_header_text in header.REASON:
                    print(f"Item: {arg[0]}\nFcSKUs: {FcSKU_count-1} | {datetime.now().time()}") 
                return True

        def select_item() -> bool:
            """Determines whether the given container entered has inventory (passes to the next step)-> True or doesn't and site returns an message -> False"""
            H1_header =  get_header_text()
            if header.REASON[0] in H1_header or header.REASON[1] in H1_header:
                continue_enter = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.select.enter))) # continue [enter]
                continue_enter.submit()
                wait_for_processing()
                return True
            elif H1_header == header.SCAN[1]:
                return enter_item(arg[0])
            elif H1_header in header.SELECT[0]:
                if title:
                    name = title['title']
                    fieldset = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.select.fieldset)))
                    boxes = fieldset.find_elements(By.XPATH, "./div")
                    nonlocal FcSKU_count
                    FcSKU_count = len(boxes)
                    print(f"Item: {arg[0]}\nFcSKUs: {FcSKU_count} | {datetime.now().time()}")
                    try:
                        if FcSKU_count >= 1:
                            for i, box in enumerate(boxes):
                                lines = box.text.splitlines()
                                for line in lines:
                                    if line == name:
                                        try:
                                            boxes[i].click()
                                        except StaleElementReferenceException:
                                            retries = 3
                                            for _ in range(retries):
                                                try:
                                                    confirm_enter = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, locator.class_name.delete.enter)))
                                                    confirm_enter.click()
                                                    wait_for_processing()
                                                    continue
                                                except StaleElementReferenceException:
                                                    continue
                                        try:
                                            self.driver.find_element(By.CLASS_NAME, locator.class_name.delete.select.continue_enter).click()
                                            wait_for_processing()
                                        except StaleElementReferenceException:
                                            self.driver.refresh()
                                            self.driver.find_element(By.CLASS_NAME, locator.class_name.delete.select.continue_enter).click()
                                            wait_for_processing()
                                            
                                        return True
                        else: # FcSKU_count < 0
                            self.driver.find_element(By.CLASS_NAME, locator.class_name.delete.select.continue_enter).click()
                            wait_for_processing()
                            return True
                    except StaleElementReferenceException:
                        self.driver.refresh()
                        self.driver.find_element(By.CLASS_NAME, locator.class_name.delete.select.continue_enter).click()
                        wait_for_processing()
                else: # no title
                    self.driver.find_element(By.CLASS_NAME, locator.class_name.delete.select.continue_enter).click()
                    wait_for_processing()
                    return True
            else: # container empty message
                cnt_empty_message = WebDriverWait(self.driver, .5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.select.container_empty)))
                if f"Container {container} is empty." in cnt_empty_message.text:
                    print(f'{container}: {cnt_empty_message.text}')
                    return False
                
        def select_reason() -> None:
            """Reason already selected, function simulates form submit"""
            # wait for selection to be present
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.reason.sweeping_out)))
            reason_continue_enter = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.reason.enter)))
            reason_continue_enter.submit()
            wait_for_processing()

        def confirm_deletion() -> None:
            """Peforms final step in deletion process"""
            #wait for  "confirm the deletion H1"
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.reason.reason_statement)))
            confirm_delete_enter = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.confirm.enter)))
            confirm_delete_enter.send_keys(Keys.ENTER)
            wait_for_processing()
            if get_header_text() == header.SELECT[0]:
                pass
            else:
                head = get_header_text()
                if head == header.SCAN[1]:
                    start_over()
                elif head == header.SCAN[0]:
                    return

        def get_header_text() -> str:
            """Gets the text of the header element to derive what step of the process the app is on"""
            try:
                return WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.H1_header))).text
            except Exception:
                self.driver.refresh()
                return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.H1_header))).text
            

        set_mode(mode)
        for _ in range(1):
            current_state = ''
            start_over() if get_header_text() != header.SCAN[0] else None
            while current_state != 'end':
                current_state = get_header_text()
                if current_state == header.SCAN[0]:
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
                elif current_state == header.SCAN[1]:
                    if not select_item():
                            current_state = 'end'
                    else:
                        continue
                elif current_state in header.SELECT:
                    if not select_item():
                        current_state = 'end'
                    else:
                        continue

                elif current_state in header.REASON:
                    try:
                        select_reason()
                    except Exception:
                        continue

                elif current_state == header.CONFIRM:
                    try:
                        confirm_deletion()
                        if FcSKU_count > 1:
                            current_state = header.SCAN[1]
                            continue
                        if arg:
                            print(f'{arg[0]} in {container} DELETED')
                        else:
                            print(f"{container} DELETED\n{'-' * 47}")
                        start_over()
                        current_state = 'end'
                    except Exception:
                        continue

    def move_items(self, mode: Literal['each', 'multi','container'], container: str, item: str, destination: str) -> None:
        mode = mode.lower()
        self.navigate('https://aft-qt-na.aka.amazon.com/app/moveitems?experience=Desktop')if self.driver.current_url != 'https://aft-qt-na.aka.amazon.com/app/deleteitems?experience=Desktop' else None

        def start_over() -> None:
            """Perform the 'start over' action in the 'Menu (m)' selection of the site"""
            head = get_header_text()
            try:
                if head != header.SCAN[0]:
                    menu = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.menu)))
                    menu.click()
                    #start over element
                    # wait for popup content
                    time.sleep(.5)
                    try:
                        restart = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.btn_restart)))
                        coord = restart.location_once_scrolled_into_view
                        self.actions.move_by_offset(coord['x'], coord['y']).click().perform()
                    except MoveTargetOutOfBoundsException:
                        self.driver.find_element(By.XPATH, locator.body).send_keys('r')
                    WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element((By.XPATH, locator.xpath.delete.H1_header), header.SCAN[0]))
                    # scan container header
                    _ = 0
                else:
                    pass
            except TimeoutException:
                pass
        def get_header_text() -> str:
            """Gets the text of the header element to derive what step of the process the app is on"""
            try:
                return WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.H1_header))).text
            except Exception:
                self.driver.refresh()
                return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.H1_header))).text
        def set_mode(mode):
            current_mode = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.modes.current_mode))).text.lower()
            
            def click_menu():
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.menu))).click()

            def click_change_mode():
                time.sleep(1)
                change_mode = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.btn_change_mode)))
                coord = change_mode.location_once_scrolled_into_view
                self.actions.move_by_offset(coord['x'], coord['y']).click().perform()
            
            def click_mode(mode_):
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.modes.select_modes_banner)))
                if mode_ == 'each':
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.moveItems.modes.each))).click()
                elif mode_ == 'multi':
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator.xpath.moveItems.modes.multi))).click()
                elif mode == 'container':
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.moveItems.modes.container))).click()
                
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.modes.continue_enter))).click()
            
            if current_mode == mode:
                pass
            else:
                click_menu()
                click_change_mode()
                click_mode(mode)

        def enter_container(cont) -> None:
            """Types in the given container in the input field"""
            input_container = self.driver.find_element(By.XPATH, locator.xpath.delete.scan.input)
            input_container.click()

            input_container.send_keys(f'{cont}')
            container_enter = self.driver.find_element(By.XPATH, locator.xpath.delete.scan.enter)
            container_enter.submit()
        
        def enter_item(item) -> bool | int:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.scan.scan_item))).send_keys(item)
            self.driver.find_element(By.XPATH, locator.xpath.delete.scan.enter).click()
            
            def check_if_multiple_item_selections():
                try:
                    count = 0
                    selection_list = WebDriverWait(self.driver, 1).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/div[2]/fieldset')))
                    for line in selection_list[0].text:
                        if line == "Title":
                            count += 1
                    a = count
                except TimeoutException:
                    try:
                        cnt_empty_message = WebDriverWait(self.driver, .5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.select.container_empty)))
                        if f"Item {item} not in container" in cnt_empty_message.text:
                            print(f'{container}: {cnt_empty_message.text}')
                            return False
                    except TimeoutException:
                        return True

                # if len(boxes) <= 1:
                #     return False
                # elif len(boxes) >= 1:
                #     return len(boxes)


            def check_if_not_in_container():
                head = get_header_text()
                try:
                    if head in header.SCAN:
                        try:
                            cnt_empty_message = WebDriverWait(self.driver, timeout=1, poll_frequency=0.1).until(EC.text_to_be_present_in_element((By.XPATH, locator.xpath.delete.select.container_empty), f"Item {item} not in container"))
                            if cnt_empty_message:
                                return 
                        except TimeoutException:
                            result = check_if_multiple_item_selections()
                            self.driver.find_element(By.XPATH, locator.xpath.delete.scan.enter).click()
                            return result
                    elif head in header.SELECT[2]:
                            result = check_if_multiple_item_selections()
                            self.driver.find_element(By.XPATH, locator.xpath.delete.scan.enter).click()
                            return result


                except TimeoutException:
                    return True
            return check_if_not_in_container()
            # check if item in container
                    

        def num_of_items() -> int:
            fieldset = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, locator.class_name.move_items.fieldset)))
            return len(fieldset)
        def enter_quantity() -> None:
            qty = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div[1]/div/dl[3]/dd[4]'))).text
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/div/input'))).send_keys(qty)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/span/span/input'))).click()
        def enter_destination() -> None:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/div/input'))).send_keys(destination)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/span/span/input'))).click()

        set_mode(mode)
        for _ in range(1):
            current_state = ''
            time.sleep(.8)
            start_over() if get_header_text() not in header.SCAN[0] else None
            while current_state != 'end':
                current_state = get_header_text()
                if current_state == header.SCAN[0]:
                    try:
                        enter_container(container)
                        time.sleep(1)
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

                elif current_state in header.SCAN[1]:
                    result = enter_item(item)
                    if isinstance(result, bool) and not result or result == None:
                        current_state = 'end'
                    elif isinstance(result, int):
                        _ = 0
                        
                
                elif current_state in header.QUANTITY:
                    time.sleep(1)
                    enter_quantity()
                elif current_state in header.DESTINATION_CONTAINER:
                    time.sleep(1)
                    enter_destination()
                    current_state = 'end'

    def rodeo_delete(self, scannable_id: str, FN_SKU: str):
        """Delete items from rodeo"""
        
        def get_title(sku: str) -> str: 
            self.navigate(f'https://fcresearch-na.aka.amazon.com/HDC3/results?s={sku}')
            try:
                table =  WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.fcresearch.table)))
                rows = table.find_elements(By.XPATH, "//tr")

                for row in rows:
                    if "Title" in row.text:
                        return row.text.split("Title ", 1)[1]
            except TimeoutException:
                return ''

        self.deleteItem(scannable_id, 'single', FN_SKU, title=get_title(FN_SKU))

    def sideline_delete(self, container: str, shorted_container_to_dz: str):
        """
        Short containers via SidelineApp
        """
        STEP = str
        url_sideline = 'https://aft-poirot-website-iad.iad.proxy.amazon.com/'
        try:
            self.navigate(url_sideline) if self.driver.current_url != url_sideline else None
        except NoSuchWindowException:
            print(f"Verify Chrome Window is displayed on-screen, it seems it is not\n\nError:\n{e}")
            sys.exit(0)
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
                            # self.move_container(200, container, shorted_container_to_dz)
                        else: self.step = 2
                    else: self.step = 2
            except TimeoutException:
                start_over()
                self.step = 0

    def pickUI(self, vehicle: str, cage: str, dirtyVehicle_dz_location: str, deleted_container_to_dz: str) -> str:
        """
        Simulate picker's picking actions followed by deleting the container and moving container to TRASH
        
        Ensure DeleteItemsApp is set to container mode. Preferably, set picking eligibilities to csX and not including paX containers
        """
        vehicle_dropoff = str(dirtyVehicle_dz_location)
        if self.driver.current_url == f'http://pickui-{self.site.lower()}.aka.amazon.com/pick/pick' or self.driver.current_url != f'http://pickui-{self.site.lower()}.aka.amazon.com/pick/scan_bin':
            if self.driver.current_url != f'https://fcmenu-iad-regionalized.corp.amazon.com/{self.site}':
                self.FCMenu_login(self.badge)
            try:
                outbound = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.outbound)))
                if outbound.is_displayed():
                    outbound.click()
                    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.picking))).click()
                else:
                    raise NoSuchWindowException
            except NoSuchWindowException as e:
                print(f"Verify Chrome Window is displayed on-screen, it seems it is not\n\nError:\n{e}")
                sys.exit(0)
        
        def scan(input, container):
            self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", input, container)

        def select_no_batch():
            time.sleep(1)
            no_batch = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pickUI.no_batch)))
            no_batch.click()

        def scan_vehicle(ve):
            time.sleep(1.5)
            # wait for "Scan Your Vehicle"
            WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, locator.xpath.fcmenu.pickUI.vehicle.title),'Scan Your Vehicle'))
            input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pickUI.input)))
            scan(input, ve)
            # commit input
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pickUI.commit))).submit()

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
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, locator.xpath.fcmenu.pickUI.cage.title),'Scan New Cage'))
            input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pickUI.input)))
            scan(input, paX)
            # commit input
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pickUI.commit))).submit()

        def new_tab():
            self.driver.execute_script("window.open('about:blank', '_blank');")
            time.sleep(.5)
            self.driver.switch_to.window(self.driver.window_handles[-1])

        def close_tab():
            switch_to_tab
            self.driver.close()
        
        def switch_to_tab(tab: int):
            self.driver.switch_to.window(self.driver.window_handles[tab])
        
        def skip_skip():
            body = self.driver.find_element(By.XPATH, locator.body)
            body.send_keys('m')
            time.sleep(1)
            body.send_keys('s')
            time.sleep(1)
            body.send_keys('s')
            time.sleep(1)
            body.send_keys(Keys.ENTER)


        def check_if_pallet():
            P2 = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pickUI.scan_bin.P2).text
            time.sleep(1)
            while 'P' in P2:
                try:
                    spinner = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, locator.ID.pick.spinner)))
                except TimeoutException:
                    spinner = 'invis'
                if spinner == WebElement:
                    invis_spinner = WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.ID, locator.ID.pick.spinner)))
                    invis_spinner = 'invis'
                else:
                    spinner = 'invis'
                if invis_spinner == 'invis':
                    if 'P' in P2:
                        skip_skip()
                    try:
                        P2 = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pickUI.scan_bin.P2))).text
                    except TimeoutException:
                        P2 = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, locator.class_name.pick.bin)))
                        P2 = P2[1].text


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
            case = ''
            while True:
                if 'csX' in case:
                    break
                try:
                    case = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pickUI.scan_bin.case))).text
                    break
                except TimeoutException:
                    skip_skip()
                    case = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.pickUI.scan_bin.case))).text

            switch_to_tab(1)
            self.deleteItem(case)
            switch_to_tab(2)
            self.move_container(200, case, str(deleted_container_to_dz))
            switch_to_tab(0)
            P1 = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pickUI.scan_bin.P1).text
            P2 = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pickUI.scan_bin.P2).text
            P3 = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pickUI.scan_bin.P3).text
            
            bin = P1 + '-' + P2 + P3

            scan(self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pickUI.scan_bin.input), bin)
            self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pickUI.scan_bin.commit).submit()
            
            scan(self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pickUI.scan_case.input), case)
            self.driver.find_element(By.XPATH, locator.xpath.fcmenu.pickUI.scan_case.commit).submit()
            return case
            # print(f'{datetime.now()} // {case} // Deleted')
            
    def PAWS_tradional_picking(self):
        site = 'https://taskui-gateway-iad.corp.amazon.com/?listingID=97fc5f2d-c627-46cb-afa0-7026e28e34fe&hideTasks=1&messaging=1&fans=1&interrupts=true&training=true&logoutWorkflowEnabled=1&skipTaskCenter=1#initialized'
        self.navigate(site)
        try:
            WebDriverWait(self.driver, .5, poll_frequency=0.01).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.PAWS_Traditional_Picking.no_batch))).click()
            print('driver click')
        except TimeoutException:
            self.driver.find_element(By.XPATH, locator.body).click()
            print('exceptioned')
            keyboard.press_and_release('n')
        # step = WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div'), 'Scan vehicle ID'))
        def paste(text):
            wc.OpenClipboard()
            wc.EmptyClipboard()
            wc.SetClipboardText(text, win32con.CF_TEXT)
            wc.CloseClipboard()
            pyg.hotkey('ctrl', 'v')
        
        def complete_setup(vehicle, cage):
            time.sleep(8)
            print("awake")
            paste(vehicle)
            time.sleep(2)
            paste(cage)

        step = True
        if step:   
            complete_setup('veCG00221', 'paX00221')
            head = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/span'))).text
            #n for char in text:
            #     keyboard.press(char)
            #     time.sleep(0.1)  # Adjust the delay as needed
            #     keyboard.release(char)
            a = 0
        
    def move_container(self, workflow: Literal[200, 300], container: str, destination: str) -> None:
        """Moves container with Move Container App"""
        move_fails = ['Move was unsuccessful']
        move_URL = f'https://aft-moveapp-iad-iad.iad.proxy.amazon.com/move-container?jobId={workflow}'
        self.navigate(move_URL) if self.driver.current_url != move_URL else None
        if self.driver.current_url != move_URL:
            # Lands at FC Menu - does not navigate - reason unknown
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.inbound))).click() # inbound
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container_145))).click() # move container (145)
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container.individually_workflow))).click() # move container individually
        try:
            ready_to_move = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container.input)))
        except TimeoutException:
            self.driver.refresh()
            ready_to_move = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container.input)))
        
        def enter_container(container_):
            try:
                # time.sleep(1)
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
            try:
                body.send_keys('t')
            except UnboundLocalError:
                body = self.driver.find_element(By.XPATH, locator.body)
                body.send_keys('t')
            try:
                input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container.input)))
                input.clear()
            except ElementNotInteractableException:
                body.send_keys('t')
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container.input)))
            if input.is_displayed():
                input.send_keys(container_)
                time.sleep(.4)
                input.send_keys(Keys.ENTER)
            else:
                print("Not displayed")

        def validate_container() -> bool:
            time.sleep(.6)
            exception_title: str = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container.error_msg))).text
            if exception_title == "Scan was unsuccessful":
                return False
            else:
                return True
            
        def checkInventory(_container: str):
            value = self.get_container_data(_container, Container.outerlocation, write_to_csv=False)
            if value == "No Inventory":
                return "No Inventory"
            else:
                return value

        if ready_to_move:

            if workflow == 200:
                enter_container(container)
                if validate_container():
                    WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/div/div[3]/div[2]/div[1]/div/div/h3'), 'Scan destination container'))
                    enter_container(destination)
                    msg = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.move_container.error_msg))).text
                    if msg == "":
                        msg = destination
                    print(f'{container} -> "{msg}"')
                    if msg in move_fails:
                        input = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.move_container.input)
                        for i in range(2):
                            time.sleep(1.2)
                            try:
                                input.send_keys(Keys.ENTER)
                            except ElementNotInteractableException:
                                self.driver.find_element(By.XPATH, locator.body).send_keys('t')
                                input.send_keys('t')
                        print(f'{container} moved\n')
                        time.sleep(.5)
                else:
                    print(f'{container} -> Failed Move // No Inventory')
            elif workflow == 300:
                enter_container(container)
                for i in range(2):
                    time.sleep(.5)
                    enter_container(destination)
                time.sleep(1.5)
        time.sleep(1)

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

    def unbindHierarchy(self, container):
        def goto_UI():
            if self.driver.current_url != 'https://tx-b-hierarchy-iad.iad.proxy.amazon.com/unbindHierarchy':
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.outbound))).click()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.unbindHierarchy))).click()
        
        def enter_container(container_):
            try:
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
            try:
                body.send_keys('t')
            except UnboundLocalError:
                body = self.driver.find_element(By.XPATH, locator.body)
                body.send_keys('t')
            try:
                input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.unbind.input)))
                input.clear()
            except ElementNotInteractableException:
                body.send_keys('t')
                input = self.driver.find_element(By.XPATH, locator.xpath.fcmenu.move_container.input)

            if input.is_displayed():
                input.click()
                input.send_keys(container_)
                input.send_keys(Keys.ENTER)
        
        def continueC():
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.unbind.continue_btn))).click()
                # Wait for success output
                WebDriverWait(self.driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, locator.xpath.fcmenu.unbind.success_banner),f'Successfully unbound {container}'))
            except ElementNotInteractableException:
                if WebDriverWait(self.driver, 1).until(EC.text_to_be_present_in_element((By.XPATH, locator.xpath.fcmenu.unbind.error_banner),'Error getting the binding summary. Please scan again')):
                    self.driver.refresh()
                    enter_container(container)
                    continueC()
        goto_UI()
        enter_container(container)
        continueC()

    def get_container_data(self, container, *extract_value: Union[str, Container], **write_to_csv: bool):
        """Gets the consumer label from a given container\n
        if `extract_value` is given, function returns said value, if not... function will write data to csv
        in current directory\n
        *`extract_value` should only be given one string*\n
        Set `write_to_csv` `False` to return the data requested, otherwise, set `True` to write data request to csv file
        """
        container_data_dict = {}
        container_paired_data = {}
        container_history_data_dict = {}
        container_history_paired_data = {}
        csv_file = "consumer_status.csv"
        headers = [Container.inventory.container,
                   Container.inventory.asin,
                   Container.inventory.fnsku,
                   Container.inventory.fcsku,
                   Container.inventory.LPN,
                   Container.inventory.quantity,
                   Container.inventory.disposition,
                   Container.inventory.consumer,
                   Container.inventory.consumerid,
                   Container.inventory.outerlocation,
                   Container.inventory.outerlocationtype,
                   Container.inventory.title,
                   Container.container_history.move_date,
                   Container.container_history.action,
                   Container.container_history.movedBy,
                   Container.container_history.oldContainer,
                   Container.container_history.newContainer,
                   Container.container_history.requestByClient]

        def goto_fcr() -> None:
            FCR = f'https://fcresearch-na.aka.amazon.com/HDC3/results?s={container}'
            self.navigate(FCR)

        def checked_inventory() -> bool:
            time.sleep(1)
            while True:
                inventory_label = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "inventory-status")))
                class_name = inventory_label.get_attribute('class')
                if class_name == "loading failure":
                    self.driver.refresh()
                elif class_name == "loading":
                    continue
                elif class_name == "inventory-status":
                    children = inventory_label.find_elements(By.XPATH, "*")
                    for child in children:
                        if child.tag_name == "i":
                            return False
                        elif child.tag_name == "a":
                            return True
                        else:
                            return None 
                
        def consumer() -> str:
            inventory_state = checked_inventory()
            if inventory_state != None and inventory_state:
                try:
                    inventory_table =  WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.fcresearch.inventory)))
                    if not inventory_table:
                        inventory_state = checked_inventory()
                        if inventory_state != None and inventory_state:
                            inventory_table =  WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator.xpath.fcmenu.fcresearch.inventory)))
                        else:
                            raise TimeoutException
                except TimeoutException:
                    return "No Inventory"
            else:
                return "No Inventory"

            trows = inventory_table.find_elements(By.TAG_NAME, "tr")
            for i, row in enumerate(trows):
                try:
                    if row.text == "":
                        continue
                    else:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        data = [cell.text for cell in cells]                
                        container_data_dict[row.get_attribute("data-row-id").split("-")[0] + f"[{i}]"] = data
                except StaleElementReferenceException:
                    container_data_dict[container] = "ERROR"
            return container_data_dict
        
        def container_history():
                try:
                    container_history_table =  WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, locator.ID.fcresearch.container_history.table)))
                except TimeoutException:
                    self.driver.refresh()
                    time.sleep(1)
                    try:
                        container_history_table =  WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, locator.ID.fcresearch.container_history.table)))
                    except TimeoutException:
                        container_history_data_dict[container] = ["error"] * 6
                        return container_history_data_dict
                trows = container_history_table.find_elements(By.TAG_NAME, "tr")
                try:
                    for row in trows:
                        if row.text == '':
                            continue
                        else:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            data = [cell.text for cell in cells]
                            container_history_data_dict[container] = data
                            return container_history_data_dict
                except StaleElementReferenceException:
                    container_history_data_dict[container] = ["error"] * 6
                    return container_history_data_dict
            
        def create_csv(filename: str):
            if not os.path.exists(filename):
                with open(filename, "w"):
                    pass
                    
        def data_pairing(dict_param, hist: bool):
            for _ , values in dict_param.items():
                if hist:
                    for header, value in zip(headers[12:], values):
                        container_history_paired_data[header] = value
                else:
                    for header, value in zip(headers, values):
                        container_paired_data[header] = value
        
        def csv_write(cont):
            with open(csv_file, "a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=[head for head in headers])
                if file.tell() == 0:
                    writer.writeheader()
                if "No Inventory" in data:
                    writer.writerow({Container.container: cont, Container.asin: "No Inventory"})
                else:
                    for _container, _ in data.items():
                        if "[" in _container:
                            _container = _container.split("[")[0]
                        writer.writerow({Container.inventory.container:                 _container, 
                                         Container.inventory.asin:                      container_paired_data[Container.inventory.asin], 
                                         Container.inventory.fnsku:                     container_paired_data[Container.inventory.fnsku], 
                                         Container.inventory.fcsku:                     container_paired_data[Container.inventory.fcsku], 
                                         Container.inventory.LPN:                       container_paired_data[Container.inventory.LPN], 
                                         Container.inventory.quantity:                  container_paired_data[Container.inventory.quantity], 
                                         Container.inventory.consumer:                  container_paired_data[Container.inventory.consumer], 
                                         Container.inventory.outerlocation:             container_paired_data[Container.inventory.outerlocation], 
                                         Container.inventory.outerlocationtype:         container_paired_data[Container.inventory.outerlocationtype], 
                                         Container.inventory.title:                     container_paired_data[Container.inventory.title],
                                         Container.container_history.move_date:         container_history_paired_data[Container.container_history.move_date],
                                         Container.container_history.action:            container_history_paired_data[Container.container_history.action],
                                         Container.container_history.movedBy:           container_history_paired_data[Container.container_history.movedBy],
                                         Container.container_history.oldContainer:      container_history_paired_data[Container.container_history.oldContainer],
                                         Container.container_history.newContainer:      container_history_paired_data[Container.container_history.newContainer],
                                         Container.container_history.requestByClient:   container_history_paired_data[Container.container_history.requestByClient]})
        goto_fcr()
        create_csv(csv_file)
        data = consumer()
        cont_hist_data = container_history()
        if data != "No Inventory":
            data_pairing(data, hist=False)
            data_pairing(cont_hist_data, hist=True)
        if not write_to_csv:
                if extract_value[0] in container_paired_data:
                    return container_paired_data[extract_value[0]]
        else:
            csv_write(container)