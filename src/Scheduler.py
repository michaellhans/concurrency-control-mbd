import Process

class Scheduler:

    def __init__(self, stringInput):
        self.arrProcess = []
        self.arrTransaction = []
        self.convertString(stringInput)

    def convertString(self, stringInput):
        temp = stringInput.replace(';', '')
        arrString = temp.split(' ')
        for string in arrString:
            process = Process.Process()