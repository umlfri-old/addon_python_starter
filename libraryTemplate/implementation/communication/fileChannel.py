class FileChannel(object):
    def __init__(self, input, output):
        self.__input = input
        self.__output = output
        
        self.__closed = False
    
    def write_line(self, data = ''):
        if self.__closed:
            raise ValueError("I/O operation on closed file")
        
        self.__output.write(data + '\r\n')
        self.__output.flush()
    
    def read_line(self):
        if self.__closed:
            raise ValueError("I/O operation on closed file")
        
        ret = self.__input.readline()
        if ret:
            return ret.rstrip('\r\n')
        
        self.__closed = True
    
    def close(self):
        self.__input.close()
        self.__output.close()
