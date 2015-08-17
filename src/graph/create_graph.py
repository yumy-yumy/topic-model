import sys
from optparse import OptionParser
from os import walk, path

import numpy as np
from numpy import cumsum

import ioFile

def createNode(dirpath):
    print "read nodes from", dirpath
    
    nodes = []
    for (dirpath, dirname, filenames) in walk(dirpath):
        filenames = sorted(filenames)
        break
    for fname in filenames:
        fname = path.join(dirpath, fname)
        print fname
        if path.isfile(fname):
            topics = ioFile.load_object(fname)
            for topic in topics:
                nodes.append({"name": ' '.join(topic)}) 
                
    print "finish creating nodes"            
    return nodes
    
'''
fun=0, create horizontal model; fun=1 create vertical model 
'''        
def createLink(dirpath, topic_num, fun):
    print "read links from", dirpath
    
    # start index of each year
    node_index = cumsum(topic_num).tolist()[:-1]
    node_index.insert(0, 0)
    
    links = []
    for (dirpath, dirname, filenames) in walk(dirpath):
        filenames = sorted(filenames)
        break
    
    i = 0
    for fname in filenames:
        fname = path.join(dirpath, fname)
        print fname
        if path.isfile(fname):
            # start indexes of year i, i+1
            node_index_j = node_index[i]
            node_index_k = node_index[i+1]
            
            distances = ioFile.load_object(fname)
            N = len(distances)
            for j in range(0, N):
                distance = np.array(distances[j])
                if fun == 0:
                    index = np.where(distance<0.5)[0]
                    for k in index:
                        links.append({"source": node_index_j+j, "target": node_index_k+k, "value": 1})
                elif fun == 1:
                    index = np.where(distance==distance.min())[0][0]
                    links.append({"source": node_index_j+j, "target": node_index_k+index, "value": 1})
                    
        i += 1              
                
    print "finish creating links"            
    return links
        
def topicNum(inFile, fun):
    num = []
    if fun == 0:
        for (dirpath, dirname, filenames) in walk(inFile):
            filenames = sorted(filenames)
            break
        for fname in filenames:
            fname = path.join(dirpath, fname)
            if path.isfile(fname):
                data_iterator = ioFile.statFromFile(fname)
                for line in data_iterator:
                    n = int(line[0])
            num.append(n)  
    elif fun == 1:
        data_iterator = inFile
        for line in data_iterator:
            num.append(int(line[0]))
        
    return np.array(num)

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-t', '--topicDir',
                         dest='topic',
                         help='directory',
                         default=None)
    optparser.add_option('-d', '--distanceDir',
                         dest='distance',
                         help='directory',
                         default=None)
    optparser.add_option('-n', '--topicNumFile',
                         dest='num',
                         help='fileName',
                         default=None)
    optparser.add_option('-o', '--outputFile',
                         dest='output',
                         help='fileName',
                         default=None)
    (options, args) = optparser.parse_args()
    
    fun = 0
    
    if options.topic is None:
            topic_dirpath = sys.stdin
    elif options.topic is not None:
            topic_dirpath = options.topic
    else:
            print 'No topic directory specified, system with exit\n'
            sys.exit('System will exit')
            
    if options.distance is None:
            distance_dirpath = sys.stdin
    elif options.distance is not None:
            distance_dirpath = options.distance
    else:
            print 'No distance directory specified, system with exit\n'
            sys.exit('System will exit')
            
    if options.num is None:
            inFile = sys.stdin
    elif options.num is not None:
            if fun == 0:
                inFile = options.num
            elif fun == 1:
                inFile = ioFile.statFromFile(options.num)
    else:
            print 'No stat file specified, system with exit\n'
            sys.exit('System will exit')
            
    if options.output is None:
            outFile = 'graph.json'
    elif options.output is not None:
            outFile = options.output      
    
    nodes = createNode(topic_dirpath)
    
    topic_num = topicNum(inFile, fun)
    
    links = createLink(distance_dirpath, topic_num, fun)
    
    graph_data = {"nodes": nodes, "links": links} 
    
    ioFile.save_json(graph_data, outFile)