import csv
import math
import time
import glob
import os, shutil
import statistics
from datetime import datetime
mp3_list = glob.glob('*.mp3')
i = 1
for interview in mp3_list:
    save = interview.split('.')[0] + ".csv"
    os.system('ffprobe -f lavfi -i amovie="'+interview+'",astats=metadata=1:reset=1 -show_entries frame=pkt_pts_time:frame_tags=lavfi.astats.Overall.RMS_level,lavfi.astats.1.RMS_level,lavfi.astats.2.RMS_level -of csv=p=0 1>"'+save+'"')
    print str(i) + "/" + str(len(mp3_list))
    i += 1
csv_list = glob.glob('*.csv')
for file in csv_list:
    name = file.split('-')[0]
    id = file.split('-')[1]
    startTime = datetime.now()

    with open(file, 'rb') as f:
        reader = csv.reader(f)
        my_array = list(reader)

    count = 0
    saveas = ''

    times = []
    avg_db = []
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
    threshold = threshold_mean - (threshold_std/2)
    print threshold_mean
    print threshold_std
    
    mean_db = 0
    silence = []
    
    for time, decibels, other, other1 in my_array:
        if int(float(time)) >= secs and int(float(time)) < secs+1:        
            if decibels == '-inf':
                decibels = -110
            mean_db += float(decibels)
            count += 1
        else:
            mean_db = mean_db/count
            avg_db.append(mean_db)
            if mean_db <= threshold: #change to one standard dev below avg
                silence.append(True)
            else:
                silence.append(False)
            mean_db = float(decibels)
            count = 1  
            secs += 1
    save = zip(times,avg_db,silence)
            
    name_list = []
    id_list = []
    start_list = []
    end_list = []
    count = 0    
    start = 0
    end = 0
    quiet = False
    
    for seconds, decibels, silence in save:
        if (silence and not quiet):
            start = int(seconds)
            quiet = True
            count += 1
        elif (silence and quiet):
            end = int(seconds)
            count += 1
        elif (not silence and quiet and count > 3): #how many seconds of silence qualify for 'silence'
            quiet = False
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
            quiet = False
    with open(file, "wb") as f:
        writer = csv.writer(f)  
        writer.writerows(zip(name_list,id_list,start_list,end_list))
    print "\n" + "Runtime: " + str(datetime.now() - startTime)
    
os.system('python chart.py')

def move(files, path, moveto):
    for f in files:
        src = path+f
        dst = moveto+f
        shutil.move(src,dst)
        
path = "C:/Users/campb/Desktop/SQL Proj/ffmpeg-20170404-1229007-win64-static/bin/"
csv_files = glob.glob("*.csv")
xlsx_files = glob.glob("*.xlsx")
mp3_files = glob.glob("*.mp3")

sil_csv = "C:/Users/campb/Desktop/SQL Proj/csv/Silence/"
move(csv_files,path,sil_csv)

sil_chart = "C:/Users/campb/Desktop/SQL Proj/Excel Charts/Silence/"
move(xlsx_files,path,sil_chart)

interview = "D:/interview mp3s/"
move(mp3_files,path,interview)