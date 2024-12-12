import sys
import os

from threading import Thread
from typing import Literal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from util.utilities import runtime, andon_types

class run():
    def __init__(self, chrome_session) -> None:
        self.instance: chromeSession = chrome_session
        
    def unbind(self, containers: list):
        for i, csX in enumerate(containers, start=1):
            print(f'{i}/{len(containers)}) // {(i/(len(containers)) * 100):.2f}% // {csX} // {runtime(self.instance.unbindHierarchy, csX)}')
    
    def sideline(self, containers: list):
        for i, csX in enumerate(containers, start=1):
            print(f'{i}/{len(list_containers)}) // {(i/(len(containers)) * 100):.2f}% // {csX} // {runtime(self.instance.sideline_delete, csX ,'TRASH')}')

    def moveContainer(self, containers: list, destination: str, dict: bool = False):
        if not dict:
            for i, csX in enumerate(containers, start=1):
                print(f'{i}/{len(containers)}) // {(i/(len(containers)) * 100):.2f}% // {csX} // {runtime(self.instance.move_container, 200 , csX, destination)}')
        else:
            for i, (container, dest) in enumerate(dict_containers.items(), start=1):
                print(f'{i}/{len(dict_containers)}) // {(i/(len(dict_containers)) * 100):.2f}% // {container} -> {dest} // {runtime(self.instance.move_container, 200, container, dest)}')

    def deleteItem(self, containers: list, mode: Literal['container', 'single']):
        for i, container in enumerate(containers, start=1):
            total = len(containers)
            counter = f'{i}/{total}'
            percentage = round(i / total * 100, 2)
            print(f'{counter}) // {percentage}% // {container} // {runtime(self.instance.deleteItem, container, mode)}')

    def containerData(self, containers: list, data: str, to_csv: bool = True):
        for i, container in enumerate(containers, start=1):
            print(f"{i}/{len(containers)}) // {(i/(len(containers)) * 100):.2f}% // {container} // {runtime(self.instance.get_container_data, container, data, write_to_csv = to_csv)}")

    def resolve_andon(self, bin_ids: list, type: str):
        for i, bin in enumerate(bin_ids, start=1):
            print(f"{i}/{len(bin_ids)}) // { (i/(len(bin_ids)) * 100):.2f}% // {bin} // {runtime(self.instance.andons, bin, type)}")
    
    def print_andons(self, bin_ids: list, type: str):
        for i, bin in enumerate(bin_ids, start=1):
            print(f"{i}/{len(bin_ids)}) // { (i/(len(bin_ids)) * 100):.2f}% / {bin} // {runtime(self.instance.print_andons, bin, "http://localhost:5965/barcodegenerator", type)}")

    def labor_track(self, code: str , badge: str):
        self.instance.labor_track(code, badge)

    def rodeo_delete(self, dict_list: dict):
        for i, (sku, container) in enumerate(dict_list.items(), start=1):
            print(f'\n{i}/{len(dict_list)}) // {(i/(len(dict_list)) * 100):.2f}% // {container} :: {sku} // {runtime(session.rodeo_delete, container, sku)}\n')

    def close(self):
        self.instance.close()


if __name__ == "__main__":
    session = chromeSession('hdc3', 12730876, 1922, False)
    instance = run(session)

    list_bins: list = [

    ]

    list_containers: list = [

    ]
        
    dict_containers: dict = {

    }

    # instance.deleteItem(list_containers, mode='container')
    # instance.rodeo_delete(dict_containers)
    # instance.sideline(list_containers)
    # instance.moveContainer(list_containers, destination='TRASH', dict=False)
    # instance.containerData(list_containers, '')
    # instance.unbind(list_containers)
    # instance.print_andons(list_bins, andon_types.noScannableBarcode)
    instance.resolve_andon(list_bins, andon_types.unexpectedContainerOverage)

    instance.close()
