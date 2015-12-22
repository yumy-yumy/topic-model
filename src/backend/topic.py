from os import path
from collections import Counter
from src.backend import graph
from src.backend import fileSys
from src import ioFile

root_path = '/home/pzwang/data/cs'
model_path = path.join(root_path, 'lda_model')

def topics_from_to(start, end):
    years = range(start, end+1)

    topicFiles = fileSys.traverseTopicDirecotry(model_path, 1, years)

    # fill the path where distances are stored
    clf_topic = path.join(root_path, 'dtm/distance')
    distanceFiles = fileSys.traverseDistanceDirectory(clf_topic, years)

    topic_graph = graph.createGraph(topicFiles, distanceFiles, 0)

    return topic_graph

def topics_for_year(year):

    topicFiles = fileSys.traverseDirectory(path.join(root_path, 'lda_model', str(year), 'topic'))

    distanceFiles = fileSys.traverseDirectory(path.join(root_path, 'lda_model', str(year), 'distance'))

    topic_tree = graph.createTree(topicFiles, distanceFiles)

    return topic_tree

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
    clf_topic = path.join(root_path, 'class_topic/distance')
    distanceFiles = fileSys.traverseDistanceDirectory(clf_topic, list(years))

    topic_graph = graph.createGraph(topicFiles, distanceFiles, 2, clf_topic_stat, topic_num)

    return topic_graph, years

def get_classes(class_mode):
    if class_mode == 'acm-class':
        fname = path.join(root_path, 'class_topic', 'acm_class.pkl')
    elif class_mode == 'arxiv-category':
        fname = path.join(root_path, 'class_topic', 'arxiv_category.pkl')
        
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

def topics_for_cs():
    topicFiles = fileSys.traverseDirectory(path.join(root_path, 'htm/topic'))
    distanceFiles = fileSys.traverseDirectory(path.join(root_path, 'htm/distance'))
    topic_tree = graph.createTree(topicFiles, distanceFiles)
    
    return topic_tree
