import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.cm import get_cmap

# Constants
Pi = np.pi
G = 6.67384e-11  # Gravitational constant
MTitanfall = 3000  # Mass of the spacecraft in kg
Limit = 8e12  # Graph limit in meters
Tijdstapfactor = 1  # Time step factor
delta_t = 86400 * Tijdstapfactor  # Tijdstappen in dagen

# Button to start simulation
control_panel_ax = plt.axes([0.7, 0.05, 0.1, 0.05])  # [left, bottom, width, height]
start_button = plt.Button(control_panel_ax, 'Start')
Start = False


# Number of days in a year and conversion factor for radians
Dagen_in_een_jaar = 365
radiaal_per_graad = 2 * Pi / 360

# Function to handle start button click event
def on_start_button_clicked(event):
    global Start
    if Start == False:
        Start = True
        print('We gaan beginnen! Riemen vast!')
    elif Start == True:
        Start = False
    print('Start =', Start)

start_button.on_clicked(on_start_button_clicked)

# Planetary data
Hemellichamen = {
    "Zon": {"Massa": 1.9884e30, "Baanstraal": 0, "Omlooptijd": 0, "Starthoek": 0, "x": 0, "y": 0},
    "Aarde": {"Massa": 5.972e24, "Baanstraal": 1.496e11, "Omlooptijd": 365.256/Tijdstapfactor, "Starthoek": 25 * radiaal_per_graad, "x": 0, "y": 0},
    "Mars": {"Massa": 6.4171e23, "Baanstraal": 2.279e11, "Omlooptijd": 687/Tijdstapfactor, "Starthoek": 329 * radiaal_per_graad, "x": 0, "y": 0},
    "Jupiter": {"Massa": 1.8982e27, "Baanstraal": 7.785e11, "Omlooptijd": 11.86 * Dagen_in_een_jaar/Tijdstapfactor, "Starthoek": 185 * radiaal_per_graad, "x": 0, "y": 0},
    "Saturnus": {"Massa": 5.6834e26, "Baanstraal": 1.427e12, "Omlooptijd": 29.45 * Dagen_in_een_jaar/Tijdstapfactor, "Starthoek": 257 * radiaal_per_graad, "x": 0, "y": 0},
    "Uranus": {"Massa": 86.8e24, "Baanstraal": 2.871e12, "Omlooptijd": 84.01 * Dagen_in_een_jaar/Tijdstapfactor, "Starthoek": 244 * radiaal_per_graad, "x": 0, "y": 0},
    "Neptunus": {"Massa": 1.0243e26, "Baanstraal": 4.498e12, "Omlooptijd": 164.8 * Dagen_in_een_jaar/Tijdstapfactor, "Starthoek": 341 * radiaal_per_graad, "x": 0, "y": 0},
    "Titan": {"Massa": 1.345e23, "Baanstraal": 1.221931e9, "Omlooptijd": 15.94513889/Tijdstapfactor, "Starthoek": 0, "x": 0, "y": 0},
    "Maan": {"Massa": 0.0735e24, "Baanstraal": 384.4e6, "Omlooptijd": 27.32/Tijdstapfactor, "Starthoek": 25 * radiaal_per_graad, "x": 0, "y": 0},
}

# Define a colormap and get colors for each planet
cmap = get_cmap('tab10')
colors = [cmap(i) for i in range(len(Hemellichamen)+1)]

# Function to calculate angular velocity
def Hoeksnelheid(R, T):
    if T == 0:
        return None
    else:
        V = (2 * Pi) / T        # Met T in dagen, dus V in radialen/dag
        return V

# Function for circular motion
def cirkelbeweging(R, T, Phi, t):
    V = Hoeksnelheid(R, T)
    if R is not None and V is not None:
        x = R * np.cos(V * t + Phi)
        y = R * np.sin(V * t + Phi)
        return x, y
    else:
        return 0, 0  # valbeveiliging zon

# Set the initial position of Titanfall
Straal_Aarde = 6.371e6      # Meters
altitude_LEO = 200e3 + Straal_Aarde
T_LEO = 2*Pi*(altitude_LEO**1.5)/(G*Hemellichamen["Aarde"]["Massa"])**0.5       #Gravitatiekracht = Fmpz, met v = 2piR/T
x_LEO, y_LEO = cirkelbeweging(Hemellichamen["Aarde"]["Baanstraal"] + altitude_LEO, 
                              Hemellichamen["Aarde"]["Omlooptijd"], 
                              Hemellichamen["Aarde"]["Starthoek"], 
                              0)  # Initial time is 0

# Initial position of Titanfall
x_titanfall = x_LEO
y_titanfall = y_LEO

# Function to calculate planetary positions

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

# Function to calculate the angle between a planet and Titanfall
def Hoekalfa(x_planeet, y_planeet, x_titanfall, y_titanfall):
    alfa = np.arctan2(y_planeet - y_titanfall, x_planeet - x_titanfall)
    return alfa

