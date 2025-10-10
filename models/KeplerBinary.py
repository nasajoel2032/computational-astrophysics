# --------------- Kepler Binary Star System Simulation ---------------

# ---------- Import Libraries ----------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import newton

# ---------- Parameters ----------

G = 6.6743e-11 # gravitational constant (m^3*kg^-1*s^-2) 
m1 = 1.989e30 # mass of star 1 (kg)
m2 = 3.989e30 # mass of star 2 (kg)
a = 5.984e12 # semi-major axis (m)
e = 0.4 # eccentricity
mu = G*(m1 + m2) # standard gravitational parameter (m^3*s^-2)

# ---------- Define Functions ---------- 
   
def binary(a, e, m1, m2, mu):
    """
    Uses Kepler's laws to solve for physical and orbital parameters of a binary star system
    Assumptions:
    - Point masses
    - Orbits are elliptical with the center of mass at one focus
    - Simple two body syste
    - Classical mechanics (v<<c and weak gravitational fields)
    Inputs:
    a = semi-major axis (m)
    e = eccentricity (unitless), range: 0-1
    m1 = mass of star 1 (kg)
    m2 = mass of star 2 (kg)
    mu = standard gravitational parameter (m^3*s^-2) = G(m1 + m2)
    Outputs:
    x1 = x position of star 1 (m)
    y1 = y position of star 1 (m)
    x2 = x position of star 2 (m)
    y2 = y position of star 2 (m)
    T = orbital period (s)
    t = time (s)
    r = radial distance between stars (m)
    r1 = radial distance of star 1 from center of mass (m)
    r2 = radial distance of star 2 from center of mass (m)
    v1 = scalar orbital velocity of star 1 (m/s)
    v2 = scalar orbital velocity of star 2 (m/s)
    KE1 = kinetic energy of star 1 (J)
    KE2 = kinetic energy of star 2 (J)
    KE = total kinetic energy of the system (J)
    U = gravitational potential energy of the system (J)
    ME = total mechanical energy of the system (J)
    dv1dt = scalar acceleration of star 1 (m/s^2)
    dv2dt = scalar acceleration of star 2 (m/s^2)
    accel = scalar relative acceleration between the two stars (m/s^2)
    w1 = angular velocity of star 1 (rad/s)
    w2 = angular velocity of star 2 (rad/s)
    """
    points = 500 # Manipulate as needed for running the simulation
    n = np.sqrt(mu/a**3)
    T = 2*np.pi*np.sqrt(a**3/mu)
    t = np.linspace(0,T,points)
    M = n*t
    def keplers_equation(M, e):
        E = np.zeros(len(M))
        """
        Uses Kepler's Equations to solve for E
        Inputs:
        M = mean anomaly (rad)
        e = eccentricity range (unitless)
        Outputs:
        E = eccentric anomaly (rad)
        """
        # for i in range(len(M)):
            # Mi = M[i]
            # def f(Ei):
                # """
                # Defines a function in which keplers equation = 0
                # """
                # return Ei - e*np.sin(Ei)-Mi
            # E[i] = brentq(f, 0, 2*np.pi) # from scipy
        # return E
        # this is commented out because brentq kept gving errors

        for i, Mi in enumerate(M):
            # Use Newton's method for faster convergence
            E[i] = newton(lambda Ei: Ei - e * np.sin(Ei) - Mi, Mi)
        return E
    E = keplers_equation(M, e)
    nu = 2*np.arctan2(np.sqrt(1 + e)*np.sin(E/2), np.sqrt(1 - e)*np.cos(E/2))
    r = (a*(1-e**2))/(1+e*np.cos(nu)) # scalar distance between both masses
    r1 = ((m2)/(m1+m2))*r # distance of star1 from barycenter
    r2 = ((m1)/(m1+m2))*r # distance of star2 from barycenter
    x1 = r1*np.cos(nu) # cartesian transformation: x coordinate of star1 relative to barycenter 
    y1 = r1*np.sin(nu) # cartesian transformation: y coordinate of star1 relative to barycenter 
    x2 = -r2*np.cos(nu) # cartesian transformation: x coordinate of star2 relative to barycenter 
    y2 = -r2*np.sin(nu) # cartesian transformation: y coordinate of star2 relative to barycenter 
    a1 = ((m2)/(m1+m2))*a # semi-major axis of star1 from barycenter
    a2 = ((m1)/(m1+m2))*a # semi-major axis of star2 from barycenter
    v_rel = np.sqrt((G*(m1+m2))*((2/r)-(1/a))) # relative orbital velocity of the system, important for calculatng v1, v2
    v1 = (m2/(m1+m2))*v_rel # angular velocity of star1 (vis-via)
    v2 = (m1/(m1+m2))*v_rel # angular velocity of star2 (vis-via)
    KE1 = (0.5)*(m1)*(v1**2) # kinetic energy of star1
    KE2 = (0.5)*(m2)*(v2**2) # kinetic energy of star2
    KE = KE1 + KE2 # relative kinetic energy 
    U = -(G*(m1*m2))/(r) # gravitational potential energy of system from Newtons law of gravity
    ME = -(G*(m1*m2))/(2*a) # total mechanical energy within the closed system (should be relatively constant in this simulation)
    dv1dt = ((G*m2)/(r**2)) # acceleration magnitude of star1
    dv2dt = ((G*m1)/(r**2)) # acceleration magnitude of star2
    accel = dv1dt + dv2dt # relative acceleration between both stars
    w1 = v1/r1 # angular velocity of star1
    w2 = v2/r2 # angular velocity of star2
    
    return x1, y1, x2, y2, T, t, r, r1, r2, v1, v2, KE1, KE2, KE, U, ME, dv1dt, dv2dt, accel, w1, w2

