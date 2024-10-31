import json
import os

colores = {
    'SILVER': 'plata',
    'BLACK': 'negro',
    'PINK': 'rosa',
    'MID BLUE': 'azul medio',
    'LIGHT BLUE': 'azul claro',
    'CREAM': 'crema',
    'YELLOW': 'amarillo',
    'WHITE': 'blanco',
    'ORANGE': 'naranja',
    'PURPLE': 'morado',
    'BROWN': 'marrón',
    'BEIGE': 'beige',
    'GREY': 'gris',
    'BLUE': 'azul',
    'NAVY': 'azul marino',
    'GREEN': 'verde',
    'RED': 'rojo',
    'DARK BROWN': 'marrón oscuro'
}

def creacion_diccionario_asos(dic_precio):
    dic_vestido = {
        "nombre" : [],
        "marca" : [],
        "precio" : [],
        "color" : [],
        "talla" : [],
        "disponible" : []
    }

    for archivo in os.listdir("../datos/api_asos")[1:]:

        with open(f"../datos/api_asos/{archivo}", 'r') as file:
            vestido = json.load(file)

        id = int(archivo.split("_")[1][:-5])
        marca = "Mango"
        for i in range(len(vestido["data"]["localisedData"])):
            if vestido["data"]["localisedData"][i]["locale"] == "es-ES":
                nombre = vestido["data"]["localisedData"][i]["title"]

        for j in range(len(vestido["data"]["variants"])):
            color = vestido["data"]["variants"][j]["colour"]
            talla = vestido["data"]["variants"][j]["brandSize"]
            dispomible = vestido["data"]["variants"][j]["isAvailable"]

            dic_vestido["nombre"].append(nombre)
            dic_vestido["marca"].append(marca)
            dic_vestido["precio"].append(dic_precio[id])
            dic_vestido["color"].append(color)
            dic_vestido["talla"].append(talla)
            dic_vestido["disponible"].append(dispomible)

    return dic_vestido
