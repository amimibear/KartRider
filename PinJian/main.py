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
# import paddleocr
# print(paddleocr.__version__)
# os.environ['PADDLE_OCR_LOG_LEVEL'] = 'ERROR'
# from paddleocr import paddleocr
# paddleocr.logging.disable(logging.DEBUG)
# paddleocr.paddleocr.logging.disable(logging.DEBUG)
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
title = ['冰雪之歌','夜行骑士']
dp, tp = [{},{}], [{},{}]
dp0, tp0 = [{},{}], [{},{}] # new
dpp = [{},{}] # danpin+ 给用户呈现的时候筛一遍
tpm = [{},{}] # 去、
# 这些东西竟然有两个品鉴值
double = [{'多彩气球炫光':[44,45],'汽车之家气球':[39,42],'黑妞生日气球':[36,43],'跑跑新生服饰':[27,34],'跑跑新生发型':[26,27],
          '礼花气球':[44,53],'章鱼气球':[37,47],'经典校服':[28,34],'南瓜假面':[39,59],'正义牛仔帽(男)':[37,39],'仙人掌气球':[43,51],'正义牛仔帽(女)':[36,37],'精灵炫光':[56,57]},
          {'礼花气球':[38,52],'仙人掌气球':[39,50],'章鱼气球':[35,50],'多彩气球炫光':[45,47],'黑妞生日气球':[34,40],'小丑气球':[36,39],
          '汽车之家气球':[32,37],'南瓜假面':[35,84],'跑跑新生服饰':[21,22],'跑跑新生发型':[15,16],'正义牛仔帽(男)':[34],'正义牛仔帽(女)':[34,36],'经典校服':[22,25]}] # 期待 正义牛仔帽(男),32 

# 特殊情况 空格被删 屏蔽词
special = {'FormulaE气球':'Formula E 气球','Formula E气球':'Formula E 气球'}#,'黑杰克**喷漆','腾讯***孩帽','腾讯***孩装'}
# 暂不用dlt
# dlt = {}

N = 1
while os.path.exists(f'data/data{N}.txt'):
    N += 1


def read_csv(file, diff={}):
    d = {}
    reader = csv.reader(open(file))
    for row in reader:
        name, num = row[0], int(row[1])
        if name in diff:
            continue
        assert(not name in d) # 无重复
        d[name] = num
    return d

def read_md(file):
    d = {}
    with open(file, 'r') as f:
        for line in f:
            parts = line.split('!')
            name, num = parts[0].split(',')
            assert(not name in d) # 无重复
            d[name] = int(num)
    return d

# 每次读最新的，没有筛选也没关系，之后通过delete.py直接筛掉
# 没有筛选会让错误的数值留下了，对的进不去，因为重复的直接忽略
for n in range(2):
    for i in range(1000,0,-1): # 找第一个(权威认证)
        if os.path.exists(f"danpin{n}.{i}.csv"):
            dp[n] = read_csv(f"danpin{n}.{i}.csv")
            break
    for i in range(1000,0,-1): # 找第一个(权威认证)
        if os.path.exists(f"taopin{n}.{i}.csv"):
            tp[n] = read_csv(f"taopin{n}.{i}.csv")
            break
    for name in tp[n]:
        tpm[n][name.replace('、','')]=tp[n][name]

    dp0[n] = read_md(f"danpin{n}.md") # 新增未处理
    tp0[n] = read_md(f"taopin{n}.md")
    dpp[n] = read_csv(f"danpin{n}+.csv")


# 暂不用delete
# reader = csv.reader(open("delete.csv"))
# for row in reader:
#     dlt[row[0]]=int(row[1])

# del_img = []


ff = open(f'data/data{N}.txt', 'w')
fmd = open(f'fmd.md', 'w')
# ff = open(f'data0.txt', 'w')

# ocr = PaddleOCR(use_angle_cls=False, lang='ch') # need to run only once to download and load model into memory # ocr_version='PP-OCRv2'
# 221
# ocr = PaddleOCR(rec_model_dir='ch_PP-OCRv4_rec_server_infer')
# 225
# PaddleOCR(rec_model_dir='ch_PP-OCRv4_rec_server_infer', det_model_dir='ch_PP-OCRv4_det_server_infer')

# 305 new

id0 = int(open(f'img/_ok.txt', 'r').read())+1

# id0 = 47101
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
     lambda x:baidu(x,'general_basic'), # 标准版 改这边要改k>=len(f)-1 or 2
     lambda x:baidu(x,'accurate_basic'), # 高精度版
     
     ]

test = 0

