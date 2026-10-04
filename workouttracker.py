from datetime import datetime
import json

class WorkoutTracker:
    def __init__(self):
        try:
            with open("workouts.json", "r") as bestand:
                self.workouts = json.load(bestand)
        except FileNotFoundError:
            self.workouts = []

    def add_workout(self, date, exercise, sets, reps, weight):
        workout = {"date": date, 
                        "exercise": exercise,
                         "sets": sets,
                          "reps": reps,
                           "weight": weight }

        self.workouts.append(workout)
        with open("workouts.json", "w") as bestand:
            json.dump(self.workouts, bestand)
            print("Workout Added.")

    def view_workout(self):
        for i in self.workouts:
            print(f"=== DATE: {i["date"]} ===")
            print(f"exercise: {i["exercise"]}: {i["sets"]} sets x {i["reps"]} reps with {i["weight"]}kg")