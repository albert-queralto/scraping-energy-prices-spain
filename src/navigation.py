

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

from font_code_pointers import *


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
        self.driver.implicitly_wait(30)    
        
        
    def date_picker(self, year, mnnth, day):
        """
        Navigates to each date from a selected range.
        """
        
        open_selector = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(MercadosPreciosPointers.SELECT_YEAR))
        self.driver.execute_script("arguments[0].click();", open_selector)
        
        
        
        
        
        
    # def click_x_button(self):
    #     button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ListopiaPointers.X_BUTTON))
    #     self.driver.execute_script("arguments[0].click();", button)
        
    # def navigate_best_books_ever(self):
    #     link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ListopiaPointers.BEST_BOOKS_EVER))
    #     self.driver.execute_script("arguments[0].click();", link)
        
    # def navigate_next_page(self):
    #     try:
    #         next_page = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(BestBooksEverPointers.NEXT_PAGE))
    #         self.driver.execute_script("arguments[0].click();", next_page)
    #         return True
    #     except WebDriverException:
    #         print('There was an issue going to the next page.')
    #         try:
    #             WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(BestBooksEverPointers.NEXT_PAGE_DISABLED))
    #             print('Next page button is disabled. Last page reached.')
    #             return False
    #         except NoSuchElementException:
    #             print("Another exception occurred. Retrying to go to the next page.")
    #             self.driver.implicitly_wait(5)
    #             return self.navigate_next_page()
        
    # def navigate_book_pages(self, book_id):
    #     try:
    #         self.driver.implicitly_wait(5)
    #         return self.driver.get(f"{self.base_url}/book/show/{book_id}")
    #     except TimeoutException as timeout:
    #         print(f"{timeout}")
    #         print('Page will be reloaded.')
    #         self.driver.implicitly_wait(5)
    #         return self.navigate_book_pages(book_id)