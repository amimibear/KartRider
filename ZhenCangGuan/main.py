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


# from cnocr import CnOcr

# img_fp = 'box05.png'
# ocr = CnOcr() 
# out = ocr.ocr(img_fp)

# print(out)

# exit()



dp, tp =set(), set()
with open("dp.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        dp.add((row[0],int(row[1])))
with open("tp.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        tp.add((row[0],int(row[1])))

ff = open('screen.txt', 'w')

for id in range(1000000):
    print(id)
    im = ImageGrab.grab(bbox=(400, 130, 1340, 1160))  # X1,Y1,X2,Y2
    # # time.sleep(5)
    im.save(f"img2/{id}.png")

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
        print(s)
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
                s = s[:i]+' '+s[:i+4]
        print(s)
        ff.write(str(id)+' '+s+'\n')

        # l = [w for w in sum([re.split("[:+/. ]", ''.join(j)) for i,j in groupby(re.sub(u'\\[.*?\\]','',s), key=lambda x: x.isdigit())],[]) if w]
        l = [w for w in sum([re.split("[':+/. ]", ''.join(j)) for i,j in groupby(s, key=lambda x: x.isdigit())],[]) if w]
        print(l)
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
            if o==1:
                if w.isdigit():
                    if int(w)>200 and w[-1]=='1':
                        w = w[:-1]
                    ss = ' '.join(t)
                    if len(t)!=1:
                        print(id,'too long ',ss,' ! ',s)
                    dp.add((ss,int(w)))
                    t = []
                else:
                    t.append(w)
            elif o==2:
                if w.isdigit():
                    if len(t)<=1:
                        print(id,'too short ',w,' ! ',s)
                    ss = '+'.join(t)
                    tp.add((ss,int(w)))
                    t = []
                else:
                    t.append(w)
    # print(dp,'\n',tp,'\n')
    with open("dp.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(sorted(list(dp),key=lambda x:(-x[1],x[0])))
    with open("tp.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(sorted(list(tp),key=lambda x:(-x[1],x[0])))




                    


            




    # # 结果
    # print(result)