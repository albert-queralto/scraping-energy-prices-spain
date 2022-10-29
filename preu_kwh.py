# Inicialització
import re
import requests

from bs4 import BeautifulSoup
from csv import writer
from datetime import datetime

# Constants.
URL = "https://tarifaluzhora.es"
NOW = datetime.now()
DATETIME_NOW = NOW.strftime("%Y-%m-%d %H:%M:%S")

# Accés a la web.
page = requests.get(URL)

# Extreu HTML de la web.
soup = BeautifulSoup(page.content, "html.parser")

# Extreu la part de HTML que conté la paraula 'Horas'.
section = soup(text=re.compile('Horas'))

# Seleccionem la part del preu per hora.
section_str = str(section)
start = section_str.find("['00h - 01h")
end = section_str.find("var options", start) - 20

# Llista de preus en format 'string'.
prices_str = section_str[start:end]

# Neteja de la 'string'.
prices_str = section_str[start:end]
prices_str = prices_str.replace("['", "")
prices_str = prices_str.replace("\n", "")
prices_str = prices_str.replace(",", "")
prices_str = prices_str.replace("'", "")

# Llista de preus per hora.
prices_list = prices_str.split("]")

# Guardem els resultats en un CSV.
for i in prices_list:
    with open(f'preu_hora_{DATETIME_NOW}.csv', 'a') as f:
        writer_object = writer(f)
        writer_object.writerow(i.split("h 0"))
        f.close()
