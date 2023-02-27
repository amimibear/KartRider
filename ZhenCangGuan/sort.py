import numpy as np
import time
import pyscreenshot as ImageGrab
import easyocr
from itertools import groupby
import re
import csv


dp, tp, dp2 = {}, {}, {}

# dp2 =  {'多彩气球炫光[1]':44,
#         '多彩气球炫光[2]':45,
#         '汽车之家气球[紫]': 39,
#         '汽车之家气球[黄]': 42,
#         '黑妞生日气球[皇冠]': 36,
#         '黑妞生日气球[帽子]': 43,
#         '跑跑新生服饰[1]': 27,
#         '跑跑新生服饰[2]': 34,
#         '跑跑新生发型[1]': 26,
#         '跑跑新生发型[2]': 27,
#         } # 这些东西竟然有两个value

# dp

with open("dp.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] in dp:
            dp2[row[0]]=int(row[1])
            print(row)
            continue
        dp[row[0]]=int(row[1])

print(dp2)

with open("dp0.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(sorted(list(dp.items())+list(dp2.items()),key=lambda x:(-x[1],x[0])))


# tp

# with open("tp.csv", newline="") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         if row[0] in tp:
#             print(row)
#             continue
#         tp[row[0]]=int(row[1])
# with open("tp.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(sorted(list(tp.items()),key=lambda x:(-x[1],x[0])))


                    


            




    # # 结果
    # print(result)