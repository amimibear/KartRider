import numpy as np
import time
import pyscreenshot as ImageGrab
import easyocr
from itertools import groupby
import re
import csv

# time.sleep(10)

# im = ImageGrab.grab()  # X1,Y1,X2,Y2
# for i in range(10):
#     im = ImageGrab.grab(bbox=(400, 130, 1340, 1160))  # X1,Y1,X2,Y2
#     time.sleep(5)
#     # save image file
#     print(type(im))
#     im.save(f"a0{i}.png")

# exit()

dp, tp = {}, {}
double = {'多彩气球炫光':[44,45],'汽车之家气球':[39,42],'黑妞生日气球':[36,43],'跑跑新生服饰':[27,34],'跑跑新生发型':[26,27]}
dp2 =  {'多彩气球炫光[1]':44,
        '多彩气球炫光[2]':45,
        '汽车之家气球[紫]': 39,
        '汽车之家气球[黄]': 42,
        '黑妞生日气球[皇冠]': 36,
        '黑妞生日气球[帽子]': 43,
        '跑跑新生服饰[1]': 27,
        '跑跑新生服饰[2]': 34,
        '跑跑新生发型[1]': 26,
        '跑跑新生发型[2]': 27,
        } # 这些东西竟然有两个value
with open("danpin.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] in dp:
            print('wait!!!!!!!!!!!')
        dp[row[0]]=int(row[1])
with open("taopin.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        tp[row[0]]=int(row[1])

ff = open('data3.txt', 'w')

for id in range(1000000):
    print(id,end=' ')
    im = ImageGrab.grab(bbox=(400, 130, 1340, 1160))  # X1,Y1,X2,Y2
    # # time.sleep(5)
    im.save(f"img3/{id}.png")

    reader = easyocr.Reader(['ch_sim','en']) 
    # reader = easyocr.Reader(['ch_sim']) 
    # # 读取图像
    # result = reader.readtext(f'test1/3.png',detail=0)
    result = reader.readtext(np.array(im),detail=0)

    o = 0
    l = []
    ll = []
    for s in result:
        # print(s,'!')
        if s[:3]=='藏珍馆':
            o = 1
        if o:
            if ':' not in s and '+' not in s and '[' not in s:
                o = 0
                ll.append(''.join(l))
                l = []
            else:
                l.append(s)
            # print(l)
    if o:
        ll.append(''.join(l))
    
    for s in ll:
        # print(s)
        ff.write(str(id)+' '+s+'\n')
        while '[' in s or ']' in s:
            i = 0
            while s[i]!='[' and s[i]!=']':
                i += 1
            if s[i]=='[':
                if (s[i-1]==':' or s[i-2]==':') and i+8<len(s): # 前一对[]
                    oo = 1
                    for j in range(i+1,i+8):
                        if s[j]==']':
                            s = s[:i]+s[j+1:]
                            oo = 0
                            break
                    if oo:
                        s = s[:i]+s[i+7:] # 没配对就删后面6个字符
                    continue
                j = i+1
                while j<len(s) and (s[j].isdigit() or s[j].islower() or s[j].isupper() or s[j]=='-'):
                    j += 1
                if j<len(s) and s[j]==']': # 结束的第j位要 除非是']'
                    j += 1
                s = s[:i]+s[j:]
            else:
                j = i-1
                s = s[:i]+s[i+1:] if s[i-1]!='-' else s[:i-1]+s[i+1:]
        d = {'I':'1','g':'9','G':'6','O':'0'}
        for i in range(len(s)):
            if s[i] in d and (s[i-1].isdigit() or s[i-1] in d or i+1<len(s) and (s[i+1].isdigit() or s[i+1] in d)):
                s = s[:i]+d[s[i]]+s[i+1:]
        for i in range(len(s)):
            if s[i]=='0' and s[i-2:i]=='Pr':
                s = s[:i]+'o'+s[i+1:]
        for i in range(len(s)-1): # ' DJ' 后第一个+后数字和大写字母变DJ
            if s[i:i+3]==' DJ':
                j = i+3
                while j<len(s) and s[j]!='+':
                    j += 1
                k = j+1 # s[j]=='+'
                while k<len(s) and (s[k]==' ' or s[k].isdigit() or s[k].isupper()):
                    k += 1
                s = s[:j+1]+'DJ'+s[k:]
        for i in range(1,len(s)-1):
            if s[i]=='0' and not s[i-1].isdigit() and not s[i+1].isdigit():
                s = s[:i]+('O' if s[i+1].isupper() else 'o')+s[i+1:]
        for i in range(len(s)-4):
            if s[i:i+4]=='1000' or s[i:i+4]=='2023' or s[i:i+4]=='2022':
                s = s[:i]+' '+s[i+4:]
        
        m = {1:{'〈':'(','〉':')','孑':'子','芾':'带','麇':'麋','圭':'主','曰':'日','居':'尾','爰':'爱'},
             2:{'字航':'宇航','-夏':'一夏','2翼':'之翼','2星':'之星','7星':'之星','自色':'白色','滨o':'滨DJ','揭蛋':'捣蛋','萌鬼':'萌兔','告自':'告白','人7':'人Z','黑自':'黑白','末来':'未来','=角':'三角',
                '酉几':'西几','月镜':'目镜','-击':'一击','士著':'土著','@P':'CP','挑-':'挑一','自羊':'白羊','塞冰':'寒冰','战土':'战士','尺军':'R军'}}
        for size in range(1,3):
            for i in range(len(s)-size+1):
                w = s[i:i+size]
                if w in m[size]:
                    s = s[:i]+m[size][w]+s[i+size:]
        for i in range(3,len(s)-1): # 处理 S**车王/神炫光 中S识别成5的问题
            if s[i:i+2]=='车王' or s[i:i+2]=='车神':
                if s[i-2]=='5':
                    s = s[:i-2]+' S'+s[i-1:]
                elif s[i-3]=='5':
                    s = s[:i-3]+' S'+s[i-2:]
        
        # print(s)
        ff.write(str(id)+' '+s+'\n')

        # l = [w for w in sum([re.split("[:+/. ]", ''.join(j)) for i,j in groupby(re.sub(u'\\[.*?\\]','',s), key=lambda x: x.isdigit())],[]) if w]
        l = [w for w in sum([re.split("[';:+/., ]|`", ''.join(j)) for i,j in groupby(s, key=lambda x: x.isdigit() or x=='S')],[]) if w]
        # print(l)
        o = 0 # 1 单品 2 套品
        t = []
        for w in l:
            if w=='单品':
                o = 1
                continue
            elif w[:2]=='单品':
                o = 1
                w = w[2:]
            if w=='套品':
                o = 2
                continue
            elif w[:2]=='套品':
                o = 2
                w = w[2:]
            if o==1: # 单品
                if w.isdigit():
                    # if len(t)!=1:
                    #     print(id,'too long ',ss,' ! ',s)
                    if int(w)>200 and w[-1]=='1':
                        w = w[:-1]
                    w = int(w)
                    ss = ' '.join(t)
                    sp = '+'.join(t)
                    ls = t[-1]
                    t = []
                    if ls in dp and dp[ls]==w: # 最后一位有一样的不要了 防止前面有乱七八糟的东西
                        continue
                    if sp in tp and tp[sp]==w: # 套品有一样的也不要了
                        continue
                    if ss in dp and dp[ss]!=w: # 处理同物品不同value
                        if w<20 or w>200 or w%100==dp[ss]: # 可能前面多个1
                            continue
                        else:
                            ff.write(f'\n!!! {w} {id} {s}\n\n')
                    dp[ss] = w
                else:
                    t.append(w)
            elif o==2: # 套品
                if w.isdigit():
                    # if len(t)<=1:
                    #     print(id,'too short ',w,' ! ',s)
                    w = int(w)
                    ss = '+'.join(t)
                    t = []
                    if ss in tp and tp[ss]!=w: # 处理同物品不同value
                        if w<20 or w>200 or w%100==dp[ss]: # 可能前面多个1
                            continue
                        else:
                            ff.write(f'\n!!! {w} {id} {s}\n\n')
                    tp[ss] = w            
                else:
                    t.append(w)
    # print(dp,'\n',tp,'\n')
    with open("danpin.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(sorted(list(dp.items())+list(dp2.items()),key=lambda x:(-x[1],x[0])))
    with open("taopin.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(sorted(list(tp.items()),key=lambda x:(-x[1],x[0])))