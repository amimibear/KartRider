import numpy as np
from PIL import Image
import io
# import easyocr
from itertools import groupby
import re
import csv
import time
import os
from datetime import datetime

# 先不考虑呈现给用户（新增数据尽量少）

from paddleocr import PaddleOCR
import paddleocr
print(paddleocr.__version__)
# 27 到 47100
# 28 到 30733
# 40 到 67597
# 41 30733 开始
# time.sleep(10)
# 77 开始几乎不留图 但要注意data里重复的!!!


import base64
import urllib
import requests

API_KEY = "FDFllVs3NVceP57oF2lkHSGF"
SECRET_KEY = "2NFAtZGj32esWgdI9hOVBqYg6nhvLiH3"

def baidu(arr,type):
    # image 可以通过 get_file_content_as_base64("C:\fakepath\kui.png",True) 方法获取
    
    # 标准版
    # url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + get_access_token()
    # payload='detect_direction=false&detect_language=false&paragraph=false&probability=false&image='+array2base64(arr,True)
    
    # 高精度版
    url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/{type}?access_token=" + get_access_token()
    payload='detect_direction=false&paragraph=false&probability=false&image='+array2base64(arr,True)
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    print(response.text,file=ff)
    return response.json()
    

def array2base64(arr, urlencoded=False):
    """
    将numpy数组转换为base64编码
    :param arr: numpy数组
    :return: base64编码
    """
    image = Image.fromarray(arr)

    # 创建一个内存缓冲区
    buffer = io.BytesIO()

    # 将图像保存到内存缓冲区中
    image.save(buffer, format='PNG')
    if test:
        image.save(f"{id}.png")

    # 获取缓冲区的字节数据
    buffer.seek(0)
    image_bytes = buffer.getvalue()
    content = base64.b64encode(image_bytes).decode("utf8")
    if urlencoded:
        content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))




# im = ImageGrab.grab()  # X1,Y1,X2,Y2
# for i in range(10):
#     im = ImageGrab.grab(bbox=(400, 130, 1340, 1160))  # X1,Y1,X2,Y2
#     time.sleep(5)
#     # save image file
#     print(type(im))
#     im.save(f"a0{i}.png")

# exit()

dp, tp = [{},{}], [{},{}]
dp0, tp0 = [{},{}], [{},{}] # new
dpp = [{},{}] # danpin+ 给用户呈现的时候筛一遍
# 这些东西竟然有两个品鉴值
double = [{'多彩气球炫光':[44,45],'汽车之家气球':[39,42],'黑妞生日气球':[36,43],'跑跑新生服饰':[27,34],'跑跑新生发型':[26,27],
          '礼花气球':[44,53],'章鱼气球':[37,47],'经典校服':[28,34],'南瓜假面':[39,59],'正义牛仔帽(男)':[37,39],'仙人掌气球':[43,51],'正义牛仔帽(女)':[36,37]},
          {'礼花气球':[38,52],'仙人掌气球':[39,50],'章鱼气球':[35,50],'多彩气球炫光':[45,47],'黑妞生日气球':[34,40],'小丑气球':[36,39],
          '汽车之家气球':[32,37],'南瓜假面':[35,84],'跑跑新生服饰':[21,22],'跑跑新生发型':[15,16],'正义牛仔帽(男)':[34]}] # 期待 正义牛仔帽(男),32 

# 特殊情况 空格被删 屏蔽词
special = {'FormulaE气球','黑杰克**喷漆','腾讯***孩帽','腾讯***孩装'}
# 暂不用dlt
# dlt = {}

N = 1
while os.path.exists(f'data/data{N}.txt'):
    N += 1


def readcsv(file, diff={}):
    d = {}
    reader = csv.reader(open(file))
    for row in reader:
        name, num = row[0], int(row[1])
        if name in diff:
            continue
        assert(not name in d) # 无重复
        d[name] = num
    return d

# 每次读最新的，没有筛选也没关系，之后通过delete.py直接筛掉
# 没有筛选会让错误的数值留下了，对的进不去，因为重复的直接忽略
for n in range(2):
    for i in range(1000,0,-1): # 找第一个.1(权威认证)
        if os.path.exists(f"danpin{n}.{i}.1.csv"):
            dp[n] = readcsv(f"danpin{n}.{i}.1.csv")
            break
    for i in range(1000,0,-1): # 找第一个.1(权威认证)
        if os.path.exists(f"taopin{n}.{i}.1.csv"):
            tp[n] = readcsv(f"taopin{n}.{i}.1.csv")
            break
    dp0[n] = readcsv(f"danpin{n}0.csv")
    tp0[n] = readcsv(f"taopin{n}0.csv")
    dpp[n] = readcsv(f"danpin{n}+.csv")
    

