from collections import Counter as Co
from plotly.offline import plot
from plotly.graph_objs import *

with open('input.txt', 'r') as input:
    log = []
    for line in input:
        logline = []
        logline.append(int(line[6:8]))
        logline.append(int(line[9:11]))
        logline.append(int(line[12:14]))
        logline.append(int(line[15:17]))
        type = line[19:24]
        logline.append(type)
        if type == 'Guard':
            logline.append(int(line[26:-13]))
        # print(logline)
        # a log has the following:
        # 0: month
        # 1: day
        # 2: hour
        # 3: minute
        # 4: type
        # 5 (if applicable): guard number
        log.append(logline)
    
    log = sorted(log)
    
    guards = {}
    
    for line in log:
        # print(line)
        if line[4] == 'Guard':
            currentGuard = line[5]
        elif line[4] == 'falls':
            sleeptime = line[3]
        elif line[4] == 'wakes':
            awaketime = line[3]
            slept = awaketime - sleeptime
            if currentGuard in guards:
                existing = guards[currentGuard]
                existing[1].append(sleeptime)
                existing[2].append(awaketime)
                existing[0] += slept
                guards[currentGuard] = existing
            else:
                guards[currentGuard] = [slept, [sleeptime], [awaketime]]
    
x = []     
for _,stats in guards.items():
    for sleep,awake in zip(stats[1], stats[2]):
        for m in range(sleep,awake):
            x.append(m)

data = [Histogram(
    x=x, 
    nbinsx=60, 
    autobinx=False
)]

layout = {
    'plot_bgcolor':'#222', 
    'paper_bgcolor':'#222',
    'font':{'color':'#eee'},
    'xaxis':{
        'gridcolor':'#aaa',
        'title':'Minutes past midnight'
    },
    'yaxis':{
        'gridcolor':'#aaa',
        'title':'Guards slept'
    },
    'title':'Popularity of each minute for sleeping'
}
fig = Figure(data=data, layout=layout)

print(plot(fig, filename='stats.html'))