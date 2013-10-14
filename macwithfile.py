# -*- coding: utf-8 -*-
'''
本文件配合CLONEIP读取文件中ip,mac对应关系。
作者：rocxer
日期：2013.10.12
Ver:beta
=======
文件格式：按照ip顺序排序
ip mac
'''
import os
#os.system('cls')
#读取文件，插入例子。
#'''
#====from http://bbs.csdn.net/topics/390109364
def eachlineof(filename):
    #逐行读取给定的文本文件，返回行号、剔除末尾空字符的行内容 
    with open(filename) as handle:
        for lno, line in enumerate(handle):
            yield lno+1, line.strip()#http://www.ibm.com/developerworks/cn/opensource/os-cn-python-yield/
#'''
#===========
def getline(thefilepath, desired_line_number):
    if desired_line_number < 1:
        return ''
    for current_line_number,line in enumerate(open(thefilepath, 'rU')):
        if current_line_number == desired_line_number - 1 :
            return line 
    return ''

#'''
def seleMac(filename):
    f=open(filename)
    print(f.tell())
    print getline(filename,12)
    for line in eachlineof(filename):
        print line
    #return ip,mac


#测试
seleMac(r"e:\github\clonemac\SCmac.txt")
