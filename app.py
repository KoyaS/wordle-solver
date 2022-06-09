'''
To run (in terminal):
- export FLASK_APP=index.py
- flask run
Hosted on localhost
'''

from flask import Flask, request, jsonify
from solver import Solver

app = Flask(__name__)

todays_word = 'not found yet'

@app.route("/")
def hello():
    return "<h1>Hello World</h1>"

@app.get("/")
def get_todays_word():
    return jsonify({'todays_word': todays_word})

@app.post("/")
def solve_wordle():
    if request.is_json:
        command = request.get_json()
        s = Solver(command['firstWord'])
        final_word = s.run()
        return final_word, 201
    return {"error": "Request must be JSON"}, 415