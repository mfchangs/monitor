#_*_coding:utf-8_*_
#
#
import filecmp
import difflib
import shutil

def SMS(src_file,dest_file):
    if filecmp.cmp(src_file,dest_file):
        return True,src_file,dest_file
    else:
        return False,src_file,dest_file


def copy():
    src_file = ["/home/test/pack/chess_svr/log/SMS.log", "/home/test/pack/connsvr/log/SMS.log",
                "/home/test/pack/ecs_svr/log/SMS.log", "/home/test/pack/event_svr/log/SMS.log",
                "/home/test/pack/online_svr/log/SMS.log"]
    dest_file = ["/root/monitor/alarm/sms_log/chess_svr/SMS.log", "/root/monitor/alarm/sms_log/connsvr/SMS.log",
                 "/root/monitor/alarm/sms_log/esc_svr/SMS.log", "/root/monitor/alarm/sms_log/event_svr/SMS.log",
                 "/root/monitor/alarm/sms_log/online_svr/SMS.log"]
    for i in range(len(src_file)):
        shutil.copy2(src_file[i],dest_file[i])

