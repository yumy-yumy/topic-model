from os import walk, path

def traverseDirectory(dirpath, arg=None):
    for (dirpath, dirnames, filenames) in walk(dirpath):
        filenames = sorted(filenames)
        break
    full_fnames = []
    for fname in filenames:
        fname = path.join(dirpath, fname)
        if arg is not None:
            year = int(fname[-8:-4])
        if path.isfile(fname):
            if arg == None or year >= arg[0] and year <= arg[1]:
                full_fnames.append(fname)          
            
    return full_fnames

'''
fun=0, bottom level topics; fun=1, top level topics 
'''
def traverseTopicDirecotry(dirpath, fun, arg=None):
    for (dirpath, dirnames, filenames) in walk(dirpath):
        dirnames = sorted(dirnames)
        break
    full_fnames = []
    for dirname in dirnames:
        if arg == None or int(dirname) >= arg[0] and int(dirname) <= arg[1]:
            filenames = traverseDirectory(path.join(dirpath, dirname, 'topic'))
            if fun == 0:
                full_fnames.append(filenames[0])
            elif fun == 1:
                full_fnames.append(filenames[-1])                       
            
    return full_fnames    