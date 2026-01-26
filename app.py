from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from main import parse_marksheet


load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
