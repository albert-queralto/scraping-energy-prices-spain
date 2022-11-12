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


class WrapperMercadoPrecios(object):
    """
    Contains methods with the program logic and other utilities to scrape the *Mercado y precios* website.
    """

    def __init__(self, date, max_hour, mercado_precio_nav, driver):
        self.date = date
        self.max_hour = max_hour
        self.mercado_precio_nav = mercado_precio_nav
        self.driver = driver

        self.market_price = {
            "date": [], "hour": [], "avg total price (euro/MWh)": [], "avg price free market (euro/MWh)": [],
            "avg price reference market (euro/MWh)": [], "energy total (MWh)": [], "energy free market (MWh)": [],
            "energy reference market (MWh)": [], "free market share (%)": [], "reference market share (%)": []
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

            # If returned value of self.mercado_precio_nav.hour_selection_mercados_precios() is False
            # Then, the amount of attempts for that hour has been exceeded indicating that the hour
            # is not available and will be skipped
            if self.mercado_precio_nav.hour_selection_mercados_precios(list_index=i) is False:
                # Append empty data to dictionary
                self.market_price["date"].append(self.date)
                self.market_price["hour"].append(f"{'0' if i < 10 else ''}{i}:00")
                self.market_price["avg total price (euro/MWh)"].append("-")
                self.market_price["avg price free market (euro/MWh)"].append("-")
                self.market_price["avg price reference market (euro/MWh)"].append("-")
                self.market_price["energy total (MWh)"].append("-")
                self.market_price["energy free market (MWh)"].append("-")
                self.market_price["energy reference market (MWh)"].append("-")
                self.market_price["free market share (%)"].append("-")
                self.market_price["reference market share (%)"].append("-")
                continue
            else:
                # If the hour is found, scrape the data                    
                mercado_precio = MercadoPreciosData(driver=self.driver)
                time.sleep(5)

                # Get the information of prices, energy and shares from *Mercado y precios* page
                pm_total, pm_com_libre, pm_com_ref = mercado_precio.get_precio_final_energia()
                energia_total, energia_com_libre, energia_com_ref = mercado_precio.get_energia()
                cuota_com_libre, cuota_com_ref = mercado_precio.get_cuota()

                # Append data to dictionary
                self.market_price["date"].append(self.date)
                self.market_price["hour"].append(f"{'0' if i < 10 else ''}{i}:00")
                self.market_price["avg total price (euro/MWh)"].append(pm_total)
                self.market_price["avg price free market (euro/MWh)"].append(pm_com_libre)
                self.market_price["avg price reference market (euro/MWh)"].append(pm_com_ref)
                self.market_price["energy total (MWh)"].append(energia_total)
                self.market_price["energy free market (MWh)"].append(energia_com_libre)
                self.market_price["energy reference market (MWh)"].append(energia_com_ref)
                self.market_price["free market share (%)"].append(cuota_com_libre)
                self.market_price["reference market share (%)"].append(cuota_com_ref)
        return self.market_price


class WrapperGeneracionConsumo(object):
    """
    Contains methods with the program logic and other utilities to scrape the *Generación y consumo* website.
    """

    def __init__(self, date, max_hour, generacion_consumo_nav, driver):
        self.date = date
        self.max_hour = max_hour
        self.generacion_consumo_nav = generacion_consumo_nav
        self.driver = driver

        self.renewable_data = {
            "date": [], "hour": [], "renewable generation (%)": [], "renewable generation (MW)": [],
            "wind generation (MW)": [], "water generation (MW)": [], "solar generation (MW)": [],
            "nuclear generation (MW)": [], "thermorenewable generation (MW)": []
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

        # Iterate through the hour elements and select the right hour from the
        # drop down menu list
        for i in range(self.max_hour):
            self.generacion_consumo_nav.hour_selection_generacion_libre_co2(list_index=i)
            
            # If returned value of self.generacion_consumo_nav.hour_selection_generacion_libre_co2() is False
            # Then, the amount of attempts for that hour has been exceeded indicating that the hour
            # is not available and will be skipped
            if self.generacion_consumo_nav.hour_selection_generacion_libre_co2(list_index=i) is False:
                # Append empty data to dictionary
                self.renewable_data["date"].append(self.date)
                self.renewable_data["hour"].append(f"{'0' if i < 10 else ''}{i}:00")
                self.renewable_data["renewable generation (%)"].append("-")
                self.renewable_data["renewable generation (MW)"].append("-")
                self.renewable_data["wind generation (MW)"].append("-")
                self.renewable_data["water generation (MW)"].append("-")
                self.renewable_data["solar generation (MW)"].append("-")
                self.renewable_data["nuclear generation (MW)"].append("-")
                self.renewable_data["thermorenewable generation (MW)"].append("-")
                continue
            else:
                # If the hour is found, scrape the data
                generacion_consumo = GeneracionConsumoData(driver=self.driver)
                time.sleep(5)

                # Get the information of prices, energy and shares from *Generación y consumo* page
                percentage_renewable, renewable_power, wind_power, water_power, solar_power, nuclear_power, thermo_renewable_power = \
                                                                                            generacion_consumo.get_renewable_generation_data()

                # Append data to dictionary
                self.renewable_data["date"].append(self.date)
                self.renewable_data["hour"].append(f"{'0' if i < 10 else ''}{i}:00")
                self.renewable_data["renewable generation (%)"].append(percentage_renewable)
                self.renewable_data["renewable generation (MW)"].append(renewable_power)
                self.renewable_data["wind generation (MW)"].append(wind_power)
                self.renewable_data["water generation (MW)"].append(water_power)
                self.renewable_data["solar generation (MW)"].append(solar_power)
                self.renewable_data["nuclear generation (MW)"].append(nuclear_power)
                self.renewable_data["thermorenewable generation (MW)"].append(thermo_renewable_power)
        renewable_data_df = pd.DataFrame(self.renewable_data)
        return renewable_data_df

class FileUtils(object):
    def __init__(self, filename, dictionary) -> None:

        # Check if folder to store data exists otherwise create it
        if not os.path.exists("data"):
            os.makedirs("data")

        # Initialize variables to save data or check missing files
        self.filename = os.path.join("data", filename)
        self.dictionary = dictionary
        self.missing_files_mercados_precios = []
        self.missing_files_generacion_consumo = []

    def save_data(self):
        """
        Saves the data to a CSV file.
        """
        try:
            with open(self.filename, "w", newline="\n") as csv_file:
                writer = csv.writer(csv_file, delimiter=";")
                writer.writerow(self.dictionary.keys())
                writer.writerows(zip(*self.dictionary.values()))
        except Exception as e:
            print(f"Error saving data to {self.filename}: {e}")
            print("Trying again...")
            self.save_data()
            
            
    def empty_files(self, filenames):
        """
        Method that finds if scrape data has not been saved properly.
        If so, deletes the file so that these dates can be scraped again.
        
        Empty files only contain headers but no other data. Their size
        is smaller than 1 kB (typically around 500 bytes)
        """
        
        for file in filenames:
            if os.path.getsize(file) < 1000:
                try:
                    os.remove(file)
                    print(f"File {file} has been deleted because it was empty.")
                except Exception as e:
                    print(f"Error deleting file {file}: {e}")
                    print("Trying again...")
                    self.empty_files(filenames)

            
    def get_file_dates(self, filenames):
        """
        Method that gets the dates of the files in the data folder.
        
        Returns:
        --------
        file_dates: list.
            List of dates in the files present in the data folder.
        """
        file_dates = []
        for file in filenames:
            date = re.findall(r'\d{4}-\d{1,2}-\d{1,2}', file)

            # Create date string and append to file_dates
            date = day + "-" + month + "-" + year
            file_dates.append(date)
        return file_dates
            
            
    def missing_mercados_precios(self):
        """
        Checks if there is data missing from *Mercados y precios* in the set 
        range of dates and return the dates missing.
        
        Parameters:
        -----------
        self.dates_list: list.
            List of dates were data has been scraped.
        self.missing_files_mercados_precios: list.
            List of dates were data is missing.
        self.empty_files: method.
            Method that deletes empty files.
        self.get_file_dates: method.
            Method that gets the dates of the files in the data folder.
            
        Returns:
        --------
        self.missing_files_mercados_precios: list.
            List of dates that are missing from the data folder.
        """
        
        # Get all filenames with .csv extension in data folder and that
        # do not have "renewable_generation" in the name (i.e. files
        # containing only data from *Mercados y precios*)
        filenames = [filename for filename in os.listdir("data") if filename.endswith(".csv") and "renewable_generation" not in filename]
        
        # Check if there are empty files and delete them
        self.empty_files(filenames=filenames)
        
        # Get the dates of the remaining files
        file_dates = self.get_file_dates(filenames=filenames)

        # Find missing dates to scrape again
        for date_element in self.dates_list:
            if date_element not in file_dates:
                date = datetime.datetime.strptime(date_element, "%d-%m-%Y")
                print(f"Missing data for {date.strftime('%d-%m-%Y')}")
                self.missing_files_mercados_precios.append(date)
        
        self.missing_files_mercados_precios = [(date.year, date.month, date.day) for date in reversed(self.missing_files_mercados_precios)]
        print(f"Missing files: {len(self.missing_files_mercados_precios)}")
        
        
    def missing_generacion_consumo(self):
        """
        Checks if there is data missing from *Generación y consumo* in the set 
        range of dates and return the dates missing.
        
        Parameters:
        -----------
        self.dates_list: list.
            List of dates were data has been scraped.
        self.missing_files_generacion_consumo: list.
            List of dates were data is missing.
        self.empty_files: method.
            Method that deletes empty files.
        self.get_file_dates: method.
            Method that gets the dates of the files in the data folder.
            
        Returns:
        --------
        self.missing_files_generacion_consumo: list.
            List of dates that are missing from the data folder.
        """
        
        # Get all filenames with .csv extension in data folder and that
        # have "renewable_generation" in the name (i.e. files
        # containing only data from *Generación y consumo*)
        filenames = [filename for filename in os.listdir("data") if filename.endswith(".csv") and "renewable_generation" in filename]
        
        # Check if there are empty files and delete them
        self.empty_files(filenames=filenames)
        
        # Get the dates of the remaining files
        file_dates = self.get_file_dates(filenames=filenames)

        # Find missing dates to scrape again
        for date_element in self.dates_list:
            if date_element not in file_dates:
                date = datetime.datetime.strptime(date_element, "%d-%m-%Y")
                print(f"Missing data for {date.strftime('%d-%m-%Y')}")
                self.missing_files_generacion_consumo.append(date)
        
        self.missing_files_generacion_consumo = [(date.year, date.month, date.day) for date in reversed(self.missing_files_generacion_consumo)]
        print(f"Missing files: {len(self.missing_files_generacion_consumo)}")