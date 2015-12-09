import sys
from optparse import OptionParser

import re

import ioFile

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='fileName',
                         default=None)
    optparser.add_option('-a', '--referenceFile',
                         dest='all',
                         help='fileName',
                         default=None)    
    optparser.add_option('-o', '--outputFile',
                         dest='output',
                         help='fileName',
                         default=None)
        
    (options, args) = optparser.parse_args()
    
    #fun=0, arxiv_category; fun=1, acm_class
    fun = 1
    year = options.input[-8:-4]
    
    if options.input is None:
            print 'No input filename specified, system with exit\n'
            sys.exit('System will exit')
    elif options.input is not None:
            inFile = ioFile.dataFromFile(options.input)

    if options.all is None:
            print 'No reference filename specified, system with exit\n'
            sys.exit('System will exit')
    elif options.all is not None:
            inFile_all = ioFile.dataFromFile(options.all)
    if options.output is None:
        if fun == 0:
            outFile = 'category_' + year + '.txt'
        elif fun == 1:
            outFile = 'acm-class_' + year + '.txt'
    elif options.output is not None:
            outFile = options.output    
    
    acm_class_dict = ioFile.load_object("/home/pzwang/data/lda_new/topic_class/acm_class_dict.pkl")
        
    data_iterator = inFile_all

    clf_dict = dict()
    for line in data_iterator:
        line = line.split('\t')
        if fun == 0:
            clf = line[0]
        elif fun == 1:
            clf = line[1]
            if clf != '':
                clf = clf.upper()
                if clf == 'NOT AVAILABLE':
                    clf = ''
                else:
                    clf = re.sub(r"[A-Z]{2,}", '', clf)
                    clfs = []
                    # acm-class is English text
                    if clf.replace(' ','') == '':
                        print "English text"
                    else:
                        clf = re.sub(r"[0-9A-Z]{5}", '', clf)
                        # class cannot be recognised by classification system 1998
                        clf = re.sub(r"[0-9]{2}[.][0-9]{2}[+][EN]", '', clf)
                        clf = clf.replace('X', '')
                        f = re.findall(r"([A-Z])[ ,.]{0,1}([0-9M]{0,1})[ ,.]{0,1}([0-9]{0,2}[M]{0,1})", clf)
                        for level in f:
                            i = 3
                            # if a class is not in the dictionary, try its parent class
                            while i > 0:
                                c = '.'.join([l for l in level[:i] if l is not None and l != ''])
                                if len(c) == 1: c += '.'                               
                                if acm_class_dict.keys().count(c) > 0:
                                    clfs.append(c)
                                    break
                                i -= 1
                            '''
                            if i != 3:
                                print i, '|', tmp, '|', c
                            '''
                    clf = ' '.join(clfs)
        # the same document with different classifications
        if clf_dict.keys().count(line[2]) > 0:
            if clf != '':
                clf_dict[line[2]] = ' '.join(set([clf_dict[line[2]], clf]))
        else:
            clf_dict[line[2]] = clf


    data_iterator = inFile
    for line in data_iterator:
        ioFile.dataToFile(clf_dict[line]+'\n', outFile)
