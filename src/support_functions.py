# -*- coding: utf-8 -*-
# Path: src/support_functions.py
# Authors: Esther Manzano, Albert Queraltó

"""
This is module contains all classes and methods that act as general utilities.
It contains class extensions, wrapper functions and file utils.
"""

import os
import csv
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains

# Custom libraries
from navigation import *
from data_scraper import *


class ExtendedActions(ActionChains):
    """
    Extends the functionality of the ActionChains method from the Selenium WebDriver.
    Source: https://stackoverflow.com/questions/53467739/how-to-implement-method-chaining-of-selenium-multiple-webdriverwait-in-python
    """
    def wait(self, second, condition):
        element = WebDriverWait(self._driver, second).until(condition)
        self.move_to_element(element)
        return self


class WrapperFunctionsMercadoPrecios(object):
    """
    Contains functions with the program logic and other utilities to scrape the *Mercado y precios* website.
    """
    
    def __init__(self, date, max_hour, mercado_precio_nav, driver):
        self.date = date
        self.max_hour = max_hour
        self.mercado_precio_nav = mercado_precio_nav
        self.driver = driver
        
        self.market_price = {'date': [], 'hour': [],
                        'avg total price (euro/MWh)': [],
                        'avg price free market (euro/MWh)': [],
                        'avg price reference market (euro/MWh)': [],
                        'energy total (MWh)': [],
                        'energy free market (MWh)': [],
                        'energy reference market (MWh)': [],
                        'free market share (%)': [],
                        'reference market share (%)': []
            }
        
        
    def hour_iterator_mercado_precios(self) -> dict:
        """
        Iterates over the hours in the *Mercado y precios* webpage.

        Parameters:
        -----------
        self.driver: WebDriver object.
            The webdriver that will be used to scrape the webpage.
        self.max_hour: int.
            The maximum hour (+1) to iterate over.
            
        Returns:
        --------
        self.market_price: dict.
            The data of market prices.
        """
        
        # Iterate through the hour elements and select the right hour from the drop down menu list
        for i in range(self.max_hour):
            self.mercado_precio_nav.hour_selection_mercados_precios(list_index=i)
            mercado_precio = MercadoPreciosData(driver=self.driver)
            time.sleep(5)
            
            # Get the information of prices, energy and shares from *Mercado y precios* page
            pm_total, pm_com_libre, pm_com_ref = mercado_precio.get_precio_final_energia()
            energia_total, energia_com_libre, energia_com_ref = mercado_precio.get_energia()
            cuota_com_libre, cuota_com_ref = mercado_precio.get_cuota()
            
            # Append data to dictionary
            self.market_price['date'].append(self.date)
            self.market_price['hour'].append(f"{'0' if i < 10 else ''}{i}:00")
            self.market_price['avg total price (euro/MWh)'].append(pm_total)
            self.market_price['avg price free market (euro/MWh)'].append(pm_com_libre)
            self.market_price['avg price reference market (euro/MWh)'].append(pm_com_ref)
            self.market_price['energy total (MWh)'].append(energia_total)
            self.market_price['energy free market (MWh)'].append(energia_com_libre)
            self.market_price['energy reference market (MWh)'].append(energia_com_ref)
            self.market_price['free market share (%)'].append(cuota_com_libre)
            self.market_price['reference market share (%)'].append(cuota_com_ref)
        return self.market_price
    
    
class WrapperFunctionsGeneracionConsumo(object):
    """
    Contains functions with the program logic and other utilities to scrape the *Generación y consumo* website.
    """
    
    def __init__(self, date, max_hour, generacion_consumo_nav, driver):
        self.date = date
        self.max_hour = max_hour
        self.generacion_consumo_nav = generacion_consumo_nav
        self.driver = driver
        
        self.renewable_data = {'date': [], 'hour': [],
                        'renewable generation (%)': [],
                        'renewable generation (MW)': [],
                        'wind generation (MW)': [],
                        'water generation (MW)': [],
                        'solar generation (MW)': [],
                        'nuclear generation (MW)': [],
                        'thermorenewable generation (MW)': []
            }
        
        
    def hour_iterator_generacion_libre_co2(self) -> pd.DataFrame():
        """
        Iterates over the hours in the *Generación y Consumo* webpage.

        Parameters:
        -----------
        self.driver: WebDriver object.
            The webdriver that will be used to scrape the webpage.
        self.max_hour: int.
            The maximum hour (+1) to iterate over.
            
        Returns:
        --------
        renewable_data_df: pd.DataFrame.
            The data of the renewable energy generation.
        """

        # Iterate through the hour elements and select the right hour from the drop down menu list
        for i in range(self.max_hour):
            self.generacion_consumo_nav.hour_selection_generacion_libre_co2(list_index=i)                
            generacion_consumo = GeneracionConsumoData(driver=self.driver)
            time.sleep(5)
            
            # Get the information of prices, energy and shares from *Generación y consumo* page
            percentage_renewable, renewable_power, wind_power, water_power, solar_power, nuclear_power, thermo_renewable_power = generacion_consumo.get_renewable_generation_data()

            # Append data to dictionary
            self.renewable_data['date'].append(self.date)
            self.renewable_data['hour'].append(f"{'0' if i < 10 else ''}{i}:00")
            self.renewable_data['renewable generation (%)'].append(percentage_renewable)
            self.renewable_data['renewable generation (MW)'].append(renewable_power)
            self.renewable_data['wind generation (MW)'].append(wind_power)
            self.renewable_data['water generation (MW)'].append(water_power)
            self.renewable_data['solar generation (MW)'].append(solar_power)
            self.renewable_data['nuclear generation (MW)'].append(nuclear_power)
            self.renewable_data['thermorenewable generation (MW)'].append(thermo_renewable_power)
            
        # Transform dictionary to dataframe and return it
        renewable_data_df = pd.DataFrame(self.renewable_data)
        return renewable_data_df
    

class FileUtils(object):
    def __init__(self, filename, dictionary) -> None:
        
        # Check if folder to store data exists otherwise create it
        if not os.path.exists('data'):
            os.makedirs('data')
            
        self.filename = os.path.join('data', filename)
        self.dictionary = dictionary
        
    def save_data(self):
        """
        Saves the data to a CSV file.
        """
        with open(self.filename, 'w', newline='\n') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(self.dictionary.keys())
            writer.writerows(zip(*self.dictionary.values()))
            
    def check_presence_read_data(self):
        """
        Checks if file is present in the folder and reads the data from a CSV file in order to store new columns to it using pandas
        """
        if os.path.exists(self.filename):
            pass