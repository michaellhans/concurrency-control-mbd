import Transaction
import Process
import Rollback
import copy

def IsAlreadyPending(id, queue):
    for process in queue:
        if (id == process.transaction.id):
            return True
    return False

# Transaction
T1 = Transaction.Transaction(1)
T2 = Transaction.Transaction(2)
T3 = Transaction.Transaction(3)

# Data
database = {}
database.update({'X' : 0})
database.update({'Y' : 0})

# All Process
arrProcess = []
arrProcess.append(Process.Process(T1, 'R', 'X'))
arrProcess.append(Process.Process(T2, 'W', 'X'))
arrProcess.append(Process.Process(T2, 'W', 'Y'))
arrProcess.append(Process.Process(T3, 'W', 'Y'))
arrProcess.append(Process.Process(T1, 'W', 'X'))
arrProcess.append(Process.Process(T1, 'C', ''))
arrProcess.append(Process.Process(T2, 'C', ''))
arrProcess.append(Process.Process(T3, 'C', ''))

lengthArrProcess = len(arrProcess)
executePending = False
previousTransaction = 0

while (lengthArrProcess > 0):
    process = arrProcess.pop(0)
    result = process.execute(database)


print("SELESAI!")
