from Common import *
import Reader

class OCCTransaction(Transaction):

    def __init__(self, transaction):
        super().__init__(transaction.id)
        self.writeSet = []
        self.readSet = []
        self.startTs = float('inf')

    def write(self, i, data):
        if (self.startTs == float('inf')):
            self.startTs = i
        if (data not in self.writeSet):
            self.writeSet.append(data)
        return True

    def read(self, i, data):
        if (self.startTs == float('inf')):
            self.startTs = i
        if (data not in self.readSet):
            self.readSet.append(data)
        return True
    
    def commit(self, i, arrTransaction):
        success = True
        for T in arrTransaction:
            if (T.startTs >= self.startTs) or not T.is_running():
                continue
            
            if (not set(T.writeSet).isdisjoint(self.readSet)):
                success = False
                break
        
        self.writeSet = []
        self.readSet = []
        self.startTs = float('inf')
            
        return success

    def is_running(self):
        return self.startTs != float('inf')
    
    def printWriteReadSet(self):
        print(f"readSet(T{self.id}): [", end="")
        for i, x in enumerate(self.readSet):
            if (i == len(self.readSet)-1):
                print(x, end="")
            else:
                print(x, end=",")
        print("]")
        print(f"writeSet(T{self.id}): [", end="")
        for i, x in enumerate(self.writeSet):
            if (i == len(self.writeSet)-1):
                print(x, end="")
            else:
                print(x, end=",")
        print("]")
            

class OCCProcess(Process):

    def __init__(self, process):
        super().__init__(process = process)
    
    def execute(self, i, arrTransaction):
        success = True
        if (self.action == 'R'):
            success = self.transaction.read(i, self.data)
        elif (self.action == 'W'):
            success = self.transaction.write(i, self.data)
        else:
            success = self.transaction.commit(i, arrTransaction)
        return success


def execute_OCC(fileName):
    arrTransaction, arrProcess, raw_data = Reader.generalSetup(fileName)
    arrTransaction, arrProcess = Reader.OCC_Converter(arrTransaction, arrProcess, raw_data)

    for i, p in enumerate(arrProcess, start=1):
        success = p.execute(i, arrTransaction)
        print(p)
        for T in arrTransaction:
            T.printWriteReadSet()
        if (not(success)):
            print(f'{p}: T{self.transaction.id} is aborted')

        print()
        input()
