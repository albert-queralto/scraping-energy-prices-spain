# -*- coding: utf-8 -*-
# Path: src/navigation.py
# Authors: Esther Manzano, Albert Queraltó

"""
This is module contains alls the classes and methods that enable navigation of the crawler
through the different pages, as well as elements of each page.
"""


import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.keys import Keys

from font_code_pointers import *
from support_functions import *


class BasePage(object):
    """
    Initializes all classes with the initial parameters.
    """

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()


class NavigationMain(BasePage):
    """
    Contains all the methods that enable navigation.
    """

    def open_chrome_session(self):
        """
        Opens the Webdriver session on a Chrome browser.

        Parameters:
        ----------
        self.driver: object.
                    The Webdriver object.
        self.base_url: string.
                        A string that contains the base URL.
        """
        # while True:
        try:
            self.driver.get(f"{self.base_url}")
            print(
                f"{self.base_url}"
            )  # Prints the base url for debugging purposes
            print(
                self.driver.execute_script("return navigator.userAgent;")
            )  # Check user agent
            return self.driver
        except TimeoutException as timeout:  # Catches the timeout exception if the page is unable to load and tries to reload it
            print(f"{timeout}")
            print(f"Page will be reloaded.")
            return self.open_chrome_session()

    def navigate_mercados_precios(self):
        """
        Navigates to the *Mercados y precios* link and clicks it.
        """
        try:
            link = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MainPagePointers.MERCADOS_PRECIOS))
            return link.click()
        except TimeoutException as timeout:  # Catches the timeout exception if the page is unable to load
            print(f"{timeout}")
            print(f"Page will be reloaded.")
            return self.navigate_mercados_precios()

    def navigate_generacion_consumo(self):
        """
        Navigates to the *Generación y consumo* link and clicks it.
        """
        try:
            link = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MainPagePointers.GENERACION_CONSUMO))
            return link.click()
        except TimeoutException as timeout:  # Catches the timeout exception if the page is unable to load
            print(f"{timeout}")
            print(f"Page will be reloaded.")
            return self.navigate_generacion_consumo()


