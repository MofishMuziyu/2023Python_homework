import numpy as np
import random
FIT = 33657 ##自己计算的失效次数 33656.558

Time = 10**9
disk_error = 30000
cabel_error = 10**9
controller_error = 3000000

### 模拟思路是总的测试步长是10**9次，每次测试三种器件完全独立，如果某个出现故障，则往后跳10个步长
##  这样一直测试完毕后，累计失效次数就是FIT，同时也求出了MTTF

##正常模拟需要10-20min的时间，这是不太利于测试的


def __test(times): ## 前面三个是平均时长故障率，最后是测试步长
    disk_err=0
    cabel_err = 0
    con_err = 0
    step = 0
    temp1 = 1/3
    temp2 = 10**(-5)
    temp3 = temp1*0.01
    while (step < times):
        fal1=fal2=fal3 = 0
        disk_rand = random.uniform(0,10000)
        cabel_rand = random.uniform(0,10000)
        con_rand = random.uniform(0,10000)
        if disk_rand <= temp1:
            fal1 = 1
            disk_err+=1
        if cabel_rand <= temp2:
            fal2 = 1
            cabel_err += 1
        if con_rand <= temp3:
            fal3 = 1
            con_err += 1
        if fal1 or fal2 or fal3:
            step += 10
            continue
        step+=1
    result = disk_err + cabel_err + con_err
    return result
fit = __test(Time)
mttf = 10**9/(fit+1)
print("模拟系统的 fit 为：%d"%fit)
print("模拟系统的 MTTF 为：%.6f"%mttf)

