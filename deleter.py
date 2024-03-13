import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession
session = chromeSession(12730876)
session.start()
session.deleteItem(100)
