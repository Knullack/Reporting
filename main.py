from selenium.webdriver import Chrome, Firefox, Edge
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from time import time
from datetime import datetime

if __name__ == "__main__":
    start_time = time()
    month = datetime.now().month
    day = datetime.now().day
    year = datetime.now().year
    session = chromeSession(12730876)
    session.start()
    websites = {
        "https://peculiar-inventory-na.aka.corp.amazon.com/HDC3/overview": {
            "inbound": {
                "1-2": '/html/body/div[1]/div[2]/div[2]/div[2]/a/span/div/div[3]',
                "2-3": '/html/body/div[1]/div[2]/div[2]/div[2]/a/span/div/div[4]',
                "3-5": '/html/body/div[1]/div[2]/div[2]/div[2]/a/span/div/div[5]',
                ">5": '/html/body/div[1]/div[2]/div[2]/div[2]/a/span/div/div[6]'
            },
            "outbound": {
                "1-2": '/html/body/div[1]/div[2]/div[2]/div[4]/a/span/div/div[3]',
                "2-3": '/html/body/div[1]/div[2]/div[2]/div[4]/a/span/div/div[4]',
                "3-5": '/html/body/div[1]/div[2]/div[2]/div[4]/a/span/div/div[5]',
                ">5": '/html/body/div[1]/div[2]/div[2]/div[4]/a/span/div/div[6]'
            }
        },
        "https://picking-console.na.picking.aft.a2z.com/fc/HDC3/process-paths/?tableFilters=%7B%22tokens%22%3A%5B%7B%22propertyKey%22%3A%22ProcessPathName%22%2C%22propertyLabel%22%3A%22Process%20Path%22%2C%22value%22%3A%22PPTransDELETE%22%2C%22label%22%3A%22PPTransDELETE%22%2C%22negated%22%3Afalse%7D%2C%7B%22propertyKey%22%3A%22ProcessPathName%22%2C%22propertyLabel%22%3A%22Process%20Path%22%2C%22value%22%3A%22PPRejectRemovals%22%2C%22label%22%3A%22PPRejectRemovals%22%2C%22negated%22%3Afalse%7D%2C%7B%22propertyKey%22%3A%22PickProcess%22%2C%22propertyLabel%22%3A%22Pick%20Process%22%2C%22value%22%3A%22MDPRejectPicking%22%2C%22label%22%3A%22MDPRejectPicking%22%2C%22negated%22%3Afalse%7D%2C%7B%22propertyKey%22%3A%22PickProcess%22%2C%22propertyLabel%22%3A%22Pick%20Process%22%2C%22value%22%3A%22HOVRejectPicking%22%2C%22label%22%3A%22HOVRejectPicking%22%2C%22negated%22%3Afalse%7D%5D%2C%22operation%22%3A%22or%22%7D": {
            "units": {
                "PPHOVReject": '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[1]/td[8]/span/a',
                "PPMDPReject": '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[2]/td[8]/span/a',
                "PPTransDELETE": '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[3]/td[8]/span/a'
            },
            "active-pickers": {
                "PPMDPReject" : '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[2]/td[10]/span/span',
                "PPTransDELETE" : '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[3]/td[10]/span/span'
            }
        },
        "https://fc-quality-dashboard-iad.aka.amazon.com/management/count_density?work_type=CYCLE_COUNT": {
            "cycle-count": {
                "all": '/html/body/div/table/tbody/tr[10]/td[3]/a'
            }
        },
        "https://fc-quality-dashboard-iad.aka.amazon.com/management/count_density?work_type=SIMPLE_BIN_COUNT": {
            "simple-bin-count" : {
                "all": '/html/body/div/table/tbody/tr[3]/td[3]/a'
            }
        },
        f"https://fclm-portal.amazon.com/reports/functionRollup?reportFormat=HTML&warehouseId=HDC3&processId=1003030&startDateWeek={year}%2F{month}%2F{day}&maxIntradayDays=1&spanType=Intraday&startDateIntraday={year}%2F{month}%2F{day}&startHourIntraday=7&startMinuteIntraday=0&endDateIntraday={year}%2F{month}%2F{day}&endHourIntraday=18&endMinuteIntraday=0": {
            "total-paid-hours" : {
                "total": '/html/body/div[4]/table[2]/tfoot/tr[1]/td[1]'
            }
        }
    }
    accuracy_dashboard = 'https://fc-quality-dashboard-iad.aka.amazon.com/reporting/dashboards/count_accuracy'
    andons_pick = 'http://fc-andons-na.corp.amazon.com/HDC3?category=Pick&type=All+types'
    andons_CC = 'http://fc-andons-na.corp.amazon.com/HDC3?category=Bin+Item+Defects&type=All+types'
    downloads = {
        accuracy_dashboard : {
            'csv': '/html/body/div[2]/div/div/dashboard-grid/ul/li[6]/dashboard-panel/div/visualize/div[2]/div/div/kbn-agg-table-group/table/tbody/tr/td/kbn-agg-table-group/table/tbody/tr/td/kbn-agg-table/paginated-table/paginate/div[2]/div/a'
        },
        andons_pick : {
            'csv': '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-table/div/div[2]/div[1]/div[1]/span/div/div[2]/awsui-button[1]/button'
        },
        andons_CC : {
            'csv' : '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-table/div/div[2]/div[1]/div[1]/span/div/div[2]/awsui-button[1]/button'
        }
    }

    
    pick_andons = session.download_csv(andons_pick, downloads[andons_pick]['csv'], r"C:\Users\nuneadon.ANT\Downloads", True)
    CC_andons = session.download_csv(andons_CC, downloads[andons_CC]['csv'], r"C:\Users\nuneadon.ANT\Downloads")
    # SBC_accuracy = session.download_csv(accuracy_dashboard, downloads[accuracy_dashboard]['csv'], r"C:\Users\nuneadon.ANT\Downloads")

    for website, categories in websites.items():
        for category, xpaths in categories.items():
            for subcategory, xpath in xpaths.items():
                value = session.get_text(website, xpath)
                # Update dictionary value with the returned value
                websites[website][category][subcategory] = value


    session.close()


    elapsed_time = time() - start_time
    if elapsed_time < 60:
        print(f"Runtime: {elapsed_time:.2f} seconds")
    elif elapsed_time >= 60:
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f"Runtime: {minutes}m:{seconds}s")

    IOL = next(iter(websites))
    PICK_CONSOLE = list(websites.keys())[1]
    FCQUALITY_CC = list(websites.keys())[2]
    FCQUALITY_SBC = list(websites.keys())[3]
    FCLM = list(websites.keys())[4]