if test:
    id0 -= 100000
    id0 = 4915088
    id0 = 4954139
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
        if image.size != (650,950): # from S28
            crop_area = (400, 0, 1050, 950) # 定义裁剪区域 (x1, y1, x2, y2)
            image = image.crop(crop_area)
        RGB = np.array(image.convert('RGB'))
        # if not test:
        #     os.remove(f"img/{id}.png") # 如果有新增，最后再保存回去 中途停止会丢失数据
        if not np.any(np.all(RGB == [227, 104, 80], axis=-1)):
            if not test:
                os.remove(f"img/{id}.png")
                open('img/_ok.txt', 'w').write(str(id))
            print('no red!')
            print('no red!',file=ff)
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
    
    # 看最后一列像素 以是不是蓝色[251,253]分块 找出有红色(227)的块
    def find_blocks_with_conditions(arr, b_range=(251, 253)):
        b_in_range = np.logical_and(arr[:, -1, 2] >= b_range[0], arr[:, -1, 2] <= b_range[1])
        blocks = np.split(arr, np.where(np.diff(b_in_range) == 1)[0] + 1)
        valid_blocks = [block for block in blocks if np.any(block[:, -1, 2]==80)]
        return valid_blocks
    
    add = 0
    byy = 0 #是否有不一样的
    bd = 0

    valid_blocks = find_blocks_with_conditions(RGB)
    for block in valid_blocks:
        lines = np.split(block, np.where(np.diff(block[:,-1,0]==255) == 1)[0] + 1)
        for i in range(len(lines)):
            if len(lines[i])>120: # 超长的分两半 遇到套品了
                lines = lines[:i] + [lines[i][:50],lines[i][50:]] + lines[i+1:]
        first = f[0](lines[0]) # 冰雪之歌/夜行骑士
        if not first[0]: # title被遮挡 fisrt==[None]
            continue
        lines = lines[1:]
        Title = ''.join([line[1][0] for res in first for line in res])
        if "冰雪之歌" in Title:
            n = 0
        elif "夜行骑士" in Title:
            n = 1
        else:
            print('no title!')
            print('no title!',file=ff)
            continue
        
        danpin = 1 # 是否是单品
        for line in lines:
            if line.shape[0]<30:
                # print(line.shape[0])
                continue
            num = f[0](line[:,500:])
            if num==[None]: # 最后一行空的
                continue
            num = f[0](line[:,500:])[0][0][1][0]
            if not num.isdigit(): # 被遮挡 下一行
                continue
            num = int(num)
            for k in range(len(f)):
                print('ocr',k)
                print('ocr',k,file=ff)

                name = f[k](line[:,:500])
                if name==[None]: # 没识别出来，下一个ocr试试
                    continue
                # print(line[:,:500].shape,np.sum(line[:,:500]))
                # print(name)
                # try:
                if k>=len(f)-2: # 最后一/两个是baidu
                    bd = 1 # 用baidu就save
                    name = ''.join([l['words'] for l in name['words_result']])
                else:
                    name = ''.join([l[1][0] for res in name for l in res])
                # except:
                #     print('ocr fail!')
                #     print(name)
                #     continue
                if name[:2]=='单品':
                    assert(danpin==1)
                    name = name[2:]
                    line = line[40:]
                if name[:2]=='套品':
                    danpin = 0
                    name = name[2:]
                    line = line[40:]
                
                print('s0',name)
                print('s0',name,file=ff)
                
                m = {1:{'±':'+','：':':','（':'(','）':')','~':' ','|':' ','[':' ',']':' ','「':' ','－':'-','囊':'翼','［':' ','］':' ','」':' ','丨':' ','【':' ','】':' ','＋':'+','！':' ','，':' ','烊':'咩咩咩'},
                    2:{'萝下':'萝卜','一女':'-女','一男':'-男','型十':'型+','诸能':'储能','翘翔':'翱翔','翅翘':'翅','倒到':'倒','不到':'不倒','游夹':'游侠','铠电':'铠甲','骑土':'骑士','然擎':'燃擎','小五':'小丑','自镜':'目镜','钢电':'钢甲','魅景':'魅影','机电':'机甲','友型':'发型','萌免':'萌兔','手权':'手杖',
                        '翘膀':'翅膀','驾鸯':'鸳鸯','贺罗':'贺岁','战土':'战士','金生':'金牛','车团':'军团','育包':'背包','揭蛋':'捣蛋','友饰':'发饰','末来':'未来','胖敦':'胖墩','头盗':'头盔','定球':'足球','白勺':'的',
                        '手特':'手持','剪者':'勇者','龟电':'龟甲','统师':'统帅','愧木':'傀木','酉长':'酋长','飘虫':'瓢虫','撩牙':'獠牙',
                        '库呀':'库伢','库牙':'库伢','库讶':'库伢','吃语':'呓语','烊烊':'咩咩咩','垂髻':'垂髫'},
                    3:{'迷夜翼':'迷璘夜翼','烊烊烊':'咩咩咩','流氓免':'流氓兔','命运言':'命运箴言'}}
                    # 3:{}}
                for size in range(3,0,-1):
                    for i in range(len(name)-size+1):
                        w = name[i:i+size]
                        if w in m[size]:
                            name = name[:i]+m[size][w]+name[i+size:]
                if name=='': # '套品'?
                    print('no name!')
                    continue
                if name[-2]=='(':
                    name += ')'

                print('s1',name)
                print('s1',name,file=ff)

                # if test:
                #     Image.fromarray(line).save(f"new/dp{n}_{name},{num}.png")
                #     fmd.write(f'{name},{num}![](new/dp{n}_{name},{num}.png)\n')

                if danpin: # 单品的情况                         
                    print(f'dp{n} {name},{num}')
                    print(f'dp{n} {name},{num}',file=ff)
                    # if name in special or dp0[n]: # 新增未处理
                    if name in special:
                        name = special[name]
                    if name in dp0[n]:
                        if num==dp0[n][name]: # 新增未处理
                            break
                        else:
                            print(f'\nnew byy!!! {name} old:{dp0[n][name]} new:{num} 留old\n')
                            ff.write(f'\nnew byy!!! {name} old:{dp0[n][name]} new:{num} 留old\n')
                            byy = 1
                            break
                    
                    # if '***' in name: # 跑跑的bug
                    #     break
                    if name in double[n] and num in double[n][name]: # 两个值的
                        break
                    if name in dp[n] and dp[n][name]==num: # 重复
                        if not os.path.exists(f'数据来源/{title[n]} 单品/{num},{name}.png'):
                            image.save(f'数据来源/{title[n]} 单品/{num},{name}.png')
                        break
                    if name in dp[n] and dp[n][name]!=num: # 处理同物品不同value 不继续识别了 之后看怎么回事
                        print(f'\nbyy!!! {name} old:{dp[n][name]} new:{num} 留old\n')
                        ff.write(f'\nbyy!!! {name} old:{dp[n][name]} new:{num} 留old\n')
                        byy = 1
                        break
                    print('add?')
                    print('add?',file=ff)
                    if k==len(f)-1:
                        # dp就不改了
                        dp0[n][name] = num
                        # if name not in dpp: 最后给用户看的时候再筛dpp 不然tuji中数据没发再发现了
                        add = 1
                        print('add!')
                        print('add!',file=ff)
                        if not os.path.exists(f'数据来源/{title[n]} 单品/{num},{name}.png'):
                            image.save(f'数据来源/{title[n]} 单品/{num},{name}.png')
                        Image.fromarray(line).save(f"new/dp{n}_{name},{num}.png")
                else: # 套品   
                    print(f'tp{n} {name},{num}')
                    print(f'tp{n} {name},{num}',file=ff)
                    if name in tp0[n]:
                        if num==tp0[n][name]: # 新增未处理
                            break
                        else:
                            print(f'\nnew byy!!! {name} old:{tp0[n][name]} new:{num} 留old\n')
                            ff.write(f'\nnew byy!!! {name} old:{tp0[n][name]} new:{num} 留old\n')
                            byy = 1
                            break
                    if name in tp[n] and tp[n][name]==num: # 重复
                        if not os.path.exists(f'数据来源/{title[n]} 套品/{num},{name}.png'):
                            image.save(f'数据来源/{title[n]} 套品/{num},{name}.png')
                        break
                    if name in tp[n] and tp[n][name]!=num: # 处理同物品不同value
                        print(f'\nbyy!!! {name} old:{tp[n][name]} new:{num} 留old\n')
                        ff.write(f'\nbyy!!! {name} old:{tp[n][name]} new:{num} 留old\n')
                        byy = 1
                        break
                    if name.replace('、','') in tpm[n]: # 去、
                        break
                    brk = 0
                    for nm in tp[n]:
                        if name in nm and num==tp[n][nm]:
                            print(f'no tail! {len(nm)-len(name)}')
                            print(f'no tail! {len(nm)-len(name)}',file=ff)
                            brk = 1
                            break
                    if brk:
                        break
                    print('add?')
                    print('add?',file=ff)
                    if k==len(f)-1:
                        # tp就不改了
                        tp0[n][name] = num
                        tpm[n][name.replace('、','')] = num # tpm还是tp+tp0合一起的
                        add = 1
                        print('add!')
                        print('add!',file=ff)
                        if not os.path.exists(f'数据来源/{title[n]} 套品/{num},{name}.png'):
                            image.save(f'数据来源/{title[n]} 套品/{num},{name}.png')
                        Image.fromarray(line).save(f"new/tp{n}_{name},{num}.png")
    if bd or byy: 
        # image.save(f'img/{id}.png')
        if add:
            print('add!')
            print('add!',file=ff)
        else:
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
        if not test:
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
    
    def write_md(filename, data, pre):
        temp_filename = f"{filename}.tmp"
        with open(temp_filename, "w", newline='') as f:
            for name, num in data:
                f.write(f'{name},{num}![](new/{pre}_{name},{num}.png)\n  ')
        os.replace(temp_filename, filename)

    for n in range(2):

        danpin_data = sorted(list(dp0[n].items()), key=lambda x: (-x[1], x[0]))
        write_md(f"danpin{n}.md", danpin_data, f'dp{n}')
        danpin_data = sorted(list(set(dp0[n].items())-set(dpp[n].items())), key=lambda x: (-x[1], x[0]))
        write_md(f"{title[n]}单品新增(未处理).md", danpin_data, f'dp{n}')

        taopin_data = sorted(list(tp0[n].items()), key=lambda x: (-x[1], x[0]))
        write_md(f"taopin{n}.md", taopin_data, f'tp{n}')
        write_md(f"{title[n]}套品新增(未处理).md", taopin_data, f'tp{n}')
    
    if test:
        break

        

    
    # 


