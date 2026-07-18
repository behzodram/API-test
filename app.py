from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

logs = []
next_id = 1


def add_log(method, endpoint, body):
    global next_id

    log = {
        "id": next_id,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "method": method,
        "endpoint": endpoint,
        "body": body,
        "ip": request.remote_addr
    }

    next_id += 1

    logs.insert(0, log)

    # Faqat oxirgi 300 ta logni saqlaymiz
    if len(logs) > 300:
        logs.pop()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logs")
def get_logs():
    return jsonify(logs)


##########################################################
# TOOL 1
##########################################################

@app.route("/api/mijoz_kimligini_aniqlash", methods=["POST"])
def mijoz_kimligini_aniqlash():

    data = request.get_json(silent=True)

    if data is None:
        data = {}

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

    data = request.get_json(silent=True)

    if data is None:
        data = {}

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