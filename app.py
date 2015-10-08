from flask import Flask, request, send_from_directory, render_template, jsonify
import json
import os
import pydash
from os import path
from src.backend import topic

app = Flask(__name__)
app.debug = True

@app.route('/static/<path:path>')
def send_static_file(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/topics_for_years/<year_from>/<year_to>')
def topics_for_years(year_from, year_to):
    data = topic.topics_from_to(int(year_from), int(year_to))

    return json.dumps(data)

@app.route('/topics_for_year/<year>')
def topics_for_year(year):
    json_data = topic.topics_for_year(int(year))

    return json.dumps(json_data)

@app.route('/topics_for_class/<class_name>')
def topics_for_class(class_name):
    year_from=1993
    year_to=2015
    class_mode='arxiv-category'

    data = topic.topics_for_class(class_mode, class_name.replace('+', ' '), year_from, year_to)

    return json.dumps({ 'topics': data[0], 'years': list(data[1]) })

@app.route('/class/<class_mode>')
def classes(class_mode='acm-class'):
    class_list = topic.get_classes(class_mode)
    class_arr = []

    for key,value in class_list.iteritems():
        class_arr.append(value)

    return json.dumps({ 'classes': class_arr })

@app.route('/statistics')
def category_statistics():
    return render_template('statistics.html')

@app.route('/statistics_for_class/<class_name>')
def statistics_for_class(class_name):
    statistics = topic.statistics_for_class('arxiv-category', class_name.replace('+', ' '))
    
    return json.dumps(statistics)

if __name__ == '__main__':
    app.run()
