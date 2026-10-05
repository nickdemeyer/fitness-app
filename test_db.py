import psycopg2
import os
from dotenv import load_dotenv

#load into memory .env file
load_dotenv()

#connect to db
con = psycopg2.connect(
            host = os.getenv("DB_HOST"),
            database = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            port = os.getenv("DB_PORT")
)

#cursor to communicate with database
cur = con.cursor()

cur.execute("insert into workouts (id, date, exercise, sets, reps, weight) values (%s, %s, %s, %s, %s, %s)", (3, "05-10-2026", "Squat", 4, 10, 75))

#execute query
cur.execute("select id, date, exercise, sets, reps, weight from workouts")

rows = cur.fetchall()

for r in rows:
    print(f"id: {r[0]} date: {r[1]} exercise: {r[2]} sets: {r[3]} reps: {r[4]} weight: {r[5]}")

#commit the transaction (insert)
con.commit()

#close the cursor dont leak things
cur.close()

#close the connection
con.close()