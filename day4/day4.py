from collections import Counter as Co

with open('input.txt', 'r') as input:
    ans = 0
    
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
        
    max = [0, [0, [], []]]
    for key,item in guards.items():
        # print(key, item)
        if item[0] > max[1][0]:
            max[0] = key
            max[1] = item
    
    # print(max)
    mins = Co()
    for sleep,awake in zip(max[1][1], max[1][2]):
        mins.update(range(sleep,awake))
            
    print(mins.most_common(1)[0][0] * max[0])
    
    maxMinGuard = [0, 0, 0]
    for guard,stats in guards.items():
        mins = Co()
        for sleep,awake in zip(stats[1], stats[2]):
            mins.update(range(sleep,awake))
        best = mins.most_common(1)[0]
        if best[1] > maxMinGuard[0]:
            maxMinGuard = [best[1], best[0], guard]
            
    print(maxMinGuard[2] * maxMinGuard[1])