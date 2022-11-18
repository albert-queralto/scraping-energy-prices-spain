# -*- coding: utf-8 -*-
# Path: src/__main__.py
# Authors: Esther Manzano, Albert Queraltó

"""
This is the main file to execute the bot used to scrape the website:
https://www.esios.ree.es/es

Two different areas of the site were scraped: *Mercados y precios* and
*Generación y consumo* The idea was to obtain daily data from energy prices, as
well as data from energy generation from renewable sources that can be later
analyzed or used to develop machine learning models.

Unit tests were used during the execution to find and handle any errors and
obtain additional information of those tests.
"""

import datetime
import pandas as pd
import random
import time

# Webscraping libraries
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Custom libraries
from navigation import *
from support_functions import *
from webdriver_utils import *

# Constants
URL = "https://www.ree.es/es"

# Checking robots.txt file of our chosen website
# Function get_robot_txt checks any url
def get_robot_txt(url):
    if url.endswith("/"):
        path = url
    else:
        path = url + "/"
    req = requests.get(path + "robots.txt", data=None)
    return req.text


# Read robots.txt file
# Print(get_robot_txt(URL))


class ElectricityScraper:
    """
    Contains the methods used to scrape data from: https://www.esios.ree.es/es.
    """

    def __init__(self, start_date, end_date):
        """
        Method that includes all the elements that are required during initialization.
        """
        
        # WebDriver options
        options = Options() 
        options.headless = (False)  # Option to show the browser window (True) or not (False)
        options.add_argument(f"user-agent={random.choice(WebDriverOptions.user_agents)}")  # Prevent being identified as a bot with custom User-Agents
        options.add_argument("content-type=application/x-www-form-urlencoded")

        # Initiate the webdriver, installs it if not present and implements the previous options
        self.driver = Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.set_page_load_timeout(30)
        self.base_url = ("https://www.esios.ree.es/es") # Base URL that we want to scrape
        
        # Generate a list with the period of time used to scrape the data
        # transform string dates to datetime and exclude the hour
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        self.delta = datetime.timedelta(days=1)
        self.dates_list_init = []
        
        while self.start_date <= self.end_date:
            self.dates_list_init.append(self.start_date.strftime("%Y-%m-%d"))
            self.start_date += self.delta
            
        self.dates_list = self.dates_list_init # The date_list variable will be overwritten depending on the presence of missing files


    def mercado_precios_scraper(self):
        """
        Method that implements the scraper for the *Mercado y precios* page.
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
        
        # Find missing files by looking in the directory.
        # If there are missing files, the date list is replaced with the list of missing dates
        files = os.listdir("data")        
        if files:
            # Initialize data_saver with empty values since we will not use them at this point
            # The data_saver will be initialized again later to save data. Here we only want
            # to find if there are missing files
            data_saver = FileUtils(filename='',dictionary={}) 
            data_saver.missing_mercados_precios(dates_list=self.dates_list)
        if len(data_saver.missing_files_mercados_precios) > 0:
            print("There are missing files for *Mercados y precios*. Starting the scraper on the missing dates...")
            self.dates_list = data_saver.missing_files_mercados_precios

        # Navigates through the defined date range
        for date in self.dates_list:
            print(f"Processing date: {date}")
            
            # Get the year, month and day. Pass it to the date navigator
            year = date.split("-")[0]
            month = date.split("-")[1]
            day = date.split("-")[2]

            mercado_precio_navigator.date_navigator(year=year, month=month, day=day)
            time.sleep(5)
            print(self.driver.current_url) # For debugging the correct URL

            # Wrapper method that contains the functionality to scrape the data from the *Mercados y precios* page
            market_prices_data_iterator = WrapperMercadoPrecios(date=date, max_hour=24, mercado_precio_nav=mercado_precio_navigator, driver=self.driver)
            market_price = market_prices_data_iterator.hour_iterator_mercado_precios()

            # Save the data of *Mercados y precios* to a CSV file for each day
            data_saver = FileUtils(filename=f'energy_prices_{date}.csv', dictionary=market_price)
            data_saver.save_data()
            
        # Check if there are missing files in the data folder after scraping of *Mercados y precios* is completed
        data_saver.missing_mercados_precios(date_list=self.dates_list_init)
            
        # If data_saver.missing_files_mercados_precios is not an empty list
        # Run the scraper again on the dates inside missing_files_mercados_precios
        # and save the data to a CSV file for each day
        if data_saver.missing_files_mercados_precios:
            print("There are missing files for *Mercados y precios*. Starting the scraper on the missing dates...")
            for date in data_saver.missing_files_mercados_precios:
                print(f"Processing date: {date}")
                
                # Get the year, month and day. Pass it to the date navigator
                year = date.split("-")[0]
                month = date.split("-")[1]
                day = date.split("-")[2]
                
                mercado_precio_navigator.date_navigator(year=year, month=month, day=day)
                time.sleep(5)
                print(self.driver.current_url)
                
                market_prices_data_iterator = WrapperMercadoPrecios(date=date, max_hour=24, mercado_precio_nav=mercado_precio_navigator, driver=self.driver)
                market_price = market_prices_data_iterator.hour_iterator_mercado_precios()
                data_saver = FileUtils(filename=f'energy_prices_{date}.csv', dictionary=market_price)
                data_saver.save_data()


    def generacion_consumo_scraper(self):
        """
        Method that implements the scraper for the *Generación y consumo* page.
        """

        # Initiate the navigation elements for the first page and open the Chrome session
        page_navigator = NavigationMain(driver=self.driver, base_url=self.base_url)
        page_navigator.open_chrome_session()
        time.sleep(1)

        # Go to the *Generación y consumo* page
        page_navigator.navigate_generacion_consumo()
        time.sleep(1)

        # Initiate the method to perform the hour selection in the *Generación y consumo* page
        generacion_consumo_navigator = NavigationGeneracionConsumo(driver=self.driver)

        # Find missing files by looking in the directory
        files = os.listdir("data")        
        if files:
            # Initialize data_saver with empty values since we will not use them at this point
            # The data_saver will be initialized again later to save data. Here we only want
            # to find if there are missing files
            data_saver = FileUtils(filename='', dictionary={}) 
            data_saver.missing_generacion_consumo(date_list=self.dates_list_init)
        if len(data_saver.missing_files_generacion_consumo) > 0:
            print("There are missing files for *Generación y consumo*. Starting the scraper on the missing dates...")
            self.dates_list = data_saver.missing_files_generacion_consumo
        else:
            self.dates_list = self.dates_list_init
        
        # Navigates through the defined date range
        for date in self.dates_list:
            print(f"Processing date: {date}")
            
            # Get the year, month and day. Pass it to the date navigator
            year = date.split("-")[0]
            month = date.split("-")[1]
            day = date.split("-")[2]

            try:
                # Check if date is in the file name and load the file of *Mercados y precios* as pandas dataframe
                file = [file for file in files if date in file]
                energy_prices = pd.read_csv(f"data/{file[0]}", sep=";")
            except Exception as e:
                print(f"{e}")
                continue

            # Initiate method to get the data from the *Generación y consumo* page and start the scraping process
            generacion_consumo_navigator.date_navigator(year=year, month=month, day=day)
            time.sleep(5)
            print(self.driver.current_url) # For debugging the correct URL
            
            renewable_data_iterator = WrapperGeneracionConsumo(date=date,max_hour=24,generacion_consumo_nav=generacion_consumo_navigator,driver=self.driver)
            renewable_data_df = renewable_data_iterator.hour_iterator_generacion_libre_co2()

            try:
                # Merge both dataframes and save the data to a CSV file for each day
                energy_prices = pd.merge(energy_prices, renewable_data_df, on=["date", "hour"])
                energy_prices.to_csv(f"data/energy_prices_renewable_generation_{date}.csv",index=False)
                
            except Exception as e:
                print(f"{e}")
                print("Retrying to save the file again.")
                renewable_data_df.to_csv(f"data/energy_prices_renewable_generation_{date}.csv",index=False)
                continue
            
            # Check if there are missing files in the data folder after scraping of *Mercados y precios* is completed
            data_saver.missing_generacion_consumo(date_list=self.dates_list_init)
            
            # If data_saver.missing_files_generacion_consumo is not empty list
            # Run the scraper again on the dates inside missing_files_generacion_consumo
            # and save the data to a CSV file for each day
            if data_saver.missing_files_generacion_consumo:
                print("There are missing files for *Generación y consumo*. Starting the scraper on the missing dates...")
                for date in data_saver.missing_files_generacion_consumo:
                    print(f"Processing date: {date}")
                    
                    # Get the year, month and day. Pass it to the date navigator
                    year = date.split("-")[0]
                    month = date.split("-")[1]
                    day = date.split("-")[2]
                    
                    generacion_consumo_navigator.date_navigator(year=year, month=month, day=day)
                    time.sleep(5)
                    print(self.driver.current_url) # For debugging the correct URL
                    
                    renewable_data_iterator = WrapperGeneracionConsumo(date=date, max_hour=24, 
                                        generacion_consumo_nav=generacion_consumo_navigator, driver=self.driver)
                    renewable_data_df = renewable_data_iterator.hour_iterator_generacion_libre_co2()

                    try:
                        energy_prices = pd.merge(energy_prices, renewable_data_df, on=["date", "hour"])
                        energy_prices.to_csv(f"data/energy_prices_renewable_generation_{date}.csv", index=False)
                    except Exception as e:
                        print(f"{e}")
                        renewable_data_df.to_csv(f"data/energy_prices_renewable_generation_{date}.csv",index=False)
                        continue
        
        # Merge all the files in the data folder, create the categorical column and save the data to a CSV file
        data_saver.file_merger()
        data_saver.create_categorical_column()
                

    def CloseDriver(self):
        """
        Method that includes all the instructions used after finishing
        to scrape the data.
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    # Set the period of time to scrape
    start_date = "2020-11-01"
    # end_date = "2022-10-31"
    end_date = "2020-11-03"
    
    electricity_scraper = ElectricityScraper(start_date=start_date, end_date=end_date)
    electricity_scraper.mercado_precios_scraper()
    electricity_scraper.generacion_consumo_scraper()
    electricity_scraper.CloseDriver()