import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

startConditie = 0
stopConditie = 2 * np.pi
aantalPunten = 128

x_as_limit = [-500*10**9, 500*10**9]
y_as_limit = [-500*10**9, 500*10**9]

fig, ax = plt.subplots()

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


# Mars


# Jupiter


# Saturnus



# Geen baanstraal, omlooptijd of starthoekgegevens beschikbaar voor Uranus

# Neptunus


# Titan (Maan van Saturnus)


pos_zon, = ax.plot([], [], 'ro')  # Create the first line object
x_zon = 0
y_zon = 0
MZon = 1.9884e30  # Massa Zon in kg


# Data for the second line (new addition)
pos_aarde, = ax.plot([], [], 'go')  
def x_aarde(t):
    return 3 * np.cos(t)
def y_aarde(t):
    return 3 * np.sin(t)
MAarde = 5.972e24  # Massa Aarde in kg
RAarde = 1.496e11  # Baanstraal Aarde in meter
TAarde = 365.256 * 24 * 3600  # Omlooptijd Aarde in seconden
PhiAarde = 0  # Starthoek baan Aarde in graden

pos_mars, = ax.plot([], [], 'bo')  
def x_mars(t):
    return 5 * np.cos(t)
def y_mars(t):
    return 5 * np.sin(t)
MMars = 6.4171e23  # Massa Mars in kg
RMars = 2.279e11  # Baanstraal Mars in meter
TMars = 687 * 24 * 3600  # Omlooptijd Mars in seconden
PhiMars = 0  # Starthoek baan Mars in graden

pos_jupiter, = ax.plot([], [], 'co')
def x_jupiter(t):
    return 7 * np.cos(t)
def y_jupiter(t):
    return 7 * np.sin(t)
MJupiter = 1.8982e27  # Massa Jupiter in kg
RJupiter = 7.785e11  # Baanstraal Jupiter in meter
TJupiter = 11.86 * 365 * 24 * 3600  # Omlooptijd Jupiter in seconden
PhiJupiter = 0  # Starthoek baan Jupiter in graden

pos_saturnus, = ax.plot([], [], 'mo')
def x_saturnus(t):
    return 9 * np.cos(t)
def y_saturnus(t):
    return 9 * np.sin(t)
MSaturnus = 5.6834e26  # Massa Saturnus in kg
RSaturnus = 1.427e12  # Baanstraal Saturnus in meter
TSaturnus = 29.45 * 365 * 24 * 3600  # Omlooptijd Saturnus in seconden
PhiSaturnus = 0  # Starthoek baan Saturnus in graden

pos_neptunus, = ax.plot([], [], 'yo')
def x_neptunus(t):
    return 11 * np.cos(t)
def y_neptunus(t):
    return 11 * np.sin(t)
MNeptunus = 1.0243e26  # Massa Neptunus in kg
RNeptunus = 4.498e12  # Baanstraal Neptunus in meter
TNeptunus = 164.8 * 365 * 24 * 3600  # Omlooptijd Neptunus in seconden
PhiNeptunus = 0  # Starthoek baan Neptunus in graden


pos_titan, = ax.plot([], [], 'm.')
def x_titan(t):
    return x_saturnus(t) - 0.5 * np.cos(t)
def y_titan(t):
    return y_saturnus(t) - 0.5 * np.sin(t)
MTitan = 1.345e23  # Massa Titan in kg
RTitan = 1.221931e9  # Baanstraal Titan in meter
TTitan = 15.94513889 * 24 * 3600  # Omlooptijd Titan in seconden
PhiTitan = 0  # Starthoek baan Titan in graden

pos_maan, = ax.plot([], [], 'g.')
def x_maan(t):
    return x_aarde(t) + 0.5 * np.cos(t)
def y_maan(t):
    return y_aarde(t) + 0.5 * np.sin(t)

MMaan = 0.0735e24  # Massa Maan in kg
RMaan = 384.4e6  # Baanstraal Maan in meter
TMaan = 27.32 * 24 * 3600  # Omlooptijd Maan in seconden
PhiMaan = 0  # Starthoek baan Maan in graden

# Uranus
MUranus = 86.8e24  # Massa Uranus in kg

def init():
    ax.set_xlim(x_as_limit[0], x_as_limit[1])
    ax.set_ylim(y_as_limit[0], y_as_limit[1])
    return pos_zon, pos_aarde, pos_mars, pos_jupiter, pos_saturnus, pos_neptunus, pos_titan, pos_maan  # Return both line objects for initialization

def update(frame):
    pos_zon.set_data(x_zon, y_zon)
    pos_aarde.set_data(x_aarde(frame), y_aarde(frame))
    pos_mars.set_data(x_mars(frame), y_mars(frame))
    pos_jupiter.set_data(x_jupiter(frame), y_jupiter(frame))
    pos_saturnus.set_data(x_saturnus(frame), y_saturnus(frame))
    pos_neptunus.set_data(x_neptunus(frame), y_neptunus(frame))
    pos_titan.set_data(x_titan(frame), y_titan(frame))
    pos_maan.set_data(x_maan(frame), y_maan(frame))
    return pos_zon, pos_aarde, pos_mars, pos_jupiter, pos_saturnus, pos_neptunus, pos_titan, pos_maan # Return the updated line objects

ani = FuncAnimation(fig, update, frames=np.linspace(startConditie, stopConditie, aantalPunten),
                    init_func=init, blit=True)

plt.show()
