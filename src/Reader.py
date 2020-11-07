import Common
from Multiversion import *
import SimpleLock as SL
import re

# General setup for transactions and data
def generalSetup(fileName):
    file = open("test/" + fileName, "r")
    buff = file.read()
    arrString = buff.split('\n')

    # Setup all transaction for Concurrency Control
    arrTransaction = []
    num_of_transaction = int(arrString.pop(0))
    for i in range(num_of_transaction):
        arrTransaction.append(Common.Transaction(i+1))
        print("transaction id", arrTransaction[-1].id)

    # Setup all needed data for Concurrency Control
    raw_data = arrString.pop(0).split(' ')

    # Setup process
    arrProcess = []
    for s in arrString:
        s = s.replace('(', '')
        s = s.replace(')', '')
        arrProcess.append(
            Common.Process(
                arrTransaction[int(s[1])-1],
                s[0],
                s[2]
            )
        )

    return arrTransaction, arrProcess, raw_data

# Simple Locking (Exclusive Lock Only) Concurrency Control Converter
def SLock_Converter(arrTransaction, arrData, arrString):
    SL_DataContainer = []
    arrDataLabel = []
    for data in arrData:
        data_label = data.label
        arrDataLabel.append(data_label)
        SL_DataContainer.append(SL.SLData(SL.Data(data_label)))
    SL_LockManager = SL.LockManager(SL_DataContainer)
    
    arrSLTransaction = []
    for transaction in arrTransaction:
        arrSLTransaction.append(SL.SLTransaction(transaction, SL_LockManager))

    arrProcess = []
    for string in arrString:
        transaction_id = int(re.findall('[0-9]+', string)[0])
        action = string[0]
        raw_data = string.split('(')[1]
        dataLabel = raw_data[0: len(raw_data)-1]
        if dataLabel != '':
            arrProcess.append(SL.Process(arrSLTransaction[transaction_id - 1], action, SL_DataContainer[arrDataLabel.index(dataLabel)], SL_LockManager))
        else:
            arrProcess.append(SL.Process(arrSLTransaction[transaction_id - 1], action, '', SL_LockManager))

    return arrProcess

    

# Serial Optimistic Concurrency Control Converter
def OCC_Converter(num_of_transaction, raw_data, arrString):
    pass

# Multiversion Timestamp Ordering Concurrency Control Converter
def MVCC_Converter(arrTransaction, arrProcess, raw_data):

    arrData = []
    MVCC_Process = []

    for data in raw_data:
        arrData.append(MVCData(data))
    print(arrData[0].label)

    MVCC_DataMap = DataMap(arrData)
    for p in arrProcess:
        MVCC_Process.append(MVCProcess(p, MVCC_DataMap))
    
    return MVCC_DataMap, MVCC_Process