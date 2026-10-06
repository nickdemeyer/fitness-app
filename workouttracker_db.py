import psycopg2
import os
from dotenv import load_dotenv

#load into the memory
load_dotenv()

class WorkoutTracker:
    def __init__(self):
        #db connectie maken
        self.con = psycopg2.connect(
                    host = os.getenv("DB_HOST"),
                    database = os.getenv("DB_NAME"),
                    user = os.getenv("DB_USER"),
                    password = os.getenv("DB_PASSWORD"),
                    port = os.getenv("DB_PORT")
        )
        #cursor to communicate with the database
        self.cur = self.con.cursor()
        return

    def add_workout(self, date, exercise, sets, reps, weight):
        self.cur.execute("insert into workouts (date, exercise, sets, reps, weight) values (%s,%s,%s,%s,%s)", (date, exercise, sets, reps, weight))
        self.con.commit() 

    def view_workouts(self):
        self.cur.execute("select id, date, exercise, sets, reps, weight from workouts")
        self.rows = self.cur.fetchall()

        for r in self.rows:
            print("------------------")
            print(f"{r[1]}:")
            print(f"{r[2]}")
            print(f"{r[3]} sets")
            print(f"{r[4]} reps")
            print(f"{r[5]} kg")
            print("------------------")

    def close_connection(self):
        self.cur.close()
        self.con.close()