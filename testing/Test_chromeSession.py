import unittest
from selenium import webdriver
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Chrome_Session import chromeSession

class TestChromeSession(unittest.TestCase):
    def setUp(self):
        self.session = chromeSession(badge=12345)  # Replace 12345 with the actual badge number
        self.session.start()

    def tearDown(self):
        self.session.close()

    def test_session_start(self):
        self.assertIsNotNone(self.session.driver, "Session should start successfully")

    def test_FCMenu_login(self):
        # Define your test logic here
        # For example:
        # self.session.FCMenu_login(self.session.driver, "your_username")
        # Add assertions to verify login behavior
        pass

    # Add more test cases as needed...

if __name__ == '__main__':
    unittest.main(verbosity=2)