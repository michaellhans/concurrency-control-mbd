import Reader

class Transaction:

    def __init__(self, id, startTs, finishTs):
        self.id = id
        self.startTs = startTs
        self.finish = finishTs

    def read(self, data):
        pass

    def write(self, data):
        pass

    def commit(self):
        pass

class Data:

    def __init__(self, label):
        self.label = label


class Process:

    def __init__(self, transaction, action, data):
        self.transaction = transaction
        self.action = action
        self.data = data
    
    def execute(self):
        pass

