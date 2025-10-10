# --------------- Kepler Two Body Problem Simulation ---------------

# ---------- Import Libraries ----------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from mpl_toolkits.mplot3d import Axes3D
# ---------- Parameters ----------

G = 6.6743e-11 # (m^3)/(kg*s^2) 
m_foci = 1.989e30 # mass of the sun (kg)
m_planet = 5.972e24 # mass of the earth (kg)
mu = G*m_foci # standard gravitational parameter (m^3/s^2)
e = 0.0167 # eccentricity. range: 0-1, 0 = circle
a = 1.496e11 # semi-major axis (m) (1 AU)

# ---------- Define Functions ----------

def kepler(a,e, mu): 
    """ 
    Uses Kepler's Laws to solve for physical and orbital parameters of a two body system
    Assumptions:
    - Point masses
    - Negligible mass of orbiting body compared to central body
    - Orbits are elliptical with the central body at one focus
    - Simple two body system (no perturbations from other bodies)
    - Newtonian mechanics (non-relativistic speeds and weak gravitational fields)
    Inputs:
    a = semi-major axis (m) 
    e = eccentricity (unitless), range: 0-1
    mu = standard gravitational parameter (m^3/s^2) = GM where G is the gravitational constant and M is the mass of the central body (kg)
    Outputs:
    x = x position (m)
    y = y position (m)
    T = orbital period (s)
    t = time (s)
    E = eccentric anomaly (rad)
    r = radial distance (m)
    v = scalar orbital velocity (m/s)
    U = gravitational potential energy (J)
    KE = kinetic energy (J)
    ME = mechanical energy (J)
    """
    points = 500 # Manipulate as needed for running the simulation
    n = np.sqrt(mu/a**3)
    T = 2*np.pi*np.sqrt(a**3/mu)
    t = np.linspace(0,T,points)
    M = n*t
    def keplers_equation(M, e):
        E = np.zeros(len(M))
        """
        Uses Kepler's Equations to solve for E where:
        M = E - esin(E) = mean anomaly 
        E = eccentric anomaly 
        r = a(1-ecos(E))
        x = rcos(nu) 
        y = rsin(nu) 
        nu = true anomaly 
        """
        for i in range(len(M)):
            Mi = M[i]
            def f(Ei):
                """
                Defines a function in which keplers equation = 0
                """
                return Ei - e*np.sin(Ei)-Mi

            E[i] = brentq(f, 0, 2*np.pi) # from scipy to solve for scalar roots
        return E
    E = keplers_equation(M, e)
    nu = 2*np.arctan2(np.sqrt(1 + e)*np.sin(E/2), np.sqrt(1 - e)*np.cos(E/2))
    r = a*(1 - e*np.cos(E))
    x = r*np.cos(nu)
    y = r*np.sin(nu) 
    v = np.sqrt((mu * (2/r - 1/a))) # vis-viva equation for non-circular orbits
    U = -(mu*m_planet)/(r)
    KE = 0.5 *m_planet*(v**2)
    ME = KE + U
    return x, y, T, t, E, r, v, U, KE, ME


def animate(a,e,mu):
    """
    Animates the simulation of the two body Keplerian system
    """
    x, y, T, t, E, r, v, U, KE, ME = kepler(a,e,mu)
    fig, ax = plt.subplots(figsize=(6,6), facecolor='black')
    ax.set_facecolor('black')  
    ax.tick_params(colors='white')
    ax.plot(x,y,'b--', label='Orbit', alpha=0.0001)
    foci, = ax.plot(0,0,'yo', label='Star', markersize=10)
    planet, = ax.plot([], [], color='green', marker='o', label='Planet', markersize=5)
    path, = ax.plot([], [], color='green', linestyle='-', alpha=0.25)
    times = ax.text( 0.1, 0.9, '', transform=ax.transAxes, color='white')
    ax.set_xlabel('x position (m)', color='white')
    ax.set_ylabel('y position (m)', color='white')
    ax.set_title('Kepler Two Body Orbit', color='white')
    ax.set_aspect('equal', adjustable='box')
    ax.legend(loc='upper right')


    ax.plot(x,y ,'--', color='blue', alpha=0.0001, label='Orbit')
    ax.plot(0,0,'yo', label='Star', markersize=10)
    planet, = ax.plot([], [], 'go', label='Planet')
                      
    def init():
        planet.set_data([], [])
        path.set_data([], [])
        times.set_text('')
        return planet, path, times

    def update(frame):
        planet.set_data([x[frame]], [y[frame]])
        path.set_data(x[:frame+1], y[:frame+1])
        times.set_text(f"Time: {t[frame]/86400:.1f} days")
        return planet, path, times

    speed = 1
    frames = range(0, len(x), speed)

    anim = FuncAnimation(fig, update, frames=len(x), init_func=init, interval=45, blit=False, repeat=True)
    # plt.savefig("kepler2body2D.png", dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    # plt.close(fig)  
    return anim
if __name__ == "__main__":
    anim = animate(a,e,mu)
    plt.show()
    # HTML(anim.to_jshtml())  # For Jupyter Notebooks
# ---------- Generate Data ----------

x, y, T, t, E, r, v, U, KE, ME = kepler(a,e,mu)
data = {
    'Time Elapsed (s)': t,
    'X Position (m)': x,
    'Y Position (m)': y,
    'Eccentric Anomaly (rad)': E,
    'Orbital Radius (m)': r,
    'Orbital Velocity (m/s)': v,
    'Gravitational Potential Energy (J)': U,
    'Kinetic Energy (J)': KE,
    'Mechanical Energy (J)': ME
}
df = pd.DataFrame(data)
df.to_csv('kepler_two_body_data.csv', index=False)