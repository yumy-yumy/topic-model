'''
fucntion:create a sequence of topic nums for htm
input: a .csv file contains numbers of documents for each year
output: a list of .csv file contains topic nums and inital value of the alpha parameter
'''

import sys
from optparse import OptionParser


from src import ioFile

def topicNum(data_iterator, outpath):
    for line in data_iterator:
        # line: [year] [num] [topic_num]
        year, doc_num = line[:2]
        fname = outpath + '/topic_num_' + year + '.csv'
        print fname
        topic_num = int(doc_num) / 50
        if topic_num <= 15:
            alpha = 1 / float(topic_num)
            ioFile.dataToCSV((topic_num, alpha), fname)
        while topic_num > 15:
            alpha = 1 / float(topic_num)
            ioFile.dataToCSV((topic_num, alpha), fname)
            topic_num = topic_num / 2


if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--statFile',
                         dest='input',
                         help='fileName',
                         default=None)
    optparser.add_option('-o', '--outputPath',
                         dest='output',
                         help='directory',
                         default=None)    

    (options, args) = optparser.parse_args()
    
    if options.input is None:
            inFile = sys.stdin
    elif options.input is not None:
            inFile = ioFile.statFromFile(options.input)
    else:
            print 'No filename specified, system with exit\n'
            sys.exit('System will exit')
            
    if options.output is None:
            outFile = sys.stdin
    elif options.output is not None:
            outFile = options.output
                        
    topicNum(inFile, outFile)
