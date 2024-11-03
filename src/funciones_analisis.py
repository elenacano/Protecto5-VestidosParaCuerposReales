import pandas as pd # type: ignore
import sys
import os
import plotly.express as px  # type: ignore
import plotly.graph_objects as go # type: ignore
from plotly.subplots import make_subplots # type: ignore
import plotly.io as pio # type: ignore


def querie_prendas_por_marca(conexion):
    cursor = conexion.cursor()
    cursor.execute("""SELECT nombre AS marca, num_vestidos
                        FROM (SELECT id_marca, count(id_vestido) AS num_vestidos
                            FROM vestidos v 
                            GROUP BY id_marca) AS taux
                        INNER JOIN marcas m ON m.id_marca=taux.id_marca
                        order by num_vestidos desc;""")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=column_names)
    return df

def grafica_prendas_por_marca(df):
    fig = px.bar(df, x="marca", y="num_vestidos", 
             title="Distribución de Vestidos por Marca", 
             labels={"marca": "Marca", "num_vestidos": "Número de Vestidos"},
             text="num_vestidos")
    fig.update_traces(textposition='inside')
    fig.update_layout(height=500, width=800)
    fig.show()

def querie_tallas_por_marca(conexion):
    cursor = conexion.cursor()
    cursor.execute(""" SELECT nombre, talla, num_tallas
                        FROM (SELECT id_marca, talla, count(talla) AS num_tallas
                                FROM vestidos v
                                GROUP BY id_marca, talla
                                ORDER BY id_marca) AS taux
                        INNER JOIN marcas AS m ON m.id_marca = taux.id_marca; """)
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=column_names)
    return df


