'''
function: align topic distributions with the same number of columns
input: a .pkl file contains the original matrix 
output: a .pkl file contains the converted one
batch mode: shell/prob.sh
''''

import sys
from optparse import OptionParser

import numpy as np

import ioFile

def convertProb(prob, n_all_term): 
    nTopic = prob.shape[0]
    nTerm = prob[0,:].shape[1]
    nConversion = n_all_term - nTerm
    
    if nConversion != 0:
        print "convert matrix from", prob.shape, "to", (nTopic, n_all_term)
        
        
        #min_prob = prob.min(1)
        #min_prob = np.repeat(min_prob, nConversion).reshape(nTopic, nConversion)
        #prob = np.append(prob, min_prob, 1)
        
        none_prob = np.empty([nTopic, nConversion])
        none_prob.fill(-100)
        prob = np.append(prob, none_prob, 1)
    
    return prob

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--finputFile',
                         dest='input',
                         help='fileName',
                         default=None)
    optparser.add_option('-n', '--numberOfVocabulary',
                         dest='num',
                         help='number',
                         default=None)    
    optparser.add_option('-o', '--outputFile',
                         dest='output',
                         help='fileName',
                         default=None)
        
    (options, args) = optparser.parse_args()
    
    if options.input is None:
            fname = sys.stdin
    elif options.input is not None:
            fname = options.input
    else:
            print 'No filename(.pkl) specified, system with exit\n'
            sys.exit('System will exit')
            
    if options.num is None:
            n_all_term = sys.stdin
    elif options.num is not None:
            n_all_term = int(options.num)
    else:
            print 'No number of conversion specified, system with exit\n'
            sys.exit('System will exit')
                       
    if options.output is None:
            outFile = 'convert_prob.pkl'
    elif options.output is not None:
            outFile = options.output
            
    prob = ioFile.load_object(fname)
    convert_prob = convertProb(prob, n_all_term)
    #print convert_prob.shape
    ioFile.save_object(convert_prob, outFile)