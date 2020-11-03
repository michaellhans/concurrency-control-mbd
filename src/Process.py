class Process:
    
    def __init__(self, transaction, action, data):
        self.transaction = transaction
        self.action = action
        self.data = data

    def __str__(self):
        output = self.action + str(self.transaction.id) + '(' + self.data + ')'
        return output

    def execute(self, database, isPending):
        if (self.action == 'R'):
            return self.transaction.read(self.data, database, isPending)
        elif (self.action == 'W'):
            return self.transaction.write(self.data, database, isPending)
        elif (self.action == 'C'):
            return self.transaction.commit(database, isPending)