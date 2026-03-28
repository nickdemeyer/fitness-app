import os
import psycopg2
from dotenv import load_dotenv
class MealTracker:
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

    
    def add_meal(self):
        #input nodig
        date = input("Date: ")
        foodname = input("Name: ")
        amount = input("Amount Food: ")
        calories = int(input("Calories: "))
        protein = int(input("Weight: "))
        carbs = int(input("Carbs: "))
        fats = int(input("Fats: "))
        #deze input moet naar object curr (insert naar database)
        insert_query = """INSERT INTO meals (date, foodname, amount, calories, protein, carbs, fats) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        data = [date, foodname, amount, calories, protein, carbs, fats]
        self.curr.execute(insert_query, data)
        self.connectie.commit()
        print("Meal Added!")

    def view_meals(self):
        #select variable maken met alle kolommen - zet de zoekopdracht in een tijdelijke wachtrij
        sql = """SELECT id, date, foodname, amount, calories, protein, carbs, fats from meals;"""
        self.curr.execute(sql)
        #fetchall om nu alles op tehalen voor alle workouts te kunnen zien in python 
        maaltijd = self.curr.fetchall()
        for m in maaltijd:
            print(f"{m[0]}. {m[1]}: {m[2]} - {m[3]} - {m[4]}Kcal - {m[5]}g protein - {m[6]}g carb - {m[7]}g fat")
    
    def update_meal(self):
        self.view_meals()
        meal_id = input("Number of meal you want to change: ")
        change = input("What do you want to change? date/foodname/amount/calories/protein/carbs/fats: ")
        if change == "date":
            new_date = input("New Date: ")
            update_query = """UPDATE meals SET date = %s WHERE id = %s"""
            data = [new_date, meal_id]
            self.curr.execute(update_query, data)
            self.connectie.commit()
            print("Updated")
        elif change == "foodname":
            new_foodname = input("New Foodname: ")
            update_query = """UPDATE meals SET foodname = %s WHERE id = %s"""
            data = [new_foodname, meal_id]
            self.curr.execute(update_query, data)
            self.connectie.commit()
            print("Updated")
        elif change == "amount":
            new_amount = input("New Amount: ")
            update_query = """UPDATE meals SET amount = %s WHERE id = %s"""
            data = [new_amount, meal_id]
            self.curr.execute(update_query, data)
            self.connectie.commit()
            print("Updated")
        elif change == "calories":
            new_calories = int(input("New Calories: "))
            update_query = """UPDATE meals SET calories = %s WHERE id = %s"""
            data = [new_calories, meal_id]
            self.curr.execute(update_query, data)
            self.connectie.commit()
            print("Updated")
        elif change == "protein":
            new_protein = int(input("New Protein: "))
            update_query = """UPDATE meals SET protein = %s WHERE id = %s"""
            data = [new_protein, meal_id]
            self.curr.execute(update_query, data)
            self.connectie.commit()
            print("Updated")
        elif change == "carbs":
            new_carbs = int(input("New Carbs: "))
            update_query = """UPDATE meals SET carbs = %s WHERE id = %s"""
            data = [new_carbs, meal_id]
            self.curr.execute(update_query, data)
            self.connectie.commit()
            print("Updated")
        elif change == "fats":
            new_fats = int(input("New Fat: "))
            update_query = """UPDATE meals SET fats = %s WHERE id = %s"""
            data = [new_fats, meal_id]
            self.curr.execute(update_query, data)
            self.connectie.commit()
            print("Updated")

    def delete_meal(self):
        self.view_meals()
        meal_id = input("Number of meal you want to delete: ")
        delete_query = """DELETE FROM meals WHERE id = %s"""
        data = [meal_id]
        self.curr.execute(delete_query, data)
        self.connectie.commit()
        print("Workout Deleted.")