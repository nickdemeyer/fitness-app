from flask import Flask, jsonify, request
from workouttracker_db import WorkoutTracker
from mealtracker_db import MealTracker
from datetime import datetime

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

#view workouts route and adding a workout
@app.route('/api/workouts', methods=['GET', 'POST'])
def api_workouts():
    tracker = WorkoutTracker()
    if request.method == 'GET':
        workouts = tracker.web_view_workouts()
        tracker.close_connection()
        return jsonify(workouts)
    
    elif request.method == 'POST':
        data = request.get_json(silent=True) #vang json data op

        #bestaat de data en of json object dict is
        if data is None or type(data) is not dict:
            tracker.close_connection()
            return jsonify("No valid data"), 400
        
        #controleren of de velden bestaan
        verplichte_velden = ["date", "exercise", "sets", "reps", "weight"]
        for veld in verplichte_velden:
            if veld not in data:
                tracker.close_connection()
                return jsonify({"error": f"Missing required field: {veld}"}), 400

        #validation points
        if type(data["date"]) is not str:
            tracker.close_connection()
            return jsonify("Error, try again. Fill in DD-MM-YYYY"), 400
        try:
            datetime.strptime(data["date"], "%d-%m-%Y")
        except ValueError:
            tracker.close_connection()
            return jsonify("Error, try again. Fill in DD-MM-YYYY"), 400

        if type(data["exercise"]) is not str or data["exercise"] == "":
            tracker.close_connection()
            return jsonify("Error, try again"), 400
        
        if type(data["sets"]) is not int or data["sets"] <= 0:
            tracker.close_connection()
            return jsonify("Error, try again"), 400
        
        if type(data["reps"]) is not int or data["reps"] <= 0:
            tracker.close_connection()
            return jsonify("Error, try again"), 400

        if type(data["weight"]) not in [int, float] or data["weight"] < 0:
            tracker.close_connection()
            return jsonify("Error, try again"), 400

        tracker.add_workout(data["date"], data["exercise"], data["sets"], data["reps"], data["weight"])
        tracker.close_connection()
        return jsonify("Workout Added!"), 201

#view one workout route, delete and update
@app.route("/api/workouts/<int:id>", methods=['GET'])
def api_one_workout(id):
    tracker = WorkoutTracker()
    workout = tracker.web_view_one_workout(id)
    tracker.close_connection()
    if workout is None:
        return jsonify("Error! Workout not found."), 404
    else:
        return jsonify(workout), 200
    
@app.route("/api/workouts/<int:id>", methods=['DELETE'])
def api_delete_workout(id):
    tracker = WorkoutTracker()
    del_workout = tracker.web_delete_workout(id)
    tracker.close_connection()
    if del_workout is False:
        return jsonify("Error! Workout does not exist."), 404
    else:
        return jsonify("Workout Deleted!"), 200

@app.route("/api/workouts/<int:id>", methods=['PUT'])
def api_update_workout(id):
    tracker = WorkoutTracker()

    #step 1: get json data
    data = request.get_json(silent=True)

    #step 2: controlling if json exist or is a dict
    if data is None or type(data) is not dict:
        tracker.close_connection()
        return jsonify("No valid data"), 400

    #step 3: controlling if field exists
    whitelist = ["date", "exercise", "sets", "reps", "weight"]

    field = data.get("field")
    new_value = data.get("new_value")

    if field not in whitelist:
        tracker.close_connection()
        return jsonify("Error, bad request!"), 400

    #step 4: controlling new_value validation as the right type for that field
    if field == "date":
        if type(new_value) is not str:
            tracker.close_connection()
            return jsonify("Error, try again. Fill in DD-MM-YYYY"), 400
        try:
            datetime.strptime(new_value, "%d-%m-%Y")
        except ValueError:
            tracker.close_connection()
            return jsonify("Error, try again. Fill in DD-MM-YYYY"), 400

    elif field == "exercise":
        if type(new_value) is not str or new_value == "":
            tracker.close_connection()
            return jsonify("Error, try again"), 400
        
    elif field == "sets":
        if type(new_value) is not int or new_value <= 0:
            tracker.close_connection()
            return jsonify("Error, try again"), 400

    elif field == "reps":
        if type(new_value) is not int or new_value <= 0:
            tracker.close_connection()
            return jsonify("Error, try again"), 400

    elif field == "weight":
        if type(new_value) not in [int, float] or new_value < 0:
            tracker.close_connection()
            return jsonify("Error, try again"), 400

    #step 5: return confirm message
    upd_workout = tracker.web_update_workout(id, field, new_value)
    tracker.close_connection()
    if upd_workout is False:
        return jsonify("Workout does not exist!"), 404
    else:
        return jsonify("workout updated!"), 200
    
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
