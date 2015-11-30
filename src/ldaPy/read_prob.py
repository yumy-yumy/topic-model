'''
function: read probability from a .txt file and save it to a .pkl file
input: a .txt file 
output: a .pkl file contains the matrix
batch mode: shell/prob.sh
'''

import sys
from optparse import OptionParser

import numpy as np

import ioFile

def readProb(fname):
    print "read probs from", fname
    prob = np.loadtxt(fname)
    prob = np.matrix(prob)

    return prob

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='fileName',
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
            print 'No filename specified, system with exit\n'
            sys.exit('System will exit')    

    if options.output is None:
            outFile = 'prob.pkl'
    elif options.output is not None:
            outFile = options.output            
            
          
    prob = readProb(fname)
    
    ioFile.save_object(prob, outFile)