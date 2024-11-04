import psycopg2 # type: ignore
import pandas as pd # type: ignore

def crear_db(database_name, postgres_pass, usuario):

    """
    Crea una base de datos en PostgreSQL si aún no existe.

    Parameters:
        - database_name (str): Nombre de la base de datos a crear.
        - postgres_pass (str): Contraseña del usuario de PostgreSQL.
        - usuario (str): Nombre del usuario de PostgreSQL.

    Notes:
        Conecta a la base de datos predeterminada `postgres` para verificar si `database_name` ya existe.
        Si no existe, se crea y se cierra la conexión.
    """

    # conexion a postgres
    conn = establecer_conn("postgres", postgres_pass, usuario) # Nos conectamos a la base de datos de postgres por defecto para poder crear la nueva base de datos
    
    # creamos un cursor con la conexion que acabamos de crear
    cur = conn.cursor()
    
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
    
    # Almacenamos en una variable el resultado del fetchone. Si existe tendrá una fila sino será None
    bbdd_existe = cur.fetchone()
    
    # Si bbdd_existe es None, creamos la base de datos
    if not bbdd_existe:
        cur.execute(f"CREATE DATABASE {database_name};")
        print(f"Base de datos {database_name} creada con éxito")
    else:
        print(f"La base de datos ya existe")
        
    # Cerramos el cursor y la conexion
    cur.close()
    conn.close()


def establecer_conn(database_name, postgres_pass, usuario, host="localhost"):

    """
    Establece una conexión a una base de datos de PostgreSQL.

    Parameters:
        - database_name (str): El nombre de la base de datos a la que conectarse.
        - postgres_pass (str): La contraseña del usuario de PostgreSQL.
        - usuario (str): El nombre del usuario de PostgreSQL.
        - host (str, opcional): La dirección del servidor PostgreSQL. Por defecto es "localhost".

    Returns:
        psycopg2.extensions.connection: La conexión establecida a la base de datos PostgreSQL.

    Notes:
        Establece la conexión en modo autocommit, eliminando la necesidad de ejecutar `commit` en cada operación.
    """

    # Crear la conexión a la base de datos PostgreSQL
    conn = psycopg2.connect(
        host=host,
        user=usuario,
        password=postgres_pass,
        database=database_name
    )

    # Establecer la conexión en modo autocommit
    conn.autocommit = True # No hace necesario el uso del commit al final de cada sentencia de insert, delete, etc.
    
    return conn



def dbeaver_commitmany(conexion, query, df):
    
    """
    Ejecuta múltiples consultas SQL en una conexión de base de datos y confirma los cambios.

    Parameters:
        - conexion (psycopg2.connection): Conexión a la base de datos PostgreSQL.
        - query (str): La consulta SQL a ejecutar con `executemany`.
        - df (str): Nombre del archivo CSV (sin extensión) que contiene los datos a insertar en la consulta SQL.

    Notes:
        Lee los datos de un archivo CSV en un DataFrame de pandas, los convierte a tuplas y ejecuta la consulta SQL
        para cada registro en `df`. Realiza el commit de los cambios automáticamente.

    Returns:
        str: Mensaje de confirmación después de ejecutar las consultas y realizar el commit.
    """
    
    df = pd.read_csv("../datos/dataframes/" + df + ".csv", index_col=0)
    values = [tuple(fila) for fila in df.values]
    cursor = conexion.cursor()
    cursor.executemany(query, values)

