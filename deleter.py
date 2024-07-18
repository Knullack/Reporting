import sys
import os
from typing import Literal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from util.utilities import runtime, Container
if __name__ == "__main__":
    session = chromeSession('hdc3', 12730876)

    list_bins: list = [

    ]

    list_containers: list = [

    ]
        
    dict_containers: dict = {

    }

    def unbind(containers: list):
        for i, csX in enumerate(containers, start=1):
            print(f'{i}/{len(containers)}) // {(i/(len(containers)) * 100):.2f}% //{csX} // {runtime(session.unbindHierarchy, csX)}')
    
    def sideline(containers: list):
        for i, csX in enumerate(containers, start=1):
            print(f'{i}/{len(list_containers)}) // {(i/(len(containers)) * 100):.2f}% //{csX} // {runtime(session.sideline_delete, csX ,'TRASH')}')

    def moveContainer(containers: list, destination: str, dict: bool = False):
        if not dict:
            for i, csX in enumerate(containers, start=1):
                print(f'{i}/{len(containers)}) // {(i/(len(containers)) * 100):.2f}% // {csX} // {runtime(session.move_container, 200 , csX, destination)}')
        else:
            for i, (container, dest) in enumerate(dict_containers.items(), start=1):
                print(f'{i}/{len(dict_containers)}) // {(i/(len(dict_containers)) * 100):.2f}% // {container} -> {dest} // {runtime(session.move_container, 200, container, dest)}')

    def deleteItem(containers: list, mode: Literal['container', 'single']):
        for i, container in enumerate(containers, start=1):
            print(f'{i}/{len(containers)}) // {(i/(len(containers)) * 100):.2f}% //{container} // {runtime(session.deleteItem, container, mode)}')

    def containerData(containers: list, data: str, to_csv: bool = True):
        for i, container in enumerate(list_containers, start=1):
            print(f"{i}/{len(containers)}) // {(i/(len(containers)) * 100):.2f}% // {container} // {runtime(session.get_container_data, container, data, write_to_csv = to_csv)}")

    def resolve_andon(bin_ids: list):
        for i, bin in enumerate(bin_ids, start=1):
            print(f"{i}/{len(bin_ids)}) // { (i/(len(bin_ids)) * 100):.2f}% //{bin} // {runtime(session.andons, bin)}")
    
    def print_andons(bin_ids: list):
        for i, bin in enumerate(bin_ids, start=1):
            print(f"{i}/{len(bin_ids)}) // { (i/(len(bin_ids)) * 100):.2f}% //{bin} // {runtime(session.print_andons, bin, "http://localhost:5965/barcodegenerator")}")
            
    # deleteItem(list_containers, mode='container')
    # sideline(list_containers)
    # moveContainer(list_containers, destination='TRASH', dict=False)
    # containerData(list_containers, '')
    # unbind(list_containers)
    # resolve_andon(list_bins)
    print_andons(list_bins)
    session.close()
