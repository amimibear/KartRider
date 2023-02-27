# KartRider
跑跑卡丁车手游
定制化小屋最高繁荣度方案

使用方式：
在定制化小屋繁荣.cpp中修改自己的摆件信息并运行，输出得到out.txt
运行plot.ipynb将out.txt中的方案可视化

算法：
在给定限制条件下(如有无魔毯、魔怪，有多少个林中飞机、拍照板等)，穷举所有繁荣度高于阈值（初值可设为当前繁荣度）的满足面积大小搭配方案（如2个8\*8,1个7\*7,9个6\*6...10个1\*1等），
并检验其是否能塞入地图中，若能塞入则记录并更新阈值，直到搜索完所有方案，即给出当前限制下最高繁荣度方案。