import pandas as pd
import logging
import mysql.connector
import json
import numpy as np

def connect_mysql():
    with open('/home/camilo/airflow_test/db_config.json') as f:
        dbfile = json.load(f)
    
    connection = mysql.connector.connect(
        host=dbfile["host"],
        user=dbfile["user"],
        password=dbfile["password"],
        database=dbfile["database"]
    )
    
    print("Database connection ok")
    return connection
    
###################BASE DE DATOS##################
def read_db():
    array = []
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM grammyawards""")
    results = cursor.fetchall()
    print('BASE DE DATOS')

    for row in results:
        array.append(row)
    dfa = pd.DataFrame(array)
    dfa.columns = ["year","title","published_at","updated_at","category","nominee","artist","workers","img","winner"]
    print(dfa)
    cursor.close()
    return dfa.to_json(orient='records')

def transform_db(**kwargs):
    print("TRANSFORMACION DB")
    ti = kwargs["ti"]
    str_data = ti.xcom_pull(task_ids="read_db")
    json_data = json.loads(str_data)
    grammy = pd.json_normalize(data=json_data)

    newgramm=grammy.drop(['year','published_at','updated_at','workers','img'], axis = 1)
    newgramm.rename(columns={'winner':'nominated'}, inplace=True)
    newgramm['nominated'] = newgramm['nominated'].astype(bool)
    logging.info("TRANSFORMACION DE LA DB REALIZADA")
    print(newgramm)
    newgramm.to_csv('revision.csv')
    return newgramm.to_json(orient='records')


#################### CSV ###########################3
def read_csv():
    df = pd.read_csv('/home/camilo/airflow_test/spotify_dataset.csv', sep=',',index_col=0)
    print('CVS')
    print(df)
    return df.to_json(orient='records')

def transform_csv(**kwargs):
    ti = kwargs['ti']
    str_data = ti.xcom_pull(task_ids="read_csv")
    json_data = json.loads(str_data)
    spotify = pd.json_normalize(data=json_data)
    spotify = spotify.fillna('')

############### Cambios a Bailabilidad ##################
    rangos1 = [0, 0.3, 0.6, 1.0]
    tipos_bailabilidad = ['Poca bailabilidad', 'Bailabilidad Moderada', 'Bailabilidad Alta']
    spotify['cat_danceability'] = pd.cut(spotify['danceability'], bins=rangos1, labels=tipos_bailabilidad, right=False)
    
############## Cambios a Popularidad ###################3
    rangos2 = [0, 30, 60, 100]
    tipos_popularidad = ['Poca Popularidad', 'Media Popularidad', 'Mucha Popularidad']
    spotify['popularity'] = pd.cut(spotify['popularity'], bins=rangos2, labels=tipos_popularidad, right=False)

############# Cambios a Ruido ######################
    valor_minimo = spotify["loudness"].min()
    valor_maximo = spotify["loudness"].max()    
    columnadecibeles = spotify['loudness']
    columna_decibeles_normalizada = (columnadecibeles - valor_minimo) / (valor_maximo - valor_minimo)
    spotify['loudness'] = columna_decibeles_normalizada
    spotify['loudness'] = pd.cut(spotify['loudness'], bins=rangos1, labels=['Canciones Ruido Bajo', 'Canciones con Ruido Moderado', 'Canciones Muy Ruidozas'], right=False)

################ Cambios a Energia ########################
    tipos_energia = ['Canciones Tranquilas', 'Canciones con Energía Moderada', 'Canciones Muy Enérgicas']
    spotify['energy'] = pd.cut(spotify['energy'], bins=rangos1, labels=tipos_energia, right=False)

    newspotify =spotify.drop(['track_id','tempo','valence','liveness','instrumentalness','time_signature','speechiness', 'duration_ms','mode','key','acousticness','artists'], axis=1)
    
    logging.info("TRANSFORMACION DEL CSV REALIZADO")
    print(spotify)
    return newspotify.to_json(orient='records')


def merge(**kwargs):
    ti = kwargs["ti"]
    logging.info("Iniciando el MERGEEEE")
    str_data = ti.xcom_pull(task_ids="transform_csv")
    json_data = json.loads(str_data)
    spotify = pd.json_normalize(data=json_data)

    str_data = ti.xcom_pull(task_ids="transform_db")
    json_data = json.loads(str_data)
    grammy = pd.json_normalize(data=json_data)
    df = spotify.merge(grammy, how='left', left_on='track_name', right_on='nominee')
    df['nominated'].fillna(False, inplace=True)
    df['explicit'].fillna(False, inplace=True)
    logging.info("MERCHEADO aishhhh")
    return df.to_json(orient='records')


def load(**kwargs):
    logging.info("Iniciando la carga del nuevo csv")
    connection = connect_mysql()
    cursor = connection.cursor()
    ti = kwargs["ti"]
    str_data = ti.xcom_pull(task_ids="merge")
    json_data = json.loads(str_data)
    df = pd.json_normalize(data=json_data)

    df = df.fillna('')
   
    logging.info("Creando tabla")
    create_table = f"""CREATE TABLE IF NOT EXISTS grammyspotify (
        artist VARCHAR(255),
        nominee VARCHAR(255),
        popularity VARCHAR(255),
        danceability FLOAT,
        energy VARCHAR(255),
        loudness VARCHAR(255),
        track_genre VARCHAR(255),
        cat_danceability VARCHAR(255),
        title VARCHAR(255),
        category VARCHAR(255),
        explicit BOOLEAN,
        nominated BOOLEAN
        )
        """
    cursor.execute(create_table)
    logging.info("Tabla creada")
    for index, row in df.iterrows():
            query = f"INSERT INTO grammyspotify (artist, nominee, popularity, danceability,explicit, energy, loudness, track_genre, cat_danceability,title,category,nominated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)"
            cursor.execute(query, (row["artist"],row["nominee"],row["popularity"],row["danceability"],row['explicit'],row["energy"],row["loudness"],row["track_genre"],row["cat_danceability"],row["title"],row["category"],row["nominated"]))
            connection.commit()
    logging.info("Datos Insertados")
    return df.to_json(orient='records') 

def store(**kwargs):
    logging.info("Iniciando Store")
    ti = kwargs["ti"]
    str_data = ti.xcom_pull(task_ids="merge")
    json_data = json.loads(str_data)
    df = pd.json_normalize(data=json_data)

    df.to_csv('/home/camilo/airflow_test/Grammy-Spotifty.csv')

