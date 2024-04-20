from time import time
from typing import Callable, Tuple
from datetime import datetime

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
class constants:
    LOGIN_URL = "https://fcmenu-iad-regionalized.corp.amazon.com/login"
    CHROME_PATH = r"C:\Users\nuneadon\AppData\Local\Google\Chrome\Application\chrome.exe"
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
            menu = '/html/body/div[1]/div[2]/div/div[2]/ul/li[2]/span/span/a'
            btn_restart = '/html/body/div[4]/div/div/div/div[1]/div[1]/span[2]/div/div/div/div[1]/h1'
            btn_change_mode = '/html/body/div[4]/div/div/div/div[1]/div[3]/span/div/div/div/div[1]/h1'
            class modes:
                current_mode = '/html/body/div[1]/div[4]/div/div[1]/div/dl/dd'
                single = '/html/body/div[1]/div[5]/div/div[2]/div[1]/span/form/div/fieldset/div[1]/div/div/label/i'
                container = '/html/body/div[1]/div[5]/div/div[2]/div[1]/span/form/div/fieldset/div[2]/div/div/label/i'
                continue_enter = '/html/body/div[1]/div[5]/div/div[2]/div[1]/span/form/span/span/input'
                select_modes_banner = '/html/body/div[1]/div[5]/div/div[2]/div[1]/div/div/h1'
            class scan:
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

        class fcmenu:
            input_badge = '//*[@id="badgeBarcodeId"]'
            inbound = '/html/body/div[3]/div/div[2]/ul[1]/li[1]/a'
            outbound = '/html/body/div[3]/div/div[2]/ul[1]/li[2]/a'
            picking = '/html/body/div[3]/div/div[2]/ul[1]/li[1]/a'
            move_container_145 = '/html/body/div[3]/div/div[2]/ul[2]/li[3]/a'
            problem_solve = '/html/body/div[3]/div/div[2]/ul[2]/li[5]/a'
            sideline_app = '/html/body/div[3]/div/div[2]/ul[1]/li[1]/a'
            unbindHierarchy = '/html/body/div[3]/div/div[2]/ul[2]/li[3]/a'
            
            class unbind:
                input = '/html/body/div[2]/div/input'
                continue_btn = '/html/body/div[1]/div[4]/div[2]/div[4]/span'
                success_banner = '/html/body/div[1]/div[3]/div/div[2]/span[1]'
                error_banner = '/html/body/div[1]/div[5]/div[2]/div[2]'
            class move_container:
                individually_workflow = '/html/body/div/div/div/ul/li[2]'
                input = '/html/body/div/div[7]/div/input'
                error_msg = '/html/body/div/div[4]/div[2]/div[1]'
            class peculiar_inventory:
                table_body = '/html/body/div[1]/div[3]/div/div[1]/div/div[1]/table/tbody'

            class fcresearch:
                asin = '/html/body/div[2]/div/div[1]/div/div[6]/div/div[2]/div/div/div[1]/div[2]/table/tbody/tr/td[2]/a'

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
                    

        class picking_console:
            error_msg = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[1]/div/span/awsui-flashbar/div/awsui-flash/div/div[2]/div/div/span/span/span'
            table = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[3]/div/div/awsui-table/div/div[3]'

        class fc_andons:
            error_msg = '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-flash/div/div[2]/div/div'

    class class_name:
        class delete:
            enter = 'a-button-input'
            box = 'a-box'
            fielset = 'a-box-group a-form-control-group'

        class counts:
            spinner = 'spinner.large'

        class sideline_app:
            step = 'text text--bold'
            trans_out = 'text text--size-xl text--variant-white'

        class pick:
            no_batch = 'button button--size-md button--variant-secondary button--fluid'
            bin = 'greyed-text'

    class ID:
        
        class pick:
            spinner = 'spinner'

class header:  
    SCAN = 'Scan container'
    SELECT = 'Select item to delete'
    REASON = ['Select reason to delete','Select deletion reason']
    CONFIRM = 'Confirm the deletion'

