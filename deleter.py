import datetime
from openpyxl import Workbook, load_workbook
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from time import time
from datetime import datetime
import pandas as pd

if __name__ == "__main__":
    download_dir = r"C:\Users\nuneadon.ANT\Downloads"
    start_time = time()
    month = datetime.now().month
    day = datetime.now().day
    year = datetime.now().year
    session = chromeSession(12730876)
    session.start()
    session.deleteItem(100)
#     websites = {
#         "https://peculiar-inventory-na.aka.corp.amazon.com/HDC3/overview": {
#             "inbound": {
    #                 "1-2": '/html/body/div[1]/div[2]/div[2]/div[2]/a/span/div/div[3]',
    #                 "2-3": '/html/body/div[1]/div[2]/div[2]/div[2]/a/span/div/div[4]',
#                 "3-5": '/html/body/div[1]/div[2]/div[2]/div[2]/a/span/div/div[5]',
#                 ">5": '/html/body/div[1]/div[2]/div[2]/div[2]/a/span/div/div[6]'
#             },
#             "outbound": {
#                 "1-2": '/html/body/div[1]/div[2]/div[2]/div[4]/a/span/div/div[3]',
#                 "2-3": '/html/body/div[1]/div[2]/div[2]/div[4]/a/span/div/div[4]',
#                 "3-5": '/html/body/div[1]/div[2]/div[2]/div[4]/a/span/div/div[5]',
#                 ">5": '/html/body/div[1]/div[2]/div[2]/div[4]/a/span/div/div[6]'
#             }
#         },
#         "https://picking-console.na.picking.aft.a2z.com/fc/HDC3/process-paths/?tableFilters=%7B%22tokens%22%3A%5B%7B%22propertyKey%22%3A%22ProcessPathName%22%2C%22propertyLabel%22%3A%22Process%20Path%22%2C%22value%22%3A%22PPTransDELETE%22%2C%22label%22%3A%22PPTransDELETE%22%2C%22negated%22%3Afalse%7D%2C%7B%22propertyKey%22%3A%22ProcessPathName%22%2C%22propertyLabel%22%3A%22Process%20Path%22%2C%22value%22%3A%22PPRejectRemovals%22%2C%22label%22%3A%22PPRejectRemovals%22%2C%22negated%22%3Afalse%7D%2C%7B%22propertyKey%22%3A%22PickProcess%22%2C%22propertyLabel%22%3A%22Pick%20Process%22%2C%22value%22%3A%22MDPRejectPicking%22%2C%22label%22%3A%22MDPRejectPicking%22%2C%22negated%22%3Afalse%7D%2C%7B%22propertyKey%22%3A%22PickProcess%22%2C%22propertyLabel%22%3A%22Pick%20Process%22%2C%22value%22%3A%22HOVRejectPicking%22%2C%22label%22%3A%22HOVRejectPicking%22%2C%22negated%22%3Afalse%7D%5D%2C%22operation%22%3A%22or%22%7D": {
#             "units": {
#                 "PPHOVReject": '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[1]/td[8]/span/a',
#                 "PPMDPReject": '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[2]/td[8]/span/a',
#                 "PPTransDELETE": '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[3]/td[8]/span/a'
#             },
#             "active-pickers": {
#                 "PPMDPReject" : '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[2]/td[10]/span/span',
#                 "PPTransDELETE" : '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[3]/td[10]/span/span'
#             }
#         },
#         "https://fc-quality-dashboard-iad.aka.amazon.com/management/count_density?work_type=CYCLE_COUNT": {
#             "cycle-count": {
#                 "all": '/html/body/div/table/tbody/tr[7]/td[3]/a'
#             }
#         },
#         "https://fc-quality-dashboard-iad.aka.amazon.com/management/count_density?work_type=SIMPLE_BIN_COUNT": {
#             "simple-bin-count" : {
#                 "all": '/html/body/div/table/tbody/tr[5]/td[3]/a'
#             }
#         },
#         f"https://fclm-portal.amazon.com/reports/functionRollup?reportFormat=HTML&warehouseId=HDC3&processId=1003030&startDateWeek={year}%2F{month}%2F{day}&maxIntradayDays=1&spanType=Intraday&startDateIntraday={year}%2F{month}%2F{day}&startHourIntraday=7&startMinuteIntraday=0&endDateIntraday={year}%2F{month}%2F{day}&endHourIntraday=18&endMinuteIntraday=0": {
#             "total-paid-hours" : {
#                 "total": '/html/body/div[3]/table[2]/tfoot/tr[1]/td[1]'
#             }
#         }
#     }
#     accuracy_dashboard = 'https://fc-quality-dashboard-iad.aka.amazon.com/reporting/dashboards/count_accuracy'
#     completion_dashboard = 'https://fc-quality-dashboard-iad.aka.amazon.com/reporting/dashboards/count_completion'
#     andons_pick = 'http://fc-andons-na.corp.amazon.com/HDC3?category=Pick&type=All+types'
#     andons_CC = 'http://fc-andons-na.corp.amazon.com/HDC3?category=Bin+Item+Defects&type=All+types'
#     downloads = {
#         accuracy_dashboard : {
#             'csv': '/html/body/div[2]/div/div/dashboard-grid/ul/li[6]/dashboard-panel/div/visualize/div[2]/div/div/kbn-agg-table-group/table/tbody/tr/td/kbn-agg-table-group/table/tbody/tr/td/kbn-agg-table/paginated-table/paginate/div[2]/div/a'
#         },
#         completion_dashboard : {
#             'csv': '/html/body/div[2]/div/div/dashboard-grid/ul/li[11]/dashboard-panel/div/doc-table/div[2]/paginate/div/a'
#         },
#         andons_pick : {
#             'csv': '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-table/div/div[2]/div[1]/div[1]/span/div/div[2]/awsui-button[1]/button'
#         },
#         andons_CC : {
#             'csv' : '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/awsui-table/div/div[2]/div[1]/div[1]/span/div/div[2]/awsui-button[1]/button'
#         }
#     }

