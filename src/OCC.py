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

class OCCData:

    def __init__(self, label):
        self.label = label

def execute_OCC(fileName):
    arrTransaction, arrProcess, raw_data = Reader.generalSetup(fileName)
    arrTransaction, arrProcess = Reader.OCC_Converter(arrTransaction, arrProcess, raw_data)

    for i in range(len(arrTransaction)-1, -1, -1):
        T = arrTransaction[i]
        Tvalid = True

        for j in range(i):
            Tc = arrTransaction[j]
            if not (Tc.finishTs < T.startTs):
                Tvalid = False
            if not Tvalid and ((T.startTs < Tc.finishTs < T.finishTs) and set(Tc.writeSet).isdisjoint(T.readSet)):
                Tvalid = True
            
            if (not Tvalid):
                break

        if (Tvalid):
            print(f'T{T.id} success')
        else:
            print(f'T{T.id} failed')

if (__name__ == '__main__'):
    execute_OCC("soal_4.txt")