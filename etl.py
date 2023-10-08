import pandas as pd
import logging
import psycopg2
import json

def connect_postgres():
    with open('db_config.json') as f:
        dbfile = json.load(f)
    connection = psycopg2.connect(
        database=dbfile["database"],
        user=dbfile["user"],
        password=dbfile["password"],
        host="localhost",
        port=5432
    )
    print("Database connection ok")
    return connection
    

def read_db():
    array = []
    connection = connect_postgres()
    cursor = connection.cursor()
    query = cursor.execute("""SELECT * FROM grammyawards""")
    connection.commit()
    results = cursor.fetchall()
    print('BASE DE DATOS')

    for row in results:
        array.append(row)
    dfa = pd.DataFrame(array)
    dfa.columns = ["year","title","published_at","updated_at","category","nominee","artist","workers","img","winner"]
    print(dfa)
    cursor.close()
    return dfa


def read_csv():
    df = pd.read_csv('spotify_dataset.csv', sep=',',index_col=0)
    print('CVS')
    print(df)
    return df

def transform_db(dfa):
    print("TRANSFORMACION DB")
    print(dfa)

def transform_csv(df):
############DROPS###########
    newdf = df.drop(["track_id","tempo","valence","liveness","instrumentalness","time_signature","danceability","speechiness"], axis=1)
    print("TRANSFORMACION CSV")
    print(newdf)

if __name__ == "__main__":
    dfa = read_db()
    df = read_csv()
    transform_db(dfa)
    transform_csv(df)