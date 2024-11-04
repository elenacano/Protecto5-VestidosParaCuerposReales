import pandas as pd # type: ignore
import sys
import os
import plotly.express as px  # type: ignore
import plotly.graph_objects as go # type: ignore
from plotly.subplots import make_subplots # type: ignore


def querie_prendas_por_marca(conexion):

    """
    Ejecuta una consulta SQL para obtener la cantidad de vestidos por marca en la base de datos.

    Parameters:
    conexion (object): Conexión a la base de datos.

    Returns:
    pd.DataFrame: DataFrame con las columnas 'marca' y 'num_vestidos' ordenadas por número de vestidos en orden descendente.
    """

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

    """
    Genera y muestra un gráfico de barras con la distribución de vestidos por marca.

    Parameters:
    df (pd.DataFrame): DataFrame que contiene las columnas 'marca' y 'num_vestidos'.
    """

    fig = px.bar(df, x="marca", y="num_vestidos", 
             title="Distribución de Vestidos por Marca", 
             labels={"marca": "Marca", "num_vestidos": "Número de Vestidos"},
             text="num_vestidos")
    fig.update_traces(textposition='inside')
    fig.update_layout(height=500, width=800)
    fig.show()


def querie_tallas_por_marca(conexion):

    """
    Ejecuta una consulta SQL para obtener la cantidad de vestidos por talla para cada marca.

    Parameters:
    conexion (object): Conexión a la base de datos.

    Returns:
    pd.DataFrame: DataFrame con las columnas 'nombre', 'talla' y 'num_tallas'.
    """

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

    """
    Genera un gráfico de barras que muestra la distribución de tallas para cada marca en subplots.

    Parameters:
    df (pd.DataFrame): DataFrame que contiene las columnas 'nombre', 'talla' y 'num_tallas'.
    """

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

    """
    Ejecuta una consulta SQL para obtener la media y mediana de precios de vestidos por marca.

    Parameters:
    conexion (object): Conexión a la base de datos.

    Returns:
    pd.DataFrame: DataFrame con las columnas 'marca', 'media_precio' y 'mediana_precio', ordenadas por mediana de precio.
    """

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

    """
    Genera un gráfico de barras que muestra la media y mediana de precios por marca.

    Parameters:
    df (pd.DataFrame): DataFrame con las columnas 'marca', 'media_precio' y 'mediana_precio'.
    """

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

    """
    Ejecuta una consulta SQL para obtener la media y mediana de precios por talla.

    Parameters:
    conexion (object): Conexión a la base de datos.

    Returns:
    pd.DataFrame: DataFrame con las columnas 'talla', 'media_precio' y 'mediana_precio', ordenado por talla.
    """

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

    """
    Genera un gráfico de barras que muestra la media y mediana de precios por talla.

    Parameters:
    df (pd.DataFrame): DataFrame que contiene las columnas 'talla', 'media_precio' y 'mediana_precio'.
    """

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

    """
    Ejecuta una consulta SQL para obtener el porcentaje de vestidos por talla para cada categoría de prenda.

    Parameters:
    conexion (object): Conexión a la base de datos.

    Returns:
    pd.DataFrame: DataFrame con las columnas 'categoria', 'talla', 'num_tallas' y 'porcentaje'.
    """

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

    """
    Genera gráficos de barras en subplots que muestran el porcentaje de vestidos por talla para cada categoría de prenda.

    Parameters:
    df (pd.DataFrame): DataFrame que contiene las columnas 'categoria', 'talla', 'num_tallas' y 'porcentaje'.
    """

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

    """
    Ejecuta una consulta SQL para obtener el porcentaje de vestidos por cada talla.

    Parameters:
    conexion (object): Conexión a la base de datos.

    Returns:
    pd.DataFrame: DataFrame con las columnas 'talla', 'vestidos_talla' y 'vestidos_talla_normalizado'.
    """

    cursor = conexion.cursor()
    cursor.execute("""SELECT talla, count(id_vestido) AS vestidos_talla, round(COUNT(id_vestido)*100.0/(SELECT COUNT(id_vestido) FROM vestidos),2) AS vestidos_talla_normalizado
                        FROM vestidos v 
                        GROUP BY talla;""")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(data, columns=column_names)

    return df


