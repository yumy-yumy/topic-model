'''
fucntion: extract necessary information such as date, category, text of articles and group data by year 
preXml.py
input: a .xml file
output: several .txt files by year, where each line is formatted by [category/id/...]\t[text]\n
'''


import sys
from optparse import OptionParser

#import xml.etree.ElementTree as ET
#from datetime import datetime
from lxml import etree as ET
from time import time

import ioFile

def traverseAllElements(fname):
    '''Traverse all tags in the xml file'''
    context = ET.iterparse(fname, events=('end',))
    i = 0   
    elements = set()
    for event, elem in context:
        elements.add(elem.tag)
        i += 1
        if i % 10000 == 0:
            print i 
        # clear elements to empty memory
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        elem.clear()
        
    del context    
    
    for elem in elements:
        print elem
    
    
def splitByYear(fname, outpath):
    '''Split a .xml file into several .txt files by years'''
    start = time()
    context = ET.iterparse(fname, events=('end',))
    i = 0
    #j = 0
    
    for event, elem in context:
        # get date
        if elem.tag.count("created"):
            year = elem.text[:4]
            fname = outpath + '/all_' + year + '.txt'
            i += 1
            if i % 10000 == 0:
                print i
        # get text
        elif elem.tag.count("text"):
            text = elem.text + '\n'  
        elif elem.tag.count("categories"):
            ioFile.dataToFile(elem.text+'\t', fname)
            
#        elif elem.tag.count('msc-class'):
#            print elem.text
        elif elem.tag.count('acm-class'):
            if elem.text is not None:
                ioFile.dataToFile(elem.text+'\t', fname)
            else:
                ioFile.dataToFile('\t', fname)        
        '''
        # get id
        elif elem.tag.count('id'):
            text_id = elem.text+'\t'

        if i == j+1:
            ioFile.dataToFile(text_id+text, fname)
            j = i
        '''
        
        # clear elements to empty memory
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        elem.clear()
        
    del context
      
    end = time()
    print "use time:", end - start
      

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing xml',
                         default=None)
    optparser.add_option('-o', '--outputPath',
                         dest='output',
                         help='directory',
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
            outpath = sys.stdin
    elif options.output is not None:
            outpath = options.output          
         
    splitByYear(fname, outpath)
    
    

