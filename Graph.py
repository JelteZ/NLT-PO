import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

startConditie = 0
stopConditie = 2 * np.pi
aantalPunten = 128

x_as_limit = [-15, 15]
y_as_limit = [-15, 15]

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

# Data for the first line (already present in the original code)
pos_zon, = ax.plot([], [], 'ro')  # Create the first line object
x_zon = 0
y_zon = 0

# Data for the second line (new addition)
pos_aarde, = ax.plot([], [], 'go')  
def x_aarde(t):
    return 3 * np.cos(t)
def y_aarde(t):
    return 3 * np.sin(t)

pos_mars, = ax.plot([], [], 'bo')  
def x_mars(t):
    return 5 * np.cos(t)
def y_mars(t):
    return 5 * np.sin(t)

pos_jupiter, = ax.plot([], [], 'co')
def x_jupiter(t):
    return 7 * np.cos(t)
def y_jupiter(t):
    return 7 * np.sin(t)

pos_saturnus, = ax.plot([], [], 'mo')
def x_saturnus(t):
    return 9 * np.cos(t)
def y_saturnus(t):
    return 9 * np.sin(t)

pos_neptunus, = ax.plot([], [], 'yo')
def x_neptunus(t):
    return 11 * np.cos(t)
def y_neptunus(t):
    return 11 * np.sin(t)

pos_titan, = ax.plot([], [], 'm.')
def x_titan(t):
    return x_saturnus(t) - 0.5 * np.cos(t)
def y_titan(t):
    return y_saturnus(t) - 0.5 * np.sin(t)

pos_maan, = ax.plot([], [], 'g.')
def x_maan(t):
    return x_aarde(t) + 0.5 * np.cos(t)
def y_maan(t):
    return y_aarde(t) + 0.5 * np.sin(t)

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
