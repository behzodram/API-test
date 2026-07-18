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

    if len(logs) > 300:
        logs.pop()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logs")
def get_logs():
    return jsonify(logs)


##########################################################
# UNIVERSAL TOOL
##########################################################

@app.route("/api/tool", methods=["POST"])
def tool():

    data = request.get_json(silent=True) or {}

    ##########################################################
    # UMUMIY MAYDONLAR
    ##########################################################

    agent_id = data.get("agent_id", "unknown")

    tool_name = data.get("tool", "")

    ##########################################################
    # LOG
    ##########################################################

    add_log(
        "POST",
        "/api/tool",
        data
    )

    ##########################################################
    # TOOL ROUTER
    ##########################################################

    if tool_name == "mijoz_kimligini_aniqlash":

        mijoz_ismi = data.get("mijoz_ismi", "space")

        mijoz_kasbi = data.get("mijoz_kasbi", "")

        print(
            f"[{agent_id}]",
            "Mijoz:",
            mijoz_ismi,
            "| Kasbi:",
            mijoz_kasbi
        )

        return jsonify({
            "success": True,
            "tool": tool_name
        })

    ##########################################################

    elif tool_name == "haydovchi_malumot_saqlash":

        ism = data.get("mijoz_ismi", "")

        lokatsiya = data.get(
            "mijoz_lokatsiyasi",
            ""
        )

        manzil = data.get(
            "mijoz_maqsad_yuki_lokatsiyasi",
            ""
        )

        print(
            f"[{agent_id}]",
            ism,
            lokatsiya,
            "->",
            manzil
        )

        return jsonify({
            "success": True,
            "tool": tool_name
        })

    ##########################################################

    return jsonify({
        "success": False,
        "message": "Unknown tool."
    }), 400


if __name__ == "__main__":
    app.run(debug=True)