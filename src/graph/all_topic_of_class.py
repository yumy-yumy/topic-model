import sys
from optparse import OptionParser
from os import walk, path

import numpy as np
from collections import Counter

import ioFile

'''
fun=0, category; fun=1, acm-class
'''
def classificationOfDocument(data_iterator, clf_dict, fun):
    all_clf = []
    unique_clf = set()
    for line in data_iterator:
        line = line.rstrip('\n')
        if line != '':
            clfs = line.split(' ')
        else:
            clfs = []
        if fun == 0:
            all_clf.append(clfs)
            for clf in clfs:
                if clf_dict.keys().count(clf) != 0:
                    unique_clf.add(clf_dict[clf])
                else:
                    unique_clf.add(clf)
        if fun == 1:
            for clf in clfs:
                full_clf = fullAcmClass(clf)
                all_clf.append(full_clf)
                [unique_clf.add(c) for c in full_clf]

    return all_clf, unique_clf             

def topicOfClassification(unique_clf, all_clf, clf_dict, topics, fun):
    clf_topic = {clf : [] for clf in unique_clf}
    i = 0
    for clfs in all_clf:
        if fun == 0:
            for clf in clfs:
                if clf_dict.keys().count(clf) != 0:
                    clf_topic[clf_dict[clf]].append(topics[i])
                else:
                    clf_topic[clf].append(topics[i])
        elif fun == 1:
            [clf_topic[clf].append(topics[i]) for clf in clfs]
        i += 1
            
    return clf_topic
    
def fullAcmClass(clf):
    levels = clf.split('.')
    N = len(levels)
    nodes = []
    for i in range(1, N+1):
        if i == 1:
            nodes.append(levels[0]+'.')
        else:
            nodes.append('.'.join(levels[:i]))

    return nodes 
    
def plotCategory(categories, categories_dict):
    convert_categories=[]
    for category in categories:
        convert_categories.append(categories_dict[category])
        
    print convert_categories
    
def topicOfClassificationForAllYear(probDir, topicDir, classDir, clf_dict, fun):

    probFiles = traverseDirectory(probDir)
    topicFiles = traverseDirectory(topicDir)
    classFiles = traverseDirectory(classDir)
    
    N = len(probFiles)
    if len(topicFiles) != N or len(classFiles) != N:
        print "numbers of files are not same"
        sys.exit('System will exit')
    
    all_clf_topic = {}
    if fun == 0:
        irange = range(0, N)
    # acm-class start from 1998
    elif fun == 1:
        irange = range(5, N)
    for i in irange:
        prob = ioFile.load_object(probFiles[i])
        topics = ioFile.load_object(topicFiles[i])
        inFile = ioFile.dataFromFile(classFiles[i])
        
        year = probFiles[i][-8:-4]
        topic_index = np.squeeze(np.array(prob.argmax(1)))
        doc_topic = topic_index
        #doc_topic = []
        #[doc_topic.append(' '.join(topics[index])) for index in topic_index]
 
        all_clf, unique_clf = classificationOfDocument(inFile, clf_dict, fun)
        clf_topic = topicOfClassification(unique_clf, all_clf, clf_dict, doc_topic, fun)
        
        all_clf_topic[year] = clf_topic
    
    return all_clf_topic
      
def convertDataToJson(all_clf_topic, clf_dict, fun):
    clf_topic_stat = []
    '''
    if fun == 1:
        clf_topic_stat = [[]*3]
    '''
    for year, clf_topic in all_clf_topic.iteritems(): 
        if fun == 0:
            for clf, topics in clf_topic.iteritems():
                clf_topic = []
                [clf_topic.append({"topic":topic, "count":count}) for topic, count in Counter(topics).iteritems()]
                clf_topic_stat.append({"name": clf, "year":year, "info":clf_topic})
        elif fun == 1:
            for clf, topics in clf_topic.iteritems():
                try:
                    name = ' '.join([clf, clf_dict[clf]])
                except KeyError:
                    print year, clf
                clf_topic = []
                [clf_topic.append({"topic":topic, "count":count}) for topic, count in Counter(topics).iteritems()]
                clf_topic_stat.append({"name": name, "year":year, "info":clf_topic})
                '''
                # level 1
                if len(clf) == 2:
                    clf_topic_stat[0].append({"name":name, "year":year, "info":clf_topic})
                # level 2
                elif len(clf) == 3:
                    clf_topic_stat[1].append({"name":name, "year":year, "info":clf_topic})
                # level 3
                elif len(clf) > 3:
                    clf_topic_stat[2].append({"name":name, "year":year, "info":clf_topic})
                '''
                    
    return clf_topic_stat
    
def traverseDirectory(dirpath):
    for (dirpath, dirname, filenames) in walk(dirpath):
        filenames = sorted(filenames)
        break
    full_fnames = []
    for fname in filenames:
        fname = path.join(dirpath, fname)
        #print fname
        if path.isfile(fname):
            full_fnames.append(fname)
            
    return full_fnames
        
                
if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-p', '--probDir',
                         dest='prob',
                         help='Directory',
                         default=None)
    optparser.add_option('-t', '--topicDir',
                         dest='topic',
                         help='Directory',
                         default=None)
    optparser.add_option('-c', '--classDir',
                         dest='clf',
                         help='Directory',
                         default=None)
    optparser.add_option('-d', '--classificationdictFile',
                         dest='clf_dict',
                         help='fileName',
                         default=None)    
    optparser.add_option('-o', '--outputFile',
                         dest='output',
                         help='fileName',
                         default=None)
        
    (options, args) = optparser.parse_args()
    
    if options.prob is None:
            print 'No prob filename specified, system with exit\n'
            sys.exit('System will exit')
    elif options.prob is not None:
            probDir = options.prob

    if options.topic is None:
            print 'No topic filename specified, system with exit\n'
            sys.exit('System will exit')
    elif options.topic is not None:
            topicDir = options.topic
            
    if options.clf is None:
            print 'No class filename specified, system with exit\n'
            sys.exit('System will exit')
    elif options.clf is not None:
            classDir = options.clf

    if options.clf_dict is None:
            print 'No class-dict filename specified, system with exit\n'
            sys.exit('System will exit') 
    elif options.clf_dict is not None:
            clf_dict = ioFile.load_object(options.clf_dict)              
            
    if options.output is None:
            outFile = 'topic_of_class.json'
    elif options.output is not None:
            outFile = options.output
    
    fun = 0
    
    all_clf_topic = topicOfClassificationForAllYear(probDir, topicDir, classDir, clf_dict, fun)
    
    ioFile.save_object(all_clf_topic, "class_topic_arxiv-category.pkl")
    
    #clf_topic_stat = convertDataToJson(all_clf_topic, clf_dict, fun)
    
    #ioFile.save_json({"category": clf_topic_stat}, outFile)
    
    
    