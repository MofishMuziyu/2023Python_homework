import numpy as np
import matplotlib.pyplot as plt

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


def bzc(source_list):
    return np.std(source_list)
time_list = dict_final["Time"]
index_time = []
index_time.append(time_list.index(2.0))
index_time.append(time_list.index(5.0))
index_time.append(time_list.index(10.0))
stand_error = []
for i in range(3):
    tmp = []
    for j in range(3,7):
        todo_list = dict_final[type_number[j]][:index_time[i]]
        tmp.append(bzc(todo_list))
    stand_error.append(tmp)
new_std = []
for i in range(4):
    tmp = []
    for j in range(3):
        tmp.append(stand_error[j][i])
    new_std.append(tmp)

plt.figure(figsize=(12,10))
X1 = ["Time:2" , "Time:5" , "Time:10"]
plt.subplot(2,2,1)
plt.ylabel("Temp")
plt.bar(X1,new_std[0])
plt.subplot(2,2,2)
plt.ylabel("Press")
plt.bar(X1,new_std[1])
plt.subplot(2,2,3)
plt.ylabel("Volume")
plt.bar(X1,new_std[2])
plt.subplot(2,2,4)
plt.ylabel("Density")
plt.bar(X1,new_std[3])

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

times = dict_final["Time"]
ts = dict_final["Temp"]
ps = dict_final["Press"]
vs = dict_final["Volume"]
ds = dict_final["Density"]
plt.figure(figsize=(12,10))

temp = plt.subplot(2,2,1)

plt.ylabel("Temp")
plt.plot(times,ts)
press = plt.subplot(2,2,2)

plt.ylabel("Press")
plt.plot(times,ps)
volume = plt.subplot(2,2,3)

plt.ylabel("Volume")
plt.plot(times,vs)
desity = plt.subplot(2,2,4)

plt.ylabel("Densitys")
plt.plot(times,ds)
temp.set_title("Temp-Time")
press.set_title("Press-Time")
volume.set_title("Volume-Time")
desity.set_title("Density-Time")

plt.tight_layout()
plt.show()

