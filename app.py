import os
from flask import Flask, request, send_from_directory
from scripts.find_way import find_way

app = Flask(__name__)


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


@app.route("/mask/<filename>")
def get_mask(filename):
    return send_from_directory(f"result/{filename[:-3]}/mask", f"{filename}.png")


@app.route("/way/<filename>")
def get_way(filename):
    return send_from_directory(f"result/{filename[:-3]}/way", f"{filename}.png")


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
