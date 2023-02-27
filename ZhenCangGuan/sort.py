import numpy as np
import time
import pyscreenshot as ImageGrab
import easyocr
from itertools import groupby
import re
import csv


dp, tp =set(), set()
with open("dp1.1.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        dp.add((row[0],int(row[1])))
# with open("tp.csv", newline="") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         tp.add((row[0],int(row[1])))


with open("dp1.1.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(sorted(list(dp),key=lambda x:(-x[1],x[0])))
# with open("tpa.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(sorted(list(tp),key=lambda x:x[0]))




                    


            




    # # 结果
    # print(result)