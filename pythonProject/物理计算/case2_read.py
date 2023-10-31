import numpy as np
import matplotlib.pyplot as plt
filename = "data/case2.dat"
file = open(filename , "r")
lines = file.readlines()
line_length = len(lines)

items = []

def cope_timesplit(timesplit):
    dict_final = {}
    length = len(timesplit)
    dict_final["TIMESTEP"] = timesplit[1][0]
    dict_final["ATOMNUM"] = timesplit[3][0]
    dict_final["BOUND"] = []
    for i in range(5,8):
        for j in range(len(timesplit[i])):
            dict_final["BOUND"].append(timesplit[i][j])
    dict_final["ATOM"] = []
    for i in range(9,length):
        dict_final["ATOM"].append(timesplit[i])

    len_atom = int(dict_final["ATOMNUM"])
    for i in  range(len_atom-1):
        for j in range(i+1,len_atom):
            if dict_final["ATOM"][i][0] > dict_final["ATOM"][j][0]:
                tmp = dict_final["ATOM"][i].copy()
                dict_final["ATOM"][i] = dict_final["ATOM"][j]
                dict_final["ATOM"][j] = tmp


    return dict_final


for i in range(line_length):
    lines[i] = lines[i][:-1]
for i in range(line_length):
    lines[i] = lines[i].split()
    for j in range(len(lines[i])):
        try:
            lines[i][j] = float(lines[i][j])
        except:
            continue


timestep_index = []
for line in range(line_length):
    datalist = lines[line]
    if datalist[0] == "ITEM:":
        if datalist[1]=="TIMESTEP":
            timestep_index.append(line)

timesplit_list = []

for i in range(len(timestep_index)-1):
    tmp = lines[timestep_index[i]:timestep_index[i+1]]
    timesplit_list.append(tmp)
split_length = len(timesplit_list)

dict_all = []
for j in range(split_length):
    dict = cope_timesplit(timesplit_list[j])
    dict_all.append(dict)


##dict_all是已经读取的数据
dict_len = len(dict_all)

for step in range(dict_len):
    dict_step = dict_all[step]
    timestep = dict_step["TIMESTEP"]
    labelstep = " timestep:" + str(timestep)
    atom_num = dict_step["ATOMNUM"]
    bound = dict_step["BOUND"]
    atom_list = dict_step["ATOM"]
    x = []
    y = []
    z = []
    vx = []
    vy = []
    vz = []
    v = []
    atom_len = len(atom_list)
    plt.figure(figsize=(6, 5))
    for  j in range(atom_len):
        x.append(atom_list[j][2])
        y.append(atom_list[j][3])
        z.append(atom_list[j][4])
        vx.append(atom_list[j][5])
        vy.append(atom_list[j][6])
        vz.append(atom_list[j][7])
        tmp_v = np.sqrt(vx[j]**2 + vy[j]**2 + vz[j]**2)
        v.append(tmp_v)

    plt.title("Velocity distribution histogram" + labelstep)
    plt.ylabel("Velocity")

    plt.hist(v,bins=50,alpha=0.5,label=labelstep)

    plt.figure(figsize=(6,5))
    plt.title("x-vx" + labelstep)
    plt.xlabel("x")
    plt.ylabel("vx")
    plt.scatter(x,vx)
plt.show()


