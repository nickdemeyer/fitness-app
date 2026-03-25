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
    
    def update_workout(self):
        self.view_workouts()
        workout_id = input("Number of workout you want to change: ")
        change = input("What do you want to change? date/exercise/sets/reps/weight: ")
        if change == "date":
            new_date = input("New Date: ")
            update_query = """UPDATE workouts SET date = %s WHERE id = %s"""
            data = [new_date, workout_id]
            self.curr.execute(update_query, data)
            self.connectie.commit()
            print("Updated")
        elif change == "exercise":
            new_exercise = input("New exercise: ")
            update_query = """UPDATE workouts SET exercise = %s WHERE id = %s"""
            data = [new_exercise, workout_id]
            self.curr.execute(update_query, data)
            self.connectie.commit()
            print("Updated")
        elif change == "sets":
            new_sets = int(input("New sets: "))
            update_query = """UPDATE workouts SET sets = %s WHERE id = %s"""
            data = [new_sets, workout_id]
            self.curr.execute(update_query, data)
            self.connectie.commit()
            print("Updated")
        elif change == "reps":
            new_reps = int(input("New reps: "))
            update_query = """UPDATE workouts SET reps = %s WHERE id = %s"""
            data = [new_reps, workout_id]
            self.curr.execute(update_query, data)
            self.connectie.commit()
            print("Updated")
        elif change == "weight":
            new_weight = float(input("new weight: "))
            update_query = """UPDATE workouts SET weight = %s WHERE id = %s"""
            data = [new_weight, workout_id]
            self.curr.execute(update_query, data)
            self.connectie.commit()
            print("Updated")

    def delete_workout(self):
        self.view_workouts()
        workout_id = input("Number of workout you want to delete: ")
        delete_query = """DELETE FROM workouts WHERE id = %s"""
        data = [workout_id]
        self.curr.execute(delete_query, data)
        self.connectie.commit()
        print("Workout Deleted.")