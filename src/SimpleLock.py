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
        if (self.SLTransaction.transaction.id in self.lockManager.deadlocked_transactions):
            pass
        else:
            success = True
            if (self.action == 'R'):
                success = self.SLTransaction.read(self.SLData)
            elif (self.action == 'W'):
                success = self.SLTransaction.write(self.SLData)
            else:
                success = self.SLTransaction.commit()

            if (not success):
                self.lockManager.pending.append(self)
                if (not isinstance(self.SLData, str) and len(self.SLData.lock) > 0):
                    wait_id = self.SLTransaction.transaction.id
                    waitee_id = self.SLData.lock[0]
                    
                    deadlock = self.lockManager.detect_deadlock(wait_id, waitee_id)

                    if not deadlock:
                        self.lockManager.deadlock_detector[wait_id] = waitee_id
                    else:
                        self.lockManager.clear_lock(wait_id)
                        self.lockManager.deadlocked_transactions.append(wait_id)
                        length = len(self.lockManager.pending)
                        for i in range(length):
                            process = self.lockManager.pending.pop(0) 
                            process.execute()

class SLTransaction:

    def __init__(self, transaction, lockManager):
        self.transaction = transaction
        self.lockManager = lockManager
    
    def read(self, SLData):       
        
        # for q in self.lockManager.pending:
        #     print(f'{q.action}{q.SLTransaction.transaction.id}({SLData.data.label})', end=" ") 
        success = self.lockManager.exclusive_lock(self, SLData)
        if (success):
            print(f'R{self.transaction.id}({SLData.data.label})')
            return True
        else:
            print(f'R{self.transaction.id}({SLData.data.label}) pending ...')
            return False

    def write(self, SLData):
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
                if (len(data.lock) > 0 and data.granted_lock() == self.transaction.id):
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
        self.deadlock_detector = {}
        self.deadlocked_transactions = []

    def exclusive_lock(self, transaction, data):
        
        if ((len(data.lock) > 0) and (transaction.transaction.id == data.lock[0])):
            return True

        success = True
        for process in self.pending:
            if (process.SLTransaction.transaction.id == transaction.transaction.id):
                success = False
                break
        if (success):
            data.lock.append(transaction.transaction.id)
            if (transaction.transaction.id != data.lock[0]):
                success = False
        return success
    
    def detect_deadlock(self, wait_id, waitee_id):
        deadlock = False
        for key, value in self.deadlock_detector.items():
            if ((key == waitee_id) and (value == wait_id)):
                deadlock = True
                print('DEADLOCK')
                break

        return deadlock

    def clear_lock(self, transaction_id):
        for data in self.all_data:
            if transaction_id in data.lock:
                data.lock.remove(transaction_id)
        for key, value in self.deadlock_detector.items():
            if value == transaction_id:
                self.deadlock_detector.pop(transaction_id, None)

if __name__ == "__main__":
    T, data, process_string = Reader.generalSetup("soal_2.txt")
    arrProcess = Reader.SLock_Converter(T, data, process_string)

    for process in arrProcess:
        input()
        process.execute()

    if len(lockManager.deadlocked_transactions) > 0:
        print('Deadlocked Transactions:')
        for deadlock in lockManager.deadlocked_transactions:
            print(deadlock)    