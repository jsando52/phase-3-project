from flask import Flask, request, jsonify
from waitress import serve
from flask_cors import CORS
import json
import psycopg2
from search import searchQuery, expandBookData
app = Flask(__name__)
CORS(app)

try:
    conn = psycopg2.connect(
        host="localhost",
        database="",
        user="",
        password="",
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
        #print("success")
        return jsonify(searchQuery(data, conn)), 200
    else:
        return jsonify({"message": "Search didn't find anything or input was wrong"})
    
@app.route("/book", methods=["POST"])
def book_page():
    data = request.get_json()
    print(data.get("title"))
    book_data = expandBookData(data.get("title"), conn)
    return jsonify({
        "book": book_data
    }), 200

# Obvious, runs the Flask backend
if __name__ == '__main__':
    print("Listening...")
    app.run(debug=True, port=5000)