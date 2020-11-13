import Common
import Multiversion as MV
from OCC import *
import SimpleLock as SL
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
        arrTransaction.append(Common.Transaction(i+1))

    # Setup all needed data for Concurrency Control
    raw_data = arrString.pop(0).split(' ')

    # Setup process
    arrProcess = []
    for s in arrString:
        s = s.replace('(', '')
        s = s.replace(')', '')
        if len(s) > 2:
            arrProcess.append(
                Common.Process(
                    arrTransaction[int(s[1])-1],
                    s[0],
                    s[2]
                )
            )
        else:
            arrProcess.append(
                Common.Process(
                    arrTransaction[int(s[1])-1],
                    s[0]
                )
            )

    return arrTransaction, arrProcess, raw_data

# Simple Locking (Exclusive Lock Only) Concurrency Control Converter
def SLock_Converter(arrTransaction, arrData, arrString):
    SL_DataContainer = []
    arrDataLabel = []
    for data in arrData:
        data_label = data.data
        arrDataLabel.append(data_label)
        SL_DataContainer.append(SL.SLData(SL.Data(data_label)))
    SL_LockManager = SL.LockManager(SL_DataContainer)
    
    arrSLTransaction = []
    for transaction in arrTransaction:
        arrSLTransaction.append(SL.SLTransaction(transaction, SL_LockManager))

    arrProcess = []
    for proc in arrData:
        transaction_id = proc.transaction.id
        action = proc.action
        dataLabel = proc.data
        arrProcess.append(SL.Process(arrSLTransaction[transaction_id - 1], action, SL_DataContainer[arrDataLabel.index(dataLabel)], SL_LockManager))

    return arrProcess, SL_LockManager

    

# Serial Optimistic Concurrency Control Converter
def OCC_Converter(arrTransaction, arrProcess, raw_data):

    newArrTransaction = []
    for T in arrTransaction:
        newArrTransaction.append(OCCTransaction(T))
    
    newArrProcess = []
    for p in arrProcess:
        newArrProcess.append(OCCProcess(p))
        newP = newArrProcess[-1]
        newP.transaction = newArrTransaction[newP.transaction.id-1]

    return newArrTransaction, newArrProcess


# Multiversion Timestamp Ordering Concurrency Control Converter
def MVCC_Converter(arrTransaction, arrProcess, raw_data):

    arrData = []
    MVCC_Process = []

    for data in raw_data:
        arrData.append(MV.MVCData(data))

    MVCC_DataMap = MV.DataMap(arrData)
    for p in arrProcess:
        MVCC_Process.append(MV.MVCProcess(p, MVCC_DataMap))
    
    return MVCC_DataMap, MVCC_Process 