import csv
import math
import time
import glob
import os, shutil
import statistics
import xlsxwriter
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
    with open(file, 'rb') as f:
        reader = csv.reader(f)
        my_array = list(reader)
        
    file = file.split('.')

    count = 0
    saveas = ''

    times = []
    avg_db = []
    threshold = []
    mean_db = 0
    temp = 0
    total_sec = math.ceil(float(my_array[len(my_array)-1][0]))

    for n in range(int(total_sec)):
        times.append(n)    
    times = []    
    secs = 0
    for time, decibels, other, other1 in my_array:
        if decibels == '-inf':
            decibels = -110
        if int(float(time)) >= secs and int(float(time)) < secs+15: #sampling rate in seconds
            mean_db += float(decibels)
            
            count += 1
        else:
            mean_db = mean_db/count
            avg_db.append(mean_db)
            mean_db = float(decibels)
            count = 1  
            times.append(secs)  
            secs += 15 #sampling rate in seconds
    
    for i, d in enumerate(avg_db):   
        if d != d:       
            avg_db[i] = -110
    save = zip(times,avg_db)
            
    time_list = []
    decibel_list = []
    
    for seconds, decibels in save:
        if (seconds >= 3600):
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            time_list.append("%d:%02d:%02d" % (h, m, s))
            decibel_list.append(decibels)
        else:
            m, s = divmod(seconds, 60)
            time_list.append("%02d:%02d" % (m, s))
            decibel_list.append(decibels)
            
    file[0] += '.xlsx'
    print file[0]
    workbook = xlsxwriter.Workbook(file[0])
    worksheet = workbook.add_worksheet()
    worksheet.write_column('A1',time_list)
    worksheet.write_column('B1',decibel_list)
    chart = workbook.add_chart({'type': 'line'})
    
    category = '=Sheet1!$A$1:$A$' + str(len(time_list))
    value = '=Sheet1!$B$1:$B$' + str(len(time_list))
    
    chart.add_series({'name': 'Decibel Level', 'categories': category, 'values': value,
    'trendline': {
        'type': 'linear',
        'name': 'Linear Trend Line',
        'order': 2,
        'forward': 0.5,
        'backward': 0.5,
        'display_equation': False,
        'line': {
            'color': 'red',
            'width': 1,
            'dash_type': 'long_dash',
        },
    }
    })
    chart.set_title({'name': 'Decibel Levels over Time'})
    worksheet.insert_chart('C2', chart, {'x_scale': 3, 'y_scale': 2})

    workbook.close()  
