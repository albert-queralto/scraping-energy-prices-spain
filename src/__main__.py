import unittest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from navigation import *
from data_scraper import *

class BookScraping(unittest.TestCase):
    
    def setUp(self):
        self.driver = Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.set_page_load_timeout(10)
        self.base_url = 'http://goodreads.com/'
        
    def test_scraper(self):
        page_navigator = Navigation(driver=self.driver, base_url=self.base_url)
        page_navigator.open_chrome_session()
        page_navigator.navigate_to_lists_page()
        page_navigator.click_x_button()
        page_navigator.navigate_best_books_ever()
        
        best_books_ever_page = BestBooksEverPageScraper(driver=self.driver, base_url=self.base_url)
        best_books_ever_page.get_all_book_pages()
        
        best_books = best_books_ever_page.get_all_book_details()
        
        data_saver = SaveUtils(filename='best_books.csv', dictionary=best_books)
        data_saver.save_data()
        
    def tearDown(self):
        self.driver.close()
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')