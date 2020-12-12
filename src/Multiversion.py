# Multiversion Timestamp Ordering Concurrency Control (MVCC)
from Common import *
import Reader
import copy

class MVCTransaction(Transaction):
    
    def __init__(self, transaction):
        super().__init__(transaction.id)
        self.arrProcess = []

    def read(self, data, dataMap):
        return dataMap.read_issue(data, self)

    def write(self, data, dataMap):
        return dataMap.write_issue(data, self)

    def commit(self):
        return True

class DataMap:

    def __init__(self, arrData):
        self.container = {}
        for data in arrData:
            self.container.update({data.label : [data]})

    def add_new_version(self, data):
        version_list = self.container[data.label]
        version_list.append(data)

    def get_all_version(self):
        for key in self.container:
            # print(f'========== [{key}] ==========')
            for data in self.container[key]:
                print(data)

    def read_issue(self, data, transaction):
        version_list = self.container[data.label]
        for data_version in reversed(version_list):
            if (data_version.readTS < transaction.id):
                data_version.readTS = transaction.id
                break
        return True
    
    def write_issue(self, data, transaction):
        version_list = self.container[data.label]
        for data_version in reversed(version_list):
            if (transaction.id < data_version.readTS):
                continue
            elif (transaction.id == data_version.writeTS):
                print(f'Overwrite value of {data_version}')
                return True
            else:
                newVersion = MVCData(data.label, version = transaction.id, readTS = transaction.id, writeTS = transaction.id)
                version_list.append(newVersion)
                return True
        return False

class MVCData:
    
    def __init__(self, label, version = 0, readTS = 0, writeTS = 0):
        self.label = label
        self.version = version
        self.readTS = readTS
        self.writeTS = writeTS
    
    def __str__(self):
        result = f'TS({self.label}{self.version}) = ({self.readTS}, {self.writeTS})'
        return result

class MVCProcess(Process):
    
    def __init__(self, process, dataMap):
        super().__init__(process = process)
        self.dataMap = dataMap
        self.transaction = MVCTransaction(self.transaction)
        self.data = MVCData(self.data)

    def __str__(self):
        output = f'{self.action}{self.transaction.id}({self.data.label})'
        return output

    def execute(self):
        success = True
        print(self)
        if (self.action == 'R'):
            success = self.transaction.read(self.data, self.dataMap)
        elif (self.action == 'W'):
            success = self.transaction.write(self.data, self.dataMap)
        else:
            success = self.transaction.commit()
        
        if (not(success)):
            print(f'Abort T{self.transaction.id}')

        return success

def execute_MV(fileName):
    T, arrProcess, raw_data = Reader.generalSetup(fileName)
    txn, dataContainer, arrProcess = Reader.MVCC_Converter(T, arrProcess, raw_data)
    txn_request = []
    
    print("Multiversion Timestamp Ordering Concurrency Protocol dimulai?")
    print("Initial State")
    dataContainer.get_all_version()
    input()

    t = 0
    for process in arrProcess:
        if (process.transaction in txn_request):
            print(f'{process}: {process.transaction} is aborted\n')
            continue
        else:
            success = process.execute()
            if (not(success)):
                txn_request.append(process.transaction)

            dataContainer.get_all_version()
            input()
        t += 1
    
    arrPending = []
    arrNew = []
    for temp in txn_request:
        arrPending.append(txn[2]);

    print("Execute pending request")
    while (len(arrPending) > 0):
        for txn in arrPending:
            txn.id = t
            t += 1
            print(len(txn.arrProcess))
            for process in txn.arrProcess:
                process.transaction = txn
                print(process)
                if (process.transaction in arrNew):
                    print(f'{process}: {process.transaction} is aborted\n')
                    continue
                else:
                    success = process.execute()
                    if (not(success)):
                        arrNew.append(process.transaction)
                        break
                    dataContainer.get_all_version()
                    input()
                t += 1

            pops = arrPending.pop()

            if (len(arrNew) > 0):
                arrPending = copy.deepcopy(arrNew)
                arrNew = []
