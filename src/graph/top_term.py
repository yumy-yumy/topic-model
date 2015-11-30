'''
function: extract top terms of each topic
input: a .pkl file contains topic distributions and a .dat file represents the vocabulary
output: a .pkl file contains a list of topics
batch mode: shell/topic.sh
'''

import sys
from optparse import OptionParser

import numpy as np
from numpy import exp

import ioFile


def topNTerm(nTop, prob, nCol, all_term):
    for i in range(0, nCol):
        topic = []
        min_prob = prob[:,i].min()
        for j in range(0, nTop):
            index = np.squeeze(np.array(prob[:,i].argmax(0)))
            if all_term is not None:
                topic.append(all_term[index])
            else:
                topic.append(index)
            prob[index,i] = min_prob - 1
            
    #print topic
            
    return topic

    
def topProbTerm(percent, prob, nCol, all_term, fname):
    for i in range(0, nCol):
        topic = []
        min_prob = prob[:,i].min()
        total_percent = 0
        while total_percent <= percent:
            index = np.squeeze(np.array(prob[:,i].argmax(0)))
            if all_term is not None:
                topic.append(all_term[index])
            else:
                topic.append(index)
            total_percent += exp(prob[index, i])
            prob[index,i] = min_prob - 1
            
    return topic

def allTerm(fname):
    with open(fname, 'rU') as fileReader:
        all_term = fileReader.read()
        all_term = all_term.split(' ')
        
    return all_term

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputtFile',
                         dest='prob',
                         help='fileName',
                         default=None)
    optparser.add_option('-t', '--vocabularyFile',
                         dest='vocabulary',
                         help='fileName',
                         default=None)
    optparser.add_option('-o', '--outputFile',
                         dest='output',
                         help='fileName',
                         default=None)    

    (options, args) = optparser.parse_args()
    
    if options.prob is None:
            inFile = sys.stdin
    elif options.prob is not None:
            inFile = options.prob
    else:
            print 'No filename specified, system with exit\n'
            sys.exit('System will exit')    

    if options.vocabulary is not None:
            fname = options.vocabulary
            all_term = allTerm(fname)
    else:
            fname = None
            all_term = None
            
    if options.output is None:
            outFile = 'topic.pkl'
    elif options.output is not None:
            outFile = options.output
            
    prob = ioFile.load_object(inFile)
    
    all_topic = []
    nTopic, nTerm = prob.shape
    for i in range(0, nTopic):
        topic = topNTerm(5, prob[i,:].reshape(nTerm,1), 1, all_term)
        all_topic.append(topic)
    
    ioFile.save_object(all_topic, outFile)

    
    