from time import time
from typing import Callable, Tuple
from datetime import datetime
import configparser
import os
import platform
import glob

def runtime(function: Callable[..., any], *args, **kwargs) -> Tuple[str, any] | str:
    """
    Returns function's returned value (if any) & the time it took to run called function
    A tuple if given function returns a value, otherwise, returns str
    """
    return_value = None
    start_time = time()
    return_value = function(*args, **kwargs)
    elapsed_time = time() - start_time
    if elapsed_time < 60:
        runtime_print = f"{datetime.now()} // Runtime: {elapsed_time:.2f} seconds\n{'-' * 47}\n"
    elif elapsed_time >= 60:
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        runtime_print = f"Runtime: {minutes}m:{seconds}s"
    
    return (runtime_print, return_value) if return_value is not None else runtime_print

class andon_types:
    all = "All+types&status=Open"
    binDoesNotExist = "Bin+does+not+Exist&status=Open"
    brokenSet = "Broken+Set&status=Open"
    damagedItem = "Damaged+Item&status=Open"
    noBinDivider = "No+Bin+Divider&status=Open"
    noScannableBarcode = "No+Scannable+Barcode&status=Open"    
    noScannableBinLabel = "No+Scannable+Bin+Label&status=Open"
    multipleScannableBarcodes = 'Multiple+Scannable+Barcodes&status=Open'
    suspectTheft = "Suspect+Theft&status=Open"
    unexpectedContainerOverage = "Unexpected+Container+Overage&status=Open"
    unsafeToCount = "Unsafe+to+Count&status=Open"

class tab_names:
    ANDONS = "Andons"
    FCR = 'FC Research'
    ADD_ITEM = 'Add Items'
    MOVE_CONTAINER = 'Move Container'
    SIDELINE = 'Sideline'
    FCR_ITEM_PRICE = 'FCR_ITEM'

