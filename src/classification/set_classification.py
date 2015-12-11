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
    optparser.add_option('-r', '--referenceFile',
                         dest='reference',
                         help='fileName',
                         default=None)
    optparser.add_option('-c', '--className',
                         dest='class_name',
                         help='className',
                         default=None)
    optparser.add_option('-d', '--classDictName',
                         dest='clf_dict',
                         help='fileName',
                         default=None)     
    optparser.add_option('-o', '--outputFile',
                         dest='output',
                         help='fileName',
                         default=None)
        
    (options, args) = optparser.parse_args()
    
    if options.input is None:
            print 'No text filename specified, system with exit\n'
            sys.exit('System will exit')
    elif options.input is not None:
            inFile = ioFile.dataFromFile(options.input)

    if options.reference is None:
            print 'No reference filename specified, system with exit\n'
            sys.exit('System will exit')
    elif options.reference is not None:
            inFile_ref = ioFile.dataFromFile(options.reference)
           
    if options.class_name is None:
            print 'No name of the category specified, system with exit\n'
            sys.exit('System will exit')        
    else:
            if options.class_name == 'arxiv-category':
                fun = 0
            elif options.class_name == 'acm-class':
                fun = 1
            else:
                print 'Name of the category is incorrect, system with exit\n'
                sys.exit('System will exit')                 
                
    if options.clf_dict is None:
        if options.class_name == 'acm-class':
            print 'No class dict filename specified, system with exit\n'
            sys.exit('System will exit')
    else:
        acm_class_dict = ioFile.load_object(options.clf_dict)
 
    if options.output is None:
        year = options.input[-8:-4]
        if fun == 0:
            outFile = 'arxiv-category_' + year + '.txt'
        elif fun == 1:
            outFile = 'acm-class_' + year + '.txt'
    elif options.output is not None:
            outFile = options.output
        
    data_iterator = inFile_ref

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


    # keep the order of text is the same as the order of posterior matrix
    data_iterator = inFile
    for line in data_iterator:
        ioFile.dataToFile(clf_dict[line]+'\n', outFile)
