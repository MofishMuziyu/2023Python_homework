import numpy as np
import random
Time = 10**9
disk_error = 30000
cabel_error = 10**9
controller_error = 3000000

### 模拟思路是总的测试步长是10**9次，每次测试三种器件完全独立，如果某个出现故障，则往后跳10个步长
##  这样一直测试完毕后，累计失效次数就是FIT，同时也求出了MTTF

##正常模拟需要40+min的时间，这是不太利于测试的，因此，可以将步长调整到5，这样就小于10min了，但是代价是结果更粗糙


def __test(times): ## 前面三个是平均时长故障率，最后是测试步长
    system_err = 0
    step = 0
    temp1 = 1/3
    temp2 = 10**(-5)
    temp3 = temp1*0.01
    fal0 = 0
    fal1 = fal2 = fal3 = 0
    fixing0 = fixing1 = 0
    while (step < times):
        if fixing0 >= 1:## 如果上次没修好，就继续修
            fixing0 = fixing0-1
            if fixing0==0:
                fal0 = 0
        if fixing1 >=1:
            fixing1 = fixing1-1
            if fixing1 ==0:
                fal1 = 0
        step+=1

        ##如果未故障则继续摇号
        if fal0==0:
            disk0_rand = random.uniform(0,10000)
            if disk0_rand <= temp1:
                fal0 = 1
        if fal1==0:
            disk_rand = random.uniform(0,10000)
            if disk_rand <= temp1:
                fal1 = 1

        cabel_rand = random.uniform(0,10000)
        con_rand = random.uniform(0,10000)
        if cabel_rand <= temp2:
            fal2 = 1
        if con_rand <= temp3:
            fal3 = 1
        if fal2 or fal3: ## 另外两个出现也是系统故障
            system_err+=1
            step+=10
            fal0=fal1=fal2=fal3=0
            fixing0 = fixing1 =0
            continue
        elif fal0 and fal1: ##同时出现则系统故障
            system_err+=1
            step+=10
            fal0=fal1=fal2=fal3=0
            continue
        elif fal0 and fal1==0 and fixing0==0:##需要修理的情况
            fixing0 = 10
        elif fal1 and fal0==0 and fixing1==0:
            fixing1 = 10
    return system_err
fit = __test(Time)
mttf = 10**9/(fit+1)
print("模拟系统的 fit 为：%d"%fit)
print("模拟系统的 MTTF 为：%.6f"%mttf)

