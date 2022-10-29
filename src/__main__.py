import unittest
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from navigation import *
from data_scraper import *

"""
https://tarifaluzhora.es/
https://www.esios.ree.es/es
https://www.ree.es/es/datos/aldia
"""

class BookScraping(unittest.TestCase):
    
    def setUp(self):
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                            +"AppleWebKit/537.36 (KHTML, like Gecko)"
                            +"Chrome/87.0.4280.141 Safari/537.36")
        self.driver = Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=opts)
        self.driver.set_page_load_timeout(10)
        self.base_url = 'https://www.esios.ree.es/es'
        
    def test_scraper(self):
        page_navigator = Navigation(driver=self.driver, base_url=self.base_url)
        page_navigator.open_chrome_session()
        # page_navigator.navigate_to_mercados_precios()
    #     page_navigator.click_x_button()
    #     page_navigator.navigate_best_books_ever()
        
    #     best_books_ever_page = BestBooksEverPageScraper(driver=self.driver, base_url=self.base_url)
    #     best_books_ever_page.get_all_book_pages()
        
    #     best_books = best_books_ever_page.get_all_book_details()
        
    #     data_saver = SaveUtils(filename='best_books.csv', dictionary=best_books)
    #     data_saver.save_data()
        
    def tearDown(self):
        self.driver.close()
        
if __name__ == '__main__':
    
    HEADERS = {
        'upgrade-insecure-requests': "1",
        'content-type': "application/x-www-form-urlencoded",
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, compress, *",
        'accept-language': "en-US, en;q=0.9, es;q=0.8, de;q=0.7, *;q=0.5",
        'cache-control': "no-cache"
    }
    
    
    unittest.main(warnings='ignore')