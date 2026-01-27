import os
import uuid
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from main import parse_marksheet


load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods = ["POST"])
def parse():

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    filepath = None
    try:
        filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        extracted_data = parse_marksheet(filepath)

        return jsonify(extracted_data)
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
    

if __name__ == "__main__":
    app.run(debug=True)
