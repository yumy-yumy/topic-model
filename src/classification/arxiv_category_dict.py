import sys
from optparse import OptionParser

import ioFile

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing txt',
                         default=None)
    optparser.add_option('-o', '--outputFile',
                         dest='output',
                         help='fileName',
                         default=None)    

    (options, args) = optparser.parse_args()
    
    if options.input is None:
            inFile = sys.stdin
    elif options.input is not None:
            inFile = ioFile.dataFromFile(options.input)
    else:
            print 'No filename specified, system with exit\n'
            sys.exit('System will exit')
            
    if options.output is None:
            outFile = "arxiv-category_dict.pkl"
    elif options.output is not None:
            outFile = options.output
             
    data_iterator = inFile
    category_dict = {}
    
    for line in data_iterator:
        line = line.rstrip('\n')
        line = line.split('\t')
        category_dict[line[0]] = line[1]
        
    ioFile.save_object(category_dict, outFile)