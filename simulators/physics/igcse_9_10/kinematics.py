"""IGCSE Grades 9-10 Physics: Kinematics Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulators.utils import nice_axes

def simulate():
    st.subheader("Kinematics: Motion Analysis")
    st.latex(r"s = ut + \frac{1}{2}at^2 \quad;\quad v = u + at \quad;\quad v^2 = u^2 + 2as")
    
    with st.sidebar.expander("Kinematics Controls", expanded=True):
        u = st.number_input("Initial velocity u (m/s)", -50.0, 100.0, 10.0, step=1.0)
        a = st.number_input("Acceleration a (m/s²)", -20.0, 20.0, 2.0, step=0.5)
        t_max = st.slider("Time period (s)", 1.0, 30.0, 10.0, step=0.5)
        n_points = st.slider("Resolution", 50, 500, 200)
    
    t = np.linspace(0, t_max, n_points)
    s = u * t + 0.5 * a * t**2
    v = u + a * t
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    
    # Distance-time graph
    axes[0, 0].plot(t, s, 'b-', linewidth=2)
    nice_axes(axes[0, 0], "Time (s)", "Displacement (m)", "Displacement vs Time")
    
    # Velocity-time graph
    axes[0, 1].plot(t, v, 'r-', linewidth=2)
    axes[0, 1].axhline(0, color='k', linewidth=0.5)
    nice_axes(axes[0, 1], "Time (s)", "Velocity (m/s)", "Velocity vs Time")
    
    # Acceleration constant line
    axes[1, 0].axhline(a, color='g', linewidth=2)
    axes[1, 0].set_ylim([a - 5, a + 5])
    nice_axes(axes[1, 0], "Time (s)", "Acceleration (m/s²)", "Acceleration vs Time")
    axes[1, 0].set_xlim([0, t_max])
    
    # v² vs s graph (kinematic curve)
    v_squared = v**2
    axes[1, 1].plot(s, v_squared, 'purple', linewidth=2)
    nice_axes(axes[1, 1], "Displacement (m)", "v² (m²/s²)", "Kinematic Relationship")
    
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    
    # Summary
    final_v = u + a * t_max
    final_s = u * t_max + 0.5 * a * t_max**2
    
    st.markdown(f"""
    **At time t = {t_max:.1f}s:**
    - Final velocity: **{final_v:.2f} m/s**
    - Total displacement: **{final_s:.2f} m**
    - Using equations of uniformly accelerated motion
    """)
