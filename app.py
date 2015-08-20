from flask import Flask, request, send_from_directory, render_template, jsonify
import json
import os
from os import path
from src.backend import topic

app = Flask(__name__)
app.debug = True

root_path = '/Users/kalleilv/desktop/topic-model/topic_data'

@app.route('/static/<path:path>')
def send_static_file(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/topics_for_years/<year_from>/<year_to>')
def topics_for_years(year_from, year_to):
    json_data = topic.topics_from_to(int(year_from), int(year_to))

    return json.dumps(json_data)

@app.route('/topics_for_year/<year>')
def topics_for_year(year):
    json_data = topic.topics_for_year(int(year))

    return json.dumps(json_data)

@app.route('/topics_for_class/<class_name>/<year_from>/<year_to>/<class_mode>')
def topics_for_class(class_name, year_from=1993, year_to=2015, class_mode='arxiv-category'):
    json_data = topic.topics_for_year(class_mode, class_name, int(year_from), int(year_to))

    return json.dumps(json_data)

@app.route('/class/<class_mode>')
def classes(class_mode='acm-class'):
    if class_mode == 'acm-class':
        fname = path.join(root_path, 'class_topic', 'acm_class.pkl')
    elif class_mode == 'arxiv-category':
        fname = path.join(root_path, 'class_topic', 'arxiv_category.pkl')

    class_list = topic.get_classes(fname)
    class_arr = []

    for key,value in class_list.iteritems():
        class_arr.append(value)

    return json.dumps({ 'classes': class_arr })

if __name__ == '__main__':
    app.run()
