from selenium.webdriver.common.by import By


class MainPagePointers(object):
    """
    Defines all the variables that link to elements on the main page.
    """
    
    MERCADOS_PRECIOS = (By.XPATH, "/html/body/header/div[2]/div/div/div[2]/nav/ul/li[3]/a")
    

class MercadosPreciosPointers(object):
    """
    Defines all the variables that enable actions in the *Mercados y precios* page.
    """    
    HOUR_SELECTOR_HIDDEN = (By.XPATH, '/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div/div')
    HOUR_LIST_HIDDEN = (By.XPATH, '/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div')
    SELECT_HOUR_LIST = (By.XPATH, '/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/select')
    FIND_CHZN_DROP = (By.XPATH, '/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/div')
    FIND_CHZN_RESULTS = (By.XPATH, '/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/div/ul')
    # li element with class active-result
    # PVPC_CEUTA_MELILLA = (By.XPATH, '//*[@id="serie-8744"]')
    # PVPC_PENINSULA_BALEARES_CANARIAS = (By.XPATH, '//*[@id="serie-8741"]')
    
    
    
    
# class ListopiaPointers(object):
#     X_BUTTON = (By.CLASS_NAME, 'gr-iconButton')
#     BEST_BOOKS_EVER = (By.LINK_TEXT, 'Best Books Ever')
    
# class BestBooksEverPointers(object):
#     POSITION_ORDER = ('td', 'number')
#     BOOK_TITLE = ('a', 'bookTitle')
#     AUTHOR_NAME = ('a', 'authorName')
#     STARS_RATINGS = ('span', 'minirating')
#     SCORE = ('a', 'score:')
#     VOTES = ('a', 'people voted')
#     NEXT_PAGE = (By.CSS_SELECTOR, '#all_votes > div.pagination > a.next_page')
#     NEXT_PAGE_DISABLED = (By.CSS_SELECTOR, '#all_votes > div.pagination > span.next_page.disabled')


# class BookPagePointers(object):
#     BOOK_DESCRIPTION_DIV = ('div', 'BookPageMetadataSection__description')
#     BOOK_DESCRIPTION_SPAN = ('span', 'Formatted')
#     PAGES = ('p', 'data-testid', 'pagesFormat')
#     PUBLICATION_YEAR = ('p', 'data-testid', 'publicationInfo')