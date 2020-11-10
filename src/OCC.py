from Common import *
import Reader

class OCCTransaction(Transaction):

    def __init__(self, transaction, writeSet, readSet, startTs=0, validationTs=0, finishTs=0):
        super().__init__(transaction.id)
        self.writeSet = writeSet
        self.readSet = readSet
        self.startTs = startTs
        self.validationTs = validationTs
        self.finishTs = finishTs

    def __str__(self):
        return (f'T{self.id}' + f'\nstart {self.startTs}' + f'\nvalidation {self.validationTs}' + f'\nfinish {self.finishTs}')

def execute_OCC(fileName):
    arrTransaction, arrProcess, raw_data = Reader.generalSetup(fileName)
    arrTransaction, arrProcess = Reader.OCC_Converter(arrTransaction, arrProcess, raw_data)

    for i in range(len(arrTransaction)):
        T = arrTransaction[i]

        print(f'T{T.id}\n')        
        Tvalid = True
        for j in range(i):
            Tc = arrTransaction[j]
            print(f'T{T.id} -> T{Tc.id}')
            rule1 = (Tc.finishTs < T.startTs)
            rule2 = ((T.startTs < Tc.finishTs < T.finishTs) and set(Tc.writeSet).isdisjoint(T.readSet))
            Tvalid = rule1 or rule2

            print(f'finishTs(T{Tc.id}) < startTs(T{T.id}):', rule1)
            print(f'startTs(T{T.id}) < finishTs(T{Tc.id}) < validationTs(T{T.id}):', rule2)

            if not Tvalid:
                break
            
            print()

        if (Tvalid):
            print(f'T{T.id} success')
        else:
            print(f'T{T.id} failed')
            print('abort')
        
        print('\n--------------------------------------------------------\n')
