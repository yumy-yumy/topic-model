'''
function: build a vocabulary from all texts
input: a .txt file contains all data
output: a all_term.dat file contains all terms
'''


import sys
from optparse import OptionParser
#from os import walk, path


import ioFile


def vocabulary(data_iterator):
    '''Get all terms from all documents'''
    all_term = set()
    i = 0
    for line in data_iterator:
        # remove the end of line
        line = line.replace('\n', '')
        line = line.split(' ')
        unique_term = set(line)
        unique_term.discard('')
        if all_term == set():
            all_term = unique_term
        else:
            all_term = all_term.union(unique_term)
            
        i += 1
        if i % 10000 == 0:
            print i
    
    print "the size of vocabulary is " + str(len(all_term))
    
    return all_term

'''
### read data from a directory
def allVocabulary(dirpath, outFile):
    all_term = set()
    for (dirpath, dirname, filenames) in walk(dirpath):
        filenames = sorted(filenames)
        break
    for fname in filenames:
            fname = path.join(dirpath, fname)
            if path.isfile(fname):
                inFile = ioFile.abstractFromFile(fname)
                file_term = vocabulary(inFile)
                if all_term == set():
                    all_term = file_term
                else:
                    all_term = all_term.union(file_term)
    all_term = list(all_term)
    
    ioFile.termToFile(all_term, outFile)
'''
    
            
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
            print 'No filename specified, system with exit\n'
            sys.exit('System will exit')
    elif options.input is not None:
            inFile = ioFile.dataFromFile(options.input)
            
    if options.output is None:
            outFile = 'all_term.dat'
    elif options.output is not None:
            outFile = options.output
            
    all_term = vocabulary(inFile)
    ioFile.termToFile(all_term, outFile)
            