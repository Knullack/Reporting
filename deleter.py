import sys
import os
from typing import Literal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from util.utilities import runtime
if __name__ == "__main__":
    session = chromeSession('hdc3', 12730876)
    list_containers: list = [

    ]
    dict_containers: dict = {

    }

    def unbind(containers: list):
        for i, csX in enumerate(containers, start=1):
            print(f'{i}/{len(containers)}) {csX} // {runtime(session.unbindHierarchy, csX)}')
    
    def sideline(containers: list):
        for i, csX in enumerate(containers, start=1):
            print(f'{i}/{len(list_containers)}) {csX} // {runtime(session.sideline_delete, csX ,'TRASH')}')

    def moveContainer(containers: list, destination: str):
        for i, csX in enumerate(containers, start=1):
            print(f'{i}/{len(containers)}) {csX} // {runtime(session.move_container, 200 , csX, destination)}')

    def deleteItem(containers: list, mode: Literal['container', 'single']):
        for i, container in enumerate(containers, start=1):
            print(f'{i}/{len(containers)} // {container} // {runtime(session.deleteItem, container, mode)}')

    def get_consumer(containers: list):
        for i, container in enumerate(list_containers, start=1):
            print(f"{i}/{len(containers)}) // {container} // {runtime(session.get_container_consumer, container)}")

    # deleteItem(list_containers, mode='container')
    # sideline(list_containers)
    # moveContainer(list_containers, destination='TRASH')
    # get_consumer(list_containers)
    session.close()