#     pick_andons = None
#     CC_andons = None
#     SBC_accuracy = None
#     count_completion = None

#     for website, categories in websites.items():
#         for category, xpaths in categories.items():
#             for subcategory, xpath in xpaths.items():
#                 # Update dictionary value with the returned value
#                 websites[website][category][subcategory] = session.get_text(website, xpath)


#     SBC_accuracy = session.SBC_accuracy(accuracy_dashboard, downloads[accuracy_dashboard]['csv'], download_dir)
#     count_completion = session.CC_Completion(completion_dashboard, downloads[completion_dashboard]['csv'], download_dir)
#     pick_andons = session.download_csv(andons_pick, downloads[andons_pick]['csv'], download_dir, True)
#     CC_andons = session.download_csv(andons_CC, downloads[andons_CC]['csv'], download_dir)

#     session.close()


#     elapsed_time = time() - start_time
#     if elapsed_time < 60:
#         print(f"Runtime: {elapsed_time:.2f} seconds")
#     elif elapsed_time >= 60:
#         minutes = int(elapsed_time // 60)
#         seconds = int(elapsed_time % 60)
#         print(f"Runtime: {minutes}m:{seconds}s")

#     IOL = next(iter(websites))
#     PICK_CONSOLE = list(websites.keys())[1]
#     FCQUALITY_CC = list(websites.keys())[2]
#     FCQUALITY_SBC = list(websites.keys())[3]
#     FCLM = list(websites.keys())[4]

# try:
#     # Inbound metrics
#     inbound_1_3 = int(websites[IOL]['inbound']['1-2']) + int(websites[IOL]['inbound']['2-3'])
#     inbound_3_5 = int(websites[IOL]['inbound']['3-5'])
#     inbound_gt_5 = int(websites[IOL]['inbound']['>5'])
    
#     print(f"IB (1-3): {inbound_1_3}")
#     print(f"IB (3-5): {inbound_3_5}")
#     print(f"IB (>5): {inbound_gt_5}")

# except TypeError as e:
#     print(f"Error: Failed to process inbound metrics. {e}")

# try:
#     # Outbound metrics
#     outbound_1_3 = int(websites[IOL]['outbound']['1-2']) + int(websites[IOL]['outbound']['2-3'])
#     outbound_3_5 = int(websites[IOL]['outbound']['3-5'])
#     outbound_gt_5 = int(websites[IOL]['outbound']['>5'])
    
#     print(f"OB (1-3): {outbound_1_3}")
#     print(f"OB (3-5): {outbound_3_5}")
#     print(f"OB (>5): {outbound_gt_5}")

# except TypeError as e:
#     print(f"Error: Failed to process outbound metrics. {e}")

# try:
#     # Unit metrics
#     unit_HOVReject = int(websites[PICK_CONSOLE]['units']['PPHOVReject'])
#     unit_MDPReject = int(websites[PICK_CONSOLE]['units']['PPMDPReject'])
#     unit_TransDELETE = int(websites[PICK_CONSOLE]['units']['PPTransDELETE'])
    
