"""CBSE Grade 11 & 12 Physics: Simple Harmonic Motion Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulators.utils import nice_axes

def simulate():
    st.subheader("Simple Harmonic Motion (SHM)")
    st.latex(r"x(t) = A\sin(\omega t + \phi) \quad;\quad v(t) = A\omega\cos(\omega t + \phi)")
    st.latex(r"\omega = 2\pi f \quad;\quad T = \frac{1}{f} \quad;\quad E = \frac{1}{2}kA^2")
    
    with st.sidebar.expander("SHM Controls", expanded=True):
        A = st.slider("Amplitude A (m)", 0.1, 2.0, 0.5, step=0.1)
        f = st.slider("Frequency f (Hz)", 0.5, 5.0, 1.0, step=0.1)
        phi_deg = st.slider("Phase φ (degrees)", 0, 360, 0, step=15)
        t_max = st.slider("Time duration (s)", 1.0, 10.0, 4.0, step=0.5)
        mass = st.slider("Mass m (kg)", 0.1, 5.0, 1.0, step=0.1)
    
    phi = np.radians(phi_deg)
    omega = 2 * np.pi * f
    T = 1 / f
    
    t = np.linspace(0, t_max, 1000)
    x = A * np.sin(omega * t + phi)
    v = A * omega * np.cos(omega * t + phi)
    a = -A * omega**2 * np.sin(omega * t + phi)
    
    # Energy
    k = mass * omega**2  # Spring constant
    E_total = 0.5 * k * A**2
    E_kinetic = 0.5 * mass * v**2
    E_potential = 0.5 * k * x**2
    
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    
    # Displacement
    axes[0].plot(t, x, 'b-', linewidth=2)
    axes[0].axhline(A, color='r', linestyle='--', alpha=0.5)
    axes[0].axhline(-A, color='r', linestyle='--', alpha=0.5)
    nice_axes(axes[0], "Time (s)", "Displacement (m)", "Position vs Time")
    
    # Velocity
    axes[1].plot(t, v, 'g-', linewidth=2)
    nice_axes(axes[1], "Time (s)", "Velocity (m/s)", "Velocity vs Time")
    
    # Energy
    axes[2].plot(t, E_kinetic, label='Kinetic Energy', linewidth=2)
    axes[2].plot(t, E_potential, label='Potential Energy', linewidth=2)
    axes[2].axhline(E_total, color='r', linestyle='--', label='Total Energy', linewidth=2)
    nice_axes(axes[2], "Time (s)", "Energy (J)", "Energy Distribution")
    axes[2].legend()
    
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    
    st.markdown(f"""
    **SHM Parameters:**
    - Amplitude: **{A:.2f} m**
    - Period: **{T:.3f} s**
    - Angular frequency: **{omega:.3f} rad/s**
    - Spring constant: **{k:.3f} N/m**
    - Total mechanical energy: **{E_total:.3f} J**
    """)
