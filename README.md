# Webscraping practicum

## Install dependencies

```bash
pip install -r requirements.txt
```

## Description

This repository contains the code, data and documentation done in the framework
of a practice exercise for the class *Tipologia i cicle de vida de les dades*
from the *Master in Data Science of the Universitat Oberta de Catalunya*.

The exercise consisted in extracting data using *Web Scraping* with Python from
the website *https://www.esios.ree.es/es/*.

**Disclaimer:** Express consent has been given by *Red Eléctrica de España*, the
source and propietary of the data, to perform this exercise and under no
circumstance they support the reutilization of the data. We express our
intention to use the data for the purpose of the activity and decline any
commercial interest in the use of the data extracted.

## Authors 

The authors of this activity are: **Esther Manzano i Martín** i **Albert
Queraltó López**.

## Source code

* **src/__main__.py:** starts the scraping process.
* **src/navigation.py:** contains all classes and methods that enable the
  navigation to the different pages and to the elements of each page.
* **src/data_scraper.py:** contains all classes and methods that enable the
  extraction of the data from the different pages.
* **src/font_code_pointers.py:** contains classes that classify the variables
  with information to locate the different page elements.
* **src/support_functions.py:** contains additional classes and methods to have
  cleaner code in the main page, as well as the functionality to save the data.

## Data

The data extracted from the website is stored in the folder **dataset**. The
data is stored in a unique *.csv* file and contains hourly data in a range of
dates from *02-11-2021* to *07-11-2022*.


## References
