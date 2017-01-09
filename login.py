#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import sys
import os
import re
import subprocess
import socket

#socket.setdefaulttimeout(10) # 10 秒钟后超时
urllib2.socket.setdefaulttimeout(4) # 另一种方式

'''author:lidage'''

reload(sys)
sys.setdefaultencoding("utf-8")

def img_process(img,output,cleanup= True):
    subprocess.check_output('tesseract' + ' ' + img + ' ' + output,shell=True)
    text = ''
    with open(output+'.txt', 'r') as f:
        text = f.read().strip()
    if cleanup:
        os.remove(output+'.txt')
    print text
    return text

def process_GP(score):
    if score == u'优秀':
        return 5.0
    elif score == u'良好':
        return 4.5
    elif score == u'中等':
        return 3.5
    else:
        score = float(score)
        if score>=90:
            return 5.0
        elif score>=85 and score <90:
            return 4.5
        elif score>=80 and score <85:
            return 4.0
        elif score>=75 and score <80:
            return 3.5
        elif score>=70 and score <75:
            return 3.0
        elif score>=65 and score <70:
            return 2.5
        elif score>=60 and score <65:
            return 2.0
#        return float(score)

def process_AVP(score):
    if score == u'优秀':
        return 90.0
    elif score == u'良好':
        return 85.0
    elif score == u'中等':
        return 75.0
    else:
        return float(score)

#if --name == '__main__':
capurl = "http://202.119.113.135/validateCodeAction.do?random=0.8532307550456932"        #验证码地址
posturl = "http://202.119.113.135/loginAction.do"              #登陆地址

# cookie自动管理

cookie = cookielib.CookieJar()
hand = urllib2.HTTPCookieProcessor(cookie)

# opener与cookie绑定

opener = urllib2.build_opener(hand)

# 用户登陆


# 用opener先访问验证码，得到验证码cookie由cookie管理器自动管理

picture = opener.open(capurl).read()
local = open('/home/lee/Desktop/image.jpg','wb') # 验证码写入本地proje目录下验证码
local.write(picture)                                                # 显示验证码
local.close()
pic = r'/home/lee/Desktop/image.jpg'
output = r'/home/lee/Desktop/test'
code = img_process(pic,output)
#code = raw_input('please input authenticate code:')                                    # 人工识别验证码e

headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,en-GB;q=0.6,en;q=0.4',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Length':'35',
        'Content-Type':'application/x-www-form-urlencoded',
        'Host':'202.119.113.135',
        'Origin':'http://202.119.113.135',
        'Referer':'http://202.119.113.135/logout.do',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            }

postdatas= {
    'zjh':,
    'mm':,
    'v_yzm':code,
}

# 模拟登陆教务处
data = urllib.urlencode(postdatas)
request = urllib2.Request(posturl,data,headers)
try:
    response = opener.open(request)
except urllib2.HTTPError,e:
    print e.code

html = response.read().decode('gbk')
print "login successfully"
testurl = 'http://202.119.113.135/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2016-2017%D1%A7%C4%EA1(%C1%BD%D1%A7%C6%DA)'
#save = urllib2.urlopen(testurl).read()
#open('E:/testimage/score.html', "w").write(save)
headerssco={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en-GB;q=0.6,en;q=0.4',
        #'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Length':'35',
        #'Content-Type':'application/x-www-form-urlencoded',
        'Host':'202.119.113.135',
        #'Origin':'http://202.119.113.135',
        'Referer':'http://202.119.113.135/gradeLnAllAction.do?type=ln&oper=qb',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            }
requestsco = urllib2.Request(testurl)
responsesco = opener.open(requestsco)
html = responsesco.read().decode('gbk')
#print html
#fl = open('/home/lee/Desktop/html','w')
#fl.writelines(html)
#fl.close()

#unicode chinese  
#re_words = re.compile(ur'<td align="center">\s+([\u4e00-\u9fa5]+)\s+</td>\s+<td align="center">\s+.+\s+</td>\s+<td align="center">\s+([\u0030-\u0039]|[\u0030-\u0039]\.[\u0030-\u0039])\s+</td>\s+<td align="center">\s+([\u4e00-\u9fa5]+)\s+</td>\s+<td align="center">\s+<p align="center">([\u0030-\u0039]+\.[\u0030-\u0039]|[\u4e00-\u9fa5]+)&nbsp;</P>')  
re_words = re.compile(ur'<td align="center">\s+(.+)\s+</td>\s+<td align="center">\s+.+\s+</td>\s+<td align="center">\s+([\u0030-\u0039]|[\u0030-\u0039]\.[\u0030-\u0039])\s+</td>\s+<td align="center">\s+([\u4e00-\u9fa5]+)\s+</td>\s+<td align="center">\s+<p align="center">([\u0030-\u0039]+\.[\u0030-\u0039]|[\u4e00-\u9fa5]+)&nbsp;</P>')  
m =  re_words.search(html,0)  
print "unicode 中文"  
#print "--------"  
#print m  
#print m.group(4)  
res = re.findall(re_words, html)       # 查询出所有的匹配字符串  
le_name = []
le_credit = []
le_type = []
le_score = []
if res:
#    print "There are %d parts:\n"% len(res)   
    for r in res:
        le_name.append(r[0])
        le_credit.append(r[1])
        le_type.append(r[2])
        le_score.append(r[3])
#        for t in r:
#            print "\t",t
#print "--------\n"
sum_score = 0.0
sum_credit = 0.0
#"*****************************************" 
#计算GPA
for i in range(len(le_type)):
    if le_type[i] == u'必修':
        sum_credit += float(le_credit[i])
        GP = float(process_GP(le_score[i]))
        credit = float(le_credit[i])
        score = float(credit * GP)
        sum_score += score
        
print u"总绩点:%f" %sum_score
print u"总学分:%f" %sum_credit
print u"GPA:%.2f" %(sum_score/sum_credit)

"*****************************************"  #计算均分
c = 0
sum_AVP = 0.0
for i in range(len(le_type)):
    if le_type[i] == u'必修':
        c += 1
        AVP = float(process_AVP(le_score[i]))
        sum_AVP += AVP
        
print u"均分:%.2f" %(sum_AVP/c)
        
            
        
