from selenium.webdriver.common.action_chains import ActionChains

class ExtendedActions(ActionChains):
    """
    Extends the functionality of the ActionChains method from the Selenium WebDriver.
    Source: https://stackoverflow.com/questions/53467739/how-to-implement-method-chaining-of-selenium-multiple-webdriverwait-in-python
    """
    def wait(self, second, condition):
        element = WebDriverWait(self._driver, second).until(condition)
        self.move_to_element(element)
        return self

# class StringProcessing(object):
    
#     def get_stars_ratings(text):
#         stripped_text = text.split(' — ')
#         stars = float(re.findall(r'\d+\.\d+', stripped_text[0])[0])
#         ratings = int(stripped_text[1].split(' rating')[0].replace(',', ''))
#         return stars, ratings
    
#     def get_scores(text):
#         return int(text.split('score: ')[1].split('</a>')[0].replace(',', ''))
    
#     def get_votes(text):
#         return int(text.split(' people voted')[0].split('>')[1].replace(',', ''))
    
#     def get_description(soup):
#         book_description = ''
#         find_description = soup.find(BookPagePointers.BOOK_DESCRIPTION_DIV[0], class_=BookPagePointers.BOOK_DESCRIPTION_DIV[1])
#         book_description = find_description.find(BookPagePointers.BOOK_DESCRIPTION_SPAN[0], class_=BookPagePointers.BOOK_DESCRIPTION_SPAN[1]).text.strip()
#         return book_description
    
#     def get_genres(soup):
#         genres = ''
#         for a in soup.find_all('a'):
#             if 'genres' in a.get('href'):
#                 if genres == '':
#                     genres = a.get_text(strip=True)
#                 else:
#                     genres += ', ' + a.get_text(strip=True)
#         return genres
    
#     def get_pages(soup):
#         find_pages = soup.find(BookPagePointers.PAGES[0], attrs={BookPagePointers.PAGES[1]:BookPagePointers.PAGES[2]}).text.strip()
#         return int(re.search(r'\d+', find_pages).group(0))
    
#     def get_publication_year(soup):
#         find_publication_year = soup.find(BookPagePointers.PUBLICATION_YEAR[0], attrs={BookPagePointers.PUBLICATION_YEAR[1]:BookPagePointers.PUBLICATION_YEAR[2]}).text.strip()
#         return int(re.search(r'\d{4}', find_publication_year).group(0))
    

class SaveUtils(object):
    def __init__(self, filename, dictionary) -> None:
        self.filename = filename
        self.dictionary = dictionary
        
    def save_data(self):
        with open(self.filename, 'w', newline='\n') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(self.dictionary.keys())
            writer.writerows(zip(*self.dictionary.values()))