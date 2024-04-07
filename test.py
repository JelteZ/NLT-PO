import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.cm import get_cmap

# Constants
Pi = np.pi
G = 6.67384e-12  # Gravitational constant
MTitanfall = 3000  # Mass of the spacecraft in kg

Limit = 8e12  # Graph limit in meters
Tijdstapfactor = 10  # Time step factor
delta_t = Pi  # Tijdstap in dagen
Totaal_opgebrande_brandstof = 0

t = 0 # tijd in dagen
t_max = 5000 # max tijd in dagen
highest_t = 0 # stopt de animatie op het hoogste tijdstip

# Button to start simulation
control_panel_ax = plt.axes([0.7, 0.05, 0.1, 0.05])  # [left, bottom, width, height]
start_button = plt.Button(control_panel_ax, 'Start')
Start = False


# Number of days in a year and conversion factor for radians
Dagen_in_een_jaar = 365
Seconden_in_een_dag = 24*3600
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
    "Zon": {"Massa": 1.9884e30, "Baanstraal": 0, "Omlooptijd": 0, "Starthoek": 0},
    "Aarde": {"Massa": 5.972e24, "Baanstraal": 1.496e11, "Omlooptijd": 365.256, "Starthoek": 25 * radiaal_per_graad},
    "Mars": {"Massa": 6.4171e23, "Baanstraal": 2.279e11, "Omlooptijd": 687, "Starthoek": 329 * radiaal_per_graad},
    "Jupiter": {"Massa": 1.8982e27, "Baanstraal": 7.785e11, "Omlooptijd": 11.86 * Dagen_in_een_jaar, "Starthoek": 185 * radiaal_per_graad},
    "Saturnus": {"Massa": 5.6834e26, "Baanstraal": 1.427e12, "Omlooptijd": 29.45 * Dagen_in_een_jaar, "Starthoek": 257 * radiaal_per_graad},
    "Uranus": {"Massa": 86.8e24, "Baanstraal": 2.871e12, "Omlooptijd": 84.01 * Dagen_in_een_jaar, "Starthoek": 244 * radiaal_per_graad,},
    "Neptunus": {"Massa": 1.0243e26, "Baanstraal": 4.498e12, "Omlooptijd": 164.8 * Dagen_in_een_jaar, "Starthoek": 341 * radiaal_per_graad},
    "Titan": {"Massa": 1.345e23, "Baanstraal": 1.221931e9, "Omlooptijd": 15.94513889, "Starthoek": 0,},
    "Maan": {"Massa": 0.0735e24, "Baanstraal": 384.4e6, "Omlooptijd": 27.32, "Starthoek": 25 * radiaal_per_graad},
}

pos_Hemellichamen_t = {
    "Zon" : {
        0: {"x" : 0, "y" : 0},
    },

    "Aarde" : {
        0: {"x" : 0, "y" : 0},
    },

    "Mars": {
        0: {"x" : 0, "y" : 0},
    },

    "Jupiter" : {
        0: {"x" : 0, "y" : 0},
    },

    "Saturnus" : {
        0: {"x" : 0, "y" : 0},
    },

    "Uranus" : {
        0: {"x" : 0, "y" : 0},
    },

    "Neptunus" : {
        0: {"x" : 0, "y" : 0},
    },

    "Titan" : {
        0: {"x" : 0, "y" : 0},
    },

    "Maan" : {
        0: {"x" : 0, "y" : 0},
    },

    "Titanfall" : {
        0: {"x" : 0, "y" : 0},
    }
}

# Define a colormap and get colors for each planet
cmap = get_cmap('tab10')
colors = [cmap(i) for i in range(len(Hemellichamen)+1)]

# Function to calculate angular velocity
def Hoeksnelheid(T):
    if T == 0: # delen door nul is flauwekul save
        return None
    else:
        V = (2 * Pi) / T        # Met T in seconden, dus V in radialen/seconde
        return V

# Function for circular motion
def cirkelbeweging(R, T, Phi, t):
    V = Hoeksnelheid(T)
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
    global pos_Hemellichamen_t

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
        pos_Hemellichamen_t[planeet][round(t, 4)] = {"x": x, "y": y}


# Function to calculate the angle between a planet and Titanfall
def Hoekalfa(x_planeet, y_planeet, x_titanfall, y_titanfall):
    alfa = np.arctan2(y_planeet - y_titanfall, x_planeet - x_titanfall)
    return alfa

def check_hoek_aarde_saturnus(t):
    global pos_Hemellichamen_t, Hemellichamen
    x_aarde = pos_Hemellichamen_t["Aarde"][t]["x"]
    y_aarde = pos_Hemellichamen_t["Aarde"][t]["y"]
    r_aarde = Hemellichamen["Aarde"]["Baanstraal"]
    x_saturnus = pos_Hemellichamen_t["Saturnus"][t]["x"]
    y_saturnus = pos_Hemellichamen_t["Saturnus"][t]["y"]
    r_saturnus = Hemellichamen["Saturnus"]["Baanstraal"]
    
    gewenste_hoek = 105.9 * radiaal_per_graad
    gewenste_afstand = round(np.sqrt(r_saturnus**2 + r_aarde**2 - 2*r_saturnus*r_aarde*np.cos(gewenste_hoek)), 3)
    afstand = round(np.sqrt((x_saturnus - x_aarde)**2 + (y_saturnus - y_aarde)**2), 3)
    # print(f"De afstand tussen Aarde en Saturnus is {afstand} en de gewenste afstand is {gewenste_afstand}")
    if afstand == gewenste_afstand:
        print("De hoek tussen Aarde en Saturnus is correct bij t =", t)







