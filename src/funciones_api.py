import json
import os
import requests # type: ignore
import dotenv # type: ignore

dotenv.load_dotenv()

def busqueda_vestido_marca(lista_id, lista_marcas):

    url = "https://asos10.p.rapidapi.com/api/v1/getProductList"
    api_key = os.getenv("api_asos")

    for i in range(len(lista_id)):
        
        id=lista_id[i]
        marca = lista_marcas[i]

        querystring = {"categoryId":id, "sort":"recommended", "limit":2000}

        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "asos10.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response_mango = response.json()

        # Guardamos el resultado en datos
        os.makedirs(f"../datos/api_asos/{marca}", exist_ok=True)
        with open(f"../datos/api_asos/{marca}/vestidos_{marca}.json", 'w') as file:
            json.dump(response_mango, file, indent=4)



def detalles_vestido(lista_marcas, dic_info):
    api_key = os.getenv("api_asos")

    for marca in lista_marcas:
        lista_id_vestido = dic_info[marca][0]

        for id in lista_id_vestido:

            url = "https://asos10.p.rapidapi.com/api/v1/getProductDetails"

            querystring = {"productId":[id]}

            headers = {
                "x-rapidapi-key": api_key,
                "x-rapidapi-host": "asos10.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)

            res = response.json()
            with open(f"../datos/api_asos/{marca}/vestido_{id}.json", 'w') as file:
                json.dump(res, file, indent=4)



def creacion_diccionario_asos(dic_info, lista_marcas):
    dic_vestido = {
        "nombre" : [],
        "marca" : [],
        "precio" : [],
        "color" : [],
        "talla" : [],
        "disponible" : []
    }

    for marca in lista_marcas:
        print(marca)
        for archivo in os.listdir(f"../datos/api_asos/{marca}")[1:]:

            with open(f"../datos/api_asos/{marca}/{archivo}", 'r') as file:
                vestido = json.load(file)

            id = int(archivo.split("_")[1][:-5])
            marca = marca
            for i in range(len(vestido["data"]["localisedData"])):
                if vestido["data"]["localisedData"][i]["locale"] == "es-ES":
                    nombre = vestido["data"]["localisedData"][i]["title"]

            for j in range(len(vestido["data"]["variants"])):
                color = vestido["data"]["variants"][j]["colour"]
                talla = vestido["data"]["variants"][j]["brandSize"]
                dispomible = vestido["data"]["variants"][j]["isAvailable"]

                dic_vestido["nombre"].append(nombre)
                dic_vestido["marca"].append(marca)
                dic_vestido["precio"].append(dic_info[marca][1][id])
                dic_vestido["color"].append(color)
                dic_vestido["talla"].append(talla)
                dic_vestido["disponible"].append(dispomible)

    return dic_vestido


def creacion_diccionario_forever21():
    dic_vestido = {
        "nombre" : [],
        "marca" : [],
        "precio" : [],
        "color" : [],
        "talla" : [],
        "stock" : []
    }

    for archivo in os.listdir("../datos/api_forever21")[:-1]:

        with open(f"../datos/api_forever21/{archivo}", 'r') as file:
            producto = json.load(file)

        id = int(archivo.split("_")[0])
        marca = "Forever21"
        for i in range(len(producto["product"]["Variants"])):
            for j in range(len(producto["product"]["Variants"][i]["Sizes"])):
                nombre = producto["product"]["Variants"][i]["Sizes"][j]["DisplayName"]
                color = producto["product"]["Variants"][i]["ColorName"]
                talla = producto["product"]["Variants"][i]["Sizes"][j]["SizeName"]
                precio = producto["product"]["Variants"][i]["Sizes"][j]["Price"]
                stock = producto["product"]["Variants"][i]["Sizes"][j]["inventories"][0]["stock_level"]

                elems_talla = talla.split("/")
                for elem in elems_talla:
                    dic_vestido["nombre"].append(nombre)
                    dic_vestido["marca"].append(marca)
                    dic_vestido["precio"].append(precio)
                    dic_vestido["color"].append(color)
                    dic_vestido["talla"].append(elem)
                    dic_vestido["stock"].append(stock)

    return dic_vestido