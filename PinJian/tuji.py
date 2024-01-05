# 将图集(https://docs.qq.com/sheet/DZldVdXNmZHR2TXpC)中单品区的数据补充进来

import csv
import shutil
import time
import os

def add(dp, dp0): # 往dp里加dp0
    for name in dp0:
        if name in dp:
            if dp0[name]!=dp[name]:
                print(f"不一样！ {name} {dp0[name]} {dp[name]}")
            else:
                print('已存在 ',name)
        dp[name] = dp0[name]

dp= [{},{}] # 0: 冰雪之歌 1: 夜行骑士
tuji = [{'腾讯视频女孩帽':39},{'黑杰克处女喷漆':34,'腾讯视频女孩装':45,'正义牛仔帽(男)[新]':32}] # 应该加入图集 暂时没加入 (带**的)
for n in range(2):
    reader = csv.reader(open(f"danpin{n}.csv"))
    for row in reader:
        dp[n][row[0]]=int(row[1])

reader = csv.reader(open("【品鉴图集】（By 酥诺）-①冰雪 单品.csv"))
d = {
    '小丑气球':'小丑气球[红头发]',
    '汉服套装服饰 女':'汉服套装服饰(女)',
    '汉服套装服饰男':'汉服套装服饰(男)',
    '汉服套装发型男':'汉服套装发型(男)',
    '古风竞技服饰女':'古风竞技套装(女)',
    '古风竞技头套女':'古风竞技头套(女)',
    '真。猫爪气球':'真·猫爪气球',
    '磨菇气球':'蘑菇气球',
    '刘备粉喷漆':'刘备粉漆',
    '刘备橙喷漆':'刘备橙漆',
    '骑士雯雯紫色漆':'骑士雯雯紫漆',
    'CP赛永恒白金炫光':'CP联赛永恒白金炫光',
    '炼金学徒美美黄喷漆哈':'炼金学徒美美黄喷漆',
    '炼金学徒美美黑喷漆':'炼金学徒美美墨喷漆', #不一定？
    '女船长紫罗兰喷漆':'女武神紫罗兰喷漆', #不一定？
    '甜梦回声装\n(女)':'甜梦回声装',
     '刀螂战盔女':'刀螂战盔(女)',
     '宝宝贵族西服':'宝宝贵族西装',
     '阿特机械臂背装(背饰)':'阿特机械臂背装',
     '蛮族勇者服饰男':'蛮族勇者服饰(男)',
     '蛮族勇者服饰女':'蛮族勇者服饰(女)',
     '蛮族勇者发型男':'蛮族勇者发型(男)',
     '蛮族勇者发型女':'蛮族勇者发型(女)',
     '喜气连连服饰 男':'喜气连连服饰',
     '竹蜻蜓头饰(大)':'竹蜻蜓头饰',
     '章鱼气球[1]':'章鱼气球[3D]',
     '章鱼气球[2]':'章鱼气球[2D]',
     '海之灵发型 女':'海之灵发型(女)',
     '托尔夏季喷漆':'托尔季夏喷漆',
     '鹦鹅气球':'鹦鹉气球',
     '星际统帅服饰(男)':'星舰统帅服饰(男)',
     '星际统帅服饰(女)':'星舰统帅服饰(女)',
     '星际统帅发型(男)':'星舰统帅发型(男)',
     '星际统帅发型(女)':'星舰统帅发型(女)',
     '仙人掌气球[1](蓝)':'仙人掌气球[蓝]',
     '仙人掌气球[2](黄)':'仙人掌气球[黄]',
     '礼花气球[1]':'礼花气球[史诗]',
    '礼花气球[2]':'礼花气球[传说]',
    '多彩气球炫光[1]':'多彩气球炫光[蓝]',
    '多彩气球炫光2':'多彩气球炫光[绿]',
    '经典校服[1]':'经典校服[2]',
    '经典校服[2]':'经典校服[1]',
    '正义牛仔帽(女)[1]':'正义牛仔帽(女)[2]',
    '正义牛仔帽(女)[2]':'正义牛仔帽(女)[1]',
    '正义牛仔帽(男)[2]':'正义牛仔帽(男)[新]',
    '正义牛仔帽(男)[1]':'正义牛仔帽(男)[旧]',

     # '(银灰之翼)':'银辉之翼',
    # '打不完的气球':'炸不完的气球',
    # '七彩葫芦背饰':'七色幻化葫芦背包',
     #  '日月同辉神话面饰':'日月同辉',
    #  '兔年新春服':'兔年新春服(女)',
    #  'DJ音响(DJ少女背饰)':'DJ音响',
    #  '金兔限定套装(男)星光夺宝':'金兔限定套装(男)',
    #  '兔年新春服(男)(除夕理财男装)':'兔年新春服(男)',
    #  '皇家海军服':'皇家海军服(男)',
    #  '心悦炫光':'心悦专属炫光',
    #  '黑灰克处女喷漆':'黑杰克处女喷漆',
    #  '腾迅浏览器气球':'腾讯浏览器气球',
    #  '福䘵寿背饰':'福禄寿背饰',
    #  '赤焰炫光':'炽焰炫光',
    #  '赤焰翼':'炽焰翼',
    #  '赤焰日轮':'炽焰日轮',
     }
