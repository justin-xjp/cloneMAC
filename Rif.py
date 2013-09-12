# -*- coding: utf-8 -*-


##上面这行很关键，~!!!!!
#初始化
import _winreg
import os
import sys
from ctypes import *
#from codecs import *
deskey=r"SYSTEM\CurrentControlSet\Control\class\{4D36E972-E325-11CE-BFC1-08002BE10318}"
netkey=r"system\currentcontrolset\control\network\{4D36E972-E325-11CE-BFC1-08002BE10318}"
nes=u"本地连接"
###常数
def diffkey(key,subkey,addkey,sName,svalue):
    try:#子目录不存在情况
        skey=_winreg.OpenKey(key,subkey+addkey)
   # print "here"
    except WindowsError:
        return 0
    try:#考虑sName不存在情况。。
        qv=_winreg.QueryValueEx(skey,sName)[0]
#        print qv
 #       print svalue
        if qv==svalue:  #中文字符串对比，很麻烦，英文可以用cmp，中文要考虑转换编码。尝试在提交svalue变量的时候定义成了UNICODE编码，其他系统未测试。
            _winreg.CloseKey(skey)
            return 1
        else:
            _winreg.CloseKey(skey)
            return 0
    except WindowsError:
        _winreg.CloseKey(skey)
        return 0
    #流程1.查询'本地连接'对应上级目录名称
    #另外，遍历4D36E972-E325-11CE-BFC1-08002BE10318下ndi\interface\lowerrange=ethernet也是个好方法~！！
def findId(subkey,addkey,des,wname): #查找所需KEY，地址，子地址（虽可精简，但效率）,描述，校对内容。
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
    NetId=findId(netkey,r"\Connection",r"Name",wname)#注册表更改IP，需要此值，看来不得不开启global了。
    if NetId:
        print "find out ! %s \nNetCfgInstanceId= %s" %(wname,NetId)
        ClassId=findId(deskey,'',r"NetCfgInstanceId",NetId)#2.遍历查询Key=NetCfgInstanceId 值483D7F95-D738-49CE-A283-8858B1C2AC6D
        if ClassId:
            print "find out ! %s" % ClassId
            return ClassId
        else:
            return 0#Classid错误
    else:
        return -1#Netid错误
def changeIP(subkey,ipAddress,subnetMask,gateway,dnsServer):
    strKeyName = 'System\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\' + subkey
    hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,strKeyName,0,_winreg.KEY_WRITE)
     # 定义需要修改的IP地址、子网掩码、默认网关和DNS等
     
    try:
        _winreg.SetValueEx(hkey, 'IPAddress', None, _winreg.REG_MULTI_SZ, ipAddress)
        _winreg.SetValueEx(hkey, 'SubnetMask', None, _winreg.REG_MULTI_SZ, subnetMask)
        _winreg.SetValueEx(hkey, 'DefaultGateway', None, _winreg.REG_MULTI_SZ, gateway)
        _winreg.SetValueEx(hkey, 'NameServer', None, _winreg.REG_SZ, ','.join(dnsServer))
    except WindowsError:
        print 'Set IP Error'
        exit()

    _winreg.CloseKey(hkey)
########更新网络适配器,dll
# 调用DhcpNotifyConfigChange函数通知IP被修改
def reDhcp():
    
    DhcpNotifyConfigChange = windll.dhcpcsvc.DhcpNotifyConfigChange

    inet_addr = windll.Ws2_32.inet_addr
# DhcpNotifyConfigChange 函数参数列表：
# LPWSTR lpwszServerName,  本地机器为None
# LPWSTR lpwszAdapterName, 网络适配器名称
# BOOL bNewIpAddress,      True表示修改IP
# DWORD dwIpIndex,         表示修改第几个IP, 从0开始
# DWORD dwIpAddress,       修改后的IP地址
# DWORD dwSubNetMask,      修改后的子码掩码
# int nDhcpAction          对DHCP的操作, 0 - 不修改, 1 - 启用, 2 - 禁用
    DhcpNotifyConfigChange(None, \
                       NetId, \
                       True, \
                       0, \
                       inet_addr(ipAdd[0]), \
                       inet_addr(subMask[0]), \
                       0)
    print u'更新IP结束'
def renet(netname):
    print isinstance(netname,unicode)#验证是否是默认unicode编码模式，以此为基础才能进行转换。
    command1='netsh interface set interface name="%s" admin="disabled"'%netname.encode('gb2312')
    command2='netsh interface set interface name="%s" admin="enabled"'%netname.encode('gb2312')#此命令成功使用，基于更换XP下ifmon.dll和netsh.exe文件，2003可用。www.dllexedown.com
    os.system(command1)
    print command1
    reDhcp()
    print command2
    os.system(command2)

##########################main######################


#NK=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,netkey)
#DK=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,deskey)
#NetId=''
############界面

print(\
u'''
###########################################
            MAC克隆
            请按键：1、更换mac,ip
                   2、恢复
###########################################'''.encode('gbk')\
)
###########选择/更换/恢复
#show1=u
#show2=u"请正确按键"
rec=raw_input(u"请按键".encode('gbk'))
print rec
#'''
while (rec!=u'1' and rec!=u'2'):
    rec=raw_input(u"请正确按键".encode('gbk'))

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
########关闭网络,目前没有做
ClassId=findKey(nes)
if ClassId:
    DK=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,deskey+'\\'+ClassId,0,_winreg.KEY_ALL_ACCESS)
    print _winreg.QueryValueEx(DK,r"DriverDesc")[0]
#4添加、修改 NetworkAddress 键
    if MAC != "":
        _winreg.SetValueEx(DK,u"NetworkAddress",0,_winreg.REG_SZ,MAC)
        print(u"设置MAC成功")
        changeIP(NetId,ipAdd,subMask,gate,dnss)
        print(u"设置ip成功")
#   _winreg.SetValue(DK,"NetworkAddresstt",1,"00112233eedd") #这是建立KEY，reg中的‘文件夹’，不是我要的。
    else:
        _winreg.DeleteValue(DK,u"NetworkAddress")#删除键值
                  
        print(u'恢复MAC完成')
        changeIP(NetId,ipAdd,subMask,gate,dnss)
        print(u'恢复ip完成')
    _winreg.CloseKey(DK)
    #显示当前，开启连接。
else:
    print ClassId


renet(nes)

############################基本完成#####################

#'''
print 'END'

