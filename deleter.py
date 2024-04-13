import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from util.utilities import runtime
if __name__ == "__main__":
    session = chromeSession('hdc3', 12730876)
    containers = [
        
    ]
    for csX in containers:
        print(f'{csX} // {runtime(session.sideline_delete, csX, "TRASH")}')
    session.close()
