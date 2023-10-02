import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
import json

def connect_postgres():
    with open('C:/Users/camil/OneDrive/Documents/GitHub/Workshop2/db_config.json') as f:
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


def create_table():
    connection = connect_postgres()
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE grammyawards (
        year integer,
        title varchar,
        published_at timestamp,
        updated_at timestamp,
        category varchar,
        nominee varchar,
        artist varchar,
        workers varchar,
        img varchar,
        winner boolean     
    )""")

    connection.commit()
    cursor.close()
    connection.close()


def insert_to_table():
    connection = connect_postgres()
    cursor = connection.cursor()
    with open("the_grammy_awards.csv", "r", encoding="utf-8") as f: 
        next(f)
        cursor.copy_from(f, "grammyawards", sep=";")
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    connection = connect_postgres()
    create_table() 
    insert_to_table()

