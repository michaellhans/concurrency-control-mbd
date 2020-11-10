from Multiversion import *
from SimpleLock import *
import re

# General setup for transactions and data
def generalSetup(fileName):
    file = open("../test/" + fileName, "r")
    buff = file.read()
    arrString = buff.split('\n')

    # Setup all transaction for Concurrency Control
    arrTransaction = []
    num_of_transaction = int(arrString.pop(0))
    for i in range(num_of_transaction):
        arrTransaction.append(Transaction(i+1))

    # Setup all needed data for Concurrency Control
    arrData = []
    raw_data = arrString.pop(0).split(' ')
    return arrTransaction, raw_data, arrString

# Simple Locking (Exclusive Lock Only) Concurrency Control Converter
def SLock_Converter(raw_transaction, raw_data, raw_string):
    SL_Data = []
    for item in raw_data:
        SL_Data.append(SLData(Data(item)))
    SL_LockManager = LockManager(SL_Data)
    
    SL_Transaction = []
    for transaction in raw_transaction:
        SL_Transaction.append(SLTransaction(transaction, SL_LockManager))

    SL_Process = []
    for string in raw_string:
        transaction_id = int(re.findall('[0-9]+', string)[0])
        action = string[0]
        raw_data = string.split('(')[1]
        dataLabel = raw_data[0: len(raw_data)-1]
        newProcess = Process(SL_Transaction[transaction_id - 1], action, SLData(Data(dataLabel)), SL_LockManager)
        SL_Process.append(newProcess)
    
    return SL_LockManager, SL_Data, SL_Transaction, SL_Process

# Serial Optimistic Concurrency Control Converter
def OCC_Converter(raw_transaction, raw_data, raw_string):
    pass

# Multiversion Timestamp Ordering Concurrency Control Converter
def MVCC_Converter(raw_transaction, raw_data, raw_string):
    MVCC_Transaction = []
    for transaction in raw_transaction:
        MVCC_Transaction.append(MVTransaction(transaction.id))
    
    MVCC_Data = []
    for data in raw_data:
        MVCC_Data.append(MVData(data))
    MVCC_DataMap = DataMap(MVCC_Data)

    MVCC_Process = []
    for string in raw_string:
        transaction_id = int(re.findall('[0-9]+', string)[0])
        action = string[0]
        raw_data = string.split('(')[1]
        dataLabel = raw_data[0: len(raw_data)-1]
        newProcess = MVProcess(MVCC_Transaction[transaction_id - 1], action, MVData(dataLabel), MVCC_DataMap)
        MVCC_Process.append(newProcess)
    
    return MVCC_DataMap, MVCC_Data, MVCC_Transaction, MVCC_Process