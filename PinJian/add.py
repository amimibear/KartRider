import shutil
import os
import csv

def read_csv(file):
    d = {}
    reader = csv.reader(open(file))
    for row in reader:
        name, num = row[0], int(row[1])
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

def write_csv(filename, data):
    temp_filename = f"{filename}.tmp"
    with open(temp_filename, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    os.replace(temp_filename, filename)

def add(dp, dp0): # 往dp里加dp0
    for name in dp0:
        if name in dp:
            if dp0[name]!=dp[name]:
                print(f"不一样！ {name} {dp0[name]} {dp[name]}")
            else:
                print('已存在 ',name)
        dp[name] = dp0[name]

N = 1
while os.path.exists(f'data/data{N}.txt'):
    N += 1
N -= 1

dp,tp = [{},{}],[{},{}]
dp0,tp0 = [{},{}],[{},{}]

title = ['冰雪之歌','夜行骑士']

for n in range(2):
    for i in range(1000,0,-1): # 找第一个(权威认证)
        if os.path.exists(f"danpin{n}.{i}.csv"):
            dp[n] = read_csv(f"danpin{n}.{i}.csv")
            break
    for i in range(1000,0,-1): # 找第一个.1(权威认证)
        if os.path.exists(f"taopin{n}.{i}.csv"):
            tp[n] = read_csv(f"taopin{n}.{i}.csv")
            break

    dp0[n] = read_md(f"danpin{n}.md") # 新增未处理
    shutil.copy(f"danpin{n}.md",f"md/danpin{n}.{N}.md")
    open(f'danpin{n}.md', 'w')
    open(f'未处理_{title[n]}单品新增.md', 'w')
    tp0[n] = read_md(f"taopin{n}.md")
    shutil.copy(f"taopin{n}.md",f"md/taopin{n}.{N}.md")
    open(f'taopin{n}.md', 'w')
    open(f'未处理{title[n]}套品新增.md', 'w')
    

    add(dp[n],dp0[n])
    add(tp[n],tp0[n])




for n in range(2):
    danpin_data = sorted(list(dp[n].items()), key=lambda x: (-x[1], x[0]))
    write_csv(f"danpin{n}.csv", danpin_data)
    shutil.copy(f"danpin{n}.csv",f"danpin{n}.{N}.csv") # 记录一下每次的

    taopin_data = sorted(list(tp[n].items()), key=lambda x: (-x[1], x[0]))
    write_csv(f"taopin{n}.csv", taopin_data)
    shutil.copy(f"taopin{n}.csv",f"taopin{n}.{N}.csv")


