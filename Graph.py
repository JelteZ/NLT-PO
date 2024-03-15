import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

startConditie = 0
stopConditie = 2 * np.pi
aantalPunten = 128

x_as_limit = [-2000*10**9, 2000*10**9]
y_as_limit = [-2000*10**9, 2000*10**9]

fig, ax = plt.subplots()

def cirkelbeweging(R, T, Phi, t):
    V = (2*np.pi*R)/T
    x = R*np.cos(V*t + Phi)
    y = R*np.sin(V*t + Phi)
    return [x,y]


# kleuren voor planeten
# black (k)
# white (w)
# red (r)
# green (g)
# blue (b)
# cyan (c)
# magenta (m)
# yellow (y)
# voor andere vormpjes zie: https://matplotlib.org/stable/api/markers_api.html

# variables Zon
MZon = 1.9884e30 
pos_zon, = ax.plot([], [], 'yo')  
x_zon = 0
y_zon = 0

# variables Aarde
MAarde = 5.972e24  
RAarde = 1.496e11  
TAarde = 365.256 * 24 * 3600  
PhiAarde = 0  
pos_aarde, = ax.plot([], [], 'go')  
def x_aarde(t):
    return cirkelbeweging(RAarde, TAarde, PhiAarde, t)[0]
def y_aarde(t):
    return RAarde * np.sin(t)

# variables Mars
MMars = 6.4171e23  
RMars = 2.279e11  
TMars = 687 * 24 * 3600 
PhiMars = 0 
pos_mars, = ax.plot([], [], 'bo')  
def x_mars(t):
    return RMars * np.cos(t)
def y_mars(t):
    return RMars * np.sin(t)

# variables Jupiter
MJupiter = 1.8982e27  
RJupiter = 7.785e11  
TJupiter = 11.86 * 365 * 24 * 3600  
PhiJupiter = 0  
pos_jupiter, = ax.plot([], [], 'co')
def x_jupiter(t):
    return RJupiter * np.cos(t)
def y_jupiter(t):
    return RJupiter * np.sin(t)

# variables Saturnus
MSaturnus = 5.6834e26  
RSaturnus = 1.427e12  
TSaturnus = 29.45 * 365 * 24 * 3600  
PhiSaturnus = 0  
pos_saturnus, = ax.plot([], [], 'mo')
def x_saturnus(t):
    return RSaturnus * np.cos(t)
def y_saturnus(t):
    return RSaturnus * np.sin(t)

# variables Neptunus
MNeptunus = 1.0243e26  
RNeptunus = 4.498e12  
TNeptunus = 164.8 * 365 * 24 * 3600  
PhiNeptunus = 0  
pos_neptunus, = ax.plot([], [], 'ro')
def x_neptunus(t):
    return RNeptunus * np.cos(t)
def y_neptunus(t):
    return RNeptunus * np.sin(t)

# variables Titan
MTitan = 1.345e23  
RTitan = 1.221931e9
TTitan = 15.94513889 * 24 * 3600  
PhiTitan = 0  
pos_titan, = ax.plot([], [], 'g.')
def x_titan(t):
    return x_saturnus(t) + RTitan  * np.cos(t)
def y_titan(t):
    return y_saturnus(t) + RTitan * np.sin(t)

# variables Maan
MMaan = 0.0735e24  
RMaan = 384.4e6  
TMaan = 27.32 * 24 * 3600  
PhiMaan = 0  
pos_maan, = ax.plot([], [], 'm.')
def x_maan(t):
    return x_aarde(t) + RMaan * np.cos(t)
def y_maan(t):
    return y_aarde(t) + RMaan * np.sin(t)

# variables Uranus
MUranus = 86.8e24  

def init():
    ax.set_xlim(x_as_limit[0], x_as_limit[1])
    ax.set_ylim(y_as_limit[0], y_as_limit[1])
    return pos_zon, pos_aarde, pos_mars, pos_jupiter, pos_saturnus, pos_neptunus, pos_titan, pos_maan  # Return both line objects for initialization

def update(frame): # 1 frame = 1 seconde
    pos_zon.set_data(x_zon, y_zon)
    pos_aarde.set_data(cirkelbeweging(RAarde, TAarde, PhiAarde, frame)[0], cirkelbeweging(RAarde, TAarde, PhiAarde, frame)[1])
    pos_mars.set_data(cirkelbeweging(RMars, TMars, PhiMars, frame)[0], cirkelbeweging(RMars, TMars, PhiMars, frame)[1])
    pos_jupiter.set_data(cirkelbeweging(RJupiter, TJupiter, PhiJupiter, frame)[0], cirkelbeweging(RJupiter, TJupiter, PhiJupiter, frame)[1])
    pos_saturnus.set_data(cirkelbeweging(RSaturnus, TSaturnus, PhiSaturnus, frame)[0], cirkelbeweging(RSaturnus, TSaturnus, PhiSaturnus, frame)[1])
    pos_neptunus.set_data(cirkelbeweging(RNeptunus, TNeptunus, PhiNeptunus, frame)[0], cirkelbeweging(RNeptunus, TNeptunus, PhiNeptunus, frame)[1])
    pos_titan.set_data(cirkelbeweging(RSaturnus, TSaturnus, PhiSaturnus, frame)[0] + cirkelbeweging(RTitan, TTitan, PhiTitan, frame)[0], cirkelbeweging(RSaturnus, TSaturnus, PhiSaturnus, frame)[1] + cirkelbeweging(RTitan, TTitan, PhiTitan, frame)[1])
    pos_maan.set_data(cirkelbeweging(RAarde, TAarde, PhiAarde, frame)[0] + cirkelbeweging(RMaan, TMaan, PhiMaan, frame)[0], cirkelbeweging(RAarde, TAarde, PhiAarde, frame)[0] + cirkelbeweging(RMaan, TMaan, PhiMaan, frame)[1])
    return pos_zon, pos_aarde, pos_mars, pos_jupiter, pos_saturnus, pos_neptunus, pos_titan, pos_maan # Return the updated line objects

ani = FuncAnimation(fig, update, frames=np.linspace(startConditie, stopConditie, aantalPunten),
                    init_func=init, blit=True)

plt.show()
