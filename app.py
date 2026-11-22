from flask import Flask, jsonify, request
from validators import check_date, check_whole_number, check_string_emptyfield, check_whole_non_negative_number, check_non_negative_number
from sqlalchemy import select
from database import SessionLocal
from models import Workout, Meal, Bodyweight

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
@app.route('/api/workouts', methods=['GET'])
def api_get_workouts():
    with SessionLocal() as session:
        stmt = select(Workout).order_by(Workout.id)
        workouts = session.scalars(stmt).all()
        result = [workout.to_dict() for workout in workouts]
    return jsonify(result)

@app.route('/api/workouts', methods=['POST'])
def api_add_workout():
        data = request.get_json(silent=True) #vang json data op

        #bestaat de data en of json object dict is
        if data is None or type(data) is not dict:
            return jsonify("No valid data"), 400
        
        #controleren of de velden bestaan
        verplichte_velden = ["date", "exercise", "sets", "reps", "weight"]
        for veld in verplichte_velden:
            if veld not in data:
                return jsonify({"error": f"Missing required field: {veld}"}), 400

        #validatie validators
        error = (check_date(data["date"]) or
                 check_string_emptyfield(data["exercise"]) or
                 check_whole_number(data["sets"]) or
                 check_whole_number(data["reps"]) or
                 check_non_negative_number(data["weight"])
        )

        if error:
            return jsonify(error), 400

        with SessionLocal() as session:
            new_workout = Workout(date=data["date"],
                                  exercise=data["exercise"],
                                  sets=data["sets"],
                                  reps=data["reps"],
                                  weight=data["weight"])
            session.add(new_workout)
            session.commit()
            return jsonify("Workout Added!"), 201


#view one workout route, delete and update
@app.route("/api/workouts/<int:id>", methods=['GET'])
def api_one_workout(id):
    with SessionLocal() as session:
        workout = session.get(Workout, id)
        if workout is None:
            return jsonify("Error! Workout not found."), 404
        else:
            return jsonify(workout.to_dict()), 200
    
@app.route("/api/workouts/<int:id>", methods=['DELETE'])
def api_delete_workout(id):
    with SessionLocal() as session:
        workout = session.get(Workout, id)
        if workout is None:
            return jsonify("Workout does not exist!"), 404

        session.delete(workout)
        session.commit()
        return jsonify("Workout Deleted!"), 200

@app.route("/api/workouts/<int:id>", methods=['PUT'])
def api_update_workout(id):

    #step 1: get json data
    data = request.get_json(silent=True)

    #step 2: controlling if json exist or is a dict
    if data is None or type(data) is not dict:
        return jsonify("No valid data"), 400

    #step 3: controlling if field exists
    whitelist = ["date", "exercise", "sets", "reps", "weight"]

    field = data.get("field")
    new_value = data.get("new_value")

    if field not in whitelist:
        return jsonify("Error, bad request!"), 400

    #step 4: controlling new_value validation as the right type for that field
    error = None
    if field == "date":
        error = check_date(new_value)

    elif field == "exercise":
        error = check_string_emptyfield(new_value)
        
    elif field == "sets":
        error = check_whole_number(new_value)

    elif field == "reps":
        error = check_whole_number(new_value)

    elif field == "weight":
        error = check_non_negative_number(new_value)

    if error:
        return jsonify(error), 400

    #zoek de workout en pass aan met setattr()
    with SessionLocal() as session:
        workout = session.get(Workout, id)
        if workout is None:
            return jsonify("Workout does not exist!"), 404

        setattr(workout, field, new_value)
        session.commit()
        return jsonify("Workout Updated!"), 200

    
#view meals
@app.route('/api/meals', methods=['GET'])
def api_meals():
    with SessionLocal() as session:
        stmt = select(Meal).order_by(Meal.id)
        meals = session.scalars(stmt).all()
        result = [meal.to_dict() for meal in meals]
        return jsonify(result)

#add meal
@app.route('/api/meals', methods=['POST'])
def api_add_meal():
    data = request.get_json(silent=True)

    #bestaat data en is json een dict?
    if data is None or type(data) is not dict:
        return jsonify("No valid data"), 400

    #do the fields exist?
    field = ["date", "name", "calories", "protein", "carbs", "fats"]
    for f in field:
        if f not in data:
            return jsonify(f"Error, missing required field: {f}"), 400

    #controlling right user input - validation input
    error = (check_date(data["date"]) or
                 check_string_emptyfield(data["name"]) or
                 check_whole_number(data["calories"]) or
                 check_whole_non_negative_number(data["protein"]) or 
                 check_whole_non_negative_number(data["carbs"]) or
                 check_whole_non_negative_number(data["fats"]))

    if error:
        return jsonify(error), 400

    with SessionLocal() as session:
        new_meal = Meal(date=data["date"],
                        name=data["name"],
                        calories=data["calories"],
                        protein=data["protein"],
                        carbs=data["carbs"],
                        fats=data["fats"])
        session.add(new_meal)
        session.commit()
        return jsonify("Meal Added!"), 201
        
        

#Route view one meal
@app.route("/api/meals/<int:id>", methods=['GET'])
def api_one_meal(id):
    with SessionLocal() as session:
        meal = session.get(Meal, id)
        if meal is None:
            return jsonify("Meal does not exist!"), 404
        else:
            return jsonify(meal.to_dict()), 200

#Route delete meal
@app.route("/api/meals/<int:id>", methods=['DELETE'])
def api_delete_meal(id):
    with SessionLocal() as session:
        meal = session.get(Meal, id)
        if meal is None:
            return jsonify("Meal does not exist!"), 404

        session.delete(meal)
        session.commit()
        return jsonify("Meal Deleted!"), 200

#Route update meal
@app.route("/api/meals/<int:id>", methods=['PUT'])
def api_update_meal(id):

    #get json data step 1
    data = request.get_json(silent=True)

    #control of json exist or dict step 2
    if data is None or type(data) is not dict:
        return jsonify("No valid data"), 400

    #make whitelist + get field and new_value from the data
    whitelist = ["date", "name", "calories", "protein", "carbs", "fats"]
    field = data.get("field")
    new_value = data.get("new_value")

    #control if field in whitelist
    if field not in whitelist:
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
        error = check_whole_non_negative_number(new_value)
    elif field == "carbs":
        error = check_whole_non_negative_number(new_value)
    elif field == "fats":
        error = check_whole_non_negative_number(new_value)

    if error:
        return jsonify(error), 400

    #zoek de maaltijd en pass aan met setattr()
    with SessionLocal() as session:
        meal = session.get(Meal, id)
        if meal is None:
            return jsonify("Meal does not exist!"), 404

        setattr(meal, field, new_value)
        session.commit()
        return jsonify("Meal Updated!"), 200

@app.route('/api/body-weight', methods=['GET'])
def api_view_bodyweights():
    with SessionLocal() as session:
        stmt = select(Bodyweight).order_by(Bodyweight.the_date)
        bodyweights = session.scalars(stmt).all()
        result = [b.to_dict() for b in bodyweights]
        return jsonify(result)
                           


#making sure the app can start
if __name__ == "__main__":
    app.run(debug=True) #debug=True makes that server restarts automatic when something changes in code
