import json
from datetime import datetime

class MealTracker:
    def __init__(self):
        try:
            with open("meals.json", "r") as bestand:
                self.meals = json.load(bestand)
        except FileNotFoundError:
            self.meals = []

    def add_meal(self, date, name, calories, protein, carbs, fats):
        self.meal = {"date": date,
                     "name": name,
                     "calories": calories,
                     "protein": protein,
                     "carbs": carbs,
                     "fats": fats}

        self.meals.append(self.meal)
        with open("meals.json", "w") as bestand:
            json.dump(self.meals, bestand)
        print("Meal Added.")

    def view_meal(self):
        for i in self.meals:
            print(" ===================================")
            print(f"== {i["date"]} MEAL: {i["name"]} ==")
            print(f"{i["calories"]} KCAL")
            print(f"{i["protein"]} g protein")
            print(f"{i["carbs"]} g carbs")
            print(f"{i["fats"]} g fats")
            print()