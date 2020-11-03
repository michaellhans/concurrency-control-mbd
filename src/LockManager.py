import Transaction
import Process
import Rollback
import TableNode

class LockManager:

    def __init__(self, all_data):
        self.table = {}
        self.initLockingTable(all_data)

    def initLockingTable(self, all_data):
        # Initiate all hash index for all data
        for data in all_data:
            self.table.update({data : []})
    
    def isAvailable(self, data, t_id):
        linked_list = self.table[data]
        if (len(linked_list) == 0):
            return True
        else:
            return False

    def requestLock(self, data, t_id):
        # Add new lock request from t_id
        linked_list = self.table[data]
        linked_list.append(TableNode.TableNode(t_id))

    def grantedLock(self, data, t_id):
        # Granted lock for t_id request on data
        linked_list = self.table[data]
        for node in linked_list:
            if (node.transaction_id == t_id):
                node.status = True

    def unlock(self, data):
        linked_list = self.table[data]
        dump = self.table[data].pop(0)
        return True


if __name__ == '__main__':
    # Transaction
    T1 = Transaction.Transaction(1)
    T2 = Transaction.Transaction(2)
    T3 = Transaction.Transaction(3)

    # Data
    database = ['X', 'Y']

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

    LM = LockManager(database)
    print(LM.table)