def grafico_tallas_por_marca(df):
    talla_orden = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL', '5XL']

    # Convertir la columna 'talla' a tipo categórico y ordenar
    df['talla'] = pd.Categorical(df['talla'], categories=talla_orden, ordered=True)

    # Agrupar el DataFrame por cada marca
    marcas_grupos = df.groupby('nombre')

    # Contar el número de marcas y configurar subplots
    num_marcas = len(marcas_grupos)
    rows = (num_marcas // 2) + (num_marcas % 2)
    fig = make_subplots(rows=rows, cols=2, subplot_titles=list(marcas_grupos.groups.keys()))

    # Añadir una gráfica de barras para cada marca en un subplot
    row, col = 1, 1
    for nombre_marca, datos_marca in marcas_grupos:
        # Ordenar las tallas dentro de cada marca
        datos_marca = datos_marca.sort_values('talla')
        
        # Añadir la barra al subplot correspondiente
        fig.add_trace(
            go.Bar(
                x=datos_marca["talla"],
                y=datos_marca["num_tallas"],
                text=datos_marca["num_tallas"],
                textposition='inside'
            ),
            row=row,
            col=col
        )
        
        # Cambiar de columna o de fila en la matriz de subplots
        col += 1
        if col > 2:
            col = 1
            row += 1

    # Ajustar el layout de la figura
    fig.update_layout(
        title="Distribución de Prendas por Talla para Cada Marca",
        margin=dict(t=60),
        height=1000,  # Altura de la figura
        width=1000
    )

    # Establecer el rango del eje y para todas las subgráficas
    #fig.update_yaxes(range=[0, 200])

    # Mostrar la figura
    fig.show()



def querie_precio_por_marca(conexion):
    cursor = conexion.cursor()
    cursor.execute("""SELECT nombre AS marca, media_precio, mediana_precio
                    FROM (SELECT id_marca, round(avg(precio),2) AS media_precio, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY precio) AS mediana_precio
                        FROM vestidos v 
                        GROUP BY id_marca) AS taux
                    INNER JOIN marcas m ON m.id_marca=taux.id_marca
                    ORDER BY mediana_precio;""")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(data, columns=column_names)
    return df

def grafico_precio_por_marca(df):
    df_melted = df.melt(id_vars='marca', value_vars=['media_precio', 'mediana_precio'], var_name='tipo_precio', value_name='precio')
    fig = px.bar(df_melted, 
                x='marca', 
                y='precio', 
                color='tipo_precio',  # Usar color para distinguir media y mediana
                barmode='group',  # Agrupar las barras
                labels={'precio': 'Precio', 'tipo_precio': 'Tipo de Precio'},
                title='Media y Mediana de Precios por Marca')
    #pio.write_image(fig, 'grafico_precio_por_marca.png', format='png')
    fig.show()


def querie_precio_por_talla(conexion):
    cursor = conexion.cursor()
    cursor.execute("""SELECT talla, round(avg(precio),2) AS media_precio, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY precio) AS mediana_precio
                    FROM vestidos v 
                    GROUP BY talla;""")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(data, columns=column_names)

    talla_orden = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL', '5XL', '6XL']
    df['talla'] = pd.Categorical(df['talla'], categories=talla_orden, ordered=True)
    df = df.sort_values('talla').reset_index(drop=True)

    return df


def grafica_precio_por_talla(df):
    df_melted = df.melt(id_vars='talla', value_vars=['media_precio', 'mediana_precio'], var_name='tipo_precio', value_name='precio')
    fig = px.bar(df_melted, 
                x='talla', 
                y='precio', 
                color='tipo_precio',  # Usar color para distinguir media y mediana
                barmode='group',  # Agrupar las barras
                labels={'precio': 'Precio', 'tipo_precio': 'Tipo de Precio'},
                title='Media y Mediana de Precios por Talla')
    fig.show()
    

def querie_porcentaje_por_talla_categoria(conexion):
    cursor = conexion.cursor()
    cursor.execute("""SELECT nombre AS categoria, talla, num_tallas, porcentaje
                    FROM (SELECT id_categoria, talla, count(talla) AS num_tallas, SUM(COUNT(talla)) OVER (PARTITION BY id_categoria) AS total_vestidos_categoria, round(count(talla)/SUM(COUNT(talla)) OVER (PARTITION BY id_categoria)*100, 2) AS porcentaje
                                FROM vestidos v 
                                GROUP BY id_categoria, talla
                                ORDER BY id_categoria) AS taux
                    INNER JOIN categorias c ON c.id_categoria=taux.id_categoria
                    WHERE c.nombre != 'sin categoria'
                    ORDER BY nombre;""")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(data, columns=column_names)
    return df


def grafica_porcentaje_por_talla_categoria(df):
    talla_orden = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL', '5XL', '6XL']
    df['talla'] = pd.Categorical(df['talla'], categories=talla_orden, ordered=True)

    # Ordenar el DataFrame para asegurar que las tallas estén en el orden correcto dentro de cada categoría
    df = df.sort_values(['categoria', 'talla'])

    # Crear el objeto make_subplots con tres filas y una columna
    fig = make_subplots(rows=3, cols=1, subplot_titles=("Corto", "Largo", "Midi"))

    # Crear gráficos de barras para cada categoría y añadirlos al subplot correspondiente
    categorias = ["corto", "largo", "midi"]
    for i, categoria in enumerate(categorias, start=1):
        datos_categoria = df[df['categoria'] == categoria]
        fig.add_trace(
            go.Bar(
                x=datos_categoria['talla'],
                y=datos_categoria['porcentaje'],
                text=datos_categoria['porcentaje'],
                textposition='inside',
                name=categoria.capitalize()
            ),
            row=i, col=1
        )

    # Ajustar el layout de la figura
    fig.update_layout(
        height=700,  # Altura del gráfico total
        title_text="Porcentaje de prendas por talla para cada categoría",
        showlegend=False,
    )

    # Mostrar el gráfico
    fig.show()


def querie_porcentaje_por_talla(conexion):
    cursor = conexion.cursor()
    cursor.execute("""SELECT talla, count(id_vestido) AS vestidos_talla, round(COUNT(id_vestido)*100.0/(SELECT COUNT(id_vestido) FROM vestidos),2) AS vestidos_talla_normalizado
                        FROM vestidos v 
                        GROUP BY talla;""")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(data, columns=column_names)

    return df


def grafica_porcentaje_por_talla(df):
    
    talla_orden = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL', '5XL', '6XL']
    df['talla'] = pd.Categorical(df['talla'], categories=talla_orden, ordered=True)

    # Ordenar el DataFrame para asegurar que las tallas estén en el orden correcto dentro de cada categoría
    df = df.sort_values('talla')
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["talla"],
            y=df["vestidos_talla_normalizado"],
            name="Distribución de Vestidos (Barras)",
            text=df["vestidos_talla_normalizado"],
            textposition="inside"
        )
    )

    # Crear gráfico de línea con relleno
    fig.add_trace(
        go.Scatter(
            x=df["talla"],
            y=df["vestidos_talla_normalizado"],
            mode="lines+markers",
            name="Distribución Normalizada (Línea con Relleno)",
            line=dict(shape="spline", width=4),  # Línea suave
            fill='tozeroy',
            text=df["vestidos_talla_normalizado"],
            textposition="top center"
        )
    )

    # Configurar el layout de la figura
    fig.update_layout(
        title="Distribución de Vestidos por Talla",
        height=500,
        width=1000,
        xaxis_title="Talla",
        yaxis_title="Porcentaje de Vestidos",
        barmode="overlay",  # Superponer la barra y el área
        showlegend=False 
    )

    # Mostrar la figura
    fig.show()
