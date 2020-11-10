from os import listdir

class Transaction:
    
    def __init__(self, id):
        self.id = id

class Data:

    def __init__(self, label):
        self.label = label

class Process:

    def __init__(self, transaction, action, data, lockManager):
        self.transaction = transaction
        self.action = action
        self.data = data
        self.lockManager = lockManager
    
    def execute(self):
        success = True
        if (self.action == 'R'):
            success = self.transaction.read(self.data)
        elif (self.action == 'W'):
            success = self.transaction.write(self.data)
        else:
            success = self.transaction.commit()
        
        if (not success):
            self.lockManager.pending.append(self)

class SLTransaction(Transaction):
    def __init__(self, id, lockManager):
        super().__init__(id)
        self.lockManager = lockManager
    
    def read(self, data):
        success = self.lockManager.exclusive_lock(self, data)
        if (success):
            print(f'R{self.id}({data.label})')
        else:
            print(f'R{self.id}({data.label}) pending ...')

        return success

    def write(self, data):
        success = self.lockManager.exclusive_lock(self, data)
        if (success):
            print(f'W{self.id}({data.label})')
        else:
            print(f'W{self.id}({data.label}) pending ...')

        return success

    def commit(self):

        success = True
        for process in self.lockManager.pending:
            if (process.transaction.id == self.id):
                success = False
                break
        
        if (success):
            for index, data in enumerate(self.lockManager.all_data):
                if (data.isGranted_lock(self.id)):
                    data_pop = data.lock.pop(0)
            print(f'C{self.id}')

            for i in range(len(self.lockManager.pending)):
                process = self.lockManager.pending.pop(0)
                process.execute()
        else:
            print(f'C{self.id} pending ...')

        return success

class SLData(Data):

    def __init__(self, label):
        super().__init__(label)
        self.lock = []
    
    def isGranted_lock(self, Tid):
        if (self.Twaiting_count() == 0):
            return False
        else:
            return self.lock[0] == Tid 
    
    def Twaiting_count(self):
        return len(self.lock)

class LockManager:

    def __init__(self, all_data):
        self.all_data = all_data
        self.pending = []

    def exclusive_lock(self, transaction, data):
        if ((data.Twaiting_count() > 0) and (data.isGranted_lock(transaction.id))):
            return True

        success = True
        for process in self.pending:
            if (process.transaction.id == transaction.id):
                success = False
                break
        if (success):
            data.lock.append(transaction.id)
            if (not data.isGranted_lock(transaction.id)):
                success = False
        return success 

class Schedule:
    def __init__(self, filename, transactions):
        self.processes = self.convertString(filename, transactions)

    def convertString(self, filename, transactions):
        with open('test/' + filename, 'r') as f:
            strings = f.read()
            for s in strings.split(' '):
                s = s.replace('(', '')
                s = s.replace(')', '')
                if (len(s) == 2):
                    q.append(Process)
        return 'S'

# print(listdir('test'))
schedule = Schedule('test1.txt')




# sldata = [
#     SLData('X'),
#     SLData('Y'),
# ]
# lockManager = LockManager(sldata)
# T1 = SLTransaction(1, lockManager)
# T2 = SLTransaction(2, lockManager)
# T3 = SLTransaction(3, lockManager)

# arrProcess = []
# arrProcess.append(Process(T1, 'R', sldata[0], lockManager))
# arrProcess.append(Process(T2, 'W', sldata[0], lockManager))
# arrProcess.append(Process(T2, 'W', sldata[1], lockManager))
# arrProcess.append(Process(T3, 'W', sldata[1], lockManager))
# arrProcess.append(Process(T1, 'W', sldata[0], lockManager))
# arrProcess.append(Process(T1, 'C', '', lockManager))
# arrProcess.append(Process(T2, 'C', '', lockManager))
# arrProcess.append(Process(T3, 'C', '', lockManager))


# for process in arrProcess:
#     process.execute()