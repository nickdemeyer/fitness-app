from workouttracker_db import WorkoutTracker
from mealtracker import MealTracker
from datetime import datetime

tracker = WorkoutTracker()
meal_tracker = MealTracker()

def get_valid_number(prompt, number_type):
    while True:
            try:
                number = number_type(input(prompt)) 
                if number <= 0:
                    print("Number must be greater then 0.")
                else:
                    return number
            except ValueError:
                print("Invalid Input. Try again.")

def get_valid_text(prompt):
    while True:
        text = input(prompt)
        if text == "":
            print("Invalid Input.")
        else:
            return text

def get_valid_date(prompt):
    while True:
        date = input(prompt)
        try:
            datetime.strptime(date, "%d-%m-%Y")
            return date
        except ValueError:
            print("Invalid Input. Try again.")

def get_valid_field(prompt):
    while True:
        text = input(prompt)
        if text == "date" or text == "exercise" or text == "sets" or text == "reps" or text == "weight":
            return text
        else:
            print("try again")
            continue
while True:
    print("==== MENU ====")
    print("1. WORKOUTS")
    print("2. MEALS")
    print("3. EXIT")

    keuze = input("Select to continue: ")

    if keuze == "1":
        while True:
                print("===== MENU =====")
                print("1. Add Workout")
                print("2. View Workout")
                print("3. Update Workout")
                print("4. Delete Workout")
                print("5. Exit")

                choice = input("Option: ")

                if choice == "1":
                        date = get_valid_date("Date (DD-MM-YYYY): ")
                        exercise = get_valid_text("Exercise: ")
                        sets = get_valid_number("Sets: ", int)
                        reps = get_valid_number("Reps:", int)
                        weight = get_valid_number("Weight: ", float)

                        tracker.add_workout(date, exercise, sets, reps, weight)

                elif choice == "2":
                    tracker.view_workouts()

                elif choice == "3":
                    tracker.view_workouts()
                    id = get_valid_number("select workout number to change: ", int)
                    field = get_valid_field("choose option to continue date/exercise/sets/reps/weight: ")
                    if field == "date":
                        new_value = get_valid_date("New date: ")
                    elif field == "exercise":
                        new_value = get_valid_text("New exercise: ")
                    elif field == "sets":
                        new_value = get_valid_number("New sets: ", int)
                    elif field == "reps":
                        new_value = get_valid_number("New reps: ", int)
                    elif field == "weight":
                        new_value = get_valid_number("New weight: ", float)
                    tracker.update_workout(id, field, new_value)

                elif choice == "4":
                    tracker.view_workouts()
                    id = get_valid_number("Select workout number to delete: ", int)
                    tracker.delete_workout(id)

                elif choice == "5":
                    tracker.close_connection()
                    print("EXIT")
                    break 

    elif keuze == "2":
        while True:
            print("==== MENU ====")
            print("1. Add Meal")
            print("2. View Meal")
            print("3. Exit")

            choice = input("Choose option: ")

            if choice == "1":
                date = get_valid_date("Date (DD-MM-YYYY): ")
                name = get_valid_text("Meal: ")
                calories = get_valid_number("Calories: ", int)
                protein = get_valid_number("Protein: ", int)
                carbs = get_valid_number("Carbs: ", int)
                fats = get_valid_number("Fats: ", int)
                meal_tracker.add_meal(date, name, calories, protein, carbs, fats)

            elif choice == "2":
                meal_tracker.view_meal()

            elif choice == "3":
                print("EXIT")
                break

    elif keuze == "3":
        print("Closing Application....")
        break