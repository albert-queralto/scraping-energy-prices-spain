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
    
    # Variables to locate different elements of the hour selector
    HOUR_SELECTOR_HIDDEN = (By.XPATH, '//*[@id="mypCosteWidgetView"]/div[1]/div/div/div[2]/div')
    HOUR_SELECTOR_HIDDEN_CHILD = (By.XPATH, '//*[@id="mypCosteWidgetView"]/div[1]/div/div/div[2]/div/div/div')
    HOUR_LIST_HIDDEN = (By.XPATH, f"//*[@class='chzn-container chzn-container-single']")
    HOUR_LIST_ACTIVE = (By.XPATH, f"//*[@class='chzn-container chzn-container-single chzn-container-active']")
    HOUR_LIST_ACTIVE_DROP = (By.XPATH, f"//*[@class='chzn-container chzn-container-single chzn-with-drop chzn-container-active']")
    HOUR_LIST_HIDDEN_CHILD = (By.XPATH, f"//*[@class='chzn-single']")
    SELECT_HOUR_LIST = (By.XPATH, '//select[contains(@class, "select-timepicker hours")]')    
    
    # Variables to locate the average price for the energy (total, free and reference)
    PRECIO_MEDIO_TOTAL = (By.XPATH, '//*[@id="mypCosteWidgetView"]/div[2]/div[3]/div/table/tbody/tr[1]/td[1]')
    PRECIO_MEDIO_COM_LIBRE = (By.XPATH, '//*[@id="mypCosteWidgetView"]/div[2]/div[3]/div/table/tbody/tr[1]/td[2]')
    PRECIO_MEDIO_COM_REF = (By.XPATH, '//*[@id="mypCosteWidgetView"]/div[2]/div[3]/div/table/tbody/tr[1]/td[3]')
    
    # Variables to locate the values of energy (total, free and reference)
    ENERGIA_TOTAL = (By.XPATH, '//*[@id="mypCosteWidgetView"]/div[2]/div[3]/div/table/tbody/tr[2]/td[1]')
    ENERGIA_COM_LIBRE = (By.XPATH, '//*[@id="mypCosteWidgetView"]/div[2]/div[3]/div/table/tbody/tr[2]/td[2]')
    ENERGIA_COM_REF = (By.XPATH, '//*[@id="mypCosteWidgetView"]/div[2]/div[3]/div/table/tbody/tr[2]/td[3]')

    # Variables to locate the share (free and reference)
    CUOTA_COM_LIBRE = (By.XPATH, '//*[@id="mypCosteWidgetView"]/div[2]/div[3]/div/table/tbody/tr[3]/td[2]')
    CUOTA_COM_REF = (By.XPATH, '//*[@id="mypCosteWidgetView"]/div[2]/div[3]/div/table/tbody/tr[3]/td[3]')