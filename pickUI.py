import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from time import time
from datetime import datetime

if __name__ == "__main__":
    session = chromeSession(12730876)
    for i in range(1000):
        start_time = time()
        csX = session.pickUI('veCG00003', 'paXCG00003')
        elapsed_time = time() - start_time
        if elapsed_time < 60:
            print(f"{datetime.now()} // Runtime: {elapsed_time:.2f} seconds // {csX} DELETED\n{'-' * 47}\n")
        elif elapsed_time >= 60:
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            print(f"Runtime: {minutes}m:{seconds}s")
    session.close()
