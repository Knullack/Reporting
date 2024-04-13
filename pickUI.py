import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
from util.utilities import runtime


if __name__ == "__main__":
    session = chromeSession('hdc3',12730876)
    for i in range(1000):
        time, csX = runtime(session.pickUI, vehicle='veCG00201', cage='paXCG00201', dirtyVehicle_dz_location='veCG00245', deleted_container_to_dz='TRASH')
        print(f' {csX}\n{'-' * 47}\n')
        # print(runtime(session.PAWS_tradional_picking))
    session.close()
