import Process
import re

class Scheduler:

    def __init__(self, fileName):
        self.arrProcess = []
        self.arrTransaction = []
        self.convertString(fileName)

    def convertString(self, fileName):
        file = open("../test/" + fileName, "r")
        buff = file.read()
        arrString = buff.split('\n')
        for string in arrString:
            print(string)
            actionID = string[0]
            transactionID = re.findall('[0-9]+', string)[0]
            data = string.split('(')[1]
            print(actionID)
            print(transactionID)
            print(data[0])
            # process = Process.Process()

if __name__ == "__main__":
    S = Scheduler("test1.txt")
