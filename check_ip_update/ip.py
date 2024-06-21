import os
import platform
import socket
import json
import netifaces as ni
from smtplib import SMTP_SSL
from email.mime.text import MIMEText


#
# path
#
path = '/path/to/check_ip_update/data.json'


def getIPAddress():
    os_platform = platform.platform().lower()
    if 'windows' in os_platform:
        ip = socket.gethostbyname(self.hostname)
    elif 'linux' in os_platform:
        #
        # info get from ifconfig
        #
        if_addresses = ni.ifaddresses('enp37s0')
        ip = if_addresses[ni.AF_INET][0]['addr']
    return ip


def getEnv():
    with open(path, 'r') as f:
        return json.load(f)
    # return os.system('echo $INET_IP')


def setEnv(ip, result):
    result['ip'] = ip
    with open(path, 'w') as f:
        json.dump(result, f, indent=2)
    # os.environ['INET_IP'] = str(ip)


def sendMail(message, subject, sender, recipient, to_addrs, cc_show=''):
    user = 'awzyc2010@163.com'
    #
    # password generated on your own server
    #
    password = 'PASSWORD'
    msg = MIMEText(message, 'plain', _charset="utf-8")
    msg["Subject"] = subject
    msg["from"] = sender
    msg["to"] = recipient
    msg["Cc"] = cc_show
    with SMTP_SSL(host="smtp.163.com", port=465) as smtp:
        smtp.login(user = user, password = password)
        smtp.sendmail(from_addr = user, to_addrs = to_addrs, msg = msg.as_string())


if __name__ == '__main__':
    IP = getIPAddress()
    data = getEnv()
    env_ip = data['ip']
    if IP != env_ip:
        setEnv(IP, data)
        message = 'New IP address: ' + IP
        message = message + '''

|  service      |  port   |
| ------------- | ------- |
|  Emby Server  |  8096   |
|  qBittorrent  |  8888   |
|  SSH Server   |  22222  |
|  ownCloud     |  9260   |

This email is sent from Augists Arch Linux for IP update, you can unsubscribe by contacting [augists@duck.com](mailto:augists@duck.com)

!!!DO NOT REPLY!!!'''
        subject = data['subject']
        sender = data['sender']
        recipient = data['recipient']
        to_addrs = data['receiver']
        sendMail(message, subject, sender, recipient, to_addrs)
