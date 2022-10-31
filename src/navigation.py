from argparse import Action
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys

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
    
    
    def hour_selection(self, list_index):
        """
        Selects the hour from where to obtain the energy prices.
        """
        select_hour_tooltip = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MercadosPreciosPointers.HOUR_SELECTOR_HIDDEN))
        select_hour_tooltip_child = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MercadosPreciosPointers.HOUR_SELECTOR_HIDDEN_CHILD))
    
        print(select_hour_tooltip_child.get_attribute("class"))
        if select_hour_tooltip_child.get_attribute("class") == 'time-selector-tooltip is-hidden':
            select_hour_tooltip.click()
            print(select_hour_tooltip_child.get_attribute("class"))


            select_hour_timepicker = select_hour_tooltip.find_element(MercadosPreciosPointers.HOUR_LIST_HIDDEN[0], MercadosPreciosPointers.HOUR_LIST_HIDDEN[1])
            select_hour_timepicker_child = select_hour_tooltip.find_element(MercadosPreciosPointers.HOUR_LIST_HIDDEN_CHILD[0], MercadosPreciosPointers.HOUR_LIST_HIDDEN_CHILD[1])
            
            print(select_hour_timepicker.get_attribute("class"))
            if select_hour_timepicker.get_attribute("class") == 'chzn-container chzn-container-single':
                try:
                    self.driver.implicitly_wait(5)
                    select_hour_tooltip_child.click()
                    time.sleep(5)
                    print(select_hour_timepicker.get_attribute("class"))
                    
                except ElementNotInteractableException as element_not_interactable:
                    print(element_not_interactable)
                    return self.hour_selection
                
                # click_hour_drop_down = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MercadosPreciosPointers.HOUR_LISTS_HIDDEN_CHILD))
                # click_hour_drop_down.click()
                # move_to_hour_selector = ActionChains(self.driver).move_to_element(select_hour_timepicker_child)
                # move_to_hour_selector.click(select_hour_timepicker_child).perform()
            print(select_hour_timepicker.get_attribute("class"))


        # select_hour_list = Select(select_hour_timepicker.find_element(MercadosPreciosPointers.SELECT_HOUR_LIST[0], MercadosPreciosPointers.SELECT_HOUR_LIST[1]))
        # select_hour_list = select_hour_timepicker.find_element(MercadosPreciosPointers.SELECT_HOUR_LIST[0], MercadosPreciosPointers.SELECT_HOUR_LIST[1])
        # select_hour_list.click()
        # test = select_hour_timepicker.find_element(MercadosPreciosPointers.SELECT_HOUR_LIST[0], MercadosPreciosPointers.SELECT_HOUR_LIST[1]).is_displayed()
        # print(test)
        # print('Print options', [o.get_attribute('textContent') for o in select_hour_list.options])   
        # for value in range(len(select_hour_list.options)):
        #     if value == list_index:
        #         print(f"visiting element {value}")
        #         select_hour_list = Select(WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(MercadosPreciosPointers.SELECT_HOUR_LIST)))
        #         # remove style attribute with "display: none;"
        #         # self.driver.execute_script("arguments[0].removeAttribute('style');", select_hour_list)
        #                             #   self.driver.find_element(MercadosPreciosPointers.SELECT_HOUR_LIST[0], MercadosPreciosPointers.SELECT_HOUR_LIST[1]))
        #         # make value on select() element interactable
        #         # self.driver.execute_script("arguments[0].removeAttribute('disabled')", select_hour_list.options[value])
        #         self.driver.execute_script("arguments[0].scrollIntoView();", select_hour_list.options[value])
        #         # self.driver.execute_script("arguments[0].setAttribute('class', 'active-result highlighted')", select_hour_list.options[value])
        #         select_hour_list.select_by_value(select_hour_list.options[value].get_attribute("value"))
        #         time.sleep(1)
        #         # self.driver.execute_script("arguments[0].setAttribute('class', 'active-result result-selected');", select_hour_list.options[value])
        #         # self.driver.execute_script("arguments[0].click();", select_hour_list.options[value])
        #         print(f"element {value} visited")
        #         time.sleep(5)       




        # find_chzn_results = self.driver.find_element(MercadosPreciosPointers.FIND_CHZN_RESULTS[0], MercadosPreciosPointers.FIND_CHZN_RESULTS[1])
        # find_chzn_drop = self.driver.find_element(MercadosPreciosPointers.FIND_CHZN_DROP[0], MercadosPreciosPointers.FIND_CHZN_DROP[1])
        # find_ul = find_chzn_drop.find_element(By.TAG_NAME, "ul")
        
        # try:
        #     # find_li_element = find_ul.find_element(By.XPATH, f"//*[contains(@id, '_chzn_o_{i}')]")
        #     find_li_element = find_ul.find_element(By.XPATH, f"//*[text()={str(list_index).zfill(2)}]")
        #     self.driver.execute_script("arguments[0].scrollIntoView();", find_li_element)
        #     print(find_li_element.get_attribute('textContent'))
        #     if find_li_element.get_attribute("class") != 'active-result result-selected' and list_index > 0:
        #         # change class of previous element to active-result
        #         find_li_element_previous = find_ul.find_element(By.XPATH, f"//*[text()={str(list_index - 1).zfill(2)}]")
        #         print("previous element class:", find_li_element_previous.get_attribute("class"))
        #         self.driver.execute_script("arguments[0].setAttribute('class', 'active-result');", find_li_element_previous)
        #         print("previous element class:", find_li_element_previous.get_attribute("class"))
        #         # set current element class to active-result result-selected
        #         print("current element class:", find_li_element.get_attribute("class"))
        #         self.driver.execute_script("arguments[0].setAttribute('class', 'active-result result-selected');", find_li_element)            
        #         self.driver.execute_script("arguments[0].click();", find_li_element)
        #         print("current element class:", find_li_element.get_attribute("class"))
        #     time.sleep(5)
        # except StaleElementReferenceException as stale_exception:
        #     print(stale_exception)
        #     find_li_element = find_ul.find_element(By.XPATH, f"//*[text()={str(list_index).zfill(2)}]")
        #     self.driver.execute_script("arguments[0].scrollIntoView();", find_li_element)
        #     self.driver.execute_script("arguments[0].click();", find_li_element)
        #     time.sleep(5)
            
            
            
    
        
        


        

            # if select_hour_list.get_attribute("class") not in ["active-result result-selected", "active-result highlighted"]:
                # selectable_hour_element = self.driver.find_element(MercadosPreciosPointers.SELECTABLE_HOUR[0], MercadosPreciosPointers.SELECTABLE_HOUR[1])
                # move_to_selectable_hour = ActionChains(self.driver).move_to_element(selectable_hour_element)
                # move_to_selectable_hour.click().perform()
            # else:
            # select_hour_list.select_by_value(f'{value}')
            # print(f"element {value} selected")        
        