# Function to calculate gravitational force
def Newton(MPlaneet, R, alfa):
    Fg_x = -np.cos(alfa) * (G * MTitanfall * MPlaneet) / R**2
    Fg_y = -np.sin(alfa) * (G * MTitanfall * MPlaneet) / R**2
    return Fg_x, Fg_y

# Function to calculate resulting force
def F_Motor(Magnitude, richting):
    richting = richting * radiaal_per_graad     #conversie naar radialen
    F_xMotor = Magnitude*np.cos(richting)
    F_yMotor = Magnitude*np.sin(richting)
    return F_xMotor, F_yMotor

def Fres(t):
    global x_titanfall, y_titanfall, Fres_x, Fres_y, F_xMotor, F_yMotor, pos_Hemellichamen_t
    Fres_x = 0
    Fres_y = 0

    for planet, data in Hemellichamen.items():
        x_planeet = pos_Hemellichamen_t[planet][t]["x"]
        y_planeet = pos_Hemellichamen_t[planet][t]["y"]
        MPlaneet = data["Massa"]
        R = np.sqrt((x_planeet - x_titanfall)**2 + (y_planeet - y_titanfall)**2)
        alfa = Hoekalfa(x_planeet, y_planeet, x_titanfall, y_titanfall)
        Fg_x, Fg_y = Newton(MPlaneet, R, alfa)
        
        Fres_x += Fg_x
        Fres_y += Fg_y

    # F_xMotor, F_yMotor = F_Motor(200,120)           # TODO mechanisme om input toe te voegen/burns uit te voeren
    # Fres_x += F_xMotor
    # Fres_y += F_yMotor

# Function to update spacecraft position
# Het berekenen van de oorspronkelijke snelheden van Titanfall middels het differntieren van cirkelbeweging
# Initial velocity of Titanfall
v_LEO = 2 * Pi / T_LEO  # Angular velocity in LEO
v_x = -altitude_LEO * np.sin(Hemellichamen["Aarde"]["Starthoek"] + Pi/2) * v_LEO  # Tangential velocity component in x-direction
v_y = altitude_LEO * np.cos(Hemellichamen["Aarde"]["Starthoek"] + Pi/2) * v_LEO  # Tangential velocity component in y-direction

def bewegingTitanfall(t):
    global x_titanfall, y_titanfall, v_x, v_y, MTitanfall, F_xMotor, F_yMotor, Totaal_opgebrande_brandstof
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
        Totaal_opgebrande_brandstof += Opgebrande_brandstof
        MTitanfall -= Opgebrande_brandstof

        print("Net forces (Fres_x, Fres_Y): ", Fres_x, Fres_y)
        print("Acceleration (a_x, a_y):", a_x, a_y)
        print("Velocity components (v_x, v_y):", v_x, v_y)
        print("Spacecraft position (x_titanfall, y_titanfall):", x_titanfall, y_titanfall)
    pos_Hemellichamen_t["Titanfall"][round(t, 4)] = {"x": x_titanfall, "y": y_titanfall}

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

def calculate_Values():
    global t, highest_t
    while t <= t_max:    
        # Calculate force and update spacecraft's position
        Planetenposities(round(t, 4))
        Fres(round(t, 4))
        bewegingTitanfall(round(t, 4))
        check_hoek_aarde_saturnus(round(t, 4))
        t += delta_t
    highest_t = t
    # for tijd in pos_Hemellichamen_t["Saturnus"]:
    #     print(f"op t = {tijd} is de x van Saturnus {pos_Hemellichamen_t['Saturnus'][tijd]['x']}")
    #     print(f"op t = {tijd} is de y van Saturnus {pos_Hemellichamen_t['Saturnus'][tijd]['y']}")    

calculate_Values()

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
    global pos_Hemellichamen_t, Tijdstapfactor, delta_t

    t_current = round(frame * Tijdstapfactor * delta_t, 4) # dit wordt afgerond omdat we twee floats met elkaar vergelijken
    
    # print(f"t = {t_current}")
    # print(f"pos aarde: {pos_Hemellichamen_t["Aarde"][t_current]}")
    
    for i, (planet, color) in enumerate(zip(Hemellichamen.keys(), colors)):
        x_current = pos_Hemellichamen_t[planet][t_current]["x"]
        y_current = pos_Hemellichamen_t[planet][t_current]["y"]
        # if planet == "Aarde":
            # print ("Aarde staat op x =", x_current," en y =", y_current)

        scatters[i].set_offsets([[x_current, y_current]])
    
    x_current = pos_Hemellichamen_t["Titanfall"][t_current]["x"] 
    y_current = pos_Hemellichamen_t["Titanfall"][t_current]["y"]

    # Update spacecraft's position on the plot
    scat.set_offsets([[x_current, y_current]])
    scatters.append(scat)
    return scatters

# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(0, round(highest_t/(Tijdstapfactor * delta_t), 1)), init_func=init, blit=True)
plt.legend(loc='upper left')
plt.show()
