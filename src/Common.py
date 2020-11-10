class Transaction:

    def __init__(self, id):
        self.id = id

    def __str__(self):
        return 'T' + str(self.id)
    
    def __eq__(self, transaction):
        return (self.id == transaction.id)
            

class Process:

    def __init__ (self, transaction=None, action=None, data=None, process=None):
        if (process):
            self.transaction = process.transaction
            self.action = process.action
            self.data = process.data
        else:
            self.transaction = transaction
            self.action = action
            self.data = data
    
    def __str__(self):
        data = f'({self.data})' if (self.action == 'R' or self.action == 'W') else ""
        return f'{self.action}{self.transaction.id}{data}'