import numpy as np
from numpy import cumsum
from src import ioFile

distance_constraint = 0.65

def createNode(filenames, clf_topic_stat=None):
    nodes = []
    topic_num = []
    i = 0
    for fname in filenames:
        topics = ioFile.load_object(fname)
        topic_num.append(len(topics))
        nodes.append({"name":''})
        if clf_topic_stat == None:
            for topic in topics:
                nodes.append({"name": ' '.join(topic)})
        else:
            clf_topic = clf_topic_stat[i]
            for index in clf_topic.keys():
                nodes.append({"name": ' '.join(topics[index])})
            i += 1

    #print "finish creating nodes"
    return nodes, np.array(topic_num)

'''
fun=0, horizontal graph; fun=1, vertical graph; fun=2, graph for class
'''
def createLink(filenames, topic_num, fun, clf_topic_stat=None):
    # start index of each year
    topic_num += 1
    node_index = cumsum(topic_num).tolist()[:-1]
    node_index.insert(0, 0)

    links = []
    i = 0
    for fname in filenames:
        # indexes of first nodes in the graph for year i and i+1
        node_index_i = node_index[i]+1
        node_index_j = node_index[i+1]+1
        # distances between year i and i+1
        distances = ioFile.load_object(fname)
        if fun < 2:
            N = len(distances)
            for index_i in range(0, N):
                clf_topic = np.array(distances[index_i])
                if fun == 0:
                    index = np.where(clf_topic<distance_constraint)[0]
                    for index_j in index:
                        links.append({"source": node_index_i+index_i, "target": node_index_j+index_j, "value": 5})
                elif fun == 1:
                    index = np.where(clf_topic==clf_topic.min())[0][0]
                    links.append({"source": node_index_i+index_i, "target": node_index_j+index, "value": 5})
        elif fun == 2:
            for index_i, count in clf_topic_stat[i].iteritems():
                clf_topic = np.array(distances[index_i])
                index = set(np.where(clf_topic<distance_constraint)[0])
                index = index.intersection(set(clf_topic_stat[i+1].keys()))
                for index_j in index:
                    links.append({"source": node_index_i+clf_topic_stat[i].keys().index(index_i), 
                                  "target": node_index_j+clf_topic_stat[i+1].keys().index(index_j), 
                                  "value": 5})
                    
        i += 1
    
    #print "finish creating links"
    return links

def addVirtualLink(links, topic_num):
    source_nodes = set()
    target_nodes = set()
    for link in links:
        source_nodes.add(link['source'])
        target_nodes.add(link['target'])
    node_num = sum(topic_num)
    node_index = cumsum(topic_num).tolist()[:-1]
    node_index.insert(0, 0)
    i = 0
    for index in range(1, node_num):
        if index < node_index[1]:
            target_node = node_index[1]
            if index not in source_nodes:
                links.append({"source": index, "target": target_node, "value":1})
        else:
            source_node = node_index[i]
            if index not in target_nodes:
                    links.append({"source": source_node, "target": index, "value":1})
            if i+2 < len(node_index) and index+1 == node_index[i+2]:
                i += 1    
                
    return links


def topicNum(inFile, fun):
    num = []
    if fun == 0:
        filenames = inFile
        for fname in filenames:
            data_iterator = ioFile.statFromFile(fname)
            for line in data_iterator:
                n = int(line[0])
            num.append(n)
    elif fun == 1:
        data_iterator = inFile
        for line in data_iterator:
            num.append(int(line[0]))

    return np.array(num)

def createGraph(topicFiles, distanceFiles, fun, clf_topic_stat=None, topic_num=None):
    if fun < 2:
        nodes, topic_num = createNode(topicFiles, clf_topic_stat)
    elif fun == 2:
        nodes, num = createNode(topicFiles, clf_topic_stat)
        topic_num = np.array(topic_num)

    links = createLink(distanceFiles, topic_num, fun, clf_topic_stat)
    links = addVirtualLink(links, topic_num)

    graph_data = {"nodes": nodes, "links": links}
    
    return graph_data

def createTree(topicFiles, distanceFiles):
    level = len(topicFiles)
    nodes = []
    parent = []
    for i in range(0, level):
        topics = ioFile.load_object(topicFiles[i])
        # nodes at the bottom level of the tree
        if i == 0:    
            [nodes.append({"name": ' '.join(topic), "size": 1}) for topic in topics]
        else:
            pre_nodes = nodes
            nodes = []
            for j in range(0, len(topics)):
                indexes = np.where(parent==j)[0]
                children = []
                [children.append(pre_nodes[index]) for index in indexes]
                nodes.append({"name": ' '.join(topics[j]), "children": children})
        if i < level-1:
            distances = np.matrix(ioFile.load_object(distanceFiles[i]))
            parent = np.squeeze(np.array(distances.argmin(1)))
        
    root = {"name": '...', "children": nodes}
    
    return root

def createBarChat(topicFiles, clf_topic_stat, years):
    N = len(topicFiles)
    bar_data = []
    for i in range(0, N):
        topics = ioFile.load_object(topicFiles[i])
        clf_topic = clf_topic_stat[i]
        year = years[i]
        doc_num, topic_percent = statOfClassification(clf_topic, topics)
        #print topic_percent
        bar_data.append({"year": year, "doc": doc_num, "topics": topic_percent})
        
        
    return bar_data

def statOfClassification(clf_topic, topics):
    doc_num = sum(clf_topic.values())
    topic_percent = []
    for index, count in clf_topic.iteritems():
        topic_percent.append({"title": topics[index], "weight":count/float(doc_num)})
    
    return doc_num, topic_percent
