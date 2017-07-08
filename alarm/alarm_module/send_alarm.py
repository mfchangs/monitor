# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time,datetime
import json
import requests


def mail_alarm(alarm_ip,alarm_type,alarm_value):
    send_mail = '17688969662@163.com'
    send_pass = 'Ajd.123'
    revice_mail = 'mfchangs@163.com'
    alarm_context = "服务器IP：{}\n{}\n告警类型：{}\n告警内容：{}\n".format(alarm_ip,alarm_time(),alarm_type,alarm_value)
    try:
        msg = MIMEText(alarm_context, 'plain', 'utf-8')  # 邮件正文
        msg['From'] = formataddr(["邮件告警", send_mail])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["大漠菰鹰", revice_mail])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "告警邮件"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，SMTP_SSL默认是465端口
        server.login(send_mail, send_pass)  # 登陆到SMTP邮箱
        server.sendmail(send_mail, [revice_mail, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:
        print("send mail false")
        pass


'''
告警格式: 
服务器告警   
告警时间：2017年7月6日4时14分7秒  
服务器IP：1.1.1.1 		
告警类型：内存告警		
告警内容：内存使用率达80% 
'''
def ding_alarm(alarm_ip,alarm_type,alarm_value): #把信息发到告警群
    ip = "服务器IP:{}".format(alarm_ip)
    if alarm_type == "SMS文件告警":
        type = "告警类型：" + alarm_type
        value = "告警内容：" + alarm_value
    else:
        type = "告警类型：{}告警".format(alarm_type)
        value = "告警内容：{}使用率{}".format(alarm_type,alarm_value)
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "服务器告警",
            "text":"#服务器告警@18877169662\n" +
                "#{}\n".format(alarm_time()) +
                "#{}\n".format(ip) +
                "#{}\n".format(type) +
                "#{}\n".format(value),

        },
        "at":{
            "atMobiles":[
                "18877169662"
            ]
        }
    }
    #url = 'https://oapi.dingtalk.com/robot/send?access_token=24774ec38d421c4f220504f3803d40a3d3fb2513f6abcac8fdfdb8bbb621b533'  #告警群token
    url = 'https://oapi.dingtalk.com/robot/send?access_token=3a9f0aaae8c5d340b00c93011e83f78efd7e04c5e5592200e9ac4f494cb016b9' #提示群token
    post_data = json.dumps(data).encode(encoding="utf8")
    HEADERS = {
    "Content-Type": "application/json ;charset=utf-8 "
    }

    requests.post(url,data=post_data,headers=HEADERS) #发送信息到钉钉

#格式化当前时间
def alarm_time():
    now_time = time.localtime(time.time())
    now_year,now_mon,now_day,now_hour,now_minute,now_second = now_time.tm_year,now_time.tm_mon,now_time.tm_mday,now_time.tm_hour,now_time.tm_min,now_time.tm_sec
    time_fromat = str(now_year) + "年" + str(now_mon) + "月" + str(now_day) + "日" + str(now_hour) + "时" + str(now_minute) + "分" + str(now_second) + "秒"
    new_time = "告警时间：{}".format(time_fromat)
    return new_time