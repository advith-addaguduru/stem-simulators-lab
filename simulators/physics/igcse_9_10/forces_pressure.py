"""IGCSE Grades 9-10 Physics: Forces and Pressure Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulators.utils import nice_axes

def simulate():
    st.subheader("Forces and Pressure")
    st.latex(r"F = ma \quad;\quad p = \frac{F}{A} \quad;\quad p = \rho g h")
    
    tab1, tab2 = st.tabs(["Newton's Second Law", "Pressure"])
    
    with tab1:
        with st.sidebar.expander("Forces Controls", expanded=True):
            F = st.slider("Force F (N)", 0.0, 500.0, 100.0, step=10.0)
            m = st.slider("Mass m (kg)", 0.5, 50.0, 10.0, step=0.5)
        
        a = F / m
        v_final = a * 5  # after 5 seconds
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Acceleration", f"{a:.2f} m/s²")
        col2.metric("Force", f"{F:.1f} N")
        col3.metric("Mass", f"{m:.1f} kg")
        
        # Force vs acceleration
        masses = [5, 10, 20, 30]
        accelerations = [F / m_val for m_val in masses]
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(masses, accelerations, 'o-', linewidth=2, markersize=8)
        nice_axes(ax, "Mass (kg)", "Acceleration (m/s²)", "F = ma Relationship")
        ax.scatter([m], [a], color='red', s=200, zorder=3, label='Current')
        ax.legend()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        
        st.markdown(f"**Acceleration = F/m = {F}/{m} = {a:.3f} m/s²**")
    
    with tab2:
        with st.sidebar.expander("Pressure Controls", expanded=True):
            rho = st.slider("Fluid density ρ (kg/m³)", 500.0, 1500.0, 1000.0, step=50.0)
            h = st.slider("Depth h (m)", 0.0, 50.0, 10.0, step=1.0)
            A = st.number_input("Area A (m²)", 0.01, 10.0, 1.0, step=0.1)
            g = st.slider("g (m/s²)", 9.0, 10.0, 9.81, step=0.01)
        
        p = rho * g * h
        F_pressure = p * A
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Pressure", f"{p:.0f} Pa")
        col2.metric("Force", f"{F_pressure:.0f} N")
        col3.metric("Depth", f"{h:.1f} m")
        
        # Pressure vs depth
        h_vals = np.linspace(0, 50, 100)
        p_vals = rho * g * h_vals
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(h_vals, p_vals, 'b-', linewidth=2)
        ax.scatter([h], [p], color='red', s=200, zorder=3)
        nice_axes(ax, "Depth (m)", "Pressure (Pa)", "Hydrostatic Pressure")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        
        st.markdown(f"**p = ρgh = {rho} × {g} × {h} = {p:.0f} Pa**")
