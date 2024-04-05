import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.cm import get_cmap
from matplotlib.collections import LineCollection

# @@ atm gaat er wat mis met de berekening van Fres_x en Fres_y. Deze waarden zijn te klein voor de werkelijkheid.

Pi = np.pi
G = 6.67384*10**-11 # Gravitatieconstante
t = 0
MTitanfall = 750    # Massa van onze Titanfall in kg

Limit = 4e12        # Hulpvariabele om de grafiek makkelijker te schalen; e11 is voor aarde/mars, e12 is voor het volledige stelsel (in meters)
Tijdstapfactor = 2  # bij Tijdstapfactor = 1 geeft de animatie 1 dag/frame
a_x = 0
a_y = 0
v_x = 0
v_y = 0
Fres_x = 0
Fres_y = 0
delta_t = 86400 * Tijdstapfactor # Tijdstap in seconden

# Knop om te beginnen
start_button_ax = plt.axes([0.7, 0.05, 0.1, 0.05])  # [left, bottom, width, height]
start_button = plt.Button(start_button_ax, 'Start')
Start = False
Dagen_in_een_jaar = 365
radiaal_per_graad = 2*Pi/360

def on_start_button_clicked(event):
    global Start
    Start = True

    start_button.on_clicked(on_start_button_clicked)

# Bibliotheek met al onze startwaarden/constanten
Hemellichamen = {
    "Zon": {
        "Massa": 1.9884 * 10**30,  # kg
        "Baanstraal": 0,  # Nvt voor de zon
        "Omlooptijd": 0,  # Nvt voor de zon 
        "Starthoek": 0,  # Nvt voor de zon
        "x": 0,
        "y": 0,
    },
    "Aarde": {
        "Massa": 5.972 * 10**24,  # kg
        "Baanstraal": 1.496 * 10**11,  # m
        "Omlooptijd": 365.256/Tijdstapfactor,  # dag
        "Starthoek": 25 * radiaal_per_graad,  # degrees
        "x": 0,
        "y": 0,
    },
    "Mars": {
        "Massa": 6.4171 * 10**23,  # kg
        "Baanstraal": 2.279 * 10**11,  # m
        "Omlooptijd": 687/Tijdstapfactor,  # dag
        "Starthoek": 329 * radiaal_per_graad,  # degrees
        "x": 0,
        "y": 0,
    },
    "Jupiter": {
        "Massa": 1.8982 * 10**27,  # kg
        "Baanstraal": 7.785 * 10**11,  # m
        "Omlooptijd": 11.86 *Dagen_in_een_jaar/Tijdstapfactor,  # dag
        "Starthoek": 185 * radiaal_per_graad,  # degrees
        "x": 0,
        "y": 0,
    },
    "Saturnus": {
        "Massa": 5.6834 * 10**26,  # kg
        "Baanstraal": 1.427 * 10**12,  # m
        "Omlooptijd": 29.45 * Dagen_in_een_jaar/Tijdstapfactor,  # dag
        "Starthoek": 257 * radiaal_per_graad,  # degrees
        "x": 0,
        "y": 0,
    },
    "Uranus": {
        "Massa": 86.8 * 10**24,  # kg
        "Baanstraal": 2.871 * 10**12,  # m
        "Omlooptijd": 84.01 * Dagen_in_een_jaar/Tijdstapfactor,  # dag
        "Starthoek": 244 * radiaal_per_graad,  # degrees
        "x": 0,
        "y": 0,
    },
    "Neptunus": {
        "Massa": 1.0243 * 10**26,  # kg
        "Baanstraal": 4.498 * 10**12,  # m
        "Omlooptijd": 164.8 * Dagen_in_een_jaar/Tijdstapfactor,  # dag
        "Starthoek": 341 * radiaal_per_graad,  # degrees
        "x": 0,
        "y": 0,
    },
    "Titan": {
        "Massa": 1.345 * 10**23,  # kg
        "Baanstraal": 1.221931 * 10**9,  # m (om Saturnus)
        "Omlooptijd": 15.94513889/Tijdstapfactor,  # dag (om Saturnus)
        "Starthoek": 0,  # degrees (om Saturnus)
        "x": 0,
        "y": 0,
    },
    "Maan": {
        "Massa": 0.0735 * 10**24,  # kg
        "Baanstraal": 384.4 * 10**6,  # m (om Aarde)
        "Omlooptijd": 27.32/Tijdstapfactor,  # dag(om Aarde)
        "Starthoek": 25 * radiaal_per_graad,  # degrees (om Aarde)
        "x": 0,
        "y": 0,
    },
}
# Define a colormap and get colors for each planet
cmap = get_cmap('tab10')
colors = [cmap(i) for i in range(len(Hemellichamen)+1)]
LEO = 2000e3           #2000km
T_LEO = 2*Pi*(LEO**1.5)/(G*Hemellichamen["Aarde"]["Massa"])**0.5              #Gravitatiekracht = Fmpz, met v = 2piR/T


def Hoeksnelheid(R, T):
    if T == 0: #delen door 0 beveiliging
        return None
    else:
        V = (2 * Pi) / T
        return V


