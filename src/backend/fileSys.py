from os import walk, path

def traverseDirectory(dirpath, years=None):
    for (dirpath, dirnames, filenames) in walk(dirpath):
        filenames = sorted(filenames)
        break
    full_fnames = []
    for fname in filenames:
        fname = path.join(dirpath, fname)
        if years is not None:
            year = int(fname[-8:-4])
        if path.isfile(fname):
            if years is None or year in years:
                full_fnames.append(fname)          
            
    return full_fnames

'''
fun=0, bottom level topics; fun=1, top level topics 
'''
def traverseTopicDirecotry(dirpath, fun, years=None):
    for (dirpath, dirnames, filenames) in walk(dirpath):
        dirnames = sorted(dirnames)
        break
    full_fnames = []
    for dirname in dirnames:
        year = int(dirname)
        if years is None or year in years:
            filenames = traverseDirectory(path.join(dirpath, dirname, 'topic'))
            if fun == 0:
                full_fnames.append(filenames[0])
            elif fun == 1:
                full_fnames.append(filenames[-1])                       
            
    return full_fnames    