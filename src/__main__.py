import unittest
import random
import time
import datetime

# Webscraping libraries
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Custom libraries
from navigation import *
from data_scraper import *
from webdriver_utils import *

"""
https://tarifaluzhora.es/
https://www.esios.ree.es/es
https://www.ree.es/es/datos/aldia
"""

class ElectricityScraper(unittest.TestCase):
    # We will use the unittest library to check if there are any errors during the execution of the Crawler, allowing for better debugging.
    def setUp(self):
        """
        Method that includes all the elements that the test each test requires for execution.
        Similar to the __init__ method.
        """
        options = Options() # Define custom options for the WebDriver
        options.headless = False # Option to show the browser window (True) or not (False)
        options.add_argument(f'user-agent={random.choice(WebDriverOptions.user_agents)}') # Setup a custom User-Agent to prevent detection
        options.add_argument("content-type=application/x-www-form-urlencoded") # Setup content-type
        
        # Initiate the webdriver, installs it if not present and implements the previous options
        self.driver = Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=options)
        self.driver.set_page_load_timeout(30)
        self.base_url = 'https://www.esios.ree.es/es' # Base URL that we want to scrape
        
        # Set days before the actual day to scrape and create a list of dates and transform them to tuples
        self.num_previous_days = 40
        self.date_range = [datetime.datetime.today() - datetime.timedelta(days=day) for day in range(self.num_previous_days)]
        self.date_range = [(date.year, date.month, date.day) for date in reversed(self.date_range)]
        
    def test_scraper(self):
        """
        Function that implements the scraper.
        """
        page_navigator = Navigation(driver=self.driver, base_url=self.base_url)
        page_navigator.open_chrome_session()
        time.sleep(1)
        page_navigator.navigate_mercados_precios()
        time.sleep(1)
        
        # Navigates through the defined dates
        for year, month, day in self.date_range:
            page_navigator.date_navigator(year=year, month=month, day=day)
            print(self.driver.current_url)
            time.sleep(5)
        
    def tearDown(self):
        """
        Method that includes all the instructions used after the unittest is performed.
        """
        self.driver.close() # We close the driver
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')