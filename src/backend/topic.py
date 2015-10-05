from os import path
from collections import Counter
from src.backend import graph
from src.backend import fileSys
from src import ioFile

root_path = '/home/pzwang/data/lda_new'
model_path = path.join(root_path, 'lda_model')

def topics_from_to(start, end):
    years = range(start, end+1)

    topicFiles = fileSys.traverseTopicDirecotry(model_path, 1, years)

    # fill the path where topic_num.csv is stored
    topic_num_dirpath = path.join(root_path, 'topic_num')
    topic_num_file = fileSys.traverseDirectory(topic_num_dirpath, years)
    # fill the path where distances are stored
    distance_dirpath = path.join(root_path, 'dtm/distance')
    distanceFiles = fileSys.traverseDistanceDirectory(distance_dirpath, years)

    topic_graph = graph.createGraph(topicFiles, distanceFiles, topic_num_file, 0)
    
    return topic_graph

def topics_for_year(year):

    topicFiles = fileSys.traverseDirectory(path.join(root_path, 'lda_model', str(year), 'topic'))

    '''
    # fill the path where topic_num.csv files are stored
    topic_num_file = path.join(root_path, 'topic_num','topic_num_' + str(year) + '.csv')
    inFile = ioFile.statFromFile(topic_num_file)
    '''

    distanceFiles = fileSys.traverseDirectory(path.join(root_path, 'lda_model', str(year), 'distance'))

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
    years = set(range(start, end+1))
    for year in range(start, end+1):
        try:
            clf_topic_stat.append(Counter(clf_topic[str(year)][class_name]))
            topic_num.append(len(set(clf_topic[str(year)][class_name])))
        except KeyError:
            years.remove(year)

    topicFiles = fileSys.traverseTopicDirecotry(model_path, 1, years)
    distance_dirpath = path.join(root_path, 'class_topic/distance')
    distanceFiles = fileSys.traverseDistanceDirectory(distance_dirpath, list(years))
    
    topic_graph = graph.createGraph(topicFiles, distanceFiles, topic_num, 2, clf_topic_stat)

    return topic_graph, years

def get_classes(fname):
    class_list = ioFile.load_object(fname)

    return class_list

def statistics_for_class(class_mode, class_name):
    if class_mode == 'acm-class':
        clf_topic = ioFile.load_object(path.join(root_path, 'class_topic/class_topic_acm-class.pkl'))
    elif class_mode == 'arxiv-category':
        clf_topic = ioFile.load_object(path.join(root_path, 'class_topic/class_topic_arxiv-category.pkl'))
    
    clf_topic_stat = []
    years = []
    for year in range(1993, 2016):
        try:
            clf_topic_stat.append(Counter(clf_topic[str(year)][class_name]))
            years.append(year)
        except KeyError:
            print "No documents belonging to %s in %s " % (class_name, year)
            
    topicFiles = fileSys.traverseTopicDirecotry(model_path, 1, years)
    
    topic_bar = graph.createBarChat(topicFiles, clf_topic_stat, years)
    
    return topic_bar
