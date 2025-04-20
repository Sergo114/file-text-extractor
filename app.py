from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF
import docx2txt
from PIL import Image
import pytesseract

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/extract", methods=["POST"])
def extract_text():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    ext = filename.lower().split(".")[-1]
    text = ""

    try:
        if ext == "pdf":
            with fitz.open(filepath) as doc:
                for page in doc:
                    text += page.get_text()
        elif ext == "docx":
            text = docx2txt.process(filepath)
        elif ext in ["jpg", "jpeg", "png"]:
            image = Image.open(filepath)
            text = pytesseract.image_to_string(image)
        else:
            return jsonify({"error": "Unsupported file type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"text": text})
