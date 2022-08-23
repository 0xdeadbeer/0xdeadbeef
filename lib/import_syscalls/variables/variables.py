
class ENVIRONMENT: 
    def __init__(self, location, file_descriptor=None):
        self.location = location 
        self.descriptor = None

        if (file_descriptor is None): 
            self.descriptor = open(self.location, "r")
        else:
            self.descriptor = file_descriptor

        self.connections = { }

    def add_connection(self, environment):
        if (environment in self.connections): 
            return False 

        self.connections[environment] = True 
        return True 
