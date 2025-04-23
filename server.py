from flask import Flask, request, jsonify
from waitress import serve
from flask_cors import CORS
import json
import psycopg2
from search import searchQuery
app = Flask(__name__)
CORS(app)

try:
    conn = psycopg2.connect(
        host="localhost",
        database="phase-03",
        user="postgres",
        password="Mirko&Chie",
        port="5432"
    )
    print("Successful Connection to Phase 3 database")
except(psycopg2.DatabaseError, Exception) as error:
    print(error)


@app.route("/search", methods=["POST"])
def search_page():
    data = request.get_json()
    success = searchQuery(data, conn)
    if success:
        return jsonify(searchQuery(data, conn)), 200
    else:
        return jsonify({"message": "Search didn't find anything or input was wrong"})
    
@app.route("/book", methods=["POST"])
def book_page():
    return

# Obvious, runs the Flask backend
if __name__ == '__main__':
    print("Listening...")
    app.run(debug=True, port=5000)