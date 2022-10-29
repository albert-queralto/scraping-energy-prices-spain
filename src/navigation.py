

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
    def open_chrome_session(self):
        while True:
            try:
                self.driver.get(f"{self.base_url}")
                print(f"{self.base_url}")
                
                user_agent = self.driver.execute_script("return navigator.userAgent")
                print(f"User Agent: {user_agent}")
                
                header = self.driver.execute_script("return navigator.header")
                print(f"Header: {header}")
                
                break
            except TimeoutException as timeout:
                print(f"{timeout}")
                print(f"Page will be reloaded.")
    
    # https://stackoverflow.com/questions/29916054/change-user-agent-for-selenium-web-driver
    
    
    def navigate_to_mercados_precios(self):
        link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(MainPagePointers.MERCADOS_PRECIOS))
        print(link)
        # self.driver.execute_script("arguments[0].click();", link)
        
        
        
        
        
        
        
        
        
        
        
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