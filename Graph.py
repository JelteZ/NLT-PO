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

MZon = 1.9884e30  # Massa Zon in kg
pos_zon, = ax.plot([], [], 'yo')  # Create the first line object
x_zon = 0
y_zon = 0

MAarde = 5.972e24  # Massa Aarde in kg
RAarde = 1.496e11  # Baanstraal Aarde in meter
TAarde = 365.256 * 24 * 3600  # Omlooptijd Aarde in seconden
PhiAarde = 0  # Starthoek baan Aarde in graden
pos_aarde, = ax.plot([], [], 'go')  
def x_aarde(t):
    return cirkelbeweging(RAarde, TAarde, PhiAarde, t)[0]
def y_aarde(t):
    return RAarde * np.sin(t)

MMars = 6.4171e23  # Massa Mars in kg
RMars = 2.279e11  # Baanstraal Mars in meter
TMars = 687 * 24 * 3600  # Omlooptijd Mars in seconden
PhiMars = 0  # Starthoek baan Mars in graden
pos_mars, = ax.plot([], [], 'bo')  
def x_mars(t):
    return RMars * np.cos(t)
def y_mars(t):
    return RMars * np.sin(t)

MJupiter = 1.8982e27  # Massa Jupiter in kg
RJupiter = 7.785e11  # Baanstraal Jupiter in meter
TJupiter = 11.86 * 365 * 24 * 3600  # Omlooptijd Jupiter in seconden
PhiJupiter = 0  # Starthoek baan Jupiter in graden
pos_jupiter, = ax.plot([], [], 'co')
def x_jupiter(t):
    return RJupiter * np.cos(t)
def y_jupiter(t):
    return RJupiter * np.sin(t)

MSaturnus = 5.6834e26  # Massa Saturnus in kg
RSaturnus = 1.427e12  # Baanstraal Saturnus in meter
TSaturnus = 29.45 * 365 * 24 * 3600  # Omlooptijd Saturnus in seconden
PhiSaturnus = 0  # Starthoek baan Saturnus in graden
pos_saturnus, = ax.plot([], [], 'mo')
def x_saturnus(t):
    return RSaturnus * np.cos(t)
def y_saturnus(t):
    return RSaturnus * np.sin(t)

MNeptunus = 1.0243e26  # Massa Neptunus in kg
RNeptunus = 4.498e12  # Baanstraal Neptunus in meter
TNeptunus = 164.8 * 365 * 24 * 3600  # Omlooptijd Neptunus in seconden
PhiNeptunus = 0  # Starthoek baan Neptunus in graden
pos_neptunus, = ax.plot([], [], 'ro')
def x_neptunus(t):
    return RNeptunus * np.cos(t)
def y_neptunus(t):
    return RNeptunus * np.sin(t)

MTitan = 1.345e23  # Massa Titan in kg
RTitan = 1.221931e9  # Baanstraal Titan in meter
TTitan = 15.94513889 * 24 * 3600  # Omlooptijd Titan in seconden
PhiTitan = 0  # Starthoek baan Titan in graden
pos_titan, = ax.plot([], [], 'g.')
def x_titan(t):
    return x_saturnus(t) + RTitan  * np.cos(t)
def y_titan(t):
    return y_saturnus(t) + RTitan * np.sin(t)

MMaan = 0.0735e24  # Massa Maan in kg
RMaan = 384.4e6  # Baanstraal Maan in meter
TMaan = 27.32 * 24 * 3600  # Omlooptijd Maan in seconden
PhiMaan = 0  # Starthoek baan Maan in graden
pos_maan, = ax.plot([], [], 'm.')
def x_maan(t):
    return x_aarde(t) + RMaan * np.cos(t)
def y_maan(t):
    return y_aarde(t) + RMaan * np.sin(t)

# Uranus
MUranus = 86.8e24  # Massa Uranus in kg

def init():
    ax.set_xlim(x_as_limit[0], x_as_limit[1])
    ax.set_ylim(y_as_limit[0], y_as_limit[1])
    return pos_zon, pos_aarde, pos_mars, pos_jupiter, pos_saturnus, pos_neptunus, pos_titan, pos_maan  # Return both line objects for initialization

def update(frame):
    pos_zon.set_data(x_zon, y_zon)
    pos_aarde.set_data(cirkelbeweging(RAarde, TAarde, PhiAarde, frame)[0], cirkelbeweging(RAarde, TAarde, PhiAarde, frame)[1])
    pos_mars.set_data(cirkelbeweging(RMars, TMars, PhiMars, frame)[0], cirkelbeweging(RMars, TMars, PhiMars, frame)[1])
    pos_jupiter.set_data(cirkelbeweging(RJupiter, TJupiter, PhiJupiter, frame)[0], cirkelbeweging(RJupiter, TJupiter, PhiJupiter, frame)[1])
    pos_saturnus.set_data(cirkelbeweging(RSaturnus, TSaturnus, PhiSaturnus, frame)[0], cirkelbeweging(RSaturnus, TSaturnus, PhiSaturnus, frame)[1])
    pos_neptunus.set_data(cirkelbeweging(RNeptunus, TNeptunus, PhiNeptunus, frame)[0], cirkelbeweging(RNeptunus, TNeptunus, PhiNeptunus, frame)[1])
    # pos_titan.set_data(cirkelbeweging(RTitan, TTitan, PhiTitan, frame)[0], cirkelbeweging(RTitan, TTitan, PhiTitan, frame)[1])
    # pos_maan.set_data(cirkelbeweging(RMaan, TMaan, PhiMaan, frame)[0], cirkelbeweging(RMaan, TMaan, PhiMaan, frame)[1])
    return pos_zon, pos_aarde, pos_mars, pos_jupiter, pos_saturnus, pos_neptunus, pos_titan, pos_maan # Return the updated line objects

ani = FuncAnimation(fig, update, frames=np.linspace(startConditie, stopConditie, aantalPunten),
                    init_func=init, blit=True)

plt.show()
