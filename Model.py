import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.cm import get_cmap

Pi = np.pi
G = 6.67384*10**-11 # Gravitatieconstante
t = 0
MTitanfall = 750    # Massa van onze Titanfall in kg

x_titanfall = 0
y_titanfall = 0
Seconden_in_een_dag = 24*3600
Seconden_in_een_jaar = Seconden_in_een_dag*365

# Bibliotheek met al onze startwaarden/constanten
Hemellichamen = {
    "Zon": {
        "Massa": 1.9884 * 10**30,  # kg
        "Baanstraal": 0,  # Nvt voor de zon
        "Omlooptijd": 0,  # Nvt voor de zon
        "Starthoek": 0,  # Nvt voor de zon
    },
    "Aarde": {
        "Massa": 5.972 * 10**24,  # kg
        "Baanstraal": 1.496 * 10**11,  # m
        "Omlooptijd": 365.256 * Seconden_in_een_dag,  # s
        "Starthoek": 25,  # degrees
    },
    "Mars": {
        "Massa": 6.4171 * 10**23,  # kg
        "Baanstraal": 2.279 * 10**11,  # m
        "Omlooptijd": 687 * Seconden_in_een_dag,  # s
        "Starthoek": 329,  # degrees
    },
    "Jupiter": {
        "Massa": 1.8982 * 10**27,  # kg
        "Baanstraal": 7.785 * 10**11,  # m
        "Omlooptijd": 11.86 * Seconden_in_een_jaar,  # s
        "Starthoek": 185,  # degrees
    },
    "Saturnus": {
        "Massa": 5.6834 * 10**26,  # kg
        "Baanstraal": 1.427 * 10**12,  # m
        "Omlooptijd": 29.45 * Seconden_in_een_jaar,  # s
        "Starthoek": 257,  # degrees
    },
    "Uranus": {
        "Massa": 86.8 * 10**24,  # kg
        "Baanstraal": 2.871 * 10**12,  # m
        "Omlooptijd": 84.01 * Seconden_in_een_jaar,  # s
        "Starthoek": 244,  # degrees
    },
    "Neptunus": {
        "Massa": 1.0243 * 10**26,  # kg
        "Baanstraal": 4.498 * 10**12,  # m
        "Omlooptijd": 164.8 * Seconden_in_een_jaar,  # s
        "Starthoek": 341,  # degrees
    },
    "Titan": {
        "Massa": 1.345 * 10**23,  # kg
        "Baanstraal": 1.221931 * 10**9,  # m (om Saturnus)
        "Omlooptijd": 15.94513889 * Seconden_in_een_dag,  # s (om Saturnus)
        "Starthoek": 0,  # degrees (om Saturnus)
    },
    "Maan": {
        "Massa": 0.0735 * 10**24,  # kg
        "Baanstraal": 384.4 * 10**6,  # m (om Aarde)
        "Omlooptijd": 27.32 * Seconden_in_een_dag,  # s (om Aarde)
        "Starthoek": 25,  # degrees (om Aarde)
    },
}
# Define a colormap and get colors for each planet
cmap = get_cmap('tab10')
colors = [cmap(i) for i in range(len(Hemellichamen))]

def Hoekalfa(x_planeet, y_planeet, x_titanfall, y_titanfall):
    alfa = np.arctan((y_planeet-y_titanfall)/(x_planeet-x_titanfall))
    return alfa

# De functie voor de zwaartekracht van de planeet
def Newton(MPlaneet, R, alfa):

    Fg_x = np.cos(alfa)*(G*MTitanfall*MPlaneet)/R**2 # Hierin is alfa de hoek tussen de lijn Titanfall - planeet en de x-as
    Fg_y = np.sin(alfa)*(G*MTitanfall*MPlaneet)/R**2

    return Fg_x, Fg_y
def Hoeksnelheid(R, T):
    if T == 0: #delen door 0 beveiliging
        return None
    else:
        V = (2 * Pi * R) / T
        return V


def cirkelbeweging(R, T, Phi, t):
    V = Hoeksnelheid(R, T)
    if R is not None and V is not None:
        x = R * np.cos(V * t + Phi)
        y = R * np.sin(V * t + Phi)
        return x, y
    else:
        return 0, 0 # Valbeveiliging voor de Zon

def Planetenposities(t):
    planeten_locaties = {}
    for planeet, gegevens in Hemellichamen.items():
        massa = gegevens["Massa"]
        baanstraal = gegevens["Baanstraal"]
        omlooptijd = gegevens["Omlooptijd"]
        starthoek = gegevens["Starthoek"]
        if planeet == "Titan":
            # Correct the initial position of Titan relative to Saturn
            x_s, y_s = cirkelbeweging(Hemellichamen["Saturnus"]["Baanstraal"], Hemellichamen["Saturnus"]["Omlooptijd"],
                                       Hemellichamen["Saturnus"]["Starthoek"], t)
            x, y = cirkelbeweging(baanstraal, omlooptijd, starthoek, t)
            x += x_s
            y += y_s
        elif planeet == "Maan":
            # Correct the initial position of Moon relative to Earth
            x_e, y_e = cirkelbeweging(Hemellichamen["Aarde"]["Baanstraal"], Hemellichamen["Aarde"]["Omlooptijd"],
                                       Hemellichamen["Aarde"]["Starthoek"], t)
            x, y = cirkelbeweging(baanstraal, omlooptijd, starthoek, t)
            x += x_e
            y += y_e
        else:
            x, y = cirkelbeweging(baanstraal, omlooptijd, starthoek, t)
        planeten_locaties[planeet] = {"x": x, "y": y}
    return planeten_locaties


def bewegingTitanfall(Fg_x, Fg_y, a_x, a_y, v_x, v_y,x_titanfall, y_titanfall):
    a_x = a_x + Fg_x/MTitanfall 
    a_y = a_y + Fg_y/MTitanfall
    v_x = v_x + a_x*t
    v_y = v_y + a_y*t
    x_titanfall = x_titanfall+ v_x*t
    y_titanfall = y_titanfall + v_y*t

fig, ax = plt.subplots(figsize = (16,16))
ax.set_xlim(-2e11, 2e11)
ax.set_ylim(-2e11, 2e11)
scat = ax.scatter([], [], s=10)
all_positions = []

def init():
    for i, (planet, color) in enumerate(zip(Hemellichamen.keys(), colors)):
        ax.scatter([], [], s=10, color=color, label=planet)
        all_positions.append([])  # Initialize all_positions list for each planet
    return scat,

def update(frame):
    t = frame
    planeten_posities = Planetenposities(t)
    for i, (planet, color) in enumerate(zip(Hemellichamen.keys(), colors)):
        positions = np.array([[planeten_posities[planet]["x"], planeten_posities[planet]["y"]]])
        all_positions[i].append(positions)
        all_positions_to_plot = np.concatenate(all_positions[i], axis=0)
        scatters[i].set_offsets(all_positions_to_plot)
    return scatters

# Create scatter plots for each planet
scatters = [ax.scatter([], [], s=50, color=color) for color in colors]

# Initialize all_positions list to store positions for each planet
all_positions = []

# Call FuncAnimation with the updated update() function
ani = FuncAnimation(fig, update, frames=np.arange(0, 365*24*3600), init_func=init, blit=True)
plt.legend(loc='upper left')
plt.show()