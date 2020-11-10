import copy
import Reader

class Transaction:
    
    def __init__(self, id):
        self.id = id

class Data:

    def __init__(self, label):
        self.label = label

class Process:

    def __init__(self, SLTransaction, action, SLData, lockManager):
        self.SLTransaction = SLTransaction
        self.action = action
        self.SLData = SLData 
        self.lockManager = lockManager
    
    def execute(self):
        success = True
        if (self.action == 'R'):
            success = self.SLTransaction.read(self.SLData)
        elif (self.action == 'W'):
            success = self.SLTransaction.write(self.SLData)
        else:
            success = self.SLTransaction.commit()

        if (not success):
            self.lockManager.pending.append(self)

class SLTransaction:

    def __init__(self, transaction, lockManager):
        self.transaction = transaction
        self.lockManager = lockManager
    
    def read(self, SLData):       
        print('pending ', end="")
        for q in self.lockManager.pending:
            print(f'{q.action}{q.SLTransaction.transaction.id}({SLData.data.label})', end=" ") 
        success = self.lockManager.exclusive_lock(self, SLData)
        if (success):
            print(f'R{self.transaction.id}({SLData.data.label})')
            return True
        else:
            print(f'R{self.transaction.id}({SLData.data.label}) pending ...')
            return False

    def write(self, SLData):
        print('pending ', end="")
        for q in self.lockManager.pending:
            print(f'{q.action}{q.SLTransaction.transaction.id}({SLData.data.label})', end=" ")
        success = self.lockManager.exclusive_lock(self, SLData)
        if (success):
            print(f'W{self.transaction.id}({SLData.data.label})')
            return True
        else:
            print(f'W{self.transaction.id}({SLData.data.label}) pending ...')
            return False

    def commit(self):


        success = True
        for process in self.lockManager.pending:
            if (process.SLTransaction.transaction.id == self.transaction.id):
                success = False
                break
        
        if (success):
            for index, data in enumerate(self.lockManager.all_data):
                if (data.granted_lock() == self.transaction.id):
                    # print(len(self.lockManager.all_data[index].lock))
                    data_pop = data.lock.pop(0)
                    # print(data_pop)
                    # print(len(self.lockManager.all_data[index].lock))
                    # print(self.lockManager.all_data[index].lock[0])
            print(f'C{self.transaction.id}')
            
            length = len(self.lockManager.pending)
            for i in range(length):
                process = self.lockManager.pending.pop(0) 
                process.execute()

            # for process in self.lockManager.pending:
            #     input()
            #     process.execute()
        else:
            print(f'C{self.transaction.id} pending ...')

        return success

class SLData:

    def __init__(self, data):
        self.data = data
        self.lock = []
    
    def granted_lock(self):
        return self.lock[0]

class LockManager:

    def __init__(self, all_data):
        self.all_data = all_data
        self.pending = []

    def exclusive_lock(self, transaction, data):
        print('exclusive lock', transaction.transaction.id)
        
        if ((len(data.lock) > 0) and (transaction.transaction.id == data.lock[0])):
            return True

        success = True
        for process in self.pending:
            if (process.SLTransaction.transaction.id == transaction.transaction.id):
                success = False
                break
        print('success 1', success)
        if (success):
            data.lock.append(transaction.transaction.id)
            if (transaction.transaction.id != data.lock[0]):
                success = False
        print('success 2', success)
        return success

if (__name__ == '__main__'):
    raw_T, raw_data, raw_process = Reader.generalSetup("soal_1.txt")
    SL_LockManager, SL_Data, SL_Transaction, SL_Process = Reader.SLock_Converter(raw_T, raw_data, raw_process)

    # lockManager = LockManager(sldata)
    # T1 = SLTransaction(Transaction(1), lockManager)
    # T2 = SLTransaction(Transaction(2), lockManager)
    # T3 = SLTransaction(Transaction(3), lockManager)

    # arrProcess = []
    # arrProcess.append(Process(T1, 'R', sldata[0], lockManager))
    # arrProcess.append(Process(T2, 'W', sldata[0], lockManager))
    # arrProcess.append(Process(T2, 'W', sldata[1], lockManager))
    # arrProcess.append(Process(T3, 'W', sldata[1], lockManager))
    # arrProcess.append(Process(T1, 'W', sldata[0], lockManager))
    # arrProcess.append(Process(T1, 'C', '', lockManager))
    # arrProcess.append(Process(T2, 'C', '', lockManager))
    # arrProcess.append(Process(T3, 'C', '', lockManager))


    for process in SL_Process:
        input()
        process.execute()
