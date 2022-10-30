

import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

from font_code_pointers import *
from support_functions import *


class BasePage(object):
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
        link = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MainPagePointers.MERCADOS_PRECIOS))
        self.driver.execute_script("arguments[0].click();", link)
        
        
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
        
        # Check if ?date=DD-MM-YYYY is present in the URL
        if '?date=' in self.driver.current_url:
            # If it is present, remove it
            page_url = self.driver.get(self.driver.current_url.split('?date=')[0])

        # Add the '?date=DD-MM-YYYY' string to the URL and go to the page
        page_url = self.driver.current_url + f"?date={day}-{month}-{year}"
        return self.driver.get(page_url)
    
    
    def hour_selection(self):
        """
        Selects the hour from where to obtain the energy prices.
        """
        mercado_precios_pointers = MercadosPreciosPointers(value=0)
        mercado_precios_pointers.hour_selectors()
        
        select_hour_tooltip = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(mercado_precios_pointers.HOUR_SELECTOR_HIDDEN))
        # if class is "time-selector-tooltip is-hidden" click
        if select_hour_tooltip.get_attribute("class") == "time-selector-tooltip is-hidden":
            self.driver.execute_script("arguments[0].click();", select_hour_tooltip)

        select_hour_timepicker = self.driver.find_element(mercado_precios_pointers.HOUR_LIST_HIDDEN[0], mercado_precios_pointers.HOUR_LIST_HIDDEN[1])
        # if class is not "chzn-container chzn-container-single chzn-container-active chzn-with-drop"
        if select_hour_timepicker.get_attribute("class") != "chzn-container chzn-container-single chzn-container-active chzn-with-drop":
            self.driver.execute_script("arguments[0].click();", select_hour_timepicker)

        select_hour_list = Select(self.driver.find_element(mercado_precios_pointers.SELECT_HOUR_LIST[0], mercado_precios_pointers.SELECT_HOUR_LIST[1]))
        for value in range(len(select_hour_list.options)):
            select_hour_list = Select(self.driver.find_element(mercado_precios_pointers.SELECT_HOUR_LIST[0], mercado_precios_pointers.SELECT_HOUR_LIST[1]))

            # make value on select() element interactable
            self.driver.execute_script("arguments[0].removeAttribute('disabled')", select_hour_list.options[value])
            self.driver.execute_script("arguments[0].scrollIntoView();", select_hour_list.options[value])
            self.driver.execute_script("arguments[0].click();", select_hour_list.options[value])
            print(f"element {value} visited")
            time.sleep(5)            

            # if select_hour_list.get_attribute("class") not in ["active-result result-selected", "active-result highlighted"]:
                # selectable_hour_element = self.driver.find_element(mercado_precios_pointers.SELECTABLE_HOUR[0], mercado_precios_pointers.SELECTABLE_HOUR[1])
                # move_to_selectable_hour = ActionChains(self.driver).move_to_element(selectable_hour_element)
                # move_to_selectable_hour.click().perform()
            # else:
            # select_hour_list.select_by_value(f'{value}')
            # print(f"element {value} selected")        
        