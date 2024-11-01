from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from time import sleep
# Selenium para establecer la configuración del driver
# -----------------------------------------------------------------------
from selenium import webdriver # type: ignore

def selenium_bylila():
    lista_url = ["https://naturalbylila.com/ropa/vestidos/?product-cat=vestidos-cortos", "https://naturalbylila.com/ropa/vestidos/?product-cat=vestidos-largos"]

    lista_vestidos_cortos_largos = []

    for url in lista_url:
        largura = url.split("-")[-1]
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome()
        driver.get(url)
        driver.maximize_window()
        sleep(1)


        driver.find_element("css selector", "#wrapper > div.page-wrapper-inner > div > div.term-description > div").click()
        sleep(5)
        #Cerramos el anuncio del black friday
        driver.find_element("css selector", "body > div.cn_content_backdrop-d09b5257-14c2-48d5-b8a8-4f63527664a6 > div > div.cn_content_close-d09b5257-14c2-48d5-b8a8-4f63527664a6 > a").click()
        sleep(1)
        # Aceptamos las cookies
        driver.find_element("css selector", "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
        sleep(1)
        #Cargamos toda la página
        driver.execute_script("window.scrollTo(0, 50000);")
        sleep(1)
        driver.execute_script("window.scrollTo(0, 50000);")

        # Obtenemos los links de los productos de la página
        sleep(1)
        marco_productos = driver.find_element("css selector", "#shop-products > div.row > div > div.wcapf-before-products > ul")
        sleep(1)
        productos = marco_productos.find_elements(By.CSS_SELECTOR, "div.product-title a.product-link")

        lista_links=[]
        for producto in productos:
            lista_links.append(producto.get_attribute("href"))
        
        lista_vestidos_cortos_largos.append(lista_links)

        driver.quit()
        
    return lista_vestidos_cortos_largos