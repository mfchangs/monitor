#_*_coding:utf-8_*_

import psutil,pathlib

def cpu():
    cpu_percent = psutil.cpu_percent()
    return cpu_percent

def write(percent):
    log_file = "/root/monitor/alarm/log/cpu.txt"
    f = open(log_file,"w")
    f.write(str(percent))
    f.close()

def append(percent):
    log_file = "/root/monitor/alarm/log/cpu_alarm.txt"
    f = pathlib.Path(log_file)
    if f.exists():
        file = open(log_file, "r+")
        if len(file.readlines()) >= 5:
            file.truncate()
            file.close()
            return False
        else:
            file.close()
            file = open(log_file, 'a+')
            file.write("{}\n".format(percent))
            file.close()
            return True
    else:
        file = open(log_file, 'a+')
        file.write("{}\n".format(percent))
        file.close()
        return True

def read():
    file="/root/monitor/alarm/log/cpu.txt"
    f = open(file,"r")
    percent = f.read()
    f.close()
    return float(percent)

'''
触发告警依赖于判断cpu_alarm.txt中是否有大于等于6行数据。
那么就要确保此文件中的数据必须是连续执行中写入到的；不能是间隔写入，间隔写入就会造成行数是累加的。
因此，只要没有到达触发写入cpu_alarm.txt文件的条件时，都要清空一次此文件
'''

def empty():
    log_file = "/root/monitor/alarm/log/cpu_alarm.txt"
    f = pathlib.Path(log_file)
    if f.exists():
        file = open(log_file, "r+")
        file.truncate()
        file.close()