# 暂不用delete
# reader = csv.reader(open("delete.csv"))
# for row in reader:
#     dlt[row[0]]=int(row[1])

# del_img = []


ff = open(f'data/data{N}.txt', 'w')
# ff = open(f'data0.txt', 'w')

# ocr = PaddleOCR(use_angle_cls=False, lang='ch') # need to run only once to download and load model into memory # ocr_version='PP-OCRv2'
# 221
# ocr = PaddleOCR(rec_model_dir='ch_PP-OCRv4_rec_server_infer')
# 225
# PaddleOCR(rec_model_dir='ch_PP-OCRv4_rec_server_infer', det_model_dir='ch_PP-OCRv4_det_server_infer')

# 305 new

id0 = int(open(f'img/_ok.txt', 'r').read())+1

# id0 = 47101

# 556ab6 蓝 25~47
# c949e0 紫 51～80
# ffe96c 黄 81~108
# da664f 红 121～121

cls = ['556ab6','556a66'
       'c949e0','o949e0',
       'ffe96c','tfe96c',
       'da664f']

# reader = easyocr.Reader(['ch_sim','en']) 
# for id in range(id0,id0+1000):
ocr1 = PaddleOCR() # need to run only once to download and load model into memory # ocr_version='PP-OCRv2'
ocr2 = PaddleOCR(det_model_dir='ch_PP-OCRv4_det_server_infer')
# ocr2 = PaddleOCR(rec_algorithm='CRNN'),
ocr3 = PaddleOCR(rec_model_dir='ch_PP-OCRv4_rec_server_infer')
ocr4 = PaddleOCR(rec_model_dir='ch_PP-OCRv4_rec_server_infer', det_model_dir='ch_PP-OCRv4_det_server_infer')
f = [lambda x:ocr1.ocr(x, cls=False),
     lambda x:ocr1.ocr(x[:-1], cls=False),
     lambda x:ocr2.ocr(x, cls=False),
     lambda x:ocr2.ocr(x[:-1], cls=False),
     lambda x:ocr3.ocr(x, cls=False),
     lambda x:ocr3.ocr(x[:-1], cls=False),
     lambda x:ocr4.ocr(x, cls=False),
     lambda x:ocr4.ocr(x[:-1], cls=False),
     lambda x:baidu(x,'accurate_basic'), # 高精度版
    #  lambda x:baidu(x,'general_basic'), # 标准版 改这边要改k>=len(f)-1 or 2
     ]

test = 0

if test:
    id0 -= 100000
    id0 = 341287
