import pandas as pd
import logging
import mysql.connector
import json

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
    query = cursor.execute("""SELECT * FROM grammyawards""")
    results = cursor.fetchall()
    print('BASE DE DATOS')

    for row in results:
        array.append(row)
    dfa = pd.DataFrame(array)
    
    dfa.columns = ["year", "title", "published_at", "updated_at", "category", "nominee", "artist", "workers", "img", "winner"]
    print(dfa)
    cursor.close()
    return dfa

def transform_db(dfa):
    grammy = dfa
    grammy.drop(columns=['year', 'title', 'published_at', 'updated_at', 'workers', 'img'])
    newcol = {'winner': 'nominated'}
    grammy.rename(columns=newcol, inplace=True)
    print(f"GRAMMY")
    print(grammy)

#################### CSV ###########################3
def read_csv():
    df = pd.read_csv('/home/camilo/airflow_test/spotify_dataset.csv', sep=',', index_col=0)
    print('CSV')
    print(df)
    return df

def transform_csv(df):
    spotify = df
    spotify['duracion'] = (spotify['duration_ms'] / 60000).round(2)

    rangos1 = [0, 0.3, 0.6, 1.0]
    tipos_bailabilidad = ['Poca bailabilidad', 'Bailabilidad Moderada', 'Bailabilidad Alta']
    spotify['cat_danceability'] = pd.cut(spotify['danceability'], bins=rangos1, labels=tipos_bailabilidad, right=False)
    
    rangos2 = [0, 30, 60, 100]
    tipos_popularidad = ['Poca Popularidad', 'Media Popularidad', 'Mucha Popularidad']
    spotify['popularity'] = pd.cut(spotify['popularity'], bins=rangos2, labels=tipos_popularidad, right=False)

    valor_minimo = df["loudness"].min()
    valor_maximo = df["loudness"].max()    
    columnadecibeles = spotify['loudness']
    columna_decibeles_normalizada = (columnadecibeles - valor_minimo) / (valor_maximo - valor_minimo)
    spotify['loudness'] = columna_decibeles_normalizada
    tipos_ruido = ['Canciones Ruido Bajo', 'Canciones con Ruido Moderado', 'Canciones Muy Ruidozas']
    spotify['loudness'] = pd.cut(spotify['loudness'], bins=rangos1, labels=tipos_ruido, right=False)

    tipos_energia = ['Canciones Tranquilas', 'Canciones con Energía Moderada', 'Canciones Muy Enérgicas']
    spotify['energy'] = pd.cut(spotify['energy'], bins=rangos1, labels=tipos_energia, right=False)

    newspotify = spotify.drop(['track_id', 'tempo', 'valence', 'liveness', 'instrumentalness', 'time_signature', 'speechiness', 'duration_ms', 'mode', 'key'], axis=1)

    newspotify.to_csv("result.csv")

if __name__ == "__main__":
    dfa = read_db()
    df = read_csv()
    transform_db(dfa)
    transform_csv(df)