class chromeFinder:
    __storage_file__ = 'local_storage.ini'
    BASE_DIRECTORY = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\FCM Automations"
    CHROME_PATH = None

    # Function to find Chrome path
    @staticmethod
    def find_chrome_path():
        os_name = platform.system()

        chrome_paths = []
        if os_name == 'Windows':
            chrome_paths.extend([
                os.path.join(os.getenv('PROGRAMFILES'), 'Google', 'Chrome', 'Application', 'chrome.exe'),
                os.path.join(os.getenv('PROGRAMFILES(X86)'), 'Google', 'Chrome', 'Application', 'chrome.exe'),
            ])
        elif os_name == 'Darwin':
            chrome_paths.append('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        elif os_name == 'Linux':
            chrome_paths.extend([
                '/usr/bin/google-chrome',
                '/usr/local/bin/google-chrome',
                '/opt/google/chrome/chrome',
            ])

        # First, check in common locations
        for path in chrome_paths:
            if os.path.isfile(path):
                return path
        
        # Search in user directory
        home_dir = os.path.expanduser('~')
        if os_name == 'Windows':
            chrome_search_pattern = os.path.join(home_dir, '**', 'chrome.exe')
        elif os_name == 'Darwin':
            chrome_search_pattern = os.path.join(home_dir, '**', 'Google Chrome')
        elif os_name == 'Linux':
            chrome_search_pattern = os.path.join(home_dir, '**', 'google-chrome')
        
        found_chrome = glob.glob(chrome_search_pattern, recursive=True)

        if found_chrome:
            return found_chrome[0]

        return None

    # Method to update configuration with Chrome path
    @staticmethod
    def configFile(chrome_executable):
        config = configparser.ConfigParser()

        # Ensure the base directory exists
        os.makedirs(chromeFinder.BASE_DIRECTORY, exist_ok=True)

        # File path for configuration file
        config_file = os.path.join(chromeFinder.BASE_DIRECTORY, chromeFinder.__storage_file__)

        # Load existing config or create a new one
        if os.path.isfile(config_file):
            config.read(config_file)
        else:
            with open(config_file, 'w') as f:
                config.write(f)

        stored_path = config.get('Paths', 'chrome_executable', fallback=None)

        if stored_path is None:
            if 'Paths' not in config.sections():
                config.add_section('Paths')

            config.set('Paths', 'chrome_executable', chrome_executable)

            # Save to configuration file
            with open(config_file, 'w') as f:
                config.write(f)

        return stored_path or chrome_executable
class constants:
    LOGIN_URL = "https://fcmenu-iad-regionalized.corp.amazon.com/login"
    CHROME_PATH = chromeFinder().configFile(chromeFinder().find_chrome_path())
    ARGUMENTS = ['--log-level=3','--force-device-scale-factor=0.7','--disable-blink-features=AutomationControlled','--disable-notifications','--disable-infobars','--disable-extensions','--disable-dev-shm-usage','--disable-gpu','--disable-browser-side-navigation','--disable-features=VizDisplayCompositor','--no-sandbox','--disable-logging']
class header:  
    SCAN = ['Scan container', 'Scan item']
    SELECT = ['Select item to delete', 'Scan item', 'Select item']
    QUANTITY = ['Enter quantity']
    DESTINATION_CONTAINER = ['Scan destination container']
    REASON = ['Select reason to delete','Select deletion reason']
    CONFIRM = 'Confirm the deletion'

class Container:
    class inventory:
        container = 'Container'
        asin = 'ASIN'
        fnsku = 'FNSku'
        fcsku = 'FCSku'
        LPN = 'LPN'
        quantity = 'Quantity'
        disposition = 'Disposition'
        consumer = 'Consumer'
        consumerid = 'Consumer ID'
        outerlocation = 'Outer Location'
        outerlocationtype = 'Outer Location Type'
        title = 'Title'

    class container_history:
        # first row
        move_date = "Move Date"
        action = "Action"
        movedBy = "Move By"
        oldContainer = "Old Container"
        newContainer = "New Container"
        requestByClient = "Request By Client"
        # second row
        move_date_2 = "Move Date 2"
        action_2 = "Action 2"
        movedBy_2 = "Move by 2"
        oldContainer_2 = "Old Container 2"
        newContainer_2 = "New Container 2"
        requestByClient_2 = "Request by Client 2"
        # third row
        move_date_3 = "Move Date 3"
        action_3 = "Action 3"
        movedBy_3 = "Move By 3"
        oldContainer_3 = "Old Container 3"
        newContainer_3 = "New Container 3"
        requestByClient_3 = "Request by Client 3"

    class container_details:
        child1 = "child1"
        child2 = "child2"

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
            container_overage_btn = '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div/div/div[3]/button'
            select_overage_banner = '/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/div[2]/div/div/span/span[3]'
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
            menu = '/html/body/div[1]/div[2]/div/div[2]/ul/li[2]/span/span/a'
            btn_restart = '/html/body/div[4]/div/div/div/div[1]/div[1]/span[2]/div/div/div/div[1]/h1'
            btn_change_mode = '/html/body/div[4]/div/div/div/div[1]/div[3]/span/div/div/div/div[1]/h1'
            processing_element = '/html/body/div[1]/div[4]/div/div[2]/div[2]'
            user_menu_popover_aria = '/html/body/div[4]/div'
            class modes:
                current_mode = '/html/body/div[1]/div[4]/div/div[1]/div/dl/dd'
                single = '/html/body/div[1]/div[5]/div/div[2]/div[1]/span/form/div/fieldset/div[1]/div/div/label/i'
                container = '/html/body/div[1]/div[5]/div/div[2]/div[1]/span/form/div/fieldset/div[2]/div/div/label/i'
                continue_enter = '/html/body/div[1]/div[5]/div/div[2]/div[1]/span/form/span/span/input'
                select_modes_banner = '/html/body/div[1]/div[5]/div/div[2]/div[1]/div/div/h1'
            class scan:
                scan_item = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/div[1]/input'
                input = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/div/input'
                enter = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/span/span/input'
            class select:
                fieldset = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/div[1]/fieldset'
                boxSku = 'div/div/div/label/span/div[2]/div/div[2]/div[2]/div[2]/div[1]/dl/dd[1]'
                enter = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/span[1]/span/input'
                container_empty = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/div[2]/div/div'
            class reason:
                reason_statement  = '/html/body/div[1]/div[4]/div/div[1]/div/dl[3]/dd'
                sweeping_out = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/div[1]/fieldset/div[1]/div/div/label/span'
                enter = '/html/body/div[1]/div[4]/div/div[2]/div[1]/span/form/span[1]/span/input'
            class confirm:
                enter = '/html/body/div[1]/div[4]/div/div[2]/div[1]/form/span[1]/span/span/input'

        class moveItems:
            
            H1_header = '/html/body/div[1]/div[4]/div/div[2]/div[1]/div/div/h1'
            class modes:
                each = '/html/body/div[1]/div[5]/div/div[2]/div[1]/span/form/div/fieldset/div[1]/div/div/label/span/h1'
                multi = '/html/body/div[1]/div[5]/div/div[2]/div[1]/span/form/div/fieldset/div[2]/div/div/label/span/h1'
                container = '/html/body/div[1]/div[5]/div/div[2]/div[1]/span/form/div/fieldset/div[3]/div/div/label/span/h1'
            
        class fcmenu:
            input_badge = '//*[@id="badgeBarcodeId"]'
            inbound = '/html/body/div[3]/div/div[2]/ul[1]/li[1]/a'
            outbound = '/html/body/div[3]/div/div[2]/ul[1]/li[2]/a'
            picking = '/html/body/div[3]/div/div[2]/ul[1]/li[1]/a'
            move_container_145 = '/html/body/div[3]/div/div[2]/ul[2]/li[3]/a'
            move_container_146 = '/html/body/div[3]/div/div[2]/ul[1]/li[3]/a'
            problem_solve = '/html/body/div[3]/div/div[2]/ul[2]/li[5]/a'
            sideline_app = '/html/body/div[3]/div/div[2]/ul[1]/li[1]/a'
            unbindHierarchy = '/html/body/div[3]/div/div[2]/ul[2]/li[4]/a'

            class labor_tracking:
                submit = "/html/body/div[3]/div/div[2]/form/input[4]"
                calmCode = "/html/body/div[3]/div/div[3]/form/input[2]"
                badge_id = "/html/body/div[3]/div/div[2]/form/input[3]"

            class unbind:
                input = '/html/body/div[2]/div/input'
                continue_btn = '/html/body/div[1]/div[4]/div[2]/div[4]/span'
                success_banner = '/html/body/div[1]/div[3]/div/div[2]/span[1]'
                error_banner = '/html/body/div[1]/div[5]/div[2]/div[2]'
                double_check_banner = '/html/body/div[1]/div[4]/div[2]/div[2]'
            class move_container:
                individually_workflow = '/html/body/div/div/div/ul/li[2]'
                input = '/html/body/div/div[7]/div/input'
                error_msg = '/html/body/div/div[4]/div[2]/div[1]'
                
            class peculiar_inventory:
                table_body = '/html/body/div[1]/div[3]/div/div[1]/div/div[1]/table/tbody'

            class fcresearch:
                table = "/html/body/div[2]/div/div[1]/div/div[1]/div/div[2]/div/div/div[2]/table"
                inventory = "/html/body/div[2]/div/div[1]/div/div[6]/div/div[2]/div/div/div[1]/div[2]/table"
                title_row = "/html/body/div[2]/div/div[1]/div/div[1]/div/div[2]/div/div/div[2]/table/tbody/tr[2]/th"
                asin = '/html/body/div[2]/div/div[1]/div/div[6]/div/div[2]/div/div/div[1]/div[2]/table/tbody/tr/td[2]/a'
                child_containers_table = "/html/body/div[2]/div/div[1]/div/div[9]/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/table"
                child_containers_table_first_row = "/html/body/div[2]/div/div[1]/div/div[9]/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div[2]/table/tbody/tr/td[1]"
                inventory_section = '/html/body/div[2]/div/div[3]/div/div[2]/div/ul/li[6]'
                inventory_history_not_found_text = '/html/body/div[2]/div/div[1]/div/div[7]/div/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[1]/td'
                asin_info_table = '/html/body/div[2]/div/div[1]/div/div[1]/div/div[2]/div/div/div[2]/table'
                class container_history:
                    last_move_login = "/html/body/div[2]/div/div[1]/div/div[8]/div/div[2]/div/div/div[1]/div[2]/table/tbody/tr[1]/td[3]"
            class pickUI:
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

            class PAWS_Traditional_Picking:
                no_batch = '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div[3]/button'
                
                class vehicle:
                    """vehilce_drozone, """
                    scan_vehicle_id_span = '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div/span'
                    input = ''
                    next_bin = '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/span/span[2]'
            
            class add_items:
                continue_enter = '/html/body/div[1]/div[3]/form/span/span/input'
                container_not_found_alert = '/html/body/div[1]/div[3]/form/div[2]/div/div'
                update_qty_btn = '/html/body/div[1]/div[3]/form[2]/span/span/input'
                start_over_btn = '/html/body/div[1]/div[3]/form[2]/span/span/input'
                step_label = '/html/body/div[1]/div[3]/form/label'
                
        class picking_console:
            error_msg = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[1]/div/span/awsui-flashbar/div/awsui-flash/div/div[2]/div/div/span/span/span'
            table = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[3]/div/div/awsui-table/div/div[3]'

        class fc_andons:
            error_msg = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-flash/div/div[2]/div/div'
            filter_by_keyword = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-table/div/div[2]/div[1]/div[2]/span/span/awsui-table-filtering/span/awsui-input/div/input'
            select_first_andon = "/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-table/div/div[3]/table/tbody/tr/td[1]/awsui-radio-button/div/label/input"
            select_second_andon = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-table/div/div[3]/table/tbody/tr[2]/td[1]/awsui-radio-button/div/label/input'
            assign_andon = "/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-table/div/div[3]/table/tbody/tr/td[12]/span/awsui-button/button"
            view_edit = "/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-table/div/div[2]/div[1]/div[1]/span/div/div[2]/awsui-button[2]/button"
            label_resolveBox = "/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-modal/div[2]/div/div/div[2]/div/span/span/awsui-form/div/div[2]/span/span/awsui-form-section/div/div[2]/span/awsui-column-layout/div/span/div/awsui-form-field[4]/div/div/div/div/span/awsui-checkbox/label"
            resolve_box = "/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-modal/div[2]/div/div/div[2]/div/span/span/awsui-form/div/div[2]/span/span/awsui-form-section/div/div[2]/span/awsui-column-layout/div/span/div/awsui-form-field[4]/div/div/div/div/span/awsui-checkbox/label/input"
            save_changes = "/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-modal/div[2]/div/div/div[3]/span/div/div[2]/awsui-button[2]"
            search_submit = "/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-form-section/div/div[2]/span/awsui-form/div/div[4]/span/div/div[2]/div/awsui-button[2]/button"
            count_search_result = "/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-table/div/div[2]/div[1]/div[2]/span/span/awsui-table-filtering/span/span"
            login_input = "/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-modal/div[2]/div/div/div[2]/div/span/span/awsui-form/div/div[2]/span/span/awsui-form-section/div/div[2]/span/awsui-column-layout/div/span/div/awsui-form-field[2]/div/div/div/div/span/awsui-input/div/input"
            userlogin = "/html/body/div/div/div/header/ul/li[3]"
            table = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-table/div/div[3]/table'
            comment_input = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-modal/div[2]/div/div/div[2]/div/span/span/awsui-form/div/div[2]/span/span/awsui-form-section/div/div[2]/span/awsui-column-layout/div/span/div/awsui-form-field[3]/div/div/div/div/span/awsui-textarea/textarea'
            root_cause_dropdown = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-modal/div[2]/div/div/div[2]/div/span/span/awsui-form/div/div[2]/span/span/awsui-form-section/div/div[2]/span/awsui-column-layout/div/span/div/awsui-form-field[1]/div/div/div/div/span/awsui-select/div/div/awsui-select-dropdown/div'

    class class_name:

        class add_items:
            continue_enter = 'a-button-input aft-scan-submit'

        class fcmenu:
            class fcresearch:
                search_buttons = 'a-button-text'
            
            class sideline:
                alert_div = 'alert--error'
        class itemApps:
            processing_visible = 'a-section aft-tool-processing aft-tool-status'
            processing_hidden = 'a-section aft-tool-hide aft-tool-processing aft-tool-status'
        class delete:
            enter = 'a-button-input'
            box = 'a-box'
            fielset = 'a-box-group a-spacing-base'

            class select:
                continue_enter = 'a-button-inner'
        
        class move_items:
            fieldset = 'a-box-group a-form-control-group'
            
        class counts:
            spinner = 'spinner.large'

        class sideline_app:
            step = 'text text--bold'
            trans_out = 'text text--size-xl text--variant-white'

        class pick:
            no_batch = 'button button--size-md button--variant-secondary button--fluid'
            bin = 'greyed-text'

        class barcodeGenerator:
            print_btn = "apmbutton"

    class ID:
        
        class fcmenu:
            class move_container:
                exception_body = 'exception-body'
        class add_items:
            container = 'containerScannableId'
            item = 'itemScannableId'
            itemQTY = 'itemQuantity'
            dest_container = 'destinationContainerId'
        class delete:
            user_menu = 'a-page'
            user_menu_overlay = 'a-popover-1'
        class pick:
            spinner = 'spinner'

        class fcresearch:
            class inventory:
                table = 'inventory-status'
            class container_history:
                table = 'table-container-history'
            class inventory_history:
                start_date = 'searchStart'
                entry_info = 'table-inventory-history_info'
                entries_table = 'table-inventory-history'
            
            class container_details:
                table = "container-hierarchy-status"

            class details:
                table = "table-container-hierarchy"

        class barcodeGenerator:
            barcodeEntry = "barcodedata"
            displayText = "displaytext"
            badgeID = "badgeid"

