from selenium.webdriver.common.by import By


class MainPagePointers(object):
    MORE_BOOK_LISTS = (By.LINK_TEXT, "More book lists")
    
class ListopiaPointers(object):
    X_BUTTON = (By.CLASS_NAME, 'gr-iconButton')
    BEST_BOOKS_EVER = (By.LINK_TEXT, 'Best Books Ever')
    
class BestBooksEverPointers(object):
    POSITION_ORDER = ('td', 'number')
    BOOK_TITLE = ('a', 'bookTitle')
    AUTHOR_NAME = ('a', 'authorName')
    STARS_RATINGS = ('span', 'minirating')
    SCORE = ('a', 'score:')
    VOTES = ('a', 'people voted')
    NEXT_PAGE = (By.CSS_SELECTOR, '#all_votes > div.pagination > a.next_page')
    NEXT_PAGE_DISABLED = (By.CSS_SELECTOR, '#all_votes > div.pagination > span.next_page.disabled')


class BookPagePointers(object):
    BOOK_DESCRIPTION_DIV = ('div', 'BookPageMetadataSection__description')
    BOOK_DESCRIPTION_SPAN = ('span', 'Formatted')
    PAGES = ('p', 'data-testid', 'pagesFormat')
    PUBLICATION_YEAR = ('p', 'data-testid', 'publicationInfo')