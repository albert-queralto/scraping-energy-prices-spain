# -*- coding: utf-8 -*-
# Path: src/__main__.py
# Authors: Esther Manzano, Albert Queraltó

"""
This is the main file to execute the bot used to scrape the website: https://www.esios.ree.es/es

Two different areas of the site were scraped: *Mercados y precios* and *Generación y consumo*
The idea was to obtain daily data from energy prices, as well as data from energy generation 
from renewable sources that can be later analyzed or used to develop machine learning models.

Unit tests were used during the execution to find and handle any errors and obtain additional
information of those tests.
"""

import unittest
import random
import time
import datetime
import pandas as pd

# Webscraping libraries
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Custom libraries
from navigation import *
from webdriver_utils import *
from support_functions import *


def order_unittests():
    """
    Allows to control the order in which unittests are performed. Works as a decorator function to be applied on the unittests.
    Source: https://codereview.stackexchange.com/questions/122532/controlling-the-order-of-unittest-testcases
    """
    ordered_tests = {}
    
    def ordered_unittests(f):
        ordered_tests[f.__name__] = len(ordered_tests)
        return f
    
    def compare_order_unittests(a, b):
        return [1, -1][ordered_tests[a] < ordered_tests[b]]

    return ordered_unittests, compare_order_unittests

# Define the order of unittests
ordered_unittests, compare_order_unittests = order_unittests()
unittest.defaultTestLoader.sortTestMethodsUsing = compare_order_unittests


class ElectricityScraper(unittest.TestCase):
    """
    Contains the methods used to scrape data from: https://www.esios.ree.es/es
    The unittest library is used to check for any errors during the execution of the crawler, allowing for better debugging.
    """
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
        self.num_previous_days = 346
        self.date_range = [datetime.datetime.today() - datetime.timedelta(days=day) for day in range(self.num_previous_days)]
        self.date_range = [(date.year, date.month, date.day) for date in reversed(self.date_range)]
                
    @ordered_unittests
    def test_mercado_precios_scraper(self):
        """
        Function that implements the scraper for the *Mercado y precios* page.
        """
        
        # Initiate the navigation elements for the first page and open the Chrome session
        page_navigator = NavigationMain(driver=self.driver, base_url=self.base_url)
        page_navigator.open_chrome_session()
        time.sleep(1)
        
        # Go to the *Mercados y precios* page
        page_navigator.navigate_mercados_precios()
        time.sleep(1)
        
        # Initiate the method to perform the hour selection in the *Mercados y precios* page
        mercado_precio_navigator =  NavigationMercadosPrecios(driver=self.driver)
        
        # Navigates through the defined date range
        for year, month, day in self.date_range:
            date = f"{day}-{month}-{year}" # Create the date variable
            
            # Initiate method to get the data from the *Mercados y precios* page
            mercado_precio_navigator.date_navigator(year=year, month=month, day=day)
            time.sleep(5)
            print(self.driver.current_url) # For debugging
            
            market_prices_data_iterator = WrapperFunctionsMercadoPrecios(date=date, max_hour=24, mercado_precio_nav=mercado_precio_navigator, driver=self.driver)
            market_price = market_prices_data_iterator.hour_iterator_mercado_precios()
                
            # Save the data to a CSV file for each day
            data_saver = FileUtils(filename=f'energy_prices_{date}.csv', dictionary=market_price)
            data_saver.save_data()
            
    # @ordered_unittests
    # def test_generacion_consumo_scraper(self):
    #     """
    #     Function that implements the scraper for the *Generación y consumo* page.
    #     """
        
    #     # Initiate the navigation elements for the first page and open the Chrome session
    #     page_navigator = NavigationMain(driver=self.driver, base_url=self.base_url)
    #     page_navigator.open_chrome_session()
    #     time.sleep(1)
        
    #     # Go to the *Generación y consumo* page
    #     page_navigator.navigate_generacion_consumo()
    #     time.sleep(1)
        
    #     # Initiate the method to perform the hour selection in the *Generación y consumo* page
    #     generacion_consumo_navigator =  NavigationGeneracionConsumo(driver=self.driver)
        
    #     # Create list with all files in the save directory
    #     files = os.listdir('data')
        
    #     # Navigates through the defined date range
    #     for year, month, day in self.date_range:
    #         date = f"{day}-{month}-{year}" # Create the date variable
            
    #         # Check if day, month and year are in the file name and load the file
    #         file = [file for file in files if date in file]
    #         energy_prices = pd.read_csv(f"data/{file[0]}", sep=";")
            
    #         # Initiate method to get the data from the *Generación y consumo* page
    #         generacion_consumo_navigator.date_navigator(year=year, month=month, day=day)
    #         time.sleep(5)
    #         print(self.driver.current_url) # For debugging
            
    #         renewable_data_iterator = WrapperFunctionsGeneracionConsumo(date=date, max_hour=24, generacion_consumo_nav=generacion_consumo_navigator, driver=self.driver)
    #         renewable_data_df = renewable_data_iterator.hour_iterator_generacion_libre_co2()
            
    #         energy_prices = pd.merge(energy_prices, renewable_data_df, on=['date', 'hour'])
            
    #         # Save the data to a CSV file for each day
    #         energy_prices.to_csv(f"data/energy_prices_renewable_generation_{date}.csv", index=False)


    def tearDown(self):
        """
        Method that includes all the instructions used after the unittest is performed.
        """
        # Close and quit the driver
        self.driver.close() 
        self.driver.quit() 
        
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')