#lordv V0  Rx
#mulv v2 a v0

#lordv V3  Ry
#addv v4 v3 v2
#store v4
#设计：一个储存器（不算设计，利用原本处理器的的内存即可），一个64*64位的向量寄存器，一些数据旁路的连线，用来进行链接

N = 64            ##向量宽度
mem = [1]*10240   ##存储器
cycle = 0           ##周期数
vec0 = [0]*64       ##向量寄存器组
for i in range(64):
    vec0[i] = [0]*64

lord_1=lord_2=lord_3=lord_4=lord_5=0
st1=st2=st3=st4=st5=st6=0
mu1=mu2=mu3=mu4=mu5=mu6=mu7=mu8=0
ad1=ad2=ad3=ad4=0

for i in range(len(mem)):
    mem[i]=i
## 将一个地址连续的64位数写入向量寄存器
def lordv (address,id,i):
    global vec0,mem
    #初始化
    global lord_1,lord_2,lord_3,lord_4,lord_5
    #模拟6拍运行过程
    try:
        vec0[id][i-5]=lord_5
    except:flag=0
    lord_5=lord_4
    lord_4=lord_3
    lord_3=lord_2
    lord_2=lord_1
    lord_1=mem[address+i]
## 将向量寄存器内的数据写入连续的地址
def storev(address,id,i):
    global vec0,mem
    global st1,st2,st3,st4,st5,st6
    if i>=6:
        mem[address+i-6]=st6
    st6=st5
    st5=st4
    st4=st3
    st3=st2
    st2=st1
    try:
        st1=vec0[id][i]
    except:st1=vec0[id][63]
## 向量乘法
def mulv(id_d,const,id_s,i):
    global vec0,mem
    global mu1,mu2,mu3,mu4,mu5,mu6,mu7,mu8
    try:
        vec0[id_d][i-8]=mu8*const
    except: flag =0
    mu8=mu7
    mu7=mu6
    mu6=mu5
    mu5=mu4
    mu4=mu3
    mu3=mu2
    mu2=mu1 
    try:
        mu1=vec0[id_s][i]
    except:mu1=vec0[id_s][63]
## 向量加法
def addv(id_d,id_s1,id_s2,i):
    global vec0,mem
    global ad1,ad2,ad3,ad4
    try:
        vec0[id_d][i-4]=ad4
    except:flag = 0
    ad4=ad3
    ad3=ad2
    ad2=ad1
    try:
        ad1=vec0[id_s1][i]+vec0[id_s2][i]
    except:ad1=vec0[id_s1][63]+vec0[id_s2][63]
## 向量指令之间的链接
def simulate0():
    cycle0 =0 #不链接时的cycle数

    #不链接时计算cycle
    for address in range(0,1023,64):
        #lordv V0  Rx
        i=0
        while i<69:
            lordv(address,0,i)
            i+=1
            cycle0+=1
        #print(cycle0)
        #mulv v2 a v0
        i=0
        while i<72:
            mulv(2,10,0,i)
            i+=1
            cycle0+=1
        #print(cycle0)
        #lordv V3  Ry
        i=0
        while i<69:
            lordv(address+1024,3,i)
            i+=1
            cycle0+=1
        #print(cycle0)
        #addv v4 v3 v2
        i=0
        while i<68:
            addv(4,3,2,i)
            i+=1
            cycle0+=1
        #print(cycle0)
        #store v4
        i=0
        while i<70:
            storev(address+1024,4,i)
            i+=1
            cycle0+=1
    return cycle0
    #print(cycle0)

cycle0 = simulate0()
for i in range(len(mem)):
    mem[i]=i
for i in range(64):
    vec0[i]=[0]*64
lord_1=lord_2=lord_3=lord_4=lord_5=0
st1=st2=st3=st4=st5=st6=0
mu1=mu2=mu3=mu4=mu5=mu6=mu7=mu8=0
ad1=ad2=ad3=ad4=0
def simulate1():
    cycle1 =0 #链接时的cycle数
    # global mu1,lord_5,ad1,ad4,st1
    for address in range(0,1023,64):
        #lordv V0  Rx
        #mulv v2 a v0
        i=0
        while i<78:
            if i<69:
                lordv(address,0,i)
            if i>5:
                mu1=lord_5
                mulv(2,10,0,i-6)
            if i>=69:
                lordv(address+1024,3,i-69)
                if i >=75:
                    addv(4,3,2,i-75)
            i+=1
            cycle1+=1
        #lordv V3  Ry
        #addv v4 v3 v2
        #store v4
        #print (vec0)
        i=0
        while i<81-9:
            if i<69-9:
                lordv(address+1024,3,i+9)
            if i<74-3:
                #print(1)
                ad1=lord_5
                addv(4,3,2,i+3)
            if i>10-9:
                st1=ad4
                storev(address+1024,4,i-2)
            i+=1
            cycle1+=1
        #print (vec0)
simulate1()   
print (vec0)
print(mem)     