#     print(f"UNITS HOVReject: {unit_HOVReject}")
#     print(f"UNITS MDPReject: {unit_MDPReject}")
#     print(f"UNITS TransDelete: {unit_TransDELETE}")

# except TypeError as e:
#     print(f"Error: Failed to process unit metrics. {e}")

# try:
#     # Count metrics
#     count_MDPReject = int(websites[PICK_CONSOLE]['active-pickers']['PPMDPReject'])
#     count_TransDELETE = int(websites[PICK_CONSOLE]['active-pickers']['PPTransDELETE'])
    
#     print(f"HC MDPReject: {count_MDPReject}")
#     print(f"HC TransDelete: {count_TransDELETE}")

# except TypeError as e:
#     print(f"Error: Failed to process count metrics. {e}")

# try:
#     # SBC and CC metrics
#     CC = websites[FCQUALITY_CC]['cycle-count']['all']
#     SBC = websites[FCQUALITY_SBC]['simple-bin-count']['all']
    
#     print(f"HC CC: {CC}")
#     print(f"HC SBC: {SBC}")

# except TypeError as e:
#     print(f"Error: Failed to process SBC and CC metrics. {e}")

# try:
#     # FCLM metrics
#     fclm_hours = float(websites[FCLM]['total-paid-hours']['total'])
    
#     print(f'IQQA Hours: {float(fclm_hours)}')

# except TypeError as e:
#     print(f"Error: Failed to process FCLM metrics. {e}")

# print(f"Pick Andons: {pick_andons}")
# print(f"CC Andons: {CC_andons}")
# print(f"SBC Accuracy: {SBC_accuracy}")
# print(f"CC Completed: {count_completion[0]}\nSBC Completed: {count_completion[1]}")




# import pandas as pd

# # Mock data
# inbound_1_3 = 100
# inbound_3_5 = 75
# inbound_gt_5 = 50
# outbound_1_3 = 80
# outbound_3_5 = 60
# outbound_gt_5 = 40
# unit_HOVReject = 20
# unit_MDPReject = 15
# unit_TransDELETE = 10
# count_MDPReject = 5
# count_TransDELETE = 8
# CC = 200
# SBC = 150
# fclm_hours = 35.5
# pick_andons = 25
# CC_andons = 30

# def get_column():
#     from datetime import datetime
#     now = datetime.now()
#     hour = now.hour
#     if 9 <= hour < 18:
#         # Convert hour to Excel column (A=1, B=2, ...)
#         return chr(ord('C') + hour - 9)
#     else:
#         return None  # Return None for hours outside of 9 AM to 5 PM

# def write_to_excel(data, filename):
#     column = get_column()
#     if column:
#         # Create a DataFrame from the data
#         df = pd.DataFrame(columns=['Data'])
#         # Create a dictionary to map each piece of data to its row
#         cell_mapping = {
#             inbound_1_3: '5',
#             inbound_3_5: '6',
#             inbound_gt_5: '7',
#             outbound_1_3: '10',
#             outbound_3_5: '11',
#             outbound_gt_5: '12',
#             unit_HOVReject: '25',
#             unit_MDPReject: '24',
#             unit_TransDELETE: '26',
#             count_MDPReject: '22',
#             count_TransDELETE: '23',
#             CC: '14',
#             SBC: '13',
#             # fclm_hours: '4',
#             pick_andons: '27',
#             CC_andons: '19'
#         }
#         # Write data to cells based on the cell mapping
#         for value, row in cell_mapping.items():
#             df.at[row, column] = value
#         # Write the DataFrame to the specified Excel file
#         df.to_excel(filename, index=False)
#         print(f"Data written to {filename}.")
#     else:
#         print("Data could not be written. Time is outside of 9 AM to 4 PM.")

# # Specify the filename to write to
# filename = r"C:\Users\nuneadon.ANT\Desktop\Reporting_Sheet - Copy.xlsx"

# data = [inbound_1_3, inbound_3_5, inbound_gt_5, outbound_1_3, outbound_3_5, outbound_gt_5, 
#         unit_HOVReject, unit_MDPReject, unit_TransDELETE, count_MDPReject, count_TransDELETE, 
#         CC, SBC, fclm_hours, pick_andons, CC_andons]
# filename = r"C:\Users\nuneadon.ANT\Desktop\Reporting_Sheet - Copy.xlsx"
# write_to_excel(data, filename)

