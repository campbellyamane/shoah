import csv
import xlsxwriter
import math
import time
import glob
import os
csv_list = glob.glob('*.csv')
index = 1
total = len(csv_list)
for file in csv_list:

    with open(file, 'rb') as f:
        reader = csv.reader(f)
        my_array = list(reader)
    file = file.split('.');
    length = file[0].split('_')
    length = int(length[1])
    
    time = []
    silent = []
    percent = []
    percentage = []
    percentage.append("Percentage")
    truth = False
    percent.append("Percent")
    for x in range(100):
        percentage.append(x)
    time.append("Time")
    silent.append("Silent?")
    for x in range(length):    
        if (x >= 3600):
            m, s = divmod(x, 60)
            h, m = divmod(m, 60)
            t = "%d:%02d:%02d" % (h, m, s)
        else:
            m, s = divmod(x, 60)
            t = "%02d:%02d" % (m, s)
            t = "00:" + t
        time.append(t)
        percent.append(math.floor(100*float(x)/float(length)))
        
        for name, id, start, end in my_array:   
            start = start.split(":")
            end = end.split(":")
            if (len(start) > 2):
                start = (int(start[0])*3600) + (int(start[1])*60) + int(start[2])
            else:
                start = (int(start[0])*60) + int(start[1])    
            if (len(end) > 2):
                end = (int(end[0])*3600) + (int(end[1])*60) + int(end[2])
            else:
                end = (int(end[0])*60) + int(end[1])
            
            if (x >= start and x <= end):
                silent.append(1)
                truth = True
                break
        if (truth  == False):
            silent.append(0)
        else:
            truth = False
    file[0] += '.xlsx'
    print file[0]
    workbook = xlsxwriter.Workbook(file[0])
    worksheet = workbook.add_worksheet()
    worksheet.write_column('A1',percent)
    worksheet.write_column('B1',time)
    worksheet.write_column('C1',silent)
    worksheet.write('D1','Silent')
    worksheet.write_formula('D2','=COUNTIF(C:C,"1")')
    worksheet.write('E1','Not')
    worksheet.write_formula('E2','=COUNTIF(C:C,"0")')
    worksheet.write_column('F1',percentage)
    worksheet.write('G1','Sil Perc')
    worksheet.write_array_formula('G2:G101','{=H2:H101/D2}')
    worksheet.write('H1','Silence')
    worksheet.write_array_formula('H2:H101','{=COUNTIFS(A:A,F2:F101,C:C,1)}')
    chart = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth_with_markers'})
    chart.add_series({'name': 'Avg Silence (out of 1)', 'categories': '=Sheet1!$F$2:$F$101', 'values': '=Sheet1!$G$2:$G$101'})
    chart.set_x_axis({'min': 0, 'max': 100})
    chart.set_y_axis({'min': 0})
    chart.set_title({'name': 'Avg Silence by Testimony Percent'})
    worksheet.insert_chart('J2', chart)
    
    length = len(silent)
    cat = '=Sheet1!$B$2:$B' + str(len(silent)+1)
    val = '=Sheet1!$C$2:$C' + str(len(silent)+1)
    chart = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
    chart.add_series({'name': 'Silent', 'categories': cat, 'values': val})
    chart.set_x_axis({'min': 0, 'max': 1})
    chart.set_title({'name': 'Silence by Second'})
    worksheet.insert_chart('R2', chart, {'x_scale': 2, 'y_scale': 1})
    
    chart = workbook.add_chart({'type': 'pie'})
    chart.add_series({'categories': ['Sheet1', 0, 3, 0, 4], 'values': ['Sheet1', 1, 3, 1, 4]})
    chart.set_title({'name': 'Silence Frequency'})
    worksheet.insert_chart('J20', chart)
        

    workbook.close()  
    print str(index) + "/" + str(total)
    index += 1