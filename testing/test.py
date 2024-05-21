import unittest
from unittest.mock import patch, MagicMock
import subprocess
from os import system
from Chrome_Session import chromeSession, Keys, EC, By
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
    
    # Test FCMenu login
    @patch('selenium.webdriver.Chrome.find_element')  # Mock finding elements
    def test_fcmenu_login(self, mock_find_element):
        # Simulate finding the badge input and performing actions
        input_element = MagicMock()
        mock_find_element.return_value = input_element
        
        self.chrome_session.driver = MagicMock()  # Simulate a Chrome driver
        self.chrome_session.FCMenu_login(self.badge)  # Attempt to login
        
        # Check if find_element was called with the expected XPath
        mock_find_element.assert_called_with('xpath', 'correct_xpath_for_badge_input')
        
        # Verify that the HELPER_type_and_click method is called with the badge and ENTER key
        input_element.send_keys.assert_any_call(str(self.badge))
        input_element.send_keys.assert_any_call(Keys.ENTER)
    
    # Test set_mode in the context of deleteItem
    @patch('selenium.webdriver.support.ui.WebDriverWait')  # Mock WebDriver interactions
    @patch('selenium.webdriver.Chrome.get')  # Mock navigation to avoid actual browsing
    def test_set_mode_in_deleteItem(self, mock_get, mock_wait):
        # Set up the initial state with navigation
        self.chrome_session.driver = MagicMock()  # Mock Chrome driver
        mock_get.return_value = None  # Simulate navigation to a specific URL
        self.chrome_session.navigate('https://aft-qt-na.aka.amazon.com/app/deleteitems?experience=Desktop')  # Set up navigation

        # Mock expected Selenium interactions
        current_mode_element = MagicMock()
        current_mode_element.text = 'single'  # The initial mode on the page
        mock_wait_instance = mock_wait.return_value
        mock_wait_instance.until.return_value = current_mode_element  # Return mock element for waiting

        # Call deleteItem, which should use set_mode
        self.chrome_session.deleteItem('some_container', 'container')  # Example call to set up mode change
        
        # Validate that the correct WebDriver interactions occurred
        mock_wait_instance.until.assert_any_call(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.menu)))  # Click menu
        mock_wait_instance.until.assert_any_call(EC.element_to_be_clickable((By.XPATH, locator.xpath.delete.btn_change_mode)))  # Click change mode
        mock_wait_instance.until.assert_any_call(EC.presence_of_element_located((By.XPATH, locator.xpath.delete.modes.container)))  # Change to container mode

        # Ensure the expected mode change interactions occur
        self.chrome_session.actions.move_by_offset.assert_called()  # Verify offset move occurred
        self.chrome_session.actions.perform.assert_called()  # Check that action was performed


    # Test closing Chrome
    @patch('os.system')  # Mock system calls for process termination
    def test_close_chrome(self, mock_system):
        self.chrome_session.driver = MagicMock()  # Simulate a Chrome driver
        self.chrome_session.close()  # Attempt to close Chrome
        
        # Check if the mock system call was used to terminate Chrome processes
        mock_system.assert_called_with('taskkill /F /IM chrome.exe > nul 2>&1')

# Run the tests
if __name__ == '__main__':
    unittest.main()
