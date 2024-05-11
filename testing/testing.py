import unittest
from unittest.mock import patch, MagicMock
import subprocess
from os import system
from Chrome_Session import chromeSession
from util.utilities import locator

# Test class for chromeSession
class TestChromeSession(unittest.TestCase):
    def setUp(self):
        # Set up any initial conditions here
        self.site = "hdc3"
        self.badge = 12345
        self.chrome_session = chromeSession(self.site, self.badge)

    def tearDown(self):
        # Clean up after each test
        self.chrome_session.close()  # Ensure Chrome processes are properly terminated
    
    def test_setUp(self):
        # Set up any initial conditions here
        self.site = "hdc3"
        self.badge = 12345
        self.chrome_session = chromeSession(self.site, self.badge)
        
    # Test navigation to a URL
    @patch('selenium.webdriver.Chrome.get')  # Mock the get method to avoid actual navigation
    def test_navigate(self, mock_get):
        test_url = "https://www.google.com/"
        # self.chrome_session.driver = MagicMock()  # Simulate a Chrome driver
        self.chrome_session.navigate(test_url)
        
        # Check if the mock 'get' method was called with the correct URL
        mock_get.assert_called_with(test_url)
    
# Run the tests
if __name__ == '__main__':
    unittest.main()
