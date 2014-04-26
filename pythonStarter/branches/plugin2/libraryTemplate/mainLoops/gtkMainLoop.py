class GtkMainLoop(object):
    def __init__(self):
        import gobject
        import gtk
        
        self.__gtk  = gtk
        self.__gobject = gobject
        
        self.__gobject.threads_init()
        
        self.__running = False
            
    @property
    def in_main_loop(self):
        return self.__running
    
    def main_loop(self):
        self.__running = True
        self.__gtk.main()
        self.__running = False
    
    def call(self, callable, *args):
        self.__gobject.idle_add(callable, *args)
    
    def quit(self):
        self.__gtk.main_quit()
