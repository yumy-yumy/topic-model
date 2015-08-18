from flask import Flask, request, send_from_directory, render_template, jsonify
import json
from os import path
from src.backend import topic

app = Flask(__name__)
app.debug = True

root_path = 'pzwang/data/lda_new'

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

    return jsonify({ 'from': year_from, 'to': year_to })

@app.route('/topics_for_year')
def topics_for_year():
    year = request.args.get('year')

    return 'hello world!'

@app.route('/topics_for_class')
def topics_for_class():
    class_name = request.args.get('class')

    return 'hello world!'

def classes_for_year():
    year = request.args.get('year')

    return 'hello world!'

@app.route('/class/<class_mode>')
def classes(class_mode='acm-class'):
    if class_mode == 'acm-class':
        fname = path.join(root_path, 'class_topic', 'acm_class.pkl')
    elif class_mode == 'arxiv-category':
        fname = path.join(root_path, 'class_topic', 'arxiv_category.pkl')
    
    class_list = topic.get_classes(fname)
    
    return render_template('class_display.html', class_list=class_list, class_mode=class_mode)

if __name__ == '__main__':
    app.run()
