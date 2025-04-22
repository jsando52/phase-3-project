from flask import Flask, request, jsonify, render_template
from waitress import serve
from flask_cors import CORS
import datetime
import json

app = Flask(__name__)
CORS(app)

# Just the home page
@app.route("/")
def index():
    return render_template("index.html")

# Obvious, runs the Flask backend
if __name__ == '__main__':
    print("Listening...")
    app.run(debug=True, port=5000)