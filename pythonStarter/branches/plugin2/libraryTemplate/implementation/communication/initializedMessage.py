class InitializedMessage(object):
    def create_message(self):
        return 'plugin', 'initialized', (), {}
    
    def send(self, server):
        server.send_command(self, async = True)
