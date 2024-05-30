import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from collections import Counter
from Chrome_Session import chromeSession
from util.utilities import runtime
if __name__ == "__main__":
    session = chromeSession('hdc3', 12730876)
    # 'fnsku' : 'scannable_id',
    containers: dict = {

    }

    for i, (sku, container) in enumerate(containers.items(), start=1):
        print(f'{i}/{len(containers)} {container} :: {sku} // {runtime(session.rodeo_delete, container, sku)}')
    session.close()
