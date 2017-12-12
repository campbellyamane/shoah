import csv
import math
import time
import glob
import os
import statistics
csv_list = glob.glob('*.csv')
for file in csv_list:
    name = file.split('-')[0]
    id = file.split('-')[1]

    from datetime import datetime
    startTime = datetime.now()

    with open(file, 'rb') as f:
        reader = csv.reader(f)
        my_array = list(reader)
        
    start = 0
    end = 0
    truth = 'false'
    name_list = []
    id_list = []
    start_list = []
    end_list = []
    count = 0
    saveas = ''

    mean_db = 0;

    times = []
    avg_db = []
    silence = []
    threshold = []
    total_sec = math.ceil(float(my_array[len(my_array)-1][0]))

    for n in range(int(total_sec)):
        times.append(n)    
        
    secs = 0
    for time, decibels, other, other1 in my_array:        
        if decibels == '-inf':
            decibels = -110
        threshold.append(float(decibels))   
    threshold_mean = statistics.mean(threshold)  
    threshold_std = statistics.pstdev(threshold)
    threshold = threshold_mean + (threshold_std/2)
    print threshold_mean
    print threshold_std
    
    for time, decibels, other, other1 in my_array:
        if int(float(time)) >= secs and int(float(time)) < secs+1:        
            if decibels == '-inf':
                decibels = -110
            mean_db += float(decibels)
            count += 1
        else:
            mean_db = mean_db/count
            avg_db.append(mean_db)
            if mean_db >= threshold: #change to one standard dev below avg
                silence.append('TRUE')
            else:
                silence.append('FALSE')
            mean_db = float(decibels)
            count = 1  
            secs += 1
    save = zip(times,avg_db,silence)
    count = 0
    for seconds, decibels, silence in save:
        if (silence == 'TRUE' and truth == 'false'):
            start = int(seconds)
            truth = 'true'
            count += 1
        elif (silence == 'TRUE' and truth == 'true'):
            end = int(seconds)
            count += 1
        elif (silence == 'FALSE' and truth == 'true' and count > 3):
            truth = 'false'
            if (start >= 3600):
                m, s = divmod(start, 60)
                h, m = divmod(m, 60)
                start_list.append("%d:%02d:%02d" % (h, m, s))
                name_list.append(name)
                id_list.append(id)
                
                m, s = divmod(end, 60)
                h, m = divmod(m, 60)
                end_list.append("%d:%02d:%02d" % (h, m, s))
            elif (end < 3600):
                m, s = divmod(start, 60)
                start_list.append("%02d:%02d" % (m, s))
                name_list.append(name)
                id_list.append(id)
                
                m, s = divmod(end, 60)
                end_list.append("%02d:%02d" % (m, s))
            else:
                m, s = divmod(start, 60)
                h, m = divmod(m, 60)
                start_list.append("%d:%02d:%02d" % (h, m, s))
                name_list.append(name)
                id_list.append(id)
                
                m, s = divmod(end, 60)
                end_list.append("%02d:%02d" % (m, s))
            count = 0
        else:
            count = 0
            truth = 'false'
    with open(file, "wb") as f:
        writer = csv.writer(f)  
        writer.writerows(zip(name_list,id_list,start_list,end_list))
    print "\n" + "Runtime: " + str(datetime.now() - startTime)