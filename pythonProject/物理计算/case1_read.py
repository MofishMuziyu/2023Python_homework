import numpy as np
filename = "data/case1.dat"
file = open(filename,"r")
lines = file.readlines()
# print(lines[14:16])
lines = lines[14:]
ll = len(lines)
data = []
for i in range(ll):
    lines[i] = lines[i][:-2]
for j in range(1,ll):
    data.append([float(i) for i in lines[j].split()])
type_number = lines[0].split()
length = len(type_number)
dict_final = {}
for i in range(length):
    dict_final[type_number[i]] = []


for line in range(len(data)):
    for col in range(length):
        dict_final[type_number[col]].append(data[line][col])


def p_out(type_name):
    global  dict_final
    print(type_name+"的数据个数为：",len(dict_final[type_name]))
    print(type_name+"的最大值为：",max(dict_final[type_name]))
    print(type_name + "的最小值为：", min(dict_final[type_name]))
    print(type_name + "的均值为：", sum(dict_final[type_name])/len(dict_final[type_name]))
    print(type_name + "的标准差为：", np.std(dict_final[type_name]))
    return


for i in range(3,length):
    p_out(type_number[i])

