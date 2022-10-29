import unittest
import random
import time

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
        
        # Set days before the actual day to scrape
        self.num_previous_days = 40
        
    def test_scraper(self):
        """
        Function that implements the scraper.
        """
        page_navigator = Navigation(driver=self.driver, base_url=self.base_url)
        page_navigator.open_chrome_session()
        time.sleep(5)
        page_navigator.navigate_mercados_precios()
        time.sleep(5)
        
        # Navigates through the dates
        for year, month, day in [datetime.datetime.today() - datetime.timedelta(days=day) for day in range(self.num_previous_days)]

            # Dictionary that maps month numbers to strings
            month_mapper = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
            month = month_mapper[month] # Transform month to string using month_mapper dictionary
            
            page_navigator.date_picker(year, month, day)
            time.sleep(5)
        
    def tearDown(self):
        """
        Method that includes all the instructions used after the unittest is performed.
        """
        self.driver.close() # We close the driver
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')