from flask import Flask, request, jsonify, render_template
from datetime import datetime
from queue import Queue
import json

app = Flask(__name__)

events = Queue()
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

    if len(logs) > 300:
        logs.pop()

    events.put(log)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logs")
def get_logs():
    return jsonify(logs)


@app.route("/stream")
def stream():

    from flask import Response

    def event_stream():
        while True:
            data = events.get()
            yield f"data:{json.dumps(data)}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")


##########################################################
# TOOL 1
##########################################################

@app.route("/api/mijoz_kimligini_aniqlash", methods=["POST"])
def mijoz_kimligini_aniqlash():

    data = request.get_json(force=True)

    mijoz_ismi = data.get("mijoz_ismi", "space")
    mijoz_kasbi = data.get("mijoz_kasbi", "")

    add_log(
        "POST",
        "/api/mijoz_kimligini_aniqlash",
        {
            "mijoz_ismi": mijoz_ismi,
            "mijoz_kasbi": mijoz_kasbi
        }
    )

    return jsonify({
        "success": True,
        "message": "Ma'lumot qabul qilindi."
    })


##########################################################
# TOOL 2
##########################################################

@app.route("/api/haydovchi_malumot_saqlash", methods=["POST"])
def haydovchi_malumot_saqlash():

    data = request.get_json(force=True)

    mijoz_ismi = data.get("mijoz_ismi", "")
    mijoz_lokatsiyasi = data.get("mijoz_lokatsiyasi", "")
    mijoz_maqsad_yuki_lokatsiyasi = data.get(
        "mijoz_maqsad_yuki_lokatsiyasi",
        ""
    )

    add_log(
        "POST",
        "/api/haydovchi_malumot_saqlash",
        {
            "mijoz_ismi": mijoz_ismi,
            "mijoz_lokatsiyasi": mijoz_lokatsiyasi,
            "mijoz_maqsad_yuki_lokatsiyasi": mijoz_maqsad_yuki_lokatsiyasi
        }
    )

    return jsonify({
        "success": True,
        "message": "Haydovchi ma'lumoti saqlandi."
    })


if __name__ == "__main__":
    app.run(debug=True)