# -*- coding: cp936 -*-

##�������кܹؼ���~!!!!!
#��ʼ��
import _winreg
import os
import sys
from ctypes import *
deskey=r"SYSTEM\CurrentControlSet\Control\class\{4D36E972-E325-11CE-BFC1-08002BE10318}"
netkey=r"system\currentcontrolset\control\network\{4D36E972-E325-11CE-BFC1-08002BE10318}"
nes=u"��������"
###����
def diffkey(key,subkey,addkey,sName,svalue):
    try:#��Ŀ¼���������
        skey=_winreg.OpenKey(key,subkey+addkey)
   # print "here"
    except WindowsError:
        return 0
    try:#����sName�������������
        qv=_winreg.QueryValueEx(skey,sName)[0]
#        print qv
 #       print svalue
        if qv==svalue:  #�����ַ����Աȣ����鷳��Ӣ�Ŀ�����cmp������Ҫ����ת�����롣�������ύsvalue������ʱ�������UNICODE���룬����ϵͳδ���ԡ�
            _winreg.CloseKey(skey)
            return 1
        else:
            _winreg.CloseKey(skey)
            return 0
    except WindowsError:
        _winreg.CloseKey(skey)
        return 0
    #����1.��ѯ'��������'��Ӧ�ϼ�Ŀ¼����
    #���⣬����4D36E972-E325-11CE-BFC1-08002BE10318��ndi\interface\lowerrange=ethernetҲ�Ǹ��÷���~����
def findId(subkey,addkey,des,wname): #��������KEY����ַ���ӵ�ַ����ɾ��򣬵�Ч�ʣ�,������У�����ݡ�
    key=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,subkey)
    try:
        i=1
        while 1:
            Id=_winreg.EnumKey(key,i)

            if diffkey(key,Id,addkey,des,wname)==1:
   
                _winreg.CloseKey(key)
                return Id
                break
            i+=1
    except WindowsError:
        _winreg.CloseKey(key)
        return 0

def findKey(wname):
   
    global NetId
    NetId=findId(netkey,r"\Connection",r"Name",wname)#ע������IP����Ҫ��ֵ���������ò�����global�ˡ�
    if NetId:
        print "find out ! %s \nNetCfgInstanceId= %s" %(wname,NetId)
        ClassId=findId(deskey,'',r"NetCfgInstanceId",NetId)#2.������ѯKey=NetCfgInstanceId ֵ483D7F95-D738-49CE-A283-8858B1C2AC6D
        if ClassId:
            print "find out ! %s" % ClassId
            return ClassId
        else:
            return 0#Classid����
    else:
        return -1#Netid����
def changeIP(subkey,ipAddress,subnetMask,gateway,dnsServer):
    strKeyName = 'System\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\' + subkey
    hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,strKeyName,0,_winreg.KEY_WRITE)
     # ������Ҫ�޸ĵ�IP��ַ���������롢Ĭ�����غ�DNS��
     
    try:
        _winreg.SetValueEx(hkey, 'IPAddress', None, _winreg.REG_MULTI_SZ, ipAddress)
        _winreg.SetValueEx(hkey, 'SubnetMask', None, _winreg.REG_MULTI_SZ, subnetMask)
        _winreg.SetValueEx(hkey, 'DefaultGateway', None, _winreg.REG_MULTI_SZ, gateway)
        _winreg.SetValueEx(hkey, 'NameServer', None, _winreg.REG_SZ, ','.join(dnsServer))
    except WindowsError:
        print 'Set IP Error'
        exit()

    _winreg.CloseKey(hkey)
########��������������,dll
# ����DhcpNotifyConfigChange����֪ͨIP���޸�
def reDhcp():
    
    DhcpNotifyConfigChange = windll.dhcpcsvc.DhcpNotifyConfigChange

    inet_addr = windll.Ws2_32.inet_addr
# DhcpNotifyConfigChange ���������б�
# LPWSTR lpwszServerName,  ���ػ���ΪNone
# LPWSTR lpwszAdapterName, ��������������
# BOOL bNewIpAddress,      True��ʾ�޸�IP
# DWORD dwIpIndex,         ��ʾ�޸ĵڼ���IP, ��0��ʼ
# DWORD dwIpAddress,       �޸ĺ��IP��ַ
# DWORD dwSubNetMask,      �޸ĺ����������
# int nDhcpAction          ��DHCP�Ĳ���, 0 - ���޸�, 1 - ����, 2 - ����
    DhcpNotifyConfigChange(None, \
                       NetId, \
                       True, \
                       0, \
                       inet_addr(ipAdd[0]), \
                       inet_addr(subMask[0]), \
                       0)
    print u'����IP����'
def renet(netname):
    print isinstance(netname,unicode)#��֤�Ƿ���Ĭ��unicode����ģʽ���Դ�Ϊ�������ܽ���ת����
    command1='netsh interface set interface name="%s" admin="disabled"'%netname.encode('gb2312')
    command2='netsh interface set interface name="%s" admin="enabled"'%netname.encode('gb2312')#������ɹ�ʹ�ã����ڸ���XP��ifmon.dll��netsh.exe�ļ���2003���á�www.dllexedown.com
    os.system(command1)
    print command1
    reDhcp()
    print command2
    os.system(command2)

##########################main######################


#NK=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,netkey)
#DK=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,deskey)
#NetId=''
############����

print(\
u'''
###########################################
            MAC��¡
            �밴����1������mac,ip
                   2���ָ�
###########################################'''\
)
###########ѡ��/����/�ָ�
#show1=u
#show2=u"����ȷ����"
rec=raw_input("�밴��")
print rec
#'''
while (rec!=u'1' and rec!=u'2'):
    rec=raw_input("����ȷ����")

#'''
gate=['192.168.1.1']
subMask=["255.255.255.0"]
dnss=['8.8.8.8','8.8.4.4']
if rec=='1':
    ipAdd=['192.168.1.3']
    MAC="00E04C317D8C"
    print ipAdd,MAC
elif rec=='2':
    ipAdd=['192.168.1.27']
    MAC=""

#'''
########�ر�����,Ŀǰû����
ClassId=findKey(nes)
if ClassId:
    DK=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,deskey+'\\'+ClassId,0,_winreg.KEY_ALL_ACCESS)
    print _winreg.QueryValueEx(DK,r"DriverDesc")[0]
#4��ӡ��޸� NetworkAddress ��
    if MAC != "":
        _winreg.SetValueEx(DK,u"NetworkAddress",0,_winreg.REG_SZ,MAC)
        print(u"����MAC�ɹ�")
        changeIP(NetId,ipAdd,subMask,gate,dnss)
        print(u"����ip�ɹ�")
#   _winreg.SetValue(DK,"NetworkAddresstt",1,"00112233eedd") #���ǽ���KEY��reg�еġ��ļ��С���������Ҫ�ġ�
    else:
        _winreg.DeleteValue(DK,u"NetworkAddress")#ɾ����ֵ
                  
        print(u'�ָ�MAC���')
        changeIP(NetId,ipAdd,subMask,gate,dnss)
        print(u'�ָ�ip���')
    _winreg.CloseKey(DK)
    #��ʾ��ǰ���������ӡ�
else:
    print ClassId


renet(nes)

############################�������#####################

#'''
print 'END'

