from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

logs = []


def add_log(method, endpoint, body):

    log = {
        "id": datetime.now().timestamp(),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "method": method,
        "endpoint": endpoint,
        "body": body,
        "ip": request.remote_addr
    }

    logs.insert(0, log)

    if len(logs) > 200:
        logs.pop()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logs")
def get_logs():
    return jsonify(logs)


@app.route("/api/hello", methods=["GET"])
def hello():

    add_log(
        "GET",
        "/api/hello",
        {}
    )

    return jsonify({
        "success": True,
        "message": "Hello World"
    })


@app.route("/api/message", methods=["POST"])
def message():

    data = request.get_json(silent=True)

    if data is None:
        data = request.form.to_dict()

    add_log(
        "POST",
        "/api/message",
        data
    )

    return jsonify({
        "success": True,
        "received": data
    })


@app.route("/api/user/<username>", methods=["GET"])
def user(username):

    add_log(
        "GET",
        f"/api/user/{username}",
        {}
    )

    return jsonify({
        "user": username
    })


if __name__ == "__main__":
    app.run(debug=True)