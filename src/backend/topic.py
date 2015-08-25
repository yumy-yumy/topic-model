from os import path
from collections import Counter
from src.backend import graph
from src.backend import fileSys
from src import ioFile

root_path = '/Users/kalleilv/desktop/topic-model/topic_data'
first_year = 1993

def topics_from_to(start, end):
    # fill the path where models are stored
    topicFiles = fileSys.traverseTopicDirecotry(path.join(root_path, 'lda_model'), 1, [start, end])

    # fill the path where topic_num.csv is stored
    topic_num_dirpath = path.join(root_path, 'topic_num')
    topic_num_file = fileSys.traverseDirectory(topic_num_dirpath, [start, end])

    # fill the path where distances are stored
    distance_dirpath = path.join(root_path, 'graph_horizontal/distance')

    if start == first_year:
        distanceFiles = fileSys.traverseDirectory(distance_dirpath, [start, end])
    else:
        distanceFiles = fileSys.traverseDirectory(distance_dirpath, [start, end])[1:]

    topic_graph = graph.createGraph(topicFiles, distanceFiles, topic_num_file, 0)

    return topic_graph

def topics_for_year(year):
    # fill the path where models are stored
    model_path = path.join(root_path, 'lda_model', str(year))

    topic_dirpath = path.join(model_path, 'topic')
    topicFiles = fileSys.traverseDirectory(topic_dirpath)

    '''
    # fill the path where topic_num.csv files are stored
    topic_num_file = path.join(root_path, 'topic_num','topic_num_' + str(year) + '.csv')
    inFile = ioFile.statFromFile(topic_num_file)
    '''

    distance_dirpath = path.join(model_path, 'distance')

    distanceFiles = fileSys.traverseDirectory(distance_dirpath)

    topic_tree = graph.createTree(topicFiles, distanceFiles)

    return topic_tree

    '''
    fun = 1
    nodes = graph.createNode(topicFiles)
    topic_num = graph.topicNum(inFile, fun)
    links = graph.createLink(distanceFiles, topic_num, fun)

    graph_data = {"nodes": nodes, "links": links}

    return graph_data
    '''

'''
example:
class_mode=acm-class, class_name=A.1;  class_mode=arxiv-category, class_name=Artificial Intelligence
'''
def topics_for_class(class_mode, class_name, start, end):
    if class_mode == 'acm-class':
        clf_topic = ioFile.load_object(path.join(root_path, 'class_topic/class_topic_acm-class.pkl'))
    elif class_mode == 'arxiv-category':
        clf_topic = ioFile.load_object(path.join(root_path, 'class_topic/class_topic_arxiv-category.pkl'))

    clf_topic_stat = []
    topic_num = []
    for year in range(start, end+1):
        clf_topic_stat.append(Counter(clf_topic[str(year)][class_name]))
        topic_num.append(len(set(clf_topic[str(year)][class_name])))

    # fill the path where models are stored
    topicFiles = fileSys.traverseTopicDirecotry(path.join(root_path, 'lda_model'), 0, [start, end])

    distance_dirpath = path.join(root_path, 'class_topic', 'distance')
    if start == first_year:
        distanceFiles = fileSys.traverseDirectory(distance_dirpath, [start, end])
    else:
        distanceFiles = fileSys.traverseDirectory(distance_dirpath, [start, end])[1:]

    topic_graph = graph.createGraph(topicFiles, distanceFiles, topic_num, 2, clf_topic_stat)

    return topic_graph

def get_classes(fname):
    class_list = ioFile.load_object(fname)

    return class_list