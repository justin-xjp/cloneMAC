# -*- coding: cp936 -*-
#��ȡ��ǰIP��MAC���ݡ�
from subprocess import *
data=Popen(r"ipconfig /all",stdout=PIPE,shell=True)
print data.stdout.read()
