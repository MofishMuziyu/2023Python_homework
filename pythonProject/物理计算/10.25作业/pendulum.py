import numpy as np
import matplotlib.pyplot as plt


def pendulum_init(theta0,omega0,dt,step,g,l,m):
    theta_list = [theta0]
    omega_list = [omega0]
    t_list = [0]
    e_list = [m*g*l*(1-np.cos(theta0)) + 0.5*m*(l**2)*(omega0**2)]
    for i in range(step):
        theta = theta_list[i] + omega_list[i]*dt
        omega = omega_list[i] - (g/l)*theta_list[i]*dt
        t = t_list[i] + dt
        e = m*g*l*(1-np.cos(theta)) + 0.5*m*(l**2)*(omega**2)
        theta_list.append(theta)
        omega_list.append(omega)
        t_list.append(t)
        e_list.append(e)

    return  theta_list,omega_list,t_list,e_list

def pendulum_choke(theta0,omega0,dt,step,g,l,m,frac):
    theta_list = [theta0]
    omega_list = [omega0]
    t_list = [0]
    e_list = [m * g * l * (1 - np.cos(theta0)) + 0.5 * m * (l ** 2) * (omega0 ** 2)]
    for i in range(step):
        theta = theta_list[i] + omega_list[i] * dt
        omega = omega_list[i] - (g / l) * theta_list[i] * dt - frac/m * omega_list[i]*dt
        t = t_list[i] + dt
        e = m * g * l * (1 - np.cos(theta)) + 0.5 * m * (l ** 2) * (omega ** 2)
        theta_list.append(theta)
        omega_list.append(omega)
        t_list.append(t)
        e_list.append(e)

    return theta_list, omega_list, t_list, e_list

l = 10 ##绳子长度
theta0 = 5/180 * np.pi
omega0 = 0
m = 1
g = 9.8
step = 50000
dt = 0.001
frac = 0.1

theta, omega, time, E = pendulum_init(theta0, omega0, dt, step, g, l, m)
length = len(time)

dE = np.zeros(length)
for i in range(length):
    if i>=1:
        dE[i] = E[i] - E[0]
plt.figure(figsize=(10,8))
plt.subplot(2,3,1)
plt.title("theta-t")
plt.plot(time,theta)

plt.subplot(2,3,2)
plt.title("omega-t")
plt.plot(time,omega)

plt.subplot(2,3,3)
plt.title("theta-omega")
plt.plot(omega,theta)


plt.subplot(2,2,3)
plt.title("E-t")
plt.plot(time,E)

plt.subplot(2,2,4)
plt.title("(E-E0)-t")
plt.plot(time,dE)
plt.savefig("pendulum0")



theta1, omega1, time1, E1 = pendulum_choke(theta0, omega0, dt, step, g, l, m, frac)
length = len(time)

dE1 = np.zeros(length)
for i in range(length):
    if i>=1:
        dE1[i] = E1[i] - E1[0]
plt.figure(figsize=(10,8))
plt.subplot(2,3,1)
plt.title("theta-t")
plt.plot(time1,theta1)

plt.subplot(2,3,2)
plt.title("omega-t")
plt.plot(time1,omega1)

plt.subplot(2,3,3)
plt.title("theta-omega")
plt.plot(omega1,theta1)


plt.subplot(2,2,3)
plt.title("E-t")
plt.plot(time1,E1)

plt.subplot(2,2,4)
plt.title("(E-E0)-t")
plt.plot(time1,dE1)
plt.savefig("pendulum1")
plt.show()
