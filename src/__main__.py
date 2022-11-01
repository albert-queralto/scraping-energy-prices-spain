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
        self.driver = Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.set_page_load_timeout(30)
        self.base_url = 'https://www.esios.ree.es/es' # Base URL that we want to scrape
        
        # Set days before the actual day to scrape and create a list of dates and transform them to tuples
        self.num_previous_days = 2
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
            
            # Initialize the variables
            date = f"{day}-{month}-{year}" # Create the date variable
            date_data = {'date': [], 'hour': [],
                        'avg total price (euro/MWh)': [],
                        'avg price free market (euro/MWh)': [],
                        'avg price reference market (euro/MWh)': [],
                        'energy total (MWh)': [],
                        'energy free market (MWh)': [],
                        'energy reference market (MWh)': [],
                        'free market share (%)': [],
                        'reference market share (%)': []
            }
            
            page_navigator.date_navigator(year=year, month=month, day=day)
            time.sleep(5)
            print(self.driver.current_url)
            
            for i in range(24):
                page_navigator.hour_selection_mercados_precios(list_index=i)                
                mercado_precio = MercadoPreciosData(driver=self.driver)
                time.sleep(5)
                
                pm_total, pm_com_libre, pm_com_ref = mercado_precio.get_precio_final_energia()
                energia_total, energia_com_libre, energia_com_ref = mercado_precio.get_energia()
                cuota_com_libre, cuota_com_ref = mercado_precio.get_cuota()
                
                # Append data to dictionary that will be used to save it into a file
                date_data['date'].append(date)
                date_data['hour'].append(f"{'0' if i < 10 else ''}{i}:00")
                date_data['avg total price (euro/MWh)'].append(pm_total)
                date_data['avg price free market (euro/MWh)'].append(pm_com_libre)
                date_data['avg price reference market (euro/MWh)'].append(pm_com_ref)
                date_data['energy total (MWh)'].append(energia_total)
                date_data['energy free market (MWh)'].append(energia_com_libre)
                date_data['energy reference market (MWh)'].append(energia_com_ref)
                date_data['free market share (%)'].append(cuota_com_libre)
                date_data['reference market share (%)'].append(cuota_com_ref)

            # Save the data to a CSV file for each day
            data_saver = SaveUtils(filename=f'energy_prices_{date}.csv', dictionary=date_data)
            data_saver.save_data()

    def tearDown(self):
        """
        Method that includes all the instructions used after the unittest is performed.
        """
        self.driver.close() # We close the driver
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')