from flask import Flask, jsonify, request
from workouttracker_db import WorkoutTracker
from mealtracker_db import MealTracker

#making the webserver flask app in a variable
app = Flask(__name__) 

#making route
@app.route('/') #this is decorator/ / surfing to this function should start
def home():
    return "Hello World" #sends text back to browser, visitor sees this on his screen

#route2
@app.route('/hello')
def hello():
    return "GOOD DAY, how are you?"

#route3
@app.route('/test-workout')
def test_workout():
    workout = {"exercise": "pullup",
               "sets": 4,
               "reps": 10,
               "weight": 50}
    return jsonify(workout)

#view workouts route
@app.route('/api/workouts', methods=['GET', 'POST'])
def api_workouts():
    tracker = WorkoutTracker()
    if request.method == 'GET':
        workouts = tracker.web_view_workouts()
        tracker.close_connection()
        return jsonify(workouts)
    
    elif request.method == 'POST':
        data = request.get_json() #vang json data op
        
        #controleren of de velden bestaan
        verplichte_velden = ["date", "exercise", "sets", "reps", "weight"]
        for veld in verplichte_velden:
            if veld not in data:
                return jsonify({"error": f"Missing required field: {veld}"}), 400

        #checking numbers being positive
        if type(data["sets"]) is not int or data["sets"] <= 0:
            return jsonify("Error, try again"), 400
        if type(data["reps"]) is not int or data["reps"] <= 0:
            return jsonify("Error, try again"), 400
        if data["weight"] < 0:
            return jsonify("Cannot be negative"), 400

        tracker.add_workout(data["date"], data["exercise"], data["sets"], data["reps"], data["weight"])
        tracker.close_connection()
        return jsonify("Workout Added!"), 201


#view meals route
@app.route('/api/meals')
def api_meals():
    meal_tracker = MealTracker()
    meals = meal_tracker.web_view_meals()
    meal_tracker.close_connection()
    return jsonify(meals)




#making sure the app can start
if __name__ == "__main__":
    app.run(debug=True) #debug=True makes that server restarts automatic when something changes in code
