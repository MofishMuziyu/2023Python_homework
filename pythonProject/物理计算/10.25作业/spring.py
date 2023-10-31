import numpy as np
import matplotlib.pyplot as plt

def spring_init(x0,v0,dt,step,omega):
    x_list = [x0]
    v_list = [v0]
    t_list = [0]
    e_list = [0.5*x0**2+0.5*v0**2]
    for i in range(step-1):
        x = x_list[i] + v_list[i] * dt
        v = v_list[i] - (x_list[i]*omega)*dt
        t = t_list[i] + dt
        e = 0.5*x_list[i]**2 + 0.5*v_list[i]**2
        x_list.append(x)
        v_list.append(v)
        t_list.append(t)
        e_list.append(e)
    return x_list,v_list,t_list,e_list

def spring_choke(x0,v0,dt,step,omega,frac):##frac是阻尼系数除以m
    x_list = [x0]
    v_list = [v0]
    t_list = [0]
    e_list = [0.5*x0**2+0.5*v0**2]
    for i in range(step-1):
        x = x_list[i] + v_list[i] * dt
        v = v_list[i] - (x_list[i]*omega)*dt - (frac*v_list[i])*dt
        t = t_list[i] + dt
        e = 0.5*x_list[i]**2 + 0.5*v_list[i]**2
        x_list.append(x)
        v_list.append(v)
        t_list.append(t)
        e_list.append(e)
    return x_list,v_list,t_list,e_list

omega = 1
x0 = 1
v0 = 1
dt = 0.001
step = 50000
m = 1

x,v,t,e = spring_init(x0,v0,dt,step,omega)
length = len(t)

dE = np.zeros(length)
for i in range(length):
    if i>=1:
        dE[i] = e[i] - e[0]
plt.figure(figsize=(10,8))
plt.subplot(2,3,1)
plt.title("v-t")
plt.plot(t,v)

plt.subplot(2,3,2)
plt.title("x-t")
plt.plot(t,x)

plt.subplot(2,3,3)
plt.title("x-v")
plt.plot(x,v)


plt.subplot(2,2,3)
plt.title("E-t")
plt.plot(t,e)

plt.subplot(2,2,4)
plt.title("(E-E0)-t")
plt.plot(t,dE)

plt.savefig("spring0")

frac = 0.1 ##阻尼系数取0.1.
xz,vz,tz,ez = spring_choke(x0,v0,dt,step,omega,frac)
length = len(tz)

dEz = np.zeros(length)
for i in range(length):
    if i>=1:
        dEz[i] = ez[i] - ez[0]
plt.figure(figsize=(10,8))
plt.subplot(2,3,1)
plt.title("v-t")
plt.plot(tz,vz)

plt.subplot(2,3,2)
plt.title("x-t")
plt.plot(tz,xz)

plt.subplot(2,3,3)
plt.title("x-v")
plt.plot(xz,vz)


plt.subplot(2,2,3)
plt.title("E-t")
plt.plot(tz,ez)

plt.subplot(2,2,4)
plt.title("(E-E0)-t")
plt.plot(tz,dEz)
plt.savefig("spring1")
plt.show()