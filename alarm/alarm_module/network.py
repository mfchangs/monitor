#_*_coding:utf-8_*_
#
import time
import psutil
import ipaddress
import pathlib


'''把网络的正常流量值写到的文本里，用于判断网络当前的流量是否正常'''

def network():
    net = psutil.net_if_addrs()
    interface = 0
    for key, value in net.items():
        if key == 'lo':
            continue
        interface_address = value[0].address
        if ipaddress.IPv4Address(interface_address).is_global and ipaddress.IPv4Address(
                interface_address).version == 4: #取出公网及IPv4的接口
            network_io_count_first = psutil.net_io_counters(True)[key]
            network_io_sent_first = network_io_count_first.bytes_sent
            network_io_recv_first = network_io_count_first.bytes_recv
            time.sleep(5)
            network_io_count_last = psutil.net_io_counters(True)[key]
            network_io_sent_last = network_io_count_last.bytes_sent
            network_io_recv_last = network_io_count_last.bytes_recv
            network_io_sent_avg = float('%.3f' % ((network_io_sent_last - network_io_sent_first) / 1024 / 1024))
            network_io_recv_avg = float('%.3f' % ((network_io_recv_last - network_io_recv_first) / 1024 / 1024))  # 单位从bytes转成MB
            interface = key
            break
    return  interface,network_io_sent_avg,network_io_recv_avg

def write(args):
    log_file = "/root/monitor/alarm/log/network.txt"
    f = open(log_file,"w")
    inter,sent,recv = args
    f.write("{}接口".format(inter))
    f.write('\n')
    f.write("5秒发送流量是{}Mb".format(sent))
    f.write('\n')
    f.write("5秒接收流量是{}Mb".format(recv))
    f.write('\n')
    f.close()

def read():
    log_file = "/root/monitor/alarm/log/network.txt"
    f = open(log_file,"r")
    interface = f.readline()[:-3]
    sent = f.readline()[7:-3]
    sent = float(sent)
    recv = f.readline()[7:-3]
    recv = float(recv)
    f.close()
    return interface,sent,recv


'''作用是当network_alarm.txt文件有等于或超过5行的行数时，将触发报警；否则就追加到此文件中'''
def append(send,recv):
    log_file = "/root/monitor/alarm/log/network_alarm.txt"
    f = pathlib.Path(log_file)
    if f.exists():
        file = open(log_file,"r+")
        if len(file.readlines()) >= 5:
            file.truncate()
            file.close()
            return False  #返回False，将触报警
        else:
            file.close()
            file = open(log_file,"a+")
            text = "{},{}\n".format(send,recv)
            file.write(text)
            file.close()
            return True
    else:
        file = open(log_file, "a+")
        text = "{},{}\n".format(send, recv)
        file.write(text)
        file.close()
        return True

'''
触发告警依赖于判断network_alarm.txt中是否有大于等于6行数据。
那么就要确保此文件中的数据必须是连续执行中写入到的；不能是间隔写入，间隔写入就会造成行数是累加的。
因此，只要没有到达触发写入network_alarm.txt文件的条件时，都要清空一次此文件
'''
def empty():
    log_file = "/root/monitor/alarm/log/network_alarm.txt"
    f = pathlib.Path(log_file)
    if f.exists():
        file = open(log_file,"r+")
        file.truncate()
        file.close()


