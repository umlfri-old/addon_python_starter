class MIMChannel(object):
    def __init__(self, channel):
        self.__channel = channel
    
    def write_line(self, data = ''):
        print 'S:', data
        self.__channel.write_line(data)
    
    def read_line(self):
        ret = self.__channel.read_line()
        print 'R:', ret
        return ret
    
    def close(self):
        self.__channel.close()
