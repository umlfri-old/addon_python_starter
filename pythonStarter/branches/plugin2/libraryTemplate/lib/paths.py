import os.path

def getPath(type):
    path = []
    tmp = type
    while tmp.parent is not None:
        path.insert(0, tmp)
        tmp = tmp.parent
    
    if type.typeName == 'Namespace':
        path = [part.identifier.lowerCamelCase for part in path] + ['__init__.py']
    else:
        path = [part.identifier.lowerCamelCase for part in path[:-1]] + [path[-1].identifier.lowerCamelCase + '.py']
    
    return os.path.join(* ['.'] + path)

def nameToString(type):
    if type.typeName == 'Namespace':
        return type.identifier.lowerCamelCase
    else:
        return type.identifier.upperCamelCase

def getFQN(type):
    path = []
    tmp = type
    while tmp.parent is not None:
        path.insert(0, tmp)
        tmp = tmp.parent
    
    return '.'.join(nameToString(part) for part in path)

def getImportPath(type, relativeTo = None):
    relativity = []
    
    if relativeTo is None:
        path = []
        tmp = type
        while tmp.parent is not None:
            path.insert(0, tmp)
            tmp = tmp.parent
    else:
        tmp2 = relativeTo
        while tmp2.parent is not None:
            relativity.append('.')
            
            path = []
            tmp = type
            while tmp.parent is not None:
                path.insert(0, tmp)
                
                if tmp.parent is tmp2.parent:
                    break
                
                tmp = tmp.parent
            else:
                tmp2 = tmp2.parent
                continue
            
            break
    
    return ''.join(relativity) + '.'.join(part.identifier.lowerCamelCase for part in path)
