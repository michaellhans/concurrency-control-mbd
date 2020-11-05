# Multiversion Timestamp Ordering Concurrency Control (MVCC)

class Transaction:
    
    def __init__(self, id):
        self.id = id
    
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
                newVersion = Data(data.label, version = transaction.id, readTS = transaction.id, writeTS = transaction.id)
                version_list.append(newVersion)
                return True
        return False

class Data:
    
    def __init__(self, label, version = 0, readTS = 0, writeTS = 0):
        self.label = label
        self.version = version
        self.readTS = readTS
        self.writeTS = writeTS
    
    def __str__(self):
        result = f'TS({self.label}{self.version}) = ({self.readTS}, {self.writeTS})'
        return result

class Process:
    
    def __init__(self, transaction, action, data, dataMap):
        self.transaction = transaction
        self.action = action
        self.data = data
        self.dataMap = dataMap 
    
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


if (__name__ == '__main__'):
    arrData = [Data('W'), Data('X'), Data('Y'), Data('Z')]
    dataContainer = DataMap(arrData)

    T1 = Transaction(1)
    T2 = Transaction(2)
    T3 = Transaction(3)
    T4 = Transaction(4)
    T5 = Transaction(5)

    noData = Data('')

    # Test Case 1: Pembahasan Soal Ibu Cia
    arrProcess = [
        Process(T5, 'R', arrData[1], dataContainer),
        Process(T2, 'R', arrData[2], dataContainer),
        Process(T1, 'R', arrData[2], dataContainer),
        Process(T3, 'W', arrData[2], dataContainer),
        Process(T3, 'W', arrData[3], dataContainer),
        Process(T5, 'R', arrData[3], dataContainer),
        Process(T2, 'R', arrData[3], dataContainer),
        Process(T1, 'R', arrData[1], dataContainer),
        Process(T4, 'R', arrData[0], dataContainer),
        Process(T3, 'W', arrData[0], dataContainer),
        Process(T5, 'W', arrData[2], dataContainer),
        Process(T5, 'W', arrData[3], dataContainer)
    ]
    
    # Test Case 2: Soal Latihan Concurrency Control
    # arrProcess = [
    #     Process(T1, 'R', arrData[1], dataContainer),
    #     Process(T2, 'W', arrData[1], dataContainer),
    #     Process(T2, 'W', arrData[2], dataContainer),
    #     Process(T3, 'W', arrData[2], dataContainer),
    #     Process(T1, 'W', arrData[2], dataContainer),
    #     Process(T1, 'C', noData, dataContainer),
    #     Process(T2, 'C', noData, dataContainer),
    #     Process(T3, 'C', noData, dataContainer),
    # ]

    print("Multiversion Timestamp Ordering Concurrency Protocol dimulai?")
    print("Initial State")
    dataContainer.get_all_version()
    input()

    for process in arrProcess:
        process.execute()
        dataContainer.get_all_version()
        input()