# 排序 查重 查少字

import csv


dp, tp = {}, {}

reader = csv.reader(open("danpin.csv"))
for row in reader:
    if row[0] in dp:
        print('重复!',row)
        continue
    dp[row[0]]=int(row[1])

# # merge
# reader = csv.reader(open("danpin24.1.csv")) # 从这个文件中的所有都加入
# for row in reader:
#     if row[0] in dp and int(row[1])!=dp[row[0]]:
#         print('不一样!',row)
#         continue
#     dp[row[0]]=int(row[1])

for i in dp:
    if i[1:] in dp: # 防止少一个字
        print(i)

# 红锦鲤头饰 锦鲤头饰
# 小白虎气球 白虎气球
# 红蘑菇气球 蘑菇气球
# 绿蘑菇气球 蘑菇气球
# 星彩虹手套气球 彩虹手套气球

writer = csv.writer(open("danpin.csv", "w"))
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