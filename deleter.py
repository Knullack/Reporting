import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from time import time

if __name__ == "__main__":
    download_dir = r"C:\Users\nuneadon.ANT\Downloads"
    session = chromeSession(12730876)
    session.start()
    containers = ['csXPH4KHYQ6',
    'csXGY8oCdgg',
    'csXGXP7JXWz',
    'csXTh0KK6pW',
    ]
    qty = len(containers)
    for csX in containers:
        start_time = time()
        session.deleteItem(csX, qty)
        elapsed_time = time() - start_time
        if elapsed_time < 60:
            print(f"Runtime: {elapsed_time:.2f} seconds")
        elif elapsed_time >= 60:
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            print(f"Runtime: {minutes}m:{seconds}s")
