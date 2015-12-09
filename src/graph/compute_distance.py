'''
function: compute distances for all pairs of topics
input: two .pkl file contains topic distributions for two years(dtm) or two layers(htm)
output: a .pkl file contains the matrix of distances
batch mode: shell/distances.sh(dtm), shell/distance.sh(htm)
'''

import sys
from optparse import OptionParser

from numpy import sqrt, exp
from numpy.linalg import norm
from scipy.stats import entropy

import ioFile

def distanceBetweenTwoYears(prob_f, prob_g):
    print "start computing..."

    nTopic_a = prob_f.shape[0]
    nTopic_b = prob_g.shape[0]
    
    all_distance = []
    count = 0
    
    for i in range(0, nTopic_a):
        print "computing topic:", i
        distances = []
        for j in range(0, nTopic_b):
            clf_topic = hellingerDistance(exp(prob_f[i,:]), exp(prob_g[j,:]))
            if clf_topic < 0.5:
                count += 1
            distances.append(clf_topic)
        all_distance.append(distances)
    return all_distance, count

def klDivergence(p, q, base):
    return entropy(p, q, base)

def hellingerDistance(p, q):
    return norm(sqrt(p)-sqrt(q))/sqrt(2)
    
if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--finputFile',
                         dest='input_f',
                         help='fileName',
                         default=None)
    optparser.add_option('-g', '--ginputFile',
                         dest='input_g',
                         help='fileName',
                         default=None)
    optparser.add_option('-o', '--outputFile',
                         dest='output',
                         help='fileName',
                         default=None)
        
    (options, args) = optparser.parse_args()
    
    if options.input_f is None:
            fname_f = sys.stdin
    elif options.input_f is not None:
            fname_f = options.input_f
    else:
            print 'No filename(.pkl) specified, system with exit\n'
            sys.exit('System will exit')

    if options.input_g is None:
            fname_g = sys.stdin
    elif options.input_g is not None:
            fname_g = options.input_g
    else:
            print 'No filename(.pkl) specified, system with exit\n'
            sys.exit('System will exit')
            
    if options.output is None:
            outFile = 'distance.pkl'
    elif options.output is not None:
            outFile = options.output            
            

    
    prob_f = ioFile.load_object(fname_f)
    prob_g = ioFile.load_object(fname_g)
    
    all_distance, count = distanceBetweenTwoYears(prob_f, prob_g)
    
    print count, len(all_distance)
    
    ioFile.save_object(all_distance, outFile)
    