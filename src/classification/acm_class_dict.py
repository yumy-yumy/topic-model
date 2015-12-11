import sys
from optparse import OptionParser

#import xml.etree.ElementTree as ET
from lxml import etree as ET
from time import time

import ioFile


def acmClassification(fname):
    start = time()
    context = ET.iterparse(fname, events=('end',))
    acm_class_dict = {}
    i = 0
    
    composedBy = []
    tree = {}
    for event, elem in context:
        i += 1
        if elem.tag.count("node"):
            content = elem.attrib
            if len(content) == 2:
                if content['id'] == 'acmccs98':
                    break
                else:
                    content['id'] = content['id'].upper()
                    if composedBy == []:
                        acm_class_dict[content['id']] = content['label']
                    else:
                        composedBy = ','.join(composedBy)
                        composedBy = '[' + composedBy
                        composedBy = composedBy + ']'
                        text = ' '.join([content['label'], composedBy])
                        acm_class_dict[content['id']] = text
                        composedBy = []
                    '''
                    # add parent class label to sub class 
                    tree[content['id']] = content['label']
                    if len(content['id']) <= 3:
                        for key in tree.keys():
                            if len(key) > len(content['id']) and key.find(content['id']) == 0:
                                acm_class_dict[key] = '-->'.join([content['label'], acm_class_dict[key]])
                    if len(content['id']) == 2:
                        tree = {}
                    '''
            elif len(content) == 1:
                if content.keys() == ['label']:
                    composedBy.append(content['label'])

                
        # remove elements in the same level to free memory
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        elem.clear()
            
    del context
      
    end = time()
    print "use time:", end - start
    
    return acm_class_dict
      

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing xml',
                         default=None)
    optparser.add_option('-o', '--outputFile',
                         dest='output',
                         help='fileName',
                         default=None)    

    (options, args) = optparser.parse_args()
    
    if options.input is None:
            fname = sys.stdin
    elif options.input is not None:
            fname = (options.input)
    else:
            print 'No filename specified, system with exit\n'
            sys.exit('System will exit')
            
    if options.output is None:
            outFile = "acm-class_dict.pkl"
    elif options.output is not None:
            outFile = options.output             
            
    acm_class_dict = acmClassification(fname)
    
    ioFile.save_object(acm_class_dict, outFile)
    
    

