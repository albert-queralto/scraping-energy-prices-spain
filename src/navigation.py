from argparse import Action
from os import listxattr
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException
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
        
class Navigation(BasePage):
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
        while True:
            try:
                self.driver.get(f"{self.base_url}")
                print(f"{self.base_url}") # Prints the base url for debugging purposes    
                break
            except TimeoutException as timeout: # Catches the timeout exception if the page is unable to load
                print(f"{timeout}")
                print(f"Page will be reloaded.")
    
    
    def navigate_mercados_precios(self):
        """
        Navigates to the *Mercados y precios* link and clicks it.
        """
        try:
            link = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MainPagePointers.MERCADOS_PRECIOS))
            link.click()
        except TimeoutException as timeout: # Catches the timeout exception if the page is unable to load
                print(f"{timeout}")
                print(f"Page will be reloaded.")
                return self.navigate_mercados_precios()
        
        
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
            if '?date=' in self.driver.current_url:
                # If it is present, remove it
                page_url = self.driver.get(self.driver.current_url.split('?date=')[0])

            # Add the '?date=DD-MM-YYYY' string to the URL and go to the page
            page_url = self.driver.current_url + f"?date={day}-{month}-{year}"
            return self.driver.get(page_url)
        except TimeoutException as timeout: # Catches the timeout exception if the page is unable to load
                print(f"{timeout}")
                print(f"Page will be reloaded.")
                return self.date_navigator(year, month, day)
    
    
    def hour_selection_mercados_precios(self, list_index):
        """
        Selects the hour from where to obtain the energy prices.
        
        Parameters:
        ----------
        list_index: int.
                    The index of the hour to select.
        """
        try:
            # Find the hour selector
            select_hour_tooltip = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MercadosPreciosPointers.HOUR_SELECTOR_HIDDEN))
            select_hour_tooltip_child = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MercadosPreciosPointers.HOUR_SELECTOR_HIDDEN_CHILD))
        
            # Click the hour selector if its class is set to 'is-hidden'
            if select_hour_tooltip_child.get_attribute("class") == 'time-selector-tooltip is-hidden':
                select_hour_tooltip.click()
            
            # Hides and unhides the hour selector to prevent and issue during changing hours were the class is kept as 'not hidden' and prevents the selection of the right hour
            if list_index > 0 and select_hour_tooltip_child.get_attribute("class") == 'time-selector-tooltip':
                select_hour_tooltip.click()
                select_hour_tooltip.click()

            # Finds the first drop down list menu and clicks it to open the second drop down menu with the list of hours to select
            select_hour_timepicker = select_hour_tooltip.find_element(MercadosPreciosPointers.HOUR_LIST_HIDDEN[0], MercadosPreciosPointers.HOUR_LIST_HIDDEN[1])
            if select_hour_timepicker.get_attribute("class") == 'chzn-container chzn-container-single':
                try:
                    select_hour_tooltip_child.click()
                    select_drop_down = select_hour_timepicker.find_element(MercadosPreciosPointers.HOUR_LIST_ACTIVE_DROP[0], MercadosPreciosPointers.HOUR_LIST_ACTIVE_DROP[1])
                    time.sleep(1)
                # Handle the exception when the element is not interactable
                except ElementNotInteractableException as element_not_interactable:
                    print(element_not_interactable)
                    select_hour_tooltip_child.click()
                    time.sleep(1)
                # Handles the exception when the element is not found
                except NoSuchElementException as no_such_element:
                    print(no_such_element)
                    select_drop_down = select_hour_timepicker.find_element(MercadosPreciosPointers.HOUR_LIST_ACTIVE[0], MercadosPreciosPointers.HOUR_LIST_ACTIVE[1])
                    select_drop_down.click()
                    time.sleep(1)
        except TimeoutException as timeout:
            print(timeout)
            return self.hour_selection_mercados_precios(list_index)
        
        # Handles the selection of the right hour
        try:
            
            LI_XPATH = f'/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/div/ul/li[{list_index+1}]'
            
            # Finds the right hour to be selected based on the value of 'list_index' + 1
            li_elements = self.driver.find_element(By.XPATH, LI_XPATH)
            print(li_elements.get_attribute("textContent"))
            
            # Chain actions to find the right hour value
            actions = ActionChains(self.driver)

            if list_index > 6: # Moves the arrow down to be able to select hour numbers above 6. Otherwise, the drop down menu goes always to the last hour (23)
                actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
            
            actions.move_to_element(WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, LI_XPATH)))).perform()
            actions.move_to_element(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, LI_XPATH)))).perform()
            
            # 
            
            # Check if the right element is located
            if li_elements.get_attribute("textContent") == MercadosPreciosPointers.HOUR_LIST[list_index]:
                actions.pause(5)
                actions.click(li_elements).perform()
            else:
                print("Wrong element located")
                return self.hour_selection_mercados_precios(list_index)
            
            # Move the window up every now and then so that the dropdown menu can be found. Otherwise, it throws an ElementClickInterceptedException
            if list_index > 9 and list_index % 3 == 0:
                actions.send_keys(Keys.ARROW_UP).send_keys(Keys.ENTER).perform()
                actions.send_keys(Keys.ARROW_UP).send_keys(Keys.ENTER).perform()
                
            time.sleep(2)
        # Handke ElementClickInterceptedException and run the function again
        except ElementClickInterceptedException as element_click_intercepted:
            print(element_click_intercepted)
            return self.hour_selection_mercados_precios(list_index)
        # Handle StaleElementReferenceException and run the function again
        except StaleElementReferenceException as stale_element:
            print(stale_element)
            return self.hour_selection_mercados_precios(list_index)
