import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from time import time

if __name__ == "__main__":
    start_time = time()
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
                "PPHOVReject": '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[1]/td[3]/span/a',
                "PPMDPReject": '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[2]/td[3]/span/a',
                "PPTransDELETE": '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[3]/td[3]/span/a'
            },
            "active-pickers": {
                "PPMDPReject" : '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[2]/td[5]/span/span',
                "PPTransDELETE" : '/html/body/div/div/div/awsui-app-layout/div/main/div/div[2]/div[2]/span/div/div[3]/div/div/awsui-table/div/div[3]/table/tbody/tr[3]/td[5]/span/span'
            }
        },
        "https://fc-quality-dashboard-iad.aka.amazon.com/management/count_density?work_type=CYCLE_COUNT": {
            "cycle count": {
                "all": '/html/body/div/table/tbody/tr[10]/td[3]/a'
            }
        },
        "https://fc-quality-dashboard-iad.aka.amazon.com/management/count_density?work_type=SIMPLE_BIN_COUNT": {
            "simple bin count" : {
                "all": '/html/body/div/table/tbody/tr[3]/td[3]/a'
            }
        }
        # need pick & CC andon csv downloader
    }
    
    all_values = {}
    
    for website, categories in websites.items():
        website_values = {}
        for category, xpaths in categories.items():
            category_values = {}
            for subcategory, xpath in xpaths.items():
                value = session.get_text(website, xpath)
                category_values[subcategory] = value
            website_values[category] = category_values
        all_values[website] = website_values

    session.close()


    elapsed_time = time() - start_time
    if elapsed_time < 60:
        print(f"Run time: {elapsed_time:.2f} seconds")
    elif elapsed_time >= 60:
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f"{minutes}m:{seconds}s")

        
    print("All Values:", all_values)