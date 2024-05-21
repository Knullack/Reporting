import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from util.utilities import runtime
if __name__ == "__main__":
    session = chromeSession('hdc3', 12730876)
    containers = [
'tsX0fw04wjm',
'csXz6PT2CRC',
'csXz5PT2CRC',
'csXTz0Ma8DI',
'csXRlHg3K1t',
'csXPJHT3QG8',
'csXPJFVBG5F',
'csXPJF6R9C5',
'csXPHNPCVRR',
'csXPHM7MRLC',
'csXKv48YVkA',
'csXGjKRGmJV',
'csX9KYS7Kzs'
    ]
    for i, con in enumerate(containers):
        print(f'{i}/{len(containers)}) //  {con} // {runtime(session.move_container, 200, con, 'TRASH')}')

    session.close()
