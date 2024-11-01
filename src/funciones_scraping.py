from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from time import sleep

from selenium import webdriver # type: ignore
from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore
import re

def selenium_bylila():
    lista_url = ["https://naturalbylila.com/ropa/vestidos/?product-cat=vestidos-cortos", "https://naturalbylila.com/ropa/vestidos/?product-cat=vestidos-largos"]

    lista_vestidos_cortos_largos = []

    for url in lista_url:
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


def extraccion_info_bylila(lista_vestidos_cortos_largos):
    dic_vestido = {
        "nombre" : [],
        "marca" : [],
        "precio" : [],
        "talla" : [],
        "categoria" :[]
        }
    i=0
    for links_vestidos in lista_vestidos_cortos_largos:
        for url in links_vestidos:
            res = requests.get(url)
            if res.status_code != 200:
                print(url)

            sopa_vestido = BeautifulSoup(res.content, "html.parser")
            
            
            nombre = sopa_vestido.find("span", {"class":"titulosinglegrande"}).getText()
            marca = "Natural by Lila"
            precio = float(sopa_vestido.find("span", {"class":"woocommerce-Price-amount amount"}).getText().replace("€", ""))
            # colores = []
            # table = sopa_vestido.find("table", {"class":"variations"})
            # colores = table.findAll("td")[1]

            # for elem in colores.findAll("option")[1:]:
            #     colores.append((elem.getText()))
            #     print(elem.getText())

            # Sacamos las tallas
            desc = sopa_vestido.find("div", {"class":"content-desc"}).findAll("p")[1].text.lower()
            table = sopa_vestido.find("table", {"class":"variations"})

            if "talla única" in desc:
                lista_tallas = ["S", "M"]

            elif "disponible en talla" in desc:
                tallas_disp = desc.split("talla ")[1:]
                lista_tallas=[]
                for talla in tallas_disp:
                    lista_tallas.append(talla[0].upper())
                    
            elif len(table.findAll('tr')) > 3:
                fila_tallas = table.findAll("tr")[3]
                tallas = fila_tallas.findAll("label")
                lista_tallas=[]
                for talla in tallas:
                    tallas_separadas = talla.text.upper().split("/")
                    lista_tallas.extend(tallas_separadas)
                    lista_tallas= list(set(lista_tallas))
                        
            else:
                lista_tallas=[sopa_vestido.find("div", {"class":"model-info"}).text[-1].upper()]

            # Creamos los diccionarios:
            for talla in lista_tallas:
                dic_vestido["nombre"].append(nombre)
                dic_vestido["marca"].append(marca)
                dic_vestido["precio"].append(precio)
                dic_vestido["talla"].append(talla)
                if i == 0:
                    dic_vestido["categoria"].append("corto")
                else:
                    dic_vestido["categoria"].append("largo")
        i+=1
    return dic_vestido


def obtencion_links_ladypipa():
    url = "https://ladypipa.com/collections/vestidos"
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    sleep(1)

    product_list= driver.find_element(By.CLASS_NAME, 'product-list')
    sleep(1)
    product_cards = product_list.find_elements(By.CLASS_NAME, 'product-card')
    sleep(1)

    lista_links=[]
    for i in range (2, len(product_cards)+1):
        tarjeta = driver.find_element("css selector", f'#ProductGridContainer > div.collection__results > div > product-list > product-card:nth-child({i})')
        div_link = tarjeta.find_element("css selector", "div.product-card__figure a")
        lista_links.append(div_link.get_attribute("href"))

    driver.quit()
    return lista_links


def extraccion_info_ladypipa(links_ladypipa):
    url_base="https://ladypipa.com"

    dic_vestido = {
            "nombre" : [],
            "marca" : [],
            "precio" : [],
            "color" : [],
            "talla" : [],
            "categoria" :[]
            }

    for url in links_ladypipa:
        res = requests.get(url)
        if res.status_code != 200:
            print(url)

        sopa = BeautifulSoup(res.content, "html.parser")


        contenedor_enlaces= sopa.find("div", {"class":"variant-picker__option-values wrap gap-2"}).find_all('a', class_='color-swatch')
        enlaces_colores = [enlace['href'] for enlace in contenedor_enlaces]

        for enlace in enlaces_colores:

            url_aux = url_base + enlace
            res = requests.get(url_aux)
            if res.status_code != 200:
                print(url)
            
            
            sopa = BeautifulSoup(res.content, "html.parser")

            nombre = sopa.find("div", {"class":"product-info__title"}).text.replace("\n","").strip()
            marca = "Ladypipa"

            # Extraemos el color
            contenedor_color = sopa.find("div", {"class":"variant-picker__option-info"}).text
            color = contenedor_color.strip().replace("Color:", "").strip()

            # Extraemos el precio
            patron = r"(\d+(?:,\d{1,2})?)\s*€"
            resultado = re.search(patron, sopa.find("sale-price").text)
            precio = resultado.group(1)

            # Buscamos en la descripcion cómo es el vestido para asignarle una categoría
            desc = sopa.select("div.prose p")[2].text

            patron = r'\b(largo|midi|corto|maxi|mini)\b'
            coincidencias = re.findall(patron, desc)
            categoria = coincidencias[0]

            # Sacamos las tallas disponibles
            lista_tallas=[]
            contenedor_tallas = sopa.find("div", {"class":"form-control"}).find("select").find_all('option')
            for talla in contenedor_tallas:
                if not talla.has_attr('disabled'):
                    lista_tallas.append(talla.text.split()[0])
            lista_tallas

            for elem in lista_tallas:
                dic_vestido["nombre"].append(nombre)
                dic_vestido["marca"].append(marca)
                dic_vestido["precio"].append(precio)
                dic_vestido["color"].append(color)
                dic_vestido["talla"].append(elem)
                dic_vestido["categoria"].append(categoria)

    return dic_vestido