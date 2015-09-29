from flask import Flask, request, send_from_directory, render_template, jsonify
import json
import os
import pydash
from os import path
from src.backend import topic

app = Flask(__name__)
app.debug = True

root_path = '/Users/kalleilv/desktop/topic-model/topic_data'

def filter_independent_nodes(data):
    nodes_to_indexes = []

    for (i, node) in enumerate(data['nodes']):
        nodes_to_indexes.append({ 'name': node['name'], 'index': i })

    sources_and_targets = []

    for link in data['links']:
        sources_and_targets.append(link['source'])
        sources_and_targets.append(link['target'])

    sources_and_targets = list(set(sources_and_targets))
    no_source_or_target = filter(lambda node: node['index'] not in sources_and_targets, nodes_to_indexes)

    for node in no_source_or_target:
        data['nodes'][node['index']]['removed'] = 1
        nodes_to_indexes[node['index']]['removed'] = 1

    old_index_to_new_index = {}

    iterator = 0

    for node in nodes_to_indexes:
        if 'removed' not in node.keys():
            old_index_to_new_index[str(node['index'])] = iterator
            iterator = iterator + 1

    filtered_data = data.copy()
    filtered_data['links'] = []
    filtered_data['nodes'] = []

    links_added = {}

    for (i, node) in enumerate(data['nodes']):
        if 'removed' not in node.keys():
          filtered_data['nodes'].append(node);
          node_links = filter(lambda link: link['source'] == i or link['target'] == i, data['links'])

          for link in node_links:
              if not '%i,%i' % (old_index_to_new_index[str(link['source'])], old_index_to_new_index[str(link['target'])]) in links_added:
                filtered_data['links'].append({ 'value': 1, 'source': old_index_to_new_index[str(link['source'])], 'target': old_index_to_new_index[str(link['target'])] })
                links_added['%i,%i' % (old_index_to_new_index[str(link['source'])], old_index_to_new_index[str(link['target'])])] = 1

    return filtered_data

@app.route('/static/<path:path>')
def send_static_file(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/topics_for_years/<year_from>/<year_to>')
def topics_for_years(year_from, year_to):
    data = topic.topics_from_to(int(year_from), int(year_to))
    independent_filtered = filter_independent_nodes(data)
    no_cycles = filter(lambda node: node['source'] != node['target'], independent_filtered['links'])
    independent_filtered['links'] = no_cycles

    #return json.dumps(independent_filtered)
    return json.dumps(data)

@app.route('/topics_for_year/<year>')
def topics_for_year(year):
    json_data = topic.topics_for_year(int(year))

    return json.dumps(json_data)

@app.route('/topics_for_class/<class_name>')
def topics_for_class(class_name):
    year_from=1998
    year_to=2015
    class_mode='arxiv-category'

    data = topic.topics_for_class(class_mode, class_name.replace('+', ' '), year_from, year_to)

    print data[1]

    #independent_filtered = filter_independent_nodes(data[0])
    #no_cycles = filter(lambda node: node['source'] != node['target'], independent_filtered['links'])
    #independent_filtered['links'] = no_cycles

    #independent_filtered

    return json.dumps({ 'topics': data[0], 'years': list(data[1]) })

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

@app.route('/statistics')
def category_statistics():
    return render_template('statistics.html')

if __name__ == '__main__':
    app.run()
