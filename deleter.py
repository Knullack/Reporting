import sys
import os
from typing import Literal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from util.utilities import runtime
if __name__ == "__main__":
    session = chromeSession('hdc3', 12730876)
    list_containers: list = [
'csXPHMTRMZ9',
'csXPHRT8RBD',
'csXGUz1DULr',
'csXPH29TVY2',
'csXPH29TVVK',
'csXPH29TW26',
'csXPH29TW3M',
'csXPHVX6H4S',
'csXGJ01txU4'

    ]
    dict_containers: dict = {

    }

    def unbind():
        for i, csX in enumerate(list_containers, start=1):
            print(f'{i}) {csX} // {runtime(session.unbindHierarchy, csX)}')
    
    def sideline():
        for i, csX in enumerate(list_containers, start=1):
            print(f'{i}/{len(list_containers)}) {csX} // {runtime(session.sideline_delete, csX ,'TRASH')}')

    def moveContainer(destination: str):
        for i, csX in enumerate(list_containers, start=1):
            print(f'{i}/{len(list_containers)}) {csX} // {runtime(session.move_container, 200 , csX, destination)}')

    def deleteItem(mode: Literal['container', 'single']):
        for i, container in enumerate(list_containers):
            print(f'{i}/{len(list_containers)} // {container} // {runtime(session.deleteItem, container, mode)}')


    # deleteItem('container')
    sideline()
    moveContainer('TRASH')
    session.close()
