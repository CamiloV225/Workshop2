import pandas as pd
import mysql.connector
import json

csv_file = "/home/camilo/airflow_test/the_grammy_awards.csv"
with open('db_config.json') as f:
    dbfile = json.load(f)

db_config = {
    "host": "localhost",
    "user": dbfile["user"],
    "password": dbfile["password"],
    "database": dbfile["database"],
}

try:
    df = pd.read_csv(csv_file)

    # Replace NaN values with empty strings
    df = df.fillna('')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    table_name = "grammyawards"

    for index, row in df.iterrows():
        query = f"INSERT INTO {table_name} (year, title, published_at, updated_at, category, nominee, artist, winner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (row["year"], row["title"], row["published_at"], row["updated_at"], row["category"], row["nominee"], row["artist"], row["winner"]))

    conn.commit()
    conn.close()

    print("Data loaded successfully.")

except Exception as e:
    print("Error:", str(e))
