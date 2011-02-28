import os.path

def getPath(type):
    path = []
    tmp = type
    while tmp.parent is not None:
        path.insert(0, tmp)
        tmp = tmp.parent
    
    if type.typeName == 'Namespace':
        return os.path.join(* ['.'] + [part.identifier.lowerCamelCase for part in path])
    else:
        return os.path.join(* ['.'] + [part.identifier.lowerCamelCase for part in path]) + '.py'
