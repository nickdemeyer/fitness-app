from flask import Flask, jsonify

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

#making sure the app can start
if __name__ == "__main__":
    app.run(debug=True) #debug=True makes that server restarts automatic when something changes in code
