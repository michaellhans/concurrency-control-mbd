import random

items = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
        'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
actions = ['R', 'C', 'W']
alrddidsomething = []
committed = []
datas = items

file = open("test/soal.txt", "w")
#transactioncount = random.randint(2, 25)
transactioncount = 25
file.write(str(transactioncount) + "\n")

'''while random.randint(0, 1) and len(datas) != 0 :
    item = items[random.randint(0, 25)]
    if item not in datas :
        datas.append(item)'''

for data in datas :
    file.write(data + " ")
file.write("\n")

while len(committed) != transactioncount :
    transactionid = random.randint(1, transactioncount)
    if transactionid not in committed :
        action = actions[random.randint(0, len(actions) - 1)]
        if transactionid not in alrddidsomething and action == 'C' :
            continue
        elif action == 'C' :
            committed.append(transactionid)
        else :
            alrddidsomething.append(transactionid)
            selecteddata = datas[random.randint(0, len(datas) - 1)]
            file.write(action + str(transactionid) + "(" + selecteddata + ")\n")

for i in range(len(committed)) :
    file.write("C" + str(committed[i]) + "()")
    if (i < len(committed) - 1) :
        file.write("\n")
file.close()