dd = [
    '精灵炫光'
    # '腾讯***孩装',
    #   '浪漫板口习习翼'
    # '爰心枕头背饰'
    ]
# dd = ['咒音书背饰','虎气球','瑞舞狮气球','多彩气球炫光','项循环炫光','黑妞生日气球','汽车之家气球','爰心枕头背饰','女雯雯绿喷漆','方块战土头盔',
#       '林客炫光','畏战旗','鹿气球','黑芾铂金牌气球','强水瓶喷漆','恐龙气球','萸灵面具','蓝芾铜牌气球','雨伞头饰','塞冰小屋气球','悦专属气球','悟空的金箍棒',
#       '蓝芾金牌气球','黑妞生日气球','跑跑新生服饰','跑跑新生发型','礼花气球','宝宝干斤坠气球','章鱼气球']

l = [(row[1].split(',')[0].replace('（','(').replace('）',')').replace('【','[').replace('】',']'),row[2],row[3]) for row in reader if row[1]][2:]
for name,num0,num1 in l:
    if name[-1]==' ':
        name = name[:-1]
    if name in d: # 纠正
        name = d[name]
    if name in dd: # 忽略
        continue
    
    # 夜行
    if num1.isdigit(): # 不一定有数值
        num1 = int(num1)
        if name not in dp[1]:
            tuji[1][name] = num1
            dp[1][name] = num1
        if name in dp[1] and dp[1][name]!=num1: # 不一样的以dp为准
            print('NO!',name,'tuji1',num1,'dp1',dp[1][name])
    
    # 冰雪
    if not num0.isdigit(): # 没数值要报错
        print('not digit! ',name,num0)
        continue
    num0 = int(num0)
    if name not in dp[0]:
        tuji[0][name] = num0
        dp[0][name] = num0
    # print(name,num0)
    if name in dp[0] and dp[0][name]!=num0:
        print('NO!',name,'tuji0',num0,'dp0',dp[0][name])

for n in range(2):
    print('tuji',n)
    for name,num in tuji[n].items():
        print(name,num)

for n in range(2):
    writer = csv.writer(open(f"tuji{n}.csv", "w"))
    writer.writerows(sorted(list(tuji[n].items()),key=lambda x:(-x[1],x[0])))
    writer = csv.writer(open(f"danpin{n}+.csv", "w"))
    writer.writerows(sorted(list(dp[n].items()),key=lambda x:(-x[1],x[0])))

