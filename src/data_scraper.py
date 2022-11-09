# -*- coding: utf-8 -*-
# Path: src/data_scraper.py
# Authors: Esther Manzano, Albert Queraltó

"""
This is module contains alls the classes and methods that allow to obtain
specific data from the pages the crawler has navigated to.
"""

from font_code_pointers import *
from navigation import *
from support_functions import *


class MercadoPreciosData(object):
    def __init__(self, driver):
        self.driver = driver

    def get_precio_final_energia(self):
        """
        Obtains the energy prices from the *Mercados y precios* webpage.

        Parameters:
        -----------
        self.driver: WebDriver object.
            The webdriver that will be used to scrape the webpage.

        Returns:
        --------
        pm_total: float.
            The total energy price.
        pm_com_libre: float.
            The energy price for the free market.
        pm_com_ref: float.
            The energy price for the reference market.
        """
        pm_total = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    MercadosPreciosPointers.PRECIO_MEDIO_TOTAL
                )
            )
            .text
        )
        pm_com_libre = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    MercadosPreciosPointers.PRECIO_MEDIO_COM_LIBRE
                )
            )
            .text
        )
        pm_com_ref = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    MercadosPreciosPointers.PRECIO_MEDIO_COM_REF
                )
            )
            .text
        )

        return pm_total, pm_com_libre, pm_com_ref

    def get_energia(self):
        """
        Obtains the energy data from the *Mercados y precios* webpage and stores
        them in lists.

        Parameters:
        -----------
        self.driver: WebDriver object.
            The webdriver that will be used to scrape the webpage.

        Returns:
        --------
        energia_total: float.
            The total energy.
        energia_comercializador_libre: float.
            The energy for the free market.
        energia_comercializador_referencia: float.
            The energy for the reference market.
        """
        energia_total = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    MercadosPreciosPointers.ENERGIA_TOTAL
                )
            )
            .text
        )
        energia_com_libre = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    MercadosPreciosPointers.ENERGIA_COM_LIBRE
                )
            )
            .text
        )
        energia_com_ref = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    MercadosPreciosPointers.ENERGIA_COM_REF
                )
            )
            .text
        )

        return energia_total, energia_com_libre, energia_com_ref

    def get_cuota(self):
        """
        Obtains the share data from the *Mercados y precios* webpage and stores
        them in lists. The total share is 100% therefore, it is not needed to
        collect it.

        Parameters:
        -----------
        self.driver: WebDriver object.
            The webdriver that will be used to scrape the webpage.

        Returns:
        --------
        cuota_comercializador_libre: float.
            The share for the free market.
        cuota_comercializador_referencia: float.
            The share for the reference market.
        """
        cuota_com_libre = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    MercadosPreciosPointers.CUOTA_COM_LIBRE
                )
            )
            .text
        )
        cuota_com_ref = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    MercadosPreciosPointers.CUOTA_COM_REF
                )
            )
            .text
        )

        return cuota_com_libre, cuota_com_ref


class GeneracionConsumoData(object):
    def __init__(self, driver):
        self.driver = driver

    def get_renewable_generation_data(self):
        """
        Obtains the energy generation data of renewable sources from the
        *Generación y Consumo* webpage.

        Parameters:
        -----------
        self.driver: WebDriver object.
            The webdriver that will be used to scrape the webpage.

        Returns:
        --------
        percentage_renewable: float.
            The percentage of generated renewable energy.
        renewable_power: float.
            The generated power of renewable energy.
        wind_power: float.
            The generated power of wind energy.
        water_power: float.
            The generated power of water energy.
        solar_power: float.
            The generated power of solar energy.
        nuclear_power: float.
            The generated power of nuclear energy.
        thermo_renewable_power: float:
            The generated power of renewable thermal energy.
        """
        percentage_renewable = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    GeneracionConsumoPointers.PERC_RENEW_GEN
                )
            )
            .text
        )
        renewable_power = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    GeneracionConsumoPointers.RENEW_GEN_MW
                )
            )
            .text
        )
        wind_power = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    GeneracionConsumoPointers.WIND_MW
                )
            )
            .text
        )
        water_power = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    GeneracionConsumoPointers.WATER_MW
                )
            )
            .text
        )
        solar_power = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    GeneracionConsumoPointers.SOLAR_MW
                )
            )
            .text
        )
        nuclear_power = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    GeneracionConsumoPointers.NUCLEAR_MW
                )
            )
            .text
        )
        thermo_renewable_power = (
            WebDriverWait(self.driver, 20)
            .until(
                EC.presence_of_element_located(
                    GeneracionConsumoPointers.THERMO_RENEW_MW
                )
            )
            .text
        )

        return (
            percentage_renewable,
            renewable_power,
            wind_power,
            water_power,
            solar_power,
            nuclear_power,
            thermo_renewable_power,
        )


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