for id in range(id0,10000000):
# for id in range(4671788,4671789):
    if not test:
        print(f'\n{id}')
    print(f'\n{id}',file=ff)

    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_time)
    print(formatted_time,file=ff)
    with open(f'img/_.txt', 'r') as fr:
        try:
            id1 = int(fr.read())
        except:
            pass
    # result = ocr.ocr(f'img/{id}.png', cls=False)
    if not os.path.exists(f'img/{id}.png'):
        if id>id1-3: # 到前沿了
            while not os.path.exists(f'img/{id}.png'):
                print('wait')
                time.sleep(1)
    try:
        if id>id1-3:
            time.sleep(2) # 前沿不能太快，可能有文件但是没存好
        if not os.path.exists(f'img/{id}.png'):
            if not test:
                print('no img!')
                print('no img!',file=ff)
        image = Image.open(f'img/{id}.png')
        if image.size != (850,950):
            crop_area = (400, 0, 1250, 950) # 定义裁剪区域 (x1, y1, x2, y2)
            image = image.crop(crop_area)
        RGB = np.array(image.convert('RGB'))
        # if not test:
        #     os.remove(f"img/{id}.png") # 如果有新增，最后再保存回去 中途停止会丢失数据
        if not np.any(np.all(RGB == [237, 163, 163], axis=-1)):
            if not test:
                os.remove(f"img/{id}.png")
            print('no pink!')
            print('no pink!',file=ff)
            continue
    
        
    except:
        if test:
            continue
        print('fail!')
        print('fail!',file=ff)
        if os.path.exists(f'img/{id}.png'):
            print('remove!')
            os.remove(f"img/{id}.png")
        continue
    if test:
        print(f'\n{id}')
    def find_blocks_with_conditions(arr, b_range=(251, 253)):
        b_in_range = np.logical_and(arr[:, -1, 2] >= b_range[0], arr[:, -1, 2] <= b_range[1])
        blocks = np.split(arr, np.where(np.diff(b_in_range) == 1)[0] + 1)
        valid_blocks = [block for block in blocks if np.any(block[:, -1, 2]==163)]
        return valid_blocks
    
    add = 0
    byy = 0 #是否有不一样的
    bd = 0
    for k in range(len(f)):
        print('ocr',k)
        print('ocr',k,file=ff)
        brk = 0
        ll = [[],[]]
        valid_blocks = find_blocks_with_conditions(RGB)
        for block in valid_blocks:
            result = f[k](block)
            try:
                if k>=len(f)-1: # 最后一/两个是baidu
                    bd = 1 # 用baidu就save
                    s = ''.join([line['words'] for line in result['words_result']])
                else:
                    s = ''.join([line[1][0] for res in result for line in res])
                if "冰雪之歌" in s:
                    ll[0].append(s)
                if "夜行骑士" in s:
                    ll[1].append(s)
            except:
                print('ocr fail!')
                print(result)
                continue
        for n in range(2):
            for s in ll[n]:
                print('s0',s)
                print('s0',s,file=ff)
                # ff.write(str(id)+' '+s+'\n')

                # 处理颜色代码bug

                ket = ['1','l','J'] # 把括号识别成这些
                
                for j in [6,5,4]:
                    for i in range(len(s)-j): # 后j位一样
                        w = s[i:i+j].lower()
                        if sum(w==cl[-j:] for cl in cls):
                            l,r = i,i+j
                            if i and s[i-1] in ket:
                                l -= 1
                            if i+j<len(s) and (s[i+j]=='l' or s[i+j]=='J'):
                                    r += 1
                            if i+j<len(s) and s[i+j]=='1':
                                if w[-4:] in ['6ab6','6a66','49e0']:
                                        r += 1
                                # if w=='da664f':
                                #     if i+9<len(s) and s[i+6]=='1' and s[i+7]=='1' and : # 1121怎么办？去前还是去后？

                                if w[-4:] == 'e96c':
                                    if i+j+1<len(s) and (s[i+j+1]=='8' or s[i+j+1]=='9' or s[i+j+1]=='1'): # 黄色没有110+
                                        r += 1
                            s = s[:l]+' '+s[r:]
                    for i in range(len(s)-j):  # 前j位一样
                        w = s[i:i+j].lower()
                        if sum(w==cl[:j] for cl in cls):
                            l,r = i,i+j
                            if i and s[i-1] in ket:
                                l -= 1
                            if i+j<len(s) and (s[i+j]=='l' or s[i+j]=='J'):
                                    r += 1
                            if i+j<len(s) and s[i+j]=='1':
                                if w[1:4] in ['56a','949']:
                                        r += 1
                                # if w=='da664f':
                                #     if i+9<len(s) and s[i+6]=='1' and s[i+7]=='1' and : # 1121怎么办？去前还是去后？

                                if w[1:4] == 'fe9':
                                    if i+j+1<len(s) and (s[i+j+1]=='8' or s[i+j+1]=='9' or s[i+j+1]=='1'): # 黄色没有110+
                                        r += 1
                            s = s[:l]+' '+s[r:]

                # for i in range(len(s)-4):
                #     if s[i:i+4]=='1000' or s[i:i+4]=='2023' or s[i:i+4]=='2022':
                #         s = s[:i]+' '+s[i+4:]
                
                m = {1:{'±':'+','：':':','（':'(','）':')','~':' ','|':' ','[':' ',']':' ','「':' ','－':'-','囊':'翼','［':' ','］':' ','」':' ','丨':' ','【':' ','】':' ','＋':'+','！':' ','，':' ','烊':'咩咩咩'},
                    2:{'萝下':'萝卜','一女':'-女','一男':'-男','型十':'型+','诸能':'储能','翘翔':'翱翔','翅翘':'翅','倒到':'倒','不到':'不倒','游夹':'游侠','铠电':'铠甲','骑土':'骑士','然擎':'燃擎','小五':'小丑','自镜':'目镜','钢电':'钢甲','魅景':'魅影','机电':'机甲','友型':'发型','萌免':'萌兔','手权':'手杖',
                        '翘膀':'翅膀','驾鸯':'鸳鸯','贺罗':'贺岁','战土':'战士','金生':'金牛','车团':'军团','育包':'背包','揭蛋':'捣蛋','友饰':'发饰','末来':'未来','胖敦':'胖墩','头盗':'头盔','定球':'足球','白勺':'的',
                        '手特':'手持','剪者':'勇者','龟电':'龟甲','统师':'统帅','愧木':'傀木','酉长':'酋长','飘虫':'瓢虫','撩牙':'獠牙',
                        '库呀':'库伢','库牙':'库伢','库讶':'库伢','吃语':'呓语','烊烊':'咩咩咩','垂髻':'垂髫'},
                    3:{'迷夜翼':'迷璘夜翼','烊烊烊':'咩咩咩','流氓免':'流氓兔'}}
                    # 3:{}}
                for size in range(3,0,-1):
                    for i in range(len(s)-size+1):
                        w = s[i:i+size]
                        if w in m[size]:
                            s = s[:i]+m[size][w]+s[i+size:]
                # for i in range(3,len(s)-1): # 处理 S**车王/神炫光 中S识别成5的问题
                #     if s[i:i+2]=='车王' or s[i:i+2]=='车神':
                #         if s[i-2]=='5':
                #             s = s[:i-2]+' S'+s[i-1:]
                #         elif s[i-3]=='5':
                #             s = s[:i-3]+' S'+s[i-2:]
                i = 0
                while i<len(s):
                    if s[i]=='S': # 分割 S**车王/神炫光
                        s = s[:i]+' '+s[i:]
                        i += 1
                    i += 1
                
                print('s1',s)
                print('s1',s,file=ff)
                # ff.write(str(id)+' '+s+'\n')

                # l = [w for w in sum([re.split("[:+/. ]", ''.join(j)) for i,j in groupby(re.sub(u'\\[.*?\\]','',s), key=lambda x: x.isdecimal())],[]) if w]
                l = [w for w in sum([re.split("[';:/·, ]|`", ''.join(j)) for i,j in groupby(s, key=lambda x: x.isdecimal() or x=='S')],[]) if w]
                print('l',l)
                print('l',l,file=ff)
                o = 0 # 1 单品 2 套品
                t = []
                for w in l:
                    if w[0]=='-':
                        w = w[1:]
                        if not w:
                            continue
                    if w=='单品':
                        o = 1
                        t = []
                        continue
                    elif w[:2]=='单品':
                        o = 1
                        t = [w[2:]]
                        continue
                    if w=='套品':
                        o = 2
                        t = []
                        continue
                    elif w[:2]=='套品':
                        o = 2
                        t = [w[2:]]
                        continue
                    elif w[1:3]=='套品':
                        o = 2
                        t = [w[3:]]
                        continue
                    if o==1: # 单品
                        if w.isdecimal() and len(w)>1 and w not in ['1000','2021','2022','2023','10000','20520']: #一位数字加入文字中
                            # 处理t
                            if not t: # 防止 t[-1] 报错
                                ff.write(f'\n??? {w} {id} {s}\n')
                                continue
                            ss = ''.join(t)
                            # ss = ss.replace('^','','|','_')
                            sp = '+'.join(t)
                            while ss and ss[0] in ['-','l','品']:
                                ss = ss[1:]
                            if ss and ss[-1]=='开':
                                ss = ss[:-1]
                            ls = t[-1]
                            t = []

                            if int(w)>200:
                                if w[0]=='1': #三位数
                                    t.append(w[3:])
                                    w = w[:3]
                                else: #两位数
                                    t.append(w[2:])
                                    w = w[:2]
                            w = int(w)
                            
                            print(f'dp{n} {ss},{w}')
                            print(f'dp{n} {ss},{w}',file=ff)
                            if ss in special or dp0[n]: # 新增未处理
                                continue
                            if '***' in ss: # 跑跑的bug
                                continue
                            # if ss in dlt and w==dlt[ss] and not test: # delete
                            #     continue
                            if ss in double[n] and w in double[n][ss]: # 两个值的
                                continue
                            if ss=='气球' and w in [91,39,31,36,41] or ss=='天气球' and w in [81,44] or ss=='头饰' and w==91:
                                continue
                            if ls in dp[n] and dp[n][ls]==w: # 最后一位有一样的不要了 防止前面有乱七八糟的东西
                                continue
                            if sp in tp and tp[n][sp]==w: # 套品有一样的也不要了
                                continue
                            if ss in dp[n] and dp[n][ss]==w: # 重复
                                continue
                            if ss in dp[n] and dp[n][ss]!=w: # 处理同物品不同value
                                if not (w<20 or w>200 or w%100==dp[n][ss]): # 可能前面多个1
                                    print(f'\nbyy!!! {ss} old:{dp[n][ss]} new:{w} 留old\n')
                                    ff.write(f'\nbyy!!! {ss} old:{dp[n][ss]} new:{w} 留old\n')
                                    byy = 1
                                continue
                            print('add?')
                            print('add?',file=ff)
                            if k==len(f)-1:
                                dp[n][ss] = w
                                # if ss not in dpp: 最后给用户看的时候再筛dpp 不然tuji中数据没发再发现了
                                dp0[n][ss] = w
                                add = 1
                                print('add!')
                                print('add!',file=ff)
                            else:
                                brk = 1
                                break
                        else:
                            t.append(w)
                    elif o==2: # 套品
                        if w.isdecimal() and len(w)>1 and w not in ['1000','2021','2022','2023','10000','20520']: # 一位数字加入文字中
                            if not t: # 防止 t[-1] 报错
                                ff.write(f'\n??? {w} {id} {s}\n')
                                continue
                            if t[-1]=='l':
                                t.pop()
                            ss = ''.join(t)
                            while ss and ss[0] in ['-','l','+']:
                                ss = ss[1:]
                            while ss and ss[-1] in ['开','+','.']:
                                ss = ss[:-1]
                            # ss = ss.replace('^','')
                            t = []
                            

                            if int(w)>200:
                                if w[0]=='1': #三位数
                                    t.append(w[3:])
                                    w = w[:3]
                                else: #两位数
                                    t.append(w[2:])
                                    w = w[:2]

                            # if len(t)<=1:
                            #     print(id,'too short ',w,' ! ',s)
                            w = int(w)
                            
                            print(f'tp{n} {ss},{w}')
                            print(f'tp{n} {ss},{w}',file=ff)
                            # if ss in dlt and w==dlt[ss] and not test: # delete
                            #     continue
                            if ss in tp0[n]: # 新增未处理
                                continue
                            if ss in tp[n] and tp[n][ss]==w: # 重复
                                continue
                            if ss in tp[n] and tp[n][ss]!=w: # 处理同物品不同value
                                if not (w<20 or w>200 or w%100==tp[n][ss]): # 可能前面多个1
                                    print(f'\nbyy!!! {ss} old:{tp[n][ss]} new:{w} 留old\n')
                                    ff.write(f'\nbyy!!! {ss} old:{tp[n][ss]} new:{w} 留old\n')
                                    byy = 1 # 可以考虑save和brk合并
                                continue
                            print('add?')
                            print('add?',file=ff)
                            if k==len(f)-1:
                                tp[n][ss] = w
                                tp0[n][ss] = w
                                add = 1
                                print('add!')
                                print('add!',file=ff)
                            else:
                                brk = 1
                                break
                        else:
                            t.append(w)
                if brk:
                    break
            if brk:
                break
        # if brk:
        #     image.save(f'img/{id}.png') # 调试 用test
        #     print('brk')
        if not brk: # 如果这个ocr函数break，就让下一个orc函数再试试
            break
            # with open('del_img.txt', 'a') as f:
            #     f.seek(0,2)
            #     f.write(str(i)+'\n')
    if bd or byy: 
        # image.save(f'img/{id}.png')
        if not add:
            print('no add!')
            print('no add!',file=ff)
        if byy:
            print('byy!')
            print('byy!',file=ff)
        if bd:
            print('baidu!') # ocr 6
            print('baidu!',file=ff)
        print('save!')
        print('save!',file=ff)
    else:
        print('remove!')
        print('remove!',file=ff)
        os.remove(f"img/{id}.png")
    if not test:
        open('img/_ok.txt', 'w').write(str(id))

    # print(dp,'\n',tp,'\n')


    def write_csv(filename, data):
        temp_filename = f"{filename}.tmp"
        with open(temp_filename, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

        os.replace(temp_filename, filename)

    title = ['冰雪之歌','夜行骑士']
    for n in range(2):
        danpin_data = sorted(list(dp[n].items()), key=lambda x: (-x[1], x[0]))
        write_csv(f"danpin{n}.{N}.0.csv", danpin_data)

        taopin_data = sorted(list(tp[n].items()), key=lambda x: (-x[1], x[0]))
        write_csv(f"taopin{n}.{N}.0.csv", taopin_data)

        danpin_data = sorted(list(dp0[n].items()), key=lambda x: (-x[1], x[0]))
        write_csv(f"danpin{n}0.csv", danpin_data)
        danpin_data = sorted(list(set(dp0[n].items())-set(dpp[n].items())), key=lambda x: (-x[1], x[0]))
        write_csv(f"{title[n]}单品新增(未处理)", danpin_data)

        taopin_data = sorted(list(tp0[n].items()), key=lambda x: (-x[1], x[0]))
        write_csv(f"taopin{n}0.csv", taopin_data)
        write_csv(f"{title[n]}套品新增(未处理)", taopin_data)

        

    
    # 


