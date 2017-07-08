#!_*_coding:utf-8_*_

import psutil
import filecmp,difflib,time
from alarm_module import network,memory,cpu


class Monitor:
    def __init__(self):
        pass

    '''
    因为cpu使用率一向较低，当使用率大于等于40%时告警
    '''
    def cpu_monitor(self):
        cpu_use = psutil.cpu_percent()
        cpu_context = "CPU使用率{}%".format(cpu_use)
        if cpu_use >= 80:
            flag=cpu.append(cpu_use) #cpu.append返回的只有True或False
            return flag,cpu_context
        cpu.empty()
        return True,cpu_context

    '''
    内存触发告警条件：
    1、当内存使用率大于80%
    2、若平常使用于率小于50%时，大于平常使用率的1.5倍即告警；
    '''
    def memory_monitor(self):
        mem_percent = memory.memory()
        mem_context = "内存使用率{}%".format(mem_percent)
        read_percent = memory.read()
        if mem_percent >= 80:
            falg = memory.append(mem_percent)
            return falg,mem_context
        if read_percent <= 50:
            if mem_percent >= read_percent * 1.5:
                falg = mem_percent(mem_percent)
                return falg,mem_context
        memory.empty()
        return True,mem_context

    def disk_monitor(self):
        disk_part = psutil.disk_partitions()
        for i in disk_part:
            # 判断当前所有分区中，只要有一个分区的使用率大于80%，则返回False触发报警
            if psutil.disk_usage(i.mountpoint).percent >= 80:
                disk_context = '"{}"分区使用率{}%'.format(i.mountpoint,psutil.disk_usage(i.mountpoint).percent)
                return False,disk_context
        return True,"disk" #

    def network_monitor(self):
        interface, network_io_sent_sum, network_io_recv_sum = network.network()
        network_context = "{}接口5秒发送速率{}Mb，5秒接收速率{}Mb".format(interface,network_io_sent_sum,network_io_recv_sum)
        read_interface,read_send,read_recv = network.read()
        if interface ==  read_interface:
            if float(network_io_sent_sum) >= read_send * 3 and float(network_io_sent_sum) >= 5:
                falg = network.append(network_io_sent_sum,network_io_recv_sum)
                return falg,network_context
        network.empty() #执行清空操作
        return True,network_context

    def tcp_monitor(self):
        pass

    def sms_log_monitor(self,src_file,dest_file):
        if filecmp.cmp(src_file,dest_file):
            return True
        else:
            return False

