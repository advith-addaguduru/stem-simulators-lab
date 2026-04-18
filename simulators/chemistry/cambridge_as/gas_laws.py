"""Chemistry: Gas Laws Simulator (Multiple Curricula)"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulators.utils import nice_axes

def simulate():
    st.subheader("Ideal Gas Law & Gas Behavior")
    st.latex(r"PV = nRT \quad;\quad \frac{P_1V_1}{T_1} = \frac{P_2V_2}{T_2}")
    
    mode = st.radio("Select experiment", ["PV=nRT Calculation", "Combined Gas Law"], horizontal=True)
    
    if mode == "PV=nRT Calculation":
        with st.sidebar.expander("Gas Law Controls", expanded=True):
            P = st.slider("Pressure P (kPa)", 10.0, 500.0, 101.325, step=10.0)
            V = st.slider("Volume V (liters)", 0.5, 100.0, 24.0, step=1.0)
            T = st.slider("Temperature T (K)", 250.0, 400.0, 298.0, step=5.0)
        
        R = 8.314  # J/(mol·K)
        n = (P * 1000 * V * 0.001) / (R * T)  # Convert to SI units
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Moles (n)", f"{n:.3f} mol")
        col2.metric("Pressure", f"{P:.1f} kPa")
        col3.metric("Volume", f"{V:.1f} L")
        col4.metric("Temperature", f"{T:.0f} K")
        
        # Show variation with temperature
        temps = np.linspace(250, 400, 100)
        Vs = (n * R * temps) / (P * 1000)  # Volume at constant P and n
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # V vs T at constant P
        axes[0].plot(temps, Vs, 'b-', linewidth=2)
        axes[0].scatter([T], [V], color='red', s=150, zorder=3)
        nice_axes(axes[0], "Temperature (K)", "Volume (liters)", "Charles's Law (P constant)")
        
        # Variation with pressure
        pressures = np.linspace(10, 500, 100)
        Ps = (n * R * T) / (pressures * 1000)
        
        axes[1].plot(pressures, Ps, 'g-', linewidth=2)
        axes[1].scatter([P], [V], color='red', s=150, zorder=3)
        nice_axes(axes[1], "Pressure (kPa)", "Volume (liters)", "Boyle's Law (T constant)")
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        
        st.markdown(f"""
        **PV = nRT calculation:**
        - {P:.1f} × {V:.1f} = {n:.3f} × 8.314 × {T:.0f}
        - n = {n:.3f} mol of gas
        """)
    
    else:
        with st.sidebar.expander("Combined Gas Law Controls", expanded=True):
            st.write("**Initial State (1):**")
            P1 = st.slider("P₁ (kPa)", 10.0, 500.0, 101.325, step=10.0, key='p1')
            V1 = st.slider("V₁ (liters)", 0.5, 100.0, 24.0, step=1.0, key='v1')
            T1 = st.slider("T₁ (K)", 250.0, 400.0, 298.0, step=5.0, key='t1')
            
            st.write("**Final State (2):**")
            change = st.radio("Which parameter changes?", ["Pressure", "Volume", "Temperature"], horizontal=True)
            
            if change == "Pressure":
                P2_val = st.slider("P₂ (kPa)", 10.0, 500.0, 202.65, step=10.0, key='p2')
                v2_mode = st.radio("Calculate or set V₂?", ["Calculate", "Manual"], horizontal=True, key='v2_mode_p')
                T2 = T1
                if v2_mode == "Calculate":
                    V2_val = V1 * P1 * T2 / (P2_val * T1)
                else:
                    V2_val = st.slider("V₂ (liters)", 0.5, 100.0, 12.0, step=1.0, key='v2_manual')
            elif change == "Volume":
                V2_val = st.slider("V₂ (liters)", 0.5, 100.0, 12.0, step=1.0, key='v2')
                p2_mode = st.radio("Calculate or set P₂?", ["Calculate", "Manual"], horizontal=True, key='p2_mode_v')
                T2 = T1
                if p2_mode == "Calculate":
                    P2_val = P1 * V1 * T2 / (V2_val * T1)
                else:
                    P2_val = st.slider("P₂ (kPa)", 10.0, 500.0, 50.0, step=10.0, key='p2_manual')
            else:
                T2 = st.slider("T₂ (K)", 250.0, 400.0, 596.0, step=5.0, key='t2')
                v2_mode = st.radio("Calculate or set V₂?", ["Calculate", "Manual"], horizontal=True, key='v2_mode_t')
                P2_val = P1
                if v2_mode == "Calculate":
                    V2_val = V1 * P1 * T2 / (P2_val * T1)
                else:
                    V2_val = st.slider("V₂ (liters)", 0.5, 100.0, 48.0, step=1.0, key='v2_manual2')
        
        fig, axes = plt.subplots(1, 3, figsize=(14, 4))
        
        axes[0].bar(["State 1", "State 2"], [P1, P2_val], color=['blue', 'red'], alpha=0.7)
        axes[0].set_ylabel("Pressure (kPa)")
        axes[1].bar(["State 1", "State 2"], [V1, V2_val], color=['blue', 'red'], alpha=0.7)
        axes[1].set_ylabel("Volume (liters)")
        axes[2].bar(["State 1", "State 2"], [T1, T2], color=['blue', 'red'], alpha=0.7)
        axes[2].set_ylabel("Temperature (K)")
        
        for ax in axes:
            ax.grid(True, alpha=0.25, axis='y')
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