class NavigationMercadosPrecios(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.hour_selection_attempts = 0

    def date_navigator(self, year, month, day):
        """
        Navigates to each date from a selected range that is provided.

        Paràmeters:
        ----------
        year: int.
                The year to navigate to.
        month: int.
                The month to navigate to.
        day: int.
                The day to navigate to.
        """
        try:
            # Check if ?date=DD-MM-YYYY is present in the URL
            if "?date=" in self.driver.current_url:
                # If it is present, remove it
                page_url = self.driver.get(self.driver.current_url.split("?date=")[0])

            # Add the '?date=DD-MM-YYYY' string to the URL and go to the page
            page_url = self.driver.current_url + f"?date={day}-{month}-{year}"
            return self.driver.get(page_url)
        except TimeoutException as timeout:  # Catches the timeout exception if the page is unable to load
            print(f"{timeout}")
            print(f"Page will be reloaded.")
            time.sleep(5)
            return self.date_navigator(year, month, day)

    def hour_selection_mercados_precios(self, list_index):
        """
        Selects the hour from where to obtain the energy prices.

        Parameters:
        ----------
        list_index: int.
                    The index of the hour to select.

        Returns:
        -------
        Returns the right hour selected.
        """
        
        try:
            # Find the hour selector
            select_hour_tooltip = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(MercadosPreciosPointers.HOUR_SELECTOR_HIDDEN))
            select_hour_tooltip_child = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(MercadosPreciosPointers.HOUR_SELECTOR_HIDDEN_CHILD))

            # Click the hour selector if its class is set to 'is-hidden'
            if select_hour_tooltip_child.get_attribute("class") == "time-selector-tooltip is-hidden":
                try:
                    select_hour_tooltip.click()
                # Handle ElementClickInterceptedException due to the element not found. Scroll up the window to be able to locate it
                except ElementClickInterceptedException as click_intercepted:
                    print(f"{click_intercepted}")
                    self.driver.refresh()
                    print("Location of element will be retried. Scrolling window up...")
                    self.driver.execute_script("window.scrollTo(0, 0)")
                    return self.hour_selection_mercados_precios(list_index)

            # Hides and unhides the hour selector to prevent and issue during changing hours were the class is kept as 'not hidden' 
            # and prevents the selection of the right hour
            if select_hour_tooltip_child.get_attribute("class") == "time-selector-tooltip":
                try:
                    select_hour_tooltip.click()
                    select_hour_tooltip.click()
                    
                # Handle ElementClickInterceptedException and run the function again
                except ElementClickInterceptedException as element_click_intercepted:
                    print(element_click_intercepted)
                    print("Location of element will be retried. Scrolling window up...")
                    self.driver.execute_script("window.scrollTo(0, 0)")
                    return self.hour_selection_mercados_precios(list_index)

            # Finds the first drop down list menu and clicks it to open the second drop down menu with the list of hours to select
            select_hour_timepicker = select_hour_tooltip.find_element(
                MercadosPreciosPointers.HOUR_LIST_HIDDEN[0], MercadosPreciosPointers.HOUR_LIST_HIDDEN[1])
            if (select_hour_timepicker.get_attribute("class") == "chzn-container chzn-container-single") or \
                (select_hour_timepicker.get_attribute("class") == "chzn-container chzn-container-single chzn-container-active"):
                    
                try:
                    select_hour_tooltip_child.click()
                    select_drop_down = select_hour_timepicker.find_element(
                        MercadosPreciosPointers.HOUR_LIST_ACTIVE_DROP[0], MercadosPreciosPointers.HOUR_LIST_ACTIVE_DROP[1])
                    time.sleep(1)
                # Handle the exception when the element is not interactable
                except ElementNotInteractableException as element_not_interactable:
                    print(element_not_interactable)
                    select_hour_tooltip_child.click()
                    time.sleep(1)
                # Handles the exception when the element is not found
                except NoSuchElementException as no_such_element:
                    print(no_such_element)
                    select_hour_timepicker = select_hour_tooltip.find_element(
                        MercadosPreciosPointers.HOUR_LIST_ACTIVE[0], MercadosPreciosPointers.HOUR_LIST_ACTIVE[1])
                    select_drop_down.click()
                    time.sleep(1)

            # Handle the selection of the right hour
            # XPATH for the li locator to be found
            LI_XPATH = f"/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/div/ul/li[{list_index+1}]"

            # Finds the right hour to be selected based on the value of 'list_index' + 1
            try:
                li_elements = self.driver.find_element(By.XPATH, LI_XPATH)
                print(li_elements.get_attribute("textContent"))
            # Handles the exception when the element is not found, the function is run again
            except NoSuchElementException as no_such_element:
                print(no_such_element)
                print(f"Unable to find the right hour to be selected. Retrying...")
                return self.hour_selection_mercados_precios(list_index)

            # Chain actions to find the right hour value
            actions = ActionChains(self.driver)

            if list_index > 6:  # Moves the arrow down to be able to select hour numbers above 6.
                # Otherwise, the drop down menu goes always to the last hour (23)
                actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

            # Ensure that the right element is found before clicking it
            actions.move_to_element(WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, LI_XPATH)))).perform()
            actions.move_to_element(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, LI_XPATH)))).perform()
            actions.pause(5)
            actions.click(li_elements).perform()

            # Scroll the window to the top every now and then so that the dropdown menu can be found. 
            # Otherwise, it throws an ElementClickInterceptedException
            if list_index > 9 and list_index % 3 == 0:
                self.driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(5)
                    
            try:
                # Read current value of the selected hour
                selected_hour = (WebDriverWait(self.driver, 20)
                    .until(EC.presence_of_element_located(MercadosPreciosPointers.SELECTED_HOUR)).get_attribute("textContent"))
                print(selected_hour)

                # Ensure that the right hour has been selected. Otherwise, perform the search again and click the found element
                if selected_hour.split(":")[0] != li_elements.get_attribute("textContent"):
                    print(f'Selected hour ({selected_hour}) is different than the expected value ({li_elements.get_attribute("textContent")}.')
                    print('Retrying to perform selection.')
                    actions.move_to_element(WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, LI_XPATH)))).perform()
                    actions.move_to_element(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, LI_XPATH)))).perform()
                    actions.pause(5)
                    actions.click(li_elements).perform()
                    time.sleep(5)
                else:
                    # Resets the counter to track the attempts to select the right hour
                    self.hour_selection_attempts = 0

            # Handle ElementClickInterceptedException and run the function again
            except ElementClickInterceptedException as element_click_intercepted:
                print(element_click_intercepted)
                time.sleep(2)
                print("Location of element will be retried. Scrolling window up...")
                self.driver.execute_script("window.scrollTo(0, 0)")
                return self.hour_selection_mercados_precios(list_index)
            # Handle StaleElementReferenceException and run the function again
            except StaleElementReferenceException as stale_element:
                print(stale_element)
                time.sleep(2)
                
                # Track the attempts to find the right hour, set a limit of attempts before switching to the next hour
                self.hour_selection_attempts += 1
                if self.hour_selection_attempts > 10:
                    print("Too many attempts to select the right hour. Selecting next hour...")
                    self.hour_selection_attempts = 0
                    return False
                else:
                    print(f"Unable to find the right hour to be selected. Attempt {self.hour_selection_attempts}")
                    return self.hour_selection_mercados_precios(list_index)

        # Handle TimeoutException and run the function again
        except TimeoutException as timeout:
            print(timeout)
            time.sleep(2)
            self.driver.refresh()
            return self.hour_selection_mercados_precios(list_index)


