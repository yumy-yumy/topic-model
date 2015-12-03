'''
function: convert text to the format required by lda-c
input: a .txt file contains text & all_term.dat
output: a foo-mult.data contains the modeling data
        format of each line: [number of unique terms] [the index of the term: the number of its occurrence] ...
batch mode: shell/batch_data.sh
'''


import sys
from optparse import OptionParser

import re

import ioFile


def termCount(data_iterator, fname, all_term):
    '''Count each term in the document'''
    i = 0
    for line in data_iterator:
        # remove the end of line
        line = line.replace('\n', '')
        line = line.split(' ')
        unique_term = set(line)
        unique_term.discard('')
        count = {}
        for term in unique_term:
            index = all_term.index(term)
            count[index] = line.count(term)
        i += 1
        if i % 10000 == 0:
            print i
        ioFile.termCountToFile(count, fname)
        
def allTerm(fname):
    with open(fname, 'rU') as fileReader:
        all_term = fileReader.read()
        all_term = all_term.split(' ')
        
    return all_term
        
        
if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--abstractFile',
                         dest='abstract',
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
    
    if options.abstract is None:
            inFile = sys.stdin
    elif options.abstract is not None:
            inFile = ioFile.dataFromFile(options.abstract)
    else:
            print 'No abstract filename specified, system with exit\n'
            sys.exit('System will exit')

    if options.vocabulary is None:
            fname = sys.stdin
    elif options.vocabulary is not None:
            fname = options.vocabulary
    else:
            print 'No vocabulary filename specified, system with exit\n'
            sys.exit('System will exit')
            
    if options.output is None:
            outFile = 'foo-mult.dat'
    elif options.output is not None:
            outFile = options.output
            
        
    all_term = allTerm(fname)
    termCount(inFile, outFile, all_term)
