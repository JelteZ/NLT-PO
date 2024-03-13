import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

startConditie = 0
stopConditie = 2 * np.pi
aantalPunten = 128

x_as_limit = [-10, 10]
y_as_limit = [-10, 10]

fig, ax = plt.subplots()

# Data for the first line (already present in the original code)
pos_zon, = ax.plot([], [], 'ro')  # Create the first line object

# Data for the second line (new addition)
pos_aarde, = ax.plot([], [], 'b')  # Create the second line object (with a blue dashed style)

def init():
    ax.set_xlim(x_as_limit[0], x_as_limit[1])
    ax.set_ylim(y_as_limit[0], y_as_limit[1])
    return pos_zon, pos_aarde  # Return both line objects for initialization

def update(frame):
    # pos_zon.set_data(np.cos(frame), np.sin(frame))
    pos_aarde.set_data(-np.cos(frame), -np.sin(frame))
    return pos_zon, pos_aarde

ani = FuncAnimation(fig, update, frames=np.linspace(startConditie, stopConditie, aantalPunten),
                    init_func=init, blit=True)

plt.show()