# for website, categories in websites.items():
#     for category, subcategories in categories.items():
#         for subcategory, value in subcategories.items():
#             print(f"{category} - {subcategory}: {value}")

try:

    inbound_1_3 = int(websites[IOL]['inbound']['1-2']) + int(websites[IOL]['inbound']['2-3'])
    inbound_3_5 = int(websites[IOL]['inbound']['3-5'])
    inbound_gt_5 = int(websites[IOL]['inbound']['>5'])
    #
    outbound_1_3 = int(websites[IOL]['outbound']['1-2']) + int(websites[IOL]['outbound']['2-3'])
    outbound_3_5 = int(websites[IOL]['outbound']['3-5'])
    outbound_gt_5 = int(websites[IOL]['outbound']['>5'])

    unit_HOVReject = int(websites[PICK_CONSOLE]['units']['PPHOVReject'])
    unit_MDPReject = int(websites[PICK_CONSOLE]['units']['PPMDPReject'])
    unit_TransDELETE = int(websites[PICK_CONSOLE]['units']['PPTransDELETE'])

    count_MDPReject = int(websites[PICK_CONSOLE]['active-pickers']['PPMDPReject'])
    count_TransDELETE = int(websites[PICK_CONSOLE]['active-pickers']['PPTransDELETE'])

    CC = int(websites[FCQUALITY_CC]['cycle-count']['all'])
    SBC = int(websites[FCQUALITY_SBC]['simple-bin-count']['all'])

    fclm_hours = float(websites[FCLM]['total-paid-hours']['total'])

    print(f"IB (1-3): {inbound_1_3}")
    print(f"IB (3-5): {inbound_3_5}")
    print(f"IB (>5): {inbound_gt_5}")

    print(f"OB (1-3): {outbound_1_3}")
    print(f"OB (3-5): {outbound_3_5}")
    print(f"OB (>5): {outbound_gt_5}")

    print(f"UNITS HOVReject: {unit_HOVReject}")
    print(f"UNITS MDPReject: {unit_MDPReject}")
    print(f"UNITS TransDelete: {unit_TransDELETE}")

    print(f"UNITS HOVReject: {unit_HOVReject}")
    print(f"UNITS MDPReject: {unit_MDPReject}")
    print(f"UNITS TransDelete: {unit_TransDELETE}")

    print(f"HC MDPReject: {count_MDPReject}")
    print(f"HC TransDelete: {count_TransDELETE}")

    print(f"CC: {CC}")
    print(f"SBC: {SBC}")

    print(f'IQQA Hours: {fclm_hours}')

except TypeError:
    pass