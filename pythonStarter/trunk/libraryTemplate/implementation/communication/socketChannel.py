import socket

class SocketChannel(object):
    def __init__(self, port):
        self.__sock = socket.socket()
        self.__sock.connect(('localhost', port))
        self.__sockFile = self.__sock.makefile()
        
        self.__closed = False
    
    def write_line(self, data = ''):
        if self.__closed:
            raise ValueError("I/O operation on closed file")
        
        self.__sockFile.write(data + '\r\n')
        self.__sockFile.flush()
    
    def read_line(self):
        if self.__closed:
            raise ValueError("I/O operation on closed file")
        
        ret = self.__sockFile.readline()
        if ret:
            return ret.rstrip('\r\n')
        
        self.__closed = True
    
    def close(self):
        self.__sockFile.close()
        self.__closed = True
