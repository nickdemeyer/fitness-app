from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json()
    return jsonify({"you_sent": data["name"]}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5001)