# danpin+.py
title = ['冰雪之歌','夜行骑士']
for n in range(2):
    reader = csv.reader(open(f"danpin{n}.csv"))
    for row in reader:
        if row[0] in dp:
            print('重复!',row)
            continue
        dp[n][row[0]]=int(row[1])

    reader = csv.reader(open(f"tuji{n}.csv"))
    for row in reader:
        if row[0] in dp:
            print('重复!',row)
            continue
        dp[n][row[0]]=int(row[1])

    with open(f"danpin{n}+.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(sorted(list(dp[n].items()),key=lambda x:(-x[1],x[0])))

# write_md.py
from datetime import datetime
current_time = datetime.now()
formatted_time = current_time.strftime("%Y年%m月%d日")
title = ['冰雪之歌','夜行骑士']
fw = open('README.md','w')
tp = [open('taopin0.csv','r').read(),open('taopin1.csv','r').read()]
dp = [open('danpin0+.csv','r').read(),open('danpin1+.csv','r').read()]
lt = [len(tp[0].split('\n'))-1,len(tp[1].split('\n'))-1]
ld = [len(dp[0].split('\n'))-1,len(dp[1].split('\n'))-1]
fw.write(f'# 藏珍馆 单品/套品品鉴（冰雪之歌+夜行骑士）\nby 啊咪咪小熊  \n更新时间: {formatted_time}  \n原理: 用adb在安卓客户端上实时对世界频道截图传到电脑，然后用PaddleOCR读取文字信息并处理。  \n图集见[【品鉴图集】（By 酥诺）](https://docs.qq.com/sheet/DZldVdXNmZHR2TXpC)  \n欢迎大家在选单品时拉到最底部把已鉴定单品截图，共享到[品鉴运势截图 远程收集](https://docs.qq.com/sheet/DR1JkTHF1RlNzUEFj)里，数据会被统计进来。  \n\n\
主要数据文件:  \n冰雪之歌套品{lt[0]}.csv  \n冰雪之歌单品{ld[0]}.csv  \n夜行骑士套品{lt[1]}.csv  \n夜行骑士单品{ld[1]}.csv  \n\n\
## 冰雪之歌套品\n套品数据来自世界频道  \n\n冰雪之歌套品{lt[0]}.csv: \n```\n'+tp[0]+f'```\n\n## 冰雪之歌单品\n单品数据来自世界频道(danpin0.csv)和图集(tuji0.csv)  \n注:有些物品会有重名(多彩气球炫光、汽车之家气球、黑妞生日气球、跑跑新生服饰、跑跑新生发型、礼花气球、章鱼气球、经典校服、南瓜假面、正义牛仔帽(男)、正义牛仔帽(女)、仙人掌气球、小丑气球)，这些物品名后面加了[]以作区分  \n\n冰雪之歌单品{ld[0]}.csv:  \n```\n'+dp[0]+f'```\n\
## 夜行骑士套品\n套品数据来自世界频道  \n\n夜行骑士套品{lt[1]}.csv: \n```\n'+tp[1]+f'```\n\n## 夜行骑士单品\n单品数据来自世界频道(danpin0.csv)和图集(tuji0.csv)  \n注:有些物品会有重名(多彩气球炫光、汽车之家气球、黑妞生日气球、跑跑新生服饰、跑跑新生发型、礼花气球、章鱼气球、经典校服、南瓜假面、正义牛仔帽(男)、正义牛仔帽(女)、仙人掌气球、小丑气球)，这些物品名后面加了[]以作区分  \n\n夜行骑士单品{ld[1]}.csv:  \n```\n'+dp[1]+'```')

# 把所有以'冰雪之歌'或'夜行骑士'开头的文件移到'old'文件夹里
for filename in os.listdir():
    if filename.startswith('冰雪之歌') or filename.startswith('夜行骑士'):
        shutil.move(filename, 'old')

for n in range(2):
    open(f'{title[n]}单品{ld[n]}.csv','w').write(dp[n])
    open(f'{title[n]}套品{lt[n]}.csv','w').write(tp[n])


# CP联赛魅力金炫光 62
# 女船长紫罗兰喷漆 53
# 燃力重工炫光 45
# NO! 南瓜假面[绿叶] 39 59
# 腾讯浏览器气球 39
# 黑杰克处女喷漆 36