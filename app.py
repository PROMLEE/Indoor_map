import os
from flask import Flask, request, jsonify, send_from_directory
from scripts.find_way import find_way

app = Flask(__name__)


@app.route("/findway", methods=["POST"])
def run_way():
    data = request.json
    response = find_way(
        data["building_name"],
        data["startFloor"],
        data["startId"],
        data["endFloor"],
        data["endId"],
        data["elev"],
    )
    return jsonify({"result": response})


@app.route("/mask/<filename>")
def get_mask(filename):
    return send_from_directory(f"result/{filename[:-3]}/mask", f"{filename}.png")


@app.route("/way/<filename>")
def get_way(filename):
    return send_from_directory(f"result/{filename[:-3]}/way", f"{filename}.png")


@app.route("/upload", methods=["POST"])
def upload_file():
    UPLOAD_FOLDER = f"sources/{request.building_name}/images"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    if file:
        filename = file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return "File successfully uploaded"


if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
