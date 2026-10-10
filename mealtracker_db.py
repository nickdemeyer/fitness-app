import os
import psycopg2
from dotenv import load_dotenv

load_dotenv() #load in the memory

class MealTracker:
    def __init__(self):
        #connectie maken
        self.con = psycopg2.connect(
            host = os.getenv("DB_HOST"),
            database = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            port = os.getenv("DB_PORT")
        )

        #cursor maken -> nodig om te kunnen communiceren met database
        self.cur = self.con.cursor()
        return

    def add_meal(self, date, name, calories, protein, carbs, fats):
        self.cur.execute("insert into meals (date, name, calories, protein, carbs, fats) values (%s, %s, %s, %s, %s, %s)", (date, name, calories, protein, carbs, fats))
        self.con.commit()

    def view_meals(self):
        self.cur.execute("select * from meals")
        self.rows = self.cur.fetchall()

        for r in self.rows:
            print("--------------------")
            print(f"{r[0]}. {r[1]}:")
            print(f"KCAL: {r[3]}")
            print(f"protein: {r[4]}g")
            print(f"carbs: {r[5]}g")
            print(f"fats: {r[6]}g")
            print("--------------------")

    def close_connection(self):
        self.cur.close()
        self.con.close()