def grafica_porcentaje_por_talla(df):

    """
    Genera un gráfico combinado de barras y líneas para mostrar el porcentaje de vestidos por talla.

    Parameters:
    df (pd.DataFrame): DataFrame que contiene las columnas 'talla', 'vestidos_talla' y 'vestidos_talla_normalizado'.
    """

    talla_orden = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL', '5XL', '6XL']
    df['talla'] = pd.Categorical(df['talla'], categories=talla_orden, ordered=True)

    # Ordenar el DataFrame para asegurar que las tallas estén en el orden correcto dentro de cada categoría
    df = df.sort_values('talla')

    df['acumulado'] = df['vestidos_talla_normalizado'].cumsum()
    total_vestidos = df['vestidos_talla_normalizado'].sum()
    mediana_pos = total_vestidos / 2

    # Encontrar la talla en la posición de la mediana
    talla_mediana = df[df['acumulado'] >= mediana_pos].iloc[0]['talla']
    valor_talla_L = df[df['talla'] == 'L']['vestidos_talla_normalizado'].values[0]


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

    fig.add_shape(
        type="line",
        x0=talla_mediana,
        x1=talla_mediana,
        y0=0,
        y1=df['vestidos_talla_normalizado'].max(),  # Extensión de la línea
        line=dict(color="red", width=2),  # Línea punteada
        xref="x",
        yref="y"
    )

    fig.add_shape(
        type="line",
        x0="L",
        x1="L",
        y0=0,
        y1=valor_talla_L,
        line=dict(color="green", width=2),
        xref="x",
        yref="y"
    )

    # Mostrar la figura
    fig.show()


def grafica_vestidos_talla_f21(conexion):

    """
    Ejecuta una consulta SQL para obtener el porcentaje de vestidos por cada talla en la tienda Forever21 y muestra un gráfico de barras.

    Parameters:
    conexion (object): Conexión a la base de datos.
    """
     
    cursor = conexion.cursor()
    cursor.execute("""SELECT talla, count(id_vestido) AS vestidos_talla, round(COUNT(id_vestido)*100.0/(SELECT COUNT(id_vestido) FROM vestidos),2) AS vestidos_talla_normalizado
                        FROM vestidos v 
                        GROUP BY talla;""")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(data, columns=column_names)
    talla_orden = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL', '5XL', '6XL']
    df['talla'] = pd.Categorical(df['talla'], categories=talla_orden, ordered=True)

    # Ordenar el DataFrame para asegurar que las tallas estén en el orden correcto dentro de cada categoría
    df = df.sort_values('talla')

    fig = px.bar(df, 
                    x='talla', 
                    y='vestidos_talla_normalizado', 
                    labels={'talla': 'Talla', 'vestidos_talla_normalizado': 'Porcentaje vestidos'},
                    title='Porcentaje de Vestidos por Talla en Forever21',
                    text='vestidos_talla_normalizado')
    fig.update_traces(textposition='inside')
    fig.show()


def grafica_stock_talla_f21(conexion):

    """
    Ejecuta una consulta SQL para obtener el stock total por cada talla en la tienda Forever21 y muestra un gráfico de barras.

    Parameters:
    conexion (object): Conexión a la base de datos.
    """
    
    cursor = conexion.cursor()
    cursor.execute("""SELECT talla, sum(stock)
                    FROM vestidos_forever21 vf
                    GROUP BY talla;""")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(data, columns=column_names)
    talla_orden = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL', '4XL', '5XL', '6XL']
    df['talla'] = pd.Categorical(df['talla'], categories=talla_orden, ordered=True)

    # Ordenar el DataFrame para asegurar que las tallas estén en el orden correcto dentro de cada categoría
    df = df.sort_values('talla')

    fig = px.bar(df, 
                    x='talla', 
                    y='sum', 
                    labels={'sum': 'Total stock', 'talla': 'Talla'},
                    title='Stock por Talla en Forever21',
                    text='sum')
    fig.update_traces(textposition='inside')
    fig.show()
            