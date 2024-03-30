import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from time import time

if __name__ == "__main__":
    download_dir = r"C:\Users\nuneadon.ANT\Downloads"
    session = chromeSession(12730876)
    session.start()
    containers = [
        'csXRtM25RbM',
        'csXRtMZThgM',
        'csXRtM8bSLL',
        'csXRtMpXJXL',
        'csXRtM6h3xx',
        'csXRtMCTVJg',
        'csXRtMPFwXg',
        'csXRtMjlVMx',
        'csXRtM9Dxgq',
        'csXRtMS2SfG',
        'csXTg0P133u',
        'csXTa0Ox1Nu',
        'csXPJBKRQM9',
        'csXRCCn2k67',
        'csXPJJP6RLS',
        'csXPJJP6P4M',
        'csXTH0Q70LI',
        'csXTV0L6F9C',
        'csXPJJKCK2B',
        'csXPJJKGY58',
        'csXPJH2663F',
        'csXPJH265TQ',
        'csXTo0R2j5w',
        'csXPJHBPJH6',
        'csXTi0Jn5Iy',
        'csXTj0No4QM',
        'csXPJJH9TZT',
        'csXPJJP8M2D',
        'csXTi0Jn5Iy',
        'csXPJHJLY95',
        'csXPJHFXYYB',
        'csXPJHFXZFT',
        'csXRtMm1nML',
        'csXRtMMSrTZ',
        'csXPJJKCHNB',
        'csXPJBKRVLX',
        'csXTC0Q7c4O',
        'csXTR0R1j5q',
        'csXRCC6MP5l',
        'csXRCCpZgjF',
        'csXG3c3wbK4'
]
    qty = len(containers)
    for csX in containers:
        start_time = time()
        session.deleteItem(csX)
        elapsed_time = time() - start_time
        if elapsed_time < 60:
            print(f"Runtime: {elapsed_time:.2f} seconds")
        elif elapsed_time >= 60:
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            print(f"Runtime: {minutes}m:{seconds}s")