class NavigationGeneracionConsumo(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def date_navigator(self, year, month, day):
        """
        Navigates to each date from a selected range that is provided.

        Parameters:
        ----------
        year: int.
                The year to navigate to.
        month: int.
                The month to navigate to.
        day: int.
                The day to navigate to.
        """
        try:
            # Check if ?date=DD-MM-YYYY is present in the URL
            if "?date=" in self.driver.current_url:
                # If it is present, remove it
                page_url = self.driver.get(self.driver.current_url.split("?date=")[0])

            # Add the '?date=DD-MM-YYYY' string to the URL and go to the page
            page_url = self.driver.current_url + f"?date={day}-{month}-{year}"
            return self.driver.get(page_url)

        # Catches the timeout exception if the page is unable to load
        except TimeoutException as timeout:
            print(f"{timeout}")
            print(f"Page will be reloaded.")
            time.sleep(5)
            return self.date_navigator(year, month, day)

    def hour_selection_generacion_libre_co2(self, list_index):
        """
        Selects the hour from where to obtain the renewable energy data
        (*Generación libre de CO2*) from *Generación y consumo* page.

        Parameters:
        ----------
        list_index: int.
                    The index of the hour to select.

        Returns:
        -------
        Returns the right hour selected.
        """
        try:
            # Find the hour selector
            select_hour_tooltip = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(GeneracionConsumoPointers.HOUR_SELECTOR_HIDDEN))
            select_hour_tooltip_child = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(GeneracionConsumoPointers.HOUR_SELECTOR_HIDDEN_CHILD))

            # Click the hour selector if its class is set to 'is-hidden'
            if select_hour_tooltip_child.get_attribute("class") == "time-selector-tooltip is-hidden":
                try:
                    select_hour_tooltip.click()
                # Handle ElementClickInterceptedException due to the element not
                # found. Scroll up the window to be able to locate it
                except ElementClickInterceptedException as click_intercepted:
                    print(f"{click_intercepted}")
                    self.driver.refresh()
                    print("Location of element will be retried. Scrolling window up...")
                    self.driver.execute_script("window.scrollTo(0, 0)")
                    return self.hour_selection_generacion_libre_co2(list_index)

            # Hides and unhides the hour selector to prevent and issue during
            # changing hours were the class is kept as 'not hidden' and prevents
            # the selection of the right hour
            if select_hour_tooltip_child.get_attribute("class") == "time-selector-tooltip":
                try:
                    select_hour_tooltip.click()
                    select_hour_tooltip.click()
                # Handle ElementClickInterceptedException and run the function again
                except ElementClickInterceptedException as element_click_intercepted:
                    print(element_click_intercepted)
                    print("Location of element will be retried. Scrolling window up...")
                    self.driver.execute_script("window.scrollTo(0, 0)")
                    return self.hour_selection_generacion_libre_co2(list_index)

            # Finds the first drop down list menu and clicks it to open the
            # second drop down menu with the list of hours to select
            select_hour_timepicker = self.driver.find_element(
                GeneracionConsumoPointers.HOUR_LIST_HIDDEN[0],GeneracionConsumoPointers.HOUR_LIST_HIDDEN[1],)
            if (select_hour_timepicker.get_attribute("class") == "chzn-container chzn-container-single") or \
                (select_hour_timepicker.get_attribute("class") == "chzn-container chzn-container-single chzn-container-active"):
                try:
                    select_hour_timepicker.click()
                    select_drop_down = self.driver.find_element(
                        GeneracionConsumoPointers.HOUR_LIST_ACTIVE_DROP[0], GeneracionConsumoPointers.HOUR_LIST_ACTIVE_DROP[1])
                    time.sleep(1)
                # Handle the exception when the element is not interactable
                except ElementNotInteractableException as element_not_interactable:
                    print(element_not_interactable)
                    select_hour_timepicker.click()
                    time.sleep(1)
                # Handles the exception when the element is not found
                except NoSuchElementException as no_such_element:
                    print(no_such_element)
                    select_drop_down = self.driver.find_element(
                        GeneracionConsumoPointers.HOUR_LIST_ACTIVE_DROP[0], GeneracionConsumoPointers.HOUR_LIST_ACTIVE_DROP[1])
                    select_drop_down.click()
                    time.sleep(1)

            # Handle the selection of the right hour
            # XPATH for the li locator to be found
            LI_XPATH = f"/html/body/div[3]/div[2]/div/div/div[3]/aside/div/div/div[3]/div/div/div[1]/div/ul/li[{list_index+1}]"

            # Finds the right hour to be selected based on the value of 'list_index' + 1
            li_elements = self.driver.find_element(By.XPATH, LI_XPATH)
            print(li_elements.get_attribute("textContent"))

            # Chain actions to find the right hour value
            actions = ActionChains(self.driver)

            if list_index > 6:  
                # Moves the arrow down to be able to select hour numbers above 6.
                # Otherwise, the drop down menu goes always to the last hour (23)
                actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

            # Ensure that the right element is found before clicking it
            actions.move_to_element(WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, LI_XPATH)))).perform()
            actions.move_to_element(WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, LI_XPATH)))).perform()
            actions.pause(5)
            actions.click(li_elements).perform()

            # Scroll the window to the top every now and then so that the dropdown menu can be found. 
            # Otherwise, it throws an ElementClickInterceptedException
            if list_index > 9 and list_index % 3 == 0:
                self.driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(5)

            try:
                # Read current value of the selected hour
                selected_hour = (WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located(GeneracionConsumoPointers.SELECTED_HOUR)).get_attribute("textContent"))
                print(selected_hour)

                # Ensure that the right hour has been selected. Otherwise, perform
                # the search again and click the found element
                if selected_hour.split(":")[0] != li_elements.get_attribute("textContent"):
                    print(f'Selected hour ({selected_hour}) is different than the expected value ({li_elements.get_attribute("textContent")}.')
                    print('Retrying to perform selection.')
                    actions.move_to_element(WebDriverWait(self.driver, 30).until(
                            EC.visibility_of_element_located((By.XPATH, LI_XPATH)))).perform()
                    actions.move_to_element(WebDriverWait(self.driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, LI_XPATH)))).perform()
                    actions.pause(5)
                    actions.click(li_elements).perform()
                    time.sleep(5)
                else:
                    # Resets the counter to track the attempts to select the right hour
                    self.hour_selection_attempts = 0

            # Handle ElementClickInterceptedException and run the function again
            except ElementClickInterceptedException as element_click_intercepted:
                print(element_click_intercepted)
                time.sleep(2)
                print("Location of element will be retried. Scrolling window up...")
                self.driver.execute_script("window.scrollTo(0, 0)")
                return self.hour_selection_generacion_libre_co2(list_index)
            # Handle StaleElementReferenceException and run the function again
            except StaleElementReferenceException as stale_element:
                print(stale_element)
                time.sleep(2)
                
                # Track the attempts to find the right hour, set a limit of attempts before switching to the next hour
                self.hour_selection_attempts += 1
                if self.hour_selection_attempts > 10:
                    print("Too many attempts to select the right hour. Selecting next hour...")
                    self.hour_selection_attempts = 0
                    return False
                else:
                    print(f"Unable to find the right hour to be selected. Attempt {self.hour_selection_attempts}")
                    return self.hour_selection_generacion_libre_co2(list_index)
        
        # Handle TimeoutException and run the function again
        except TimeoutException as timeout:
            print(timeout)
            return self.hour_selection_generacion_libre_co2(list_index)