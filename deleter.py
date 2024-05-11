import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from util.utilities import runtime
if __name__ == "__main__":
    session = chromeSession('hdc3', 12730876)
    # containers = [
        
    # ]
    containers = {
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
    }
    # for i, csX in enumerate(containers, start=1):
    #     print(f'{i}) {csX} // {runtime(session.unbindHierarchy, csX)}')
    
    # for i, csX in enumerate(containers, start=1):
    #     print(f'{i}) {csX} // {runtime(session.sideline_delete, csX, 'TRASH')}')

    for i, csX in enumerate(containers, start=1):
        print(f'{i}/{len(containers)}) {csX} // {runtime(session.sideline_delete, csX ,'TRASH')}')

    # for i, csX in enumerate(containers, start=1):
    #     print(f'{i}/{len(containers)}) {csX} // {runtime(session.move_container, 200 , csX,'TRASH')}')

    # for location, item in containers.items():
    #     print(f'{location}: {item}\n{runtime(session.deleteItem, location, 'single', item)}')

    session.close()
