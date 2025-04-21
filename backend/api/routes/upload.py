import os
from flask import Blueprint, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from uuid import uuid4

upload_bp = Blueprint("upload", __name__)

ALLLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLLOWED_EXTENSIONS


UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

UPLOAD_PATHS = {
    "recipe_thumbnail": os.path.join(UPLOAD_FOLDER, "recipe_thumbnail"),
    "user_avatar": os.path.join(UPLOAD_FOLDER, "user_avatar"),
}

for path in UPLOAD_PATHS.values():
    os.makedirs(path, exist_ok=True)


@upload_bp.route("/<upload_type>", methods=["POST"])
def upload_file(upload_type):
    if upload_type not in UPLOAD_PATHS:
        return jsonify({"error": f"Invalid upload type: {upload_type}"}), 400

    # check if not file in request
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    # check filename is not empty
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # check file extension
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # generate unique filename
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid4().hex}_{filename}"

    # save image
    upload_path = UPLOAD_PATHS[upload_type]
    file_path = os.path.join(upload_path, unique_filename)
    file.save(file_path)

    return jsonify({"filename": unique_filename, "message": "Upload succesfully"})


@upload_bp.route("/<upload_type>/<filename>", methods=["GET"])
def serve_file(upload_type, filename):
    if upload_type not in UPLOAD_PATHS:
        return jsonify({"error": f"Invalid upload type: {upload_type}"}), 400

    upload_paath = UPLOAD_PATHS[upload_type]
    return send_from_directory(upload_paath, filename)
