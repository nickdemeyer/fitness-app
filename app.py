from flask import Flask, jsonify, request
from workouttracker_db import WorkoutTracker
from mealtracker_db import MealTracker
from datetime import datetime
from validators import check_date, check_non_negative_number, check_whole_number, check_string_emptyfield

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
    
#view meals route + add meal (post)
@app.route('/api/meals', methods=['GET', 'POST'])
def api_meals():
    meal_tracker = MealTracker()
    if request.method == 'GET':
        meals = meal_tracker.web_view_meals()
        meal_tracker.close_connection()
        return jsonify(meals)

    elif request.method == 'POST':
        #getting data
        data = request.get_json(silent=True)

        #bestaat data en is json een dict?
        if data is None or type(data) is not dict:
            meal_tracker.close_connection()
            return jsonify("No valid data"), 400

        #do the fields exist?
        field = ["date", "name", "calories", "protein", "carbs", "fats"]
        for f in field:
            if f not in data:
                meal_tracker.close_connection()
                return jsonify(f"Error, missing required field: {f}"), 400

        #controlling right user input - validation input
        error = (check_date(data["date"]) or
                 check_string_emptyfield(data["name"]) or
                 check_whole_number(data["calories"]) or
                 check_non_negative_number(data["protein"]) or 
                 check_non_negative_number(data["carbs"]) or
                 check_non_negative_number(data["fats"]))

        if error:
            meal_tracker.close_connection()
            return(error), 400
        
        meal_tracker.add_meal(data["date"], data["name"], data["calories"], data["protein"], data["carbs"], data["fats"])
        meal_tracker.close_connection()
        return jsonify("Meal Added!"), 201

#Route view one meal
@app.route("/api/meals/<int:id>", methods=['GET'])
def api_one_meal(id):
    meal_tracker = MealTracker()
    meal = meal_tracker.web_view_one_meal(id)
    meal_tracker.close_connection()
    if meal is None:
        return jsonify("Error. Meal not found!"), 404
    else:
        return jsonify(meal), 200

#Route delete meal
@app.route("/api/meals/<int:id>", methods=['DELETE'])
def api_delete_meal(id):
    meal_tracker = MealTracker()
    del_meal = meal_tracker.web_delete_meal(id)
    meal_tracker.close_connection()
    if del_meal is False:
        return jsonify("Error. Meal does not exist!"), 404
    else:
        return jsonify("Meal Deleted!"), 200

#Route update meal
@app.route("/api/meals/<int:id>", methods=['PUT'])
def api_update_meal(id):
    meal_tracker = MealTracker()

    #get json data step 1
    data = request.get_json(silent=True)

    #control of json exist or dict step 2
    if data is None or type(data) is not dict:
        meal_tracker.close_connection()
        return jsonify("No valid data"), 400

    #make whitelist + get field and new_value from the data
    whitelist = ["date", "name", "calories", "protein", "carbs", "fats"]
    field = data.get("field")
    new_value = data.get("new_value")

    #control if field in whitelist
    if field not in whitelist:
        meal_tracker.close_connection()
        return jsonify("Error, bad request!"), 400

    #validation input new_value
    error = None    #empty box 

    if field == "date":
        error = check_date(new_value) 
    elif field == "name":
        error = check_string_emptyfield(new_value)
    elif field == "calories":
        error = check_whole_number(new_value)
    elif field == "protein":
        error = check_non_negative_number(new_value)
    elif field == "carbs":
        error = check_non_negative_number(new_value)
    elif field == "fats":
        error = check_non_negative_number(new_value)

    if error:
        meal_tracker.close_connection()
        return jsonify(error), 400

    #return confirm message
    upd_meal = meal_tracker.web_update_meal(id, field, new_value)
    meal_tracker.close_connection()
    if upd_meal is False:
        return jsonify("meal does not exist!"), 404
    return jsonify("Meal updated!"), 200



#making sure the app can start
if __name__ == "__main__":
    app.run(debug=True) #debug=True makes that server restarts automatic when something changes in code
