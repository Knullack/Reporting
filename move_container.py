import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from util.utilities import runtime
if __name__ == "__main__":
    session = chromeSession('hdc3', 12730876)
    containers = [

    ]

    for con in containers:
        # location = 'tsOpx03PS'
        print(f'{con} // {runtime(session.move_container, 200, con, 'dz-R-PICK-CLEAN-CAGE')}')

    session.close()
