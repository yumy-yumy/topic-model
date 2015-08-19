from flask import Flask, request, send_from_directory, render_template, jsonify
import json
import os
from src.backend import topic

app = Flask(__name__)
app.debug = True

@app.route('/static/<path:path>')
def send_static_file(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/topics_for_years')
def topics_for_years():
    year_from = request.args.get('from')
    year_to = request.args.get('to')

    filename = os.path.join(os.path.dirname(__file__), 'static/data/graph_1993_2002.json')

    data_file = open(filename, 'r')
    data_json = data_file.read()
    data_file.close()

    return data_json

@app.route('/topics_for_year')
def topics_for_year():
    year = request.args.get('year')

    filename = os.path.join(os.path.dirname(__file__), 'static/data/flare.json')

    data_file = open(filename, 'r')
    data_json = data_file.read()
    data_file.close()

    return data_json

@app.route('/topics_for_class')
def topics_for_class():
    class_name = request.args.get('class')

    return jsonify({ 'message': 'Hello World!' })

def classes_for_year():
    year = request.args.get('year')

    return jsonify({ 'message': 'Hello World!' })

if __name__ == '__main__':
    app.run()
