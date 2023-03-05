# 排序 查重 查少字

import csv


dp, tp = {}, {}

reader = csv.reader(open("danpin.csv"))
for row in reader:
    if row[0] in dp:
        print(row)
        continue
    dp[row[0]]=int(row[1])

for i in dp:
    if i[1:] in dp: # 防止少一个字
        print(i)

writer = csv.writer(open("danpin0.csv", "w"))
writer.writerows(sorted(list(dp.items()),key=lambda x:(-x[1],x[0])))
# writer.writerows([(i,j[0],j[1]) for i,j in enumerate(sorted(list(dp.items()),key=lambda x:(-x[1],x[0])),1)])

# tp

# with open("taopin.csv", newline="") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         if row[0] in tp:
#             print(row)
#             continue
#         tp[row[0]]=int(row[1])
# with open("taopin.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(sorted(list(tp.items()),key=lambda x:(-x[1],x[0])))


                    


            




    # # 结果
    # print(result)