def run(a,e, m1, m2, mu):
    """
    Runs binary star simulation
    """
    x1, y1, x2, y2, T, t, r, r1, r2, v1, v2, KE1, KE2, KE, U, ME, dv1dt, dv2dt, accel, w1, w2 = binary(a,e,m1,m2,mu)
    fig, ax = plt.subplots(figsize=(6,6), facecolor='black')
    ax.set_facecolor('black')
    ax.plot(x1, y1, 'b--', label='star 1 orbit', alpha=0.001)
    ax.plot(x2, y2, color='dodgerblue', linestyle='--', alpha=0.001, label='star 2 orbit')
    star1, = ax.plot([], [], color='cyan', label='star 1', marker='o', markersize=15)
    star2, = ax.plot([], [], color='yellow', label='star 2', marker='o', markersize=15)
    path1, = ax.plot([], [], color='r', linestyle='-', alpha=0.3)
    path2, = ax.plot([], [], color='orange', linestyle='-', alpha=0.3)
    time = ax.text(0.1, 0.9, '', transform=ax.transAxes, color='white')
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('x position (m)', color='white')
    ax.set_ylabel('y position (m)', color='white')
    ax.set_title('Binary Star System', color='white')
    ax.legend(loc='upper right', fontsize='small')
    ax.tick_params(colors='white')


    def init():
        star1.set_data([], [])
        star2.set_data([], [])
        path1.set_data([], [])
        path2.set_data([], [])
        time.set_text('')
        return star1, star2, path1, path2, time

    def update(frame):
        star1.set_data([x1[frame]], [y1[frame]])
        star2.set_data([x2[frame]], [y2[frame]])
        path1.set_data([x1[:frame+1]], [y1[:frame+1]])
        path2.set_data([x2[:frame+1]], [y2[:frame+1]])
        time.set_text(f"Time: {t[frame]/3.15576e7:.1f} years")
        return star1, star2, path1, path2, time

    speed = 1
    frames = range(len(x1))
    anim = FuncAnimation(fig, update, frames=frames, init_func=init, interval=60, blit=False, repeat=True)
    return anim


if __name__ == "__main__":
    anim = run(a, e, m1, m2, mu)
    plt.show()
# ----------- Generate Data ----------

x1, y1, x2, y2, T, t, r, r1, r2, v1, v2, KE1, KE2, KE, U, ME, dv1dt, dv2dt, accel, w1, w2 = binary(a,e,m1,m2,mu)
data = {
    'Time Elapsed (s)': t,
    'Distance Between Both Masses (m)': r,
    'Distance of Star 1 from Barycenter (m)': r1,
    'Distance of Star 2 from Barycenter (m)': r2,
    'Scalar Velocity of Star 1 (m/s)': v1,
    'Scalar Velocity of Star 2 (m/s)': v2,
    'Kinetic Energy of Star 1 (J)': KE1,
    'Kinetic Energy of Star 2 (J)': KE2,
    'Total Kinetic Energy (J)': KE,
    'Gravitational Potential Energy (J)': U,
    'Total Mechanical Energy (J)': ME,
    'Acceleration of Star 1 (m/s^2)': dv1dt,
    'Acceleration of Star 2 (m/s^2)': dv2dt,
    'Relative Acceleration (m/s^2)': accel,
    'Angular Velocity of Star 1 (rad/s)': w1,
    'Angular Velocity of Star 2 (rad/s)': w2
}
df = pd.DataFrame(data)
df.to_csv('kepler_binary_data.csv', index=False)