import json
import os
from flask import Flask, jsonify, request, send_from_directory, make_response
from scripts.find_way import find_way
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/findway", methods=["POST"])
def run_way():
    data = request.json
    find_way(
        data["building_name"],
        data["startFloor"],
        data["startId"],
        data["endFloor"],
        data["endId"],
        data["elev"],
    )
    return "길 탐색(find_way) 완료!!"


@app.route("/editstore", methods=["POST"])
def edit_store():
    data = request.json
    find_way(
        data["building_name"],
        data["startFloor"],
        data["startId"],
        data["endFloor"],
        data["endId"],
        data["elev"],
    )
    return "길 탐색(find_way) 완료!!"


@app.route("/mask/<filename>")
def get_mask(filename):
    img_path = f"result/{filename[:-3]}/mask"
    fname = f"{filename}.png"
    if os.path.exists(os.path.join(img_path, fname)):
        return send_from_directory(img_path, fname)
    else:
        return send_from_directory("sources", "404err.png")


@app.route("/way/<filename>")
def get_way(filename):
    img_path = f"result/{filename[:-3]}/way"
    fname = f"{filename}.png"
    if os.path.exists(os.path.join(img_path, fname)):
        return send_from_directory(img_path, fname)
    else:
        return send_from_directory("sources", "404err.png")


@app.route("/source/<filename>")
def get_source(filename):
    img_path = f"sources/{filename[:-3]}/images"
    fname = f"{filename}.png"
    if os.path.exists(os.path.join(img_path, fname)):
        return send_from_directory(img_path, fname)
    else:
        return send_from_directory("sources", "404err.png")


@app.route("/json/<filename>")
def filtered_json(filename):
    img_path = f"result/{filename[:-3]}/data"
    fname = f"{filename}.json"
    with open(os.path.join(img_path, fname), "r") as file:
        data = json.load(file)
    filtered_data = []
    for item in data:
        # if item["id"] not in [-2, 1]:
        filtered_data.append({"id": item["id"], "caption": item["caption"]})
    return jsonify(filtered_data)


@app.route("/dir/<buildingname>")
def list_directory(buildingname):
    directory_path = f"result/{buildingname}/data"
    try:
        file_list = os.listdir(directory_path)
        for i in range(len(file_list)):
            file_list[i] = file_list[i][-7:-5]
        return jsonify(file_list)
    except FileNotFoundError:
        return jsonify({"error": "Directory not found"}), 404


@app.route("/buildinglist")
def building_list():
    directory_path = "result"
    try:
        file_list = os.listdir(directory_path)
        return jsonify(file_list)
    except FileNotFoundError:
        return jsonify({"error": "Directory not found"}), 404


@app.route("/upload/<filename>", methods=["POST"])
def upload_file(filename):
    UPLOAD_FOLDER = f"./sources/{filename[:-3]}/images"
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    if file:
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], f"{filename}.png"))
        return "File successfully uploaded"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
