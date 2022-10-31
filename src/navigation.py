from argparse import Action
from os import listxattr
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
        try:
            link = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MainPagePointers.MERCADOS_PRECIOS))
            # self.driver.execute_script("arguments[0].click();", link)
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
    
    
    def hour_selection(self, list_index):
        """
        Selects the hour from where to obtain the energy prices.
        """
        select_hour_tooltip = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MercadosPreciosPointers.HOUR_SELECTOR_HIDDEN))
        select_hour_tooltip_child = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MercadosPreciosPointers.HOUR_SELECTOR_HIDDEN_CHILD))
    
        # print(select_hour_tooltip_child.get_attribute("class"))
        if select_hour_tooltip_child.get_attribute("class") == 'time-selector-tooltip is-hidden':
            select_hour_tooltip.click()
            # print(select_hour_tooltip_child.get_attribute("class"))
        
        if list_index > 0 and select_hour_tooltip_child.get_attribute("class") == 'time-selector-tooltip':
            select_hour_tooltip.click()
            select_hour_tooltip.click()

        select_hour_timepicker = select_hour_tooltip.find_element(MercadosPreciosPointers.HOUR_LIST_HIDDEN[0], MercadosPreciosPointers.HOUR_LIST_HIDDEN[1])
        # print("select_hour_timepicker", select_hour_timepicker.get_attribute("class"))
        if select_hour_timepicker.get_attribute("class") == 'chzn-container chzn-container-single':
            try:
                select_hour_tooltip_child.click()
                select_drop_down = select_hour_timepicker.find_element(MercadosPreciosPointers.HOUR_LIST_ACTIVE_DROP[0], MercadosPreciosPointers.HOUR_LIST_ACTIVE_DROP[1])
                time.sleep(1)
                
            except ElementNotInteractableException as element_not_interactable:
                print(element_not_interactable)
                select_hour_tooltip_child.click()
                time.sleep(1)
            except NoSuchElementException as no_such_element:
                print(no_such_element)
                select_drop_down = select_hour_timepicker.find_element(MercadosPreciosPointers.HOUR_LIST_ACTIVE[0], MercadosPreciosPointers.HOUR_LIST_ACTIVE[1])
                select_drop_down.click()

        # print("select_hour_timepicker",  select_hour_timepicker.get_attribute("class"))
        # time.sleep(5)
            

        # select_hour_timepicker_child = select_hour_tooltip.find_element(MercadosPreciosPointers.HOUR_LIST_HIDDEN_CHILD[0], MercadosPreciosPointers.HOUR_LIST_HIDDEN_CHILD[1])
        
        # self.driver.execute_script("arguments[0].click();", select_hour_timepicker_child)
        # print("select_drop_down", select_drop_down.get_attribute("class"))
        # time.sleep(5)
        
        
        li_elements = self.driver.find_element(By.XPATH, 
                                            f'/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/div/ul/li[{list_index+1}]')
        print(li_elements.get_attribute("textContent"))
        actions = ActionChains(self.driver)
        # actions.move_to_element(li_elements).perform()
        # self.driver.execute_script("arguments[0].scrollIntoView();", li_elements.get(f"{list_index+1}"))
        actions.move_to_element(WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, 
                                                    f'/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/div/ul')))).perform()
        if list_index > 6:
            # actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
            self.driver.execute_script("arguments[0].scrollTo(0,0);", li_elements)
            actions.move_to_element(WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, 
                                                        f'/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/div/ul/li[{list_index+1}]')))).perform()
        actions.pause(2)
        actions.click(li_elements).perform()
        # if list_index > 9 and list_index % 4 == 0:
        #     actions.send_keys(Keys.ARROW_UP).send_keys(Keys.ENTER).perform()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # li_elements = self.driver.find_element(MercadosPreciosPointers.TEST_FULL_PATH[0], 
        #                                     f'/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/div/ul/li[{list_index+1}]')
        
        # find_chzn_drop = self.driver.find_element(MercadosPreciosPointers.FIND_CHZN_DROP[0], MercadosPreciosPointers.FIND_CHZN_DROP[1])
        # # find_chzn_results = find_chzn_drop.find_element(MercadosPreciosPointers.FIND_CHZN_RESULTS[0], MercadosPreciosPointers.FIND_CHZN_RESULTS[1])
        # find_ul = find_chzn_drop.find_element(By.TAG_NAME, "ul")
        
        # try:
        #     # find_li_element = find_ul.find_element(By.XPATH, f"//*[contains(@id, '_chzn_o_{i}')]")
        #     find_li_element = find_ul.find_element(By.XPATH, f"//*[text()={str(list_index).zfill(2)}]")
        #     self.driver.execute_script("arguments[0].scrollIntoView();", find_li_element)
        #     print(find_li_element.get_attribute('textContent'))
        #     if find_li_element.get_attribute("class") != 'active-result result-selected' and list_index > 0:
        #         try:
        #             move_to_hour = ActionChains(self.driver)
        #             move_to_hour.move_to_element(find_li_element).click().perform()
        #         except ElementNotInteractableException as element_not_interactable:
        #             print(element_not_interactable)
        #             self.driver.execute_script("arguments[0].scrollIntoView();", find_li_element)
        #             self.driver.execute_script("arguments[0].click();", find_li_element)
        #             find_li_element.click()
        #             time.sleep(5)
        #             # change class of previous element to active-result
        #             find_li_element_previous = find_ul.find_element(By.XPATH, f"//*[text()={str(list_index - 1).zfill(2)}]")
        #             print("previous element class:", find_li_element_previous.get_attribute("class"))
        #             self.driver.execute_script("arguments[0].setAttribute('class', 'active-result');", find_li_element_previous)
        #             print("previous element class:", find_li_element_previous.get_attribute("class"))
        #             # set current element class to active-result result-selected
        #             print("current element class:", find_li_element.get_attribute("class"))
        #             self.driver.execute_script("arguments[0].setAttribute('class', 'active-result result-selected');", find_li_element)            
        #             # self.driver.execute_script("arguments[0].click();", find_li_element)
        #             find_li_element.click()
        #             print("current element class:", find_li_element.get_attribute("class"))
        #     time.sleep(5)
        # except StaleElementReferenceException as stale_exception:
        #     print(stale_exception)
        #     find_li_element = find_ul.find_element(By.XPATH, f"//*[text()={str(list_index).zfill(2)}]")
        #     self.driver.execute_script("arguments[0].scrollIntoView();", find_li_element)
        #     self.driver.execute_script("arguments[0].click();", find_li_element)
        #     time.sleep(5)
        
        
        # select_hour_list = Select(select_drop_down.find_element(MercadosPreciosPointers.SELECT_HOUR_LIST[0], MercadosPreciosPointers.SELECT_HOUR_LIST[1]))
        # select_hour_list = select_hour_timepicker.find_element(MercadosPreciosPointers.SELECT_HOUR_LIST[0], MercadosPreciosPointers.SELECT_HOUR_LIST[1])

        # print('Print options', [o.get_attribute('textContent') for o in select_hour_list.options])   
        # for value in range(len(select_hour_list.options)):
        #     if value == list_index:
        #         print(f"visiting element {value}")
        #         # select_right_hour = ActionChains(self.driver)
        #         # select_right_hour.move_to_element(select_hour_list.options[value])
        #         # select_right_hour.click(select_hour_list.options[value]).perform()
        #         select_hour_list = Select(WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(MercadosPreciosPointers.SELECT_HOUR_LIST)))
        #         # select_hour_list.select_by_value(value)
        #         self.driver.execute_script("arguments[0].style.visibility = 'visible';", select_hour_list.options[value])
        #         self.driver.execute_script("arguments[0].click();", select_hour_list.options[value])
        #         # select_hour_list.options[value].click()

        #         # self.driver.execute_script("arguments[0].setAttribute('style', 'display: block;');", select_hour_list.options[value])
        #         # self.driver.execute_script("arguments[0].scrollIntoView();", select_hour_list.options[value])
        #         # self.driver.execute_script("arguments[0].click();", select_hour_list.options[value])
        #         # select_hour_list.select_by_visible_text(f"{str(list_index).zfill(2)}")
        #         print("Real value of element is:", select_hour_list.first_selected_option.get_attribute('textContent'))
        #         # remove style attribute with "display: none;"
        #         # self.driver.execute_script("arguments[0].removeAttribute('style');", select_hour_list)
        #                             #   self.driver.find_element(MercadosPreciosPointers.SELECT_HOUR_LIST[0], MercadosPreciosPointers.SELECT_HOUR_LIST[1]))
        #         # make value on select() element interactable
        #         # self.driver.execute_script("arguments[0].removeAttribute('disabled')", select_hour_list.options[value])
        #         # self.driver.execute_script("arguments[0].scrollIntoView();", select_hour_list.options[value])
        #         # self.driver.execute_script("arguments[0].setAttribute('class', 'active-result highlighted')", select_hour_list.options[value])
        #         # select_hour_list.select_by_value(select_hour_list.options[value].get_attribute("value"))
        #         # select_hour_list.options[value].click()
        #         # time.sleep(1)
        #         # self.driver.execute_script("arguments[0].setAttribute('class', 'active-result result-selected');", select_hour_list.options[value])
        #         # self.driver.execute_script("arguments[0].click();", select_hour_list.options[value])
        #         print(f"element {value} visited")
        #         time.sleep(5)       
        
        # if select_hour_list.get_attribute("class") not in ["active-result result-selected", "active-result highlighted"]:
            # selectable_hour_element = self.driver.find_element(MercadosPreciosPointers.SELECTABLE_HOUR[0], MercadosPreciosPointers.SELECTABLE_HOUR[1])
            # move_to_selectable_hour = ActionChains(self.driver).move_to_element(selectable_hour_element)
            # move_to_selectable_hour.click().perform()
        # else:
        # select_hour_list.select_by_value(f'{value}')
        # print(f"element {value} selected")        