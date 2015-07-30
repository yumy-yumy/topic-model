import csv
import pickle
import json

'''
Output
'''
def dataToFile(item, fname):
    """Function which writes each line to the file"""
    with open(fname, 'a') as fileWriter:
            fileWriter.write(item)
            
def abstractsToFile(all_abstract, fname):
    """Writes abstract to the txt file"""
    with open(fname, 'w') as fileWriter:
        for abstract in all_abstract:
            fileWriter.write(abstract)
    
def statToFile(item, fname):
    """Write year and number of docuemnts to the csv file"""
    with open(fname, 'a') as csvfile:
        fileWriter = csv.writer(csvfile, delimiter=',')
        fileWriter.writerow(item)
        
def statsToFile(item, fname):
    """Function which writes each line to the csv file"""
    with open(fname, 'w') as csvfile:
        fieldnames = ['year', 'num']
        fileWriter = csv.writer(csvfile, delimiter=',')
        fileWriter.writerow(fieldnames)
        for key, value in item.iteritems():
            fileWriter.writerow((key, value))
                    
def statSeqToFile(seq, fname):
    '''Write a sequnence of numbers of documents'''
    with open(fname, 'w') as fileWriter:
        fileWriter.write(str(len(seq)) + '\n')
        for num in seq:
            fileWriter.write(str(num) + '\n')
        
def termCountToFile(count, fname):
    '''Write data with format [M] [term|index]:[count]'''
    with open(fname, 'a') as fileWriter:
        N = len(count)
        fileWriter.write(str(N) + ' ')
        for key, value in count.iteritems():
            fileWriter.write(str(key) + ':' + str(value) + ' ')
        fileWriter.write('\n')

def termToFile(all_term, fname):
    '''Write all terms to a file'''
    with open(fname, 'w') as fileWriter:
        for term in all_term:
            fileWriter.write(term + ' ')

'''
Input
'''
def dataFromFile(fname):
    '''Read file and generate a iterator'''
    file_iter = open(fname, 'rU')
    for line in file_iter:
            yield line
            
def statFromFile(fname):
    '''Read the number of documents each year'''
    with open(fname, 'rU') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',')
        for line in fileReader:
            yield line
            
'''
pickle
'''
def save_object(obj, fname):
    print "save object to", fname
    with open(fname, 'wb') as fileWriter:
        pickle.dump(obj, fileWriter, pickle.HIGHEST_PROTOCOL)
        
def load_object(fname): #EXAMPLE CODE HOW TO LOAD THE FILES (PICKLES)
    with open(fname, 'rb') as fileReader:
        return pickle.load(fileReader)

'''
json
'''
def save_json(obj, filename):
    print "save object to", filename
    with open(filename, 'wb') as fileWriter:
        json.dump(obj, fileWriter)
        
def load_json(filename):
    print "load object from", filename
    with open(filename, 'rb') as fileReader:
        return json.load(fileReader)        