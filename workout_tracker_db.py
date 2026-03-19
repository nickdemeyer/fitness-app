import os
import psycopg2
from dotenv import load_dotenv
class WorkoutTracker:
    def __init__(self):
        load_dotenv()  #laad dotenv bestand met gegevens
        db_name = os.getenv('database')  
        db_user = os.getenv('user')      #env variables ophalen
        db_pass = os.getenv('password')
        db_host = os.getenv('host')
        db_port = os.getenv('port')

        #CONNECTIE MAKEN
        self.connectie = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
        #cursor object nodig
        self.curr = self.connectie.cursor()

    
    def add_workout(self):
        #input nodig
        date = input("Date: ")
        exercise = input("Exercise: ")
        sets = int(input("Sets: "))
        reps = int(input("Reps: "))
        weight = float(input("Weight: "))
        #deze input moet naar object curr (insert naar database)
        insert_query = """INSERT INTO workouts (date, exercise, sets, reps, weight) VALUES (%s, %s, %s, %s, %s);"""
        data = [date, exercise, sets, reps, weight]
        self.curr.execute(insert_query, data)
        self.connectie.commit()
        print("Workout Added")

    def view_workouts(self):
        #select variable maken met alle kolommen - zet de zoekopdracht in een tijdelijke wachtrij
        sql = """SELECT id, date, exercise, sets, reps, weight from workouts;"""
        self.curr.execute(sql)
        #fetchall om nu alles op tehalen voor alle workouts te kunnen zien in python 
        trainingen = self.curr.fetchall()
        for t in trainingen:
            print(f"{t[0]}. {t[1]}: {t[2]} - {t[3]} sets - {t[4]} reps - {t[5]} kg")
    
    def update_workout(self)