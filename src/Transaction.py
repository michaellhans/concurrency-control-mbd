class Transaction:
    
    def __init__(self, id):
        self.id = id
        self.datalocked = []

    def read(self, data, database, isPending):
        availability = (database[data] == 0) or (database[data] == self.id)
        if (availability) and (not(isPending)):
            self.exclusive_lock(data, database)
            print(f'T{self.id} read {data}!')
            return True
        else:
            print(f'T{self.id} read {data} PENDING!')
            return False

    def write(self, data, database, isPending):
        availability = (database[data] == 0) or (database[data] == self.id)
        if (availability) and (not(isPending)):
            self.exclusive_lock(data, database)
            print(f'T{self.id} write {data}!')
            return True
        else:
            print(f'T{self.id} write {data} PENDING!')
            return False

    def commit(self, database, isPending):
        if not(isPending):
            print(f'T{self.id} commit!')
            for data in self.datalocked:
                self.unlock(data, database)
            return True
        else:
            print(f'T{self.id} commit PENDING!')
            return False

    def exclusive_lock(self, data, database):
        database[data] = self.id
        print(f'T{self.id} exclusive lock {data}!')
        self.datalocked.append(data)

    def unlock(self, data, database):
        database[data] = 0
        print(f'T{self.id} unlock {data}!')