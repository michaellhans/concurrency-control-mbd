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

# Backup Schedule
originalProcess = copy.deepcopy(arrProcess)

# Queue of Pending Process
pendingProcess = []

# Main Program
lengthPending = len(pendingProcess)
lengthArrProcess = len(arrProcess)
executePending = False
previousTransaction = 0

while ((lengthPending > 0) or (lengthArrProcess > 0)):
    # Get the process
    if (lengthPending == 0):
        executePending = False
    if (executePending):
        process = pendingProcess.pop(0)
    elif (lengthArrProcess > 0):
        process = arrProcess[0]
    elif (lengthPending > 0):
        process = pendingProcess.pop(0)
    
    # Execute the process
    isPending = IsAlreadyPending(process.transaction.id, pendingProcess)
    
    if ((previousTransaction != process.transaction.id) and (isPending)):
        print("hello")
        previousTransaction = process.transaction.id
        executePending = True
        continue
    if (previousTransaction != process.transaction.id) and (executePending):
        print("hello2")
        previousTransaction = process.transaction.id
        executePending = False
        continue
    else:
        if (executePending):
            isPending = False
        res = process.execute(database, isPending)
        previousTransaction = process.transaction.id
        # If the process is waiting, add to pending list
        if not(res):
            pendingProcess.append(process)
        if not(executePending):
            dump = arrProcess.pop(0)

    # Update length of pending and arrProcess
    lengthPending = len(pendingProcess)
    lengthArrProcess = len(arrProcess)
    input()

print("SELESAI!")


