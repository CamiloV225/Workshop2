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
################Database#################
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
    dfa.to_csv("db.csv")
    print(dfa)
    cursor.close()


def read_csv():
#################CSV#####################
    df = pd.read_csv('spotify_dataset.csv', sep=',',index_col=0)
    df.to_csv("filecsv.csv")
    print('CVS')
    print(df)

def transform_db():
    print()

def transform_csv():
    print()

if __name__ == "__main__":
    read_csv()
    read_db()