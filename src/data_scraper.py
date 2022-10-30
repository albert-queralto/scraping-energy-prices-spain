import re
from sqlite3 import connect
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from font_code_pointers import *
from navigation import *
from support_functions import *


class get_pvpc_data(BasePage):
    
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)

        self.pvpc_ceuta_melilla = 0
        
        self.pvpc_peninsula_baleares_canarias = 0





# class BestBooksEverPageScraper(BasePage):
    
#     def __init__(self, driver, base_url):
#         super().__init__(driver, base_url)
        
#         self.best_books_ever = {
#                                 'position':[], 'title':[], 'author':[], 'book_id':[], 'stars':[], 'ratings':[], 'score':[],
#                                 'people_voted':[], 'description': [], 'genres': [], 'pages': [], 'publication_year': []
#                                 }
        
#     def get_all_book_pages(self):
#         while True:
#             try:
#                 self.get_best_books_info(self.best_books_ever)
#                 self.driver.implicitly_wait(5)
#                 if Navigation.navigate_next_page(self) == False:
#                     break
#             except Exception as e:
#                 print(e)
#                 break
#         return self.best_books_ever
    
#     def get_best_books_info(self, dictionary: dict):
#         soup = BeautifulSoup(self.driver.page_source, "html.parser")
        
#         if soup is not None:
#             for book in soup.find_all('tr'):
#                 try:
#                     dictionary['position'].append(book.find(BestBooksEverPointers.POSITION_ORDER[0], class_=BestBooksEverPointers.POSITION_ORDER[1]).text.strip())
#                     dictionary['title'].append(book.find(BestBooksEverPointers.BOOK_TITLE[0], class_=BestBooksEverPointers.BOOK_TITLE[1]).text.strip())
#                     dictionary['author'].append(book.find(BestBooksEverPointers.AUTHOR_NAME[0], class_=BestBooksEverPointers.AUTHOR_NAME[1]).text.strip())
#                     dictionary['book_id'].append(book.find(BestBooksEverPointers.BOOK_TITLE[0], class_=BestBooksEverPointers.BOOK_TITLE[1]).get('href').split('/')[-1])
                    
#                     stars, ratings = StringProcessing.get_stars_ratings(book.find(BestBooksEverPointers.STARS_RATINGS[0], class_=BestBooksEverPointers.STARS_RATINGS[1]).text)
#                     dictionary['stars'].append(stars)
#                     dictionary['ratings'].append(ratings)
                    
#                     score = StringProcessing.get_scores(str(book.find(BestBooksEverPointers.SCORE[0], text=re.compile(BestBooksEverPointers.SCORE[1]))))
#                     dictionary['score'].append(score)
                    
#                     votes = StringProcessing.get_votes(str(book.find(BestBooksEverPointers.VOTES[0], text=re.compile(BestBooksEverPointers.VOTES[1]))))
#                     dictionary['people_voted'].append(votes)
                    
#                 except Exception as e:
#                     print(e)
#                     continue
#             return dictionary
#         else:
#             print('Soup object is None')
#             return None
    
#     def get_all_book_details(self):
#         for idx, book_id in enumerate(self.best_books_ever['book_id']):
#             if idx <= len(self.best_books_ever['book_id']):
#                 try:
#                     Navigation.navigate_book_pages(self, book_id)
#                     self.get_book_additional_info()
#                     self.driver.implicitly_wait(5)
#                 except Exception as e:
#                     print(e)
#                     continue
#             else:
#                 break
#         return self.best_books_ever
    
#     def get_book_additional_info(self):
#         self.driver.implicitly_wait(5)
#         print(self.driver.current_url)
        
#         session = HTMLSession()
#         connect_page = session.get(self.driver.current_url)
#         connect_page.html.render(sleep=5)
        
#         soup = BeautifulSoup(connect_page.html.html, "html.parser")
        
#         if soup is not None:
#             self.best_books_ever['description'].append(StringProcessing.get_description(soup))
#             self.best_books_ever['genres'].append(StringProcessing.get_genres(soup))
#             self.best_books_ever['pages'].append(StringProcessing.get_pages(soup))
#             self.best_books_ever['publication_year'].append(StringProcessing.get_publication_year(soup))
#         else:
#             print('Soup object is None')
#             return None