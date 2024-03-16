import numpy as np

Pi = np.pi
G = 6.67384*10**-11 # Gravitatieconstante
t = 0
MTitanfall = 750    # Massa van onze Titanfall in kg

x_titanfall = 0
y_titanfall = 0
# Massa's hemellichamen in kg
MZon = 1.9884*10**30
MAarde = 5.972*10**24
MMars = 6.4171*10**23
MJupiter = 1.8982*10**27
MSaturnus = 5.6834*10**26
MUranus = 86.8*10**24
MNeptunus = 1.0243*10**26
MTitan = 1.345*10**23
MMaan = 0.0735*10**24

#Baanstraal van de planeten (Bij manen gaat het om de baanstraal om de planeet) in meters
RAarde = 1.496*10**11
RMars =  2.279*10**11
RJupiter = 7.785*10**11
RSaturnus = 1.427*10**11
RNeptunus = 4.498*10**12
RTitan = 1.221931*10**9
RMaan = 384.4*10**6

# Omlooptijden in seconden
Seconden_in_een_dag = 24*3600
Seconden_in_een_jaar = Seconden_in_een_dag*365
TAarde = 365.256 * Seconden_in_een_dag
TMars =  687*Seconden_in_een_dag
TJupiter = 11.86*Seconden_in_een_jaar
TSaturnus = 29.45*Seconden_in_een_jaar
TNeptunus = 164.8*Seconden_in_een_jaar
TTitan = 15.94513889*Seconden_in_een_dag
TMaan = 27.32*Seconden_in_een_dag

# Starthoek baan in graden zoals op de eenheidscirkel
PhiAarde = 0
PhiMars = 0
PhiJupiter = 0
PhiSaturnus = 0
PhiNeptunus = 0
PhiTitan = 0 #bij de manen (Titan en Maan) gaat het om de starthoek van de maan om de planeet
PhiMaan = 0

def Hoekalfa(x_planeet, y_planeet, x_titanfall, y_titanfall):
    alfa = np.arctan((y_planeet-y_titanfall)/(x_planeet-x_titanfall))
    return alfa

# De functie voor de zwaartekracht van de planeet
def Newton(MPlaneet, R, alfa):

    Fg_x = np.cos(alfa)*(G*MTitanfall*MPlaneet)/R**2 #hierin is alfa de hoek tussen de lijn Titanfall - planeet en de x-as
    Fg_y = np.sin(alfa)*(G*MTitanfall*MPlaneet)/R**2

    return Fg_x, Fg_y
def Hoeksnelheid(R, T):

    V = (2*Pi*R)/T
    return V

def cirkelbeweging(R,T,Phi):

    V = Hoeksnelheid(R,T)
    x = R*np.cos(V*t + Phi)
    y = R*np.sin(V*t + Phi)
    return [x,y]
def bewegingTitanfall(Fg_x, Fg_y, a_x, a_y, v_x, v_y,x_titanfall, y_titanfall):
    a_x = a_x + Fg_x/MTitanfall 
    a_y = a_y + Fg_y/MTitanfall
    v_x = v_x + a_x*t
    v_y = v_y + a_y*t
    x_titanfall = x_titanfall+ v_x*t
    y_titanfall = y_titanfall + v_y*t

Distance = np.sqrt((x_Titan - x_titanfall)**2 + (y_Titan - y_titanfall)**2)

while Distance > 0:
    bewegingTitanfall()
    Distance = np.sqrt((x_Titan - x_titanfall)**2 + (y_Titan - y_titanfall)**2)
    t += 1
