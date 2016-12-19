# -*- coding: utf-8 -*-
"""
Created on Wed Dec 07 21:16:48 2016

@author: skyja
"""
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
fl = open('E:/testimage/html.txt','r')
html=fl.readlines()
html = unicode(html)
html.decode('gbk')
print html
fl.close()