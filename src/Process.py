class Process:
    
    def __init__(self, transaction, action, data):
        self.transaction = T
        self.action = action
        self.data = data

    def __str__(self):
        output = self.action + str(self.transaction.id) + self.data
        return output

    def execute(self):
        if (action == 'R'):
            self.transaction.read(self.data)
        elif (action == 'W'):
            self.transaction.write(self.data)
        elif (action == 'C'):
            self.transaction.commit()