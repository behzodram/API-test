from flask import Flask, request, jsonify, render_template
from datetime import datetime
from queue import Queue
import json

app = Flask(__name__)

# Server-Sent Events uchun navbat
events = Queue()

# API loglari
logs = []


def add_log(method, endpoint, body):
    log = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "method": method,
        "endpoint": endpoint,
        "body": body,
        "ip": request.remote_addr
    }

    logs.insert(0, log)

    if len(logs) > 200:
        logs.pop()

    events.put(log)


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


@app.route("/stream")
def stream():

    from flask import Response

    def event_stream():

        while True:

            data = events.get()

            yield f"data:{json.dumps(data)}\n\n"

    return Response(
        event_stream(),
        mimetype="text/event-stream"
    )


if __name__ == "__main__":
    app.run(debug=True)