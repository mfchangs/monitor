#_*_coding:utf-8_*_
#
#
import monitor
from alarm_module import send_alarm
import threading
import psutil
import ipaddress,json,time

class alarm:
    def __init__(self):
        self.m = monitor.Monitor()
        self.cpu = self.m.cpu_monitor()
        self.disk = self.m.disk_monitor()
        self.memory = self.m.memory_monitor()
        self.network = self.m.network_monitor()
    def judge(self):
        if self.cpu[0] and self.disk[0] and self.memory[0] and self.network[0]:
            pass
        else:

            if self.cpu[0] == False:
                send_alarm.mail_alarm(server_ip(),"CPU",self.cpu[1])
                send_alarm.ding_alarm(server_ip(),"CPU",self.cpu[1])
            if self.memory[0] == False:
                send_alarm.mail_alarm(server_ip(), "内存", self.memory[1])
                send_alarm.ding_alarm(server_ip(), "内存", self.memory[1])
            if self.disk[0] == False:
                send_alarm.mail_alarm(server_ip(), "硬盘", self.disk[1])
                send_alarm.ding_alarm(server_ip(), "硬盘", self.disk[1])
            if self.network[0] == False:
                send_alarm.mail_alarm(server_ip(), "网络", self.network[1])
                send_alarm.ding_alarm(server_ip(), "网络", self.network[1])

    def sms_judge(self):
        src_file = ["/home/test/pack/chess_svr/log/SMS.log", "/home/test/pack/connsvr/log/SMS.log",
                    "/home/test/pack/ecs_svr/log/SMS.log", "/home/test/pack/event_svr/log/SMS.log",
                    "/home/test/pack/online_svr/log/SMS.log"]
        dest_file = ["/root/monitor/alarm/sms_log/chess_svr/SMS.log","/root/monitor/alarm/sms_log/connsvr/SMS.log",
                     "/root/monitor/alarm/sms_log/esc_svr/SMS.log","/root/monitor/alarm/sms_log/event_svr/SMS.log",
                     "/root/monitor/alarm/sms_log/online_svr/SMS.log"]
        for i in range(len(src_file)):
            tmp_judge = self.m.sms_log_monitor(src_file[i],dest_file[i])
            if tmp_judge == False:
                context = src_file[i] + "文件产生告警"
                send_alarm.mail_alarm(server_ip(),"SMS文件告警",context)
                send_alarm.ding_alarm(server_ip(),"SMS文件告警",context)


def server_ip():
    interface = psutil.net_if_addrs()
    for key,value in interface.items():
        if key == "lo":
            continue
        else:
            ip = value[0].address
            if ipaddress.IPv4Address(ip).is_global:
                break
    return ip

if __name__ == "__main__":
    a = alarm()
    a.sms_judge()
    a.judge()