# Function to calculate gravitational force
def Newton(MPlaneet, R, alfa):
    Fg_x = -np.cos(alfa) * (G * MTitanfall * MPlaneet) / R**2
    Fg_y = -np.sin(alfa) * (G * MTitanfall * MPlaneet) / R**2
    return Fg_x, Fg_y

# Function to calculate resulting force

def Fres():
    global x_titanfall, y_titanfall, Fres_x, Fres_y
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

# Function to update spacecraft position
# Het berekenen van de oorspronkelijke snelheden van Titanfall middels het differntieren van cirkelbeweging
# Initial velocity of Titanfall
v_LEO = 2 * Pi / T_LEO  # Angular velocity in LEO
v_x = -altitude_LEO * np.sin(Hemellichamen["Aarde"]["Starthoek"] + Pi/2) * v_LEO  # Tangential velocity component in x-direction
v_y = altitude_LEO * np.cos(Hemellichamen["Aarde"]["Starthoek"] + Pi/2) * v_LEO  # Tangential velocity component in y-direction


def bewegingTitanfall(t):
    global x_titanfall, y_titanfall, v_x, v_y, MTitanfall, F_xMotor, F_yMotor
    if Start != True:
        # Spacecraft stays in its initial position
        x_e, y_e = cirkelbeweging(Hemellichamen["Aarde"]["Baanstraal"], Hemellichamen["Aarde"]["Omlooptijd"],
                                   Hemellichamen["Aarde"]["Starthoek"], t)
        x_titanfall, y_titanfall = cirkelbeweging(altitude_LEO,T_LEO,0,t)

        x_titanfall += x_e
        y_titanfall += y_e
    else:
        # Calculate acceleration, velocity, and position of the spacecraft
        a_x = Fres_x / MTitanfall 
        a_y = Fres_y / MTitanfall
        a_x_Motor = F_xMotor / MTitanfall
        a_y_Motor = F_yMotor / MTitanfall
        v_x = v_x + a_x * delta_t
        v_y = v_y + a_y * delta_t

        x_titanfall = x_titanfall + v_x * delta_t
        y_titanfall = y_titanfall + v_y * delta_t

        Opgebrande_brandstof = Brandstof(a_x_Motor, a_y_Motor)
        MTitanfall -= Opgebrande_brandstof

        print("Net forces (Fres_x, Fres_Y): ", Fres_x, Fres_y)
        print("Acceleration (a_x, a_y):", a_x, a_y)
        print("Velocity components (v_x, v_y):", v_x, v_y)
        print("Spacecraft position (x_titanfall, y_titanfall):", x_titanfall, y_titanfall)

def bereken_delta_v(a_x, a_y):
    return np.sqrt((a_x*delta_t)**2 + (a_y*delta_t)**2)     #index 0 is v_x, index 1 is v_y

def bereken_arbeid(delta_v, massa):
    return 0.5 * massa * (delta_v)**2       # W = F*x = ∫Fdx = ∫madx = ∫m dv/dt dx = m∫vdv = 0.5mv² = Ek

def Brandstof(a_x_Motor, a_y_Motor):
    Methane_density = 0.72      #kg/m³
    Methaan_stookwaarde = 35.8e6    #J/m³
    Methaan_stookwaarde_per_kg = Methaan_stookwaarde/Methane_density    #J/kg

    delta_v = bereken_delta_v(a_x_Motor, a_y_Motor)
    arbeid = bereken_arbeid(delta_v, MTitanfall)
    Massa_brandstof = arbeid/Methaan_stookwaarde_per_kg         #J/J/kg = kg methaan

    return Massa_brandstof


# Initialize the plot
fig, ax = plt.subplots()
ax.set_xlim(-Limit, Limit)
ax.set_ylim(-Limit, Limit)

# Initialize scatter plots for each planet
scatters = [ax.scatter([], [], s=50, color=color) for color in colors]

# Initialize the spacecraft plot
scat = ax.scatter([], [], s=10)

# Function to initialize the animation
def init():
    for i, (planet, color) in enumerate(zip(Hemellichamen.keys(), colors)):
        ax.scatter([], [], s=10, color=color, label=planet)
        # Add circles representing orbits with respective planet color
        orbit_radius = Hemellichamen[planet]["Baanstraal"]
        if planet not in ["Titan", "Maan"]:
            orbit_circle = plt.Circle((0, 0), orbit_radius, color=color, fill=False)
            ax.add_artist(orbit_circle)
    return scat,

# Function to update the animation
def update(frame):
    global t, x_titanfall, y_titanfall
    t = frame
    planeten_posities = Planetenposities(t)
    for i, (planet, color) in enumerate(zip(Hemellichamen.keys(), colors)):
        x_current = planeten_posities[planet]["x"]
        y_current = planeten_posities[planet]["y"]
        scatters[i].set_offsets([[x_current, y_current]])
    
    # Calculate force and update spacecraft's position
    Fres()
    bewegingTitanfall(t)
    
    # Update spacecraft's position on the plot
    scat.set_offsets([[x_titanfall, y_titanfall]])
    scatters.append(scat)
    return scatters

# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 5000), init_func=init, blit=True)
plt.legend(loc='upper left')
plt.show()
