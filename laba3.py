import math
import random
import matplotlib.pyplot as plt
import numpy as np
import random as r


def expG():
    x = random.random()
    return -1 / lamda1 * math.log(x)


def doublepokazatG():
    log2 = (-1) * math.log(random.random())
    log = math.log(h) - math.log(log2)
    while log < 0:
        log2 = (-1) * math.log(random.random())
        log = (math.log(h) - math.log(log2))/lamda
    return log


def myPlot(list):
    plt.bar(x + width / 2, list, width=0.8)
    plt.show()

h = 5
sigma = 0.3
lamda1 = 1
lamda = 1
mu = 2
m = 4

time = 1000
requests = [0 for i in range(time)]
channels = [[0 for i in range(time)] for i in range(m)]
workingtimes = [[0 for i in range(time)] for i in range(m)]
doneTickets = 0
request = 0
requestCount = 0
que = [0 for i in range(time)]
workingTime = 0
busyTime = 0
queTime = 0
readyCounter = 0
averageQueNum = 0
emptyArr = []
emptyArr2 = []
for t in range(1, time):
    que[t] = que[t - 1]
    for i in range(m):  # работаем
        if workingtimes[i][t - 1] > 0:
            workingtimes[i][t] = max(workingtimes[i][t - 1] - 1, 0)
            channels[i][t] = 1
        else:
            channels[i][t] = 0

    freeChan = 0
    for i in range(m):
        if (channels[i][t] == 0):
            freeChan += 1

    if request > 0 and freeChan > 0 and que[t] > 0:
        for free in range(freeChan):
            if que[t] > 0:
                que[t] -= 1
                emptyArr2.append(temp)
                for i in range(m):
                    if (channels[i][t] <= 0):
                        channels[i][t] = 1
                        workingtimes[i][t] = expG()
                        emptyArr.append(workingtimes[i][t])
                        doneTickets += 1
                        break

    elif request <= 0 and freeChan > 0:
        que[t] += 1
        temp = 0
        request = doublepokazatG()
        requests[t] = request
        requestCount += 1
        for i in range(m):
            if (que[t] > 0 and channels[i][t] <= 0):
                que[t] -= 1
                emptyArr2.append(temp)
                channels[i][t] = 1
                workingtimes[i][t] = expG()
                emptyArr.append(workingtimes[i][t])
                doneTickets += 1
                break
    elif request <= 0:
        que[t] += 1
        temp = 0
        request = doublepokazatG()
        requests[t] = request
    flag1 = 0
    flag = 0
    for i in range(m):
        if channels[i][t] == 1 and flag == 0:
            flag1 = 1
            busyTime += 1
        if channels[i][t] == 0 and flag1 == 0:
            flag1 = 1
            readyCounter += 1
    request -= 1
    temp += 1

for i in range(time):
    if que[i] != 0:
        queTime += 1
    averageQueNum += que[i]

timeline = [i for i in range(time)]
x = np.arange(len(timeline))
width = 0.25

print("Абсолютная пропускная способность", doneTickets / time)
print("Относительная пропускная способность", doneTickets / (doneTickets + 2))
print("Средняя продолжительность периода занятости СМО", busyTime / doneTickets)
print("Коэффициент использования СМО", busyTime / (time))
print("Среднне время в очереди", queTime / doneTickets)
print("Среднне время в СМО", (busyTime + queTime) / doneTickets)
print("Вероятность немедленного обслуживания", readyCounter / time)
print("Среднее число заявок в очереди", averageQueNum / time)
print("Среднее число заявок в СМО", doneTickets / time + averageQueNum / time)
print(doneTickets)
##for i in range(m):
##    myPlot(workingtimes[i])
##myPlot(que)

for i in range(len(emptyArr)):
    emptyArr[i] += emptyArr2[i]

tMax = max(emptyArr)
tMin = min(emptyArr)
N = 1 + int(math.log(doneTickets,2))
print(N)
intervalRange = (tMax - tMin) / N
plt.hist(emptyArr, bins= N, density=True)
plt.show()