def cirkelbeweging(R, T, Phi, t):
    V = Hoeksnelheid(R, T)
    if R is not None and V is not None:
        x = R * np.cos(V * t + Phi)
        y = R * np.sin(V * t + Phi)
        return x, y
    else:
        return 0, 0 # Valbeveiliging voor de Zon
altitude_LEO = 200e3
x_LEO, y_LEO = cirkelbeweging(Hemellichamen["Aarde"]["Baanstraal"] + altitude_LEO, 
                              Hemellichamen["Aarde"]["Omlooptijd"], 
                              Hemellichamen["Aarde"]["Starthoek"], 
                              t)

# Set the initial position of Titanfall
x_titanfall = x_LEO
y_titanfall = y_LEO
def Planetenposities(t):
    planeten_locaties = {}
    for planeet, gegevens in Hemellichamen.items():
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

def Hoekalfa(x_planeet, y_planeet, x_titanfall, y_titanfall):
    alfa = np.arctan((y_planeet-y_titanfall)/(x_planeet-x_titanfall))
    return alfa

# De functie voor de zwaartekracht van de planeet
def Newton(MPlaneet, R, alfa):

    Fg_x = np.cos(alfa)*(G*MTitanfall*MPlaneet)/R**2 # Hierin is alfa de hoek tussen de lijn Titanfall - planeet en de x-as
    Fg_y = np.sin(alfa)*(G*MTitanfall*MPlaneet)/R**2

    return Fg_x, Fg_y

# hoofdfunctie voor de resulterende kracht
def Fres():
    global Fres_x, Fres_y, x_titanfall, y_titanfall
    Fres_x = 0
    Fres_y = 0

    for planet, data in Hemellichamen.items():
        x_planeet = data["x"]
        y_planeet = data["y"]
        MPlaneet = data["Massa"]
        R = np.sqrt((x_planeet - x_titanfall)**2 + (y_planeet - y_titanfall)**2)
        alfa = Hoekalfa(x_planeet, y_planeet, x_titanfall, y_titanfall)
        Fg_x, Fg_y = Newton(MPlaneet, R, alfa)
        
        Fres_x += Fg_x
        Fres_y += Fg_y

def bewegingTitanfall(t):
    global a_x, a_y, v_x, v_y, x_titanfall, y_titanfall, Fres_x, Fres_y

    while Start != True:
        x_e, y_e = cirkelbeweging(Hemellichamen["Aarde"]["Baanstraal"], Hemellichamen["Aarde"]["Omlooptijd"],
                                       Hemellichamen["Aarde"]["Starthoek"], t)
        x_titanfall, y_titanfall = cirkelbeweging(LEO, T_LEO, 0,t)
        x_titanfall, y_titanfall =+ x_e, y_e

    
    a_x = Fres_x/MTitanfall 
    a_y = Fres_y/MTitanfall
    v_x = v_x + a_x*delta_t
    v_y = v_y + a_y*delta_t
    x_titanfall = x_titanfall+ v_x*delta_t
    y_titanfall = y_titanfall + v_y*delta_t
    print('---------------------------------------------------------------------------------------------')
    print('x_titanfall:', x_titanfall, 'y_titanfall:', y_titanfall)
    print('v_x:', v_x, 'v_y:', v_y)
    print('a_x:', a_x, 'a_y:', a_y)
    print('fg_x:', Fres_x, 'fg_y:', Fres_y)

fig, ax = plt.subplots()
ax.set_xlim(-Limit, Limit)
ax.set_ylim(-Limit, Limit)
scat = ax.scatter([], [], s=10)
all_positions = []

def init():
    for i, (planet, color) in enumerate(zip(Hemellichamen.keys(), colors)):
        ax.scatter([], [], s=10, color=color, label=planet)
        all_positions.append([])  # Initialize all_positions list for each planet
        # Add circles representing orbits with respective planet color
        orbit_radius = Hemellichamen[planet]["Baanstraal"]
        if planet not in ["Titan", "Maan"]:  # Exclude Titan and the Moon
            orbit_circle = plt.Circle((0, 0), orbit_radius, color=color, fill=False)
            ax.add_artist(orbit_circle)
    return scat,


def update(frame):
    global t, x_titanfall, y_titanfall  # Declare global variables
    global a_x, a_y, v_x, v_y, Fres_x, Fres_y  # Declare global variables

    t = frame
    planeten_posities = Planetenposities(t)
    for i, (planet, color) in enumerate(zip(Hemellichamen.keys(), colors)):
        # Voeg huidige positie als stip toe
        x_current = planeten_posities[planet]["x"]
        y_current = planeten_posities[planet]["y"]
        scatters[i].set_offsets([[x_current, y_current]])
    
    # Calculate force and update Titanfall's position, velocity, and acceleration
    Fres()

    bewegingTitanfall(t)
    
    # Update Titanfall's position on the plot
    scat.set_offsets([[x_titanfall, y_titanfall]])
    scatters.append(scat)
    return scatters


# Create scatter plots for each planet
scatters = [ax.scatter([], [], s=50, color=color) for color in colors]

# Call FuncAnimation with the updated update() function
ani = FuncAnimation(fig, update, frames=np.arange(0, 5000), init_func=init, blit=True)
plt.legend(loc='upper left')
plt.show()
