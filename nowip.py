# -*- coding: cp936 -*-
#读取当前IP及MAC数据。
from subprocess import *
data=Popen(r"ipconfig /all",stdout=PIPE,shell=True)
print data.stdout.read()
