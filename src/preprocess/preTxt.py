import sys
from optparse import OptionParser

import ioFile

def removeDuplicate(data_iterator, year, outpath):
    '''Remove duplicate records and write the number of documents to a .csv file'''
    data = []
    for line in data_iterator:
        line = line.split('\t')
        data.append(line[-1])
        
    abstract = sorted(set(data))
    #abstract = set(data)
    num_with_duplicate = len(data)
    num_without_duplicate = len(abstract)
    
    fname = outpath + '/text_' + year + '.txt'  
    ioFile.abstractsToFile(abstract, fname)
    fname = outpath + '/stat.csv'
    ioFile.dataToCSV((year, num_without_duplicate), fname)
    
    print "number including duplicate =", num_with_duplicate, "number excluding duplicate =", num_without_duplicate

    
if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename',
                         default=None)

    optparser.add_option('-o', '--outputPath',
                         dest='output',
                         help='directory',
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
            outpath = sys.stdin
    elif options.output is not None:
            outpath = options.output

    year = options.input[-8:-4]
    
    removeDuplicate(inFile, year, outpath)

    