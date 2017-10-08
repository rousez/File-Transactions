class Transaction(object):
    
    def __init__(self,id,items):
        self.id = id
        self.items = items

    def get_id(self):
    	return self.id    

    def get_items(self):
        return self.items