"""
Grade 7 — Energy Transfers & Forces
Cambridge Lower Secondary Science (Stage 8)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("⚡ Energy Transfers & Forces")
    st.markdown("_Learn how energy moves between objects and changes form._")

    mode = st.selectbox(
        "Choose an activity",
        ["Kinetic & Potential Energy", "Energy Conservation — Ball Drop", "Heating & Cooling"],
    )

    if mode == "Kinetic & Potential Energy":
        st.subheader("🔋 Kinetic & Potential Energy")
        st.latex(r"E_k = \tfrac{1}{2}mv^2 \qquad E_p = mgh")

        col1, col2, col3 = st.columns(3)
        with col1:
            mass = st.slider("Mass (kg)", 0.1, 20.0, 5.0, step=0.5)
        with col2:
            velocity = st.slider("Speed (m/s)", 0, 30, 10)
        with col3:
            height = st.slider("Height (m)", 0, 50, 10)

        g = 9.81
        KE = 0.5 * mass * velocity ** 2
        PE = mass * g * height
        total = KE + PE

        c1, c2, c3 = st.columns(3)
        c1.metric("Kinetic Energy", f"{KE:.1f} J")
        c2.metric("Potential Energy", f"{PE:.1f} J")
        c3.metric("Total Energy", f"{total:.1f} J")

        fig, ax = plt.subplots(figsize=(8, 4))
        categories = ["Kinetic\nEnergy", "Potential\nEnergy", "Total\nEnergy"]
        values = [KE, PE, total]
        colors = ["#f59e0b", "#3b82f6", "#10b981"]

        bars = ax.bar(categories, values, color=colors, edgecolor="#1e3a5f", width=0.5)
        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + total * 0.02,
                f"{val:.1f} J",
                ha="center",
                fontweight="bold",
            )

        ax.set_ylabel("Energy (Joules)")
        ax.set_title("Energy Comparison")
        ax.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info("💡 **Remember:** Energy can change form but the total energy stays the same!")

    elif mode == "Energy Conservation — Ball Drop":
        st.subheader("🏀 Ball Drop — Energy Conservation")
        st.markdown("Watch how potential energy converts to kinetic energy as a ball falls.")

        h_max = st.slider("Drop height (m)", 1, 100, 20, step=1)
        mass = st.slider("Ball mass (kg)", 0.1, 5.0, 1.0, step=0.1, key="ball_mass")

        g = 9.81
        dist = np.linspace(0, h_max, 200)
        PE = mass * g * (h_max - dist)
        KE = mass * g * dist
        total = PE + KE

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(dist, PE, label="Potential Energy", lw=2, color="#3b82f6")
        ax.plot(dist, KE, label="Kinetic Energy", lw=2, color="#f59e0b")
        ax.plot(dist, total, label="Total Energy", lw=2, color="#10b981", ls="--")
        ax.set_xlabel("Distance fallen (m)")
        ax.set_ylabel("Energy (J)")
        ax.set_title("Energy during a ball drop")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        v_impact = np.sqrt(2 * g * h_max)
        st.metric("Impact speed", f"{v_impact:.1f} m/s", delta=f"{v_impact * 3.6:.0f} km/h")
        st.info("💡 **Notice:** As potential energy goes down, kinetic energy goes up by the same amount!")

    elif mode == "Heating & Cooling":
        st.subheader("🌡️ Heating & Cooling")
        st.latex(r"Q = mc\Delta T")

        material = st.selectbox("Material", ["Water", "Aluminium", "Iron", "Copper"])
        specific_heat = {"Water": 4186, "Aluminium": 897, "Iron": 449, "Copper": 385}
        c = specific_heat[material]

        col1, col2 = st.columns(2)
        with col1:
            mass = st.slider("Mass (kg)", 0.1, 5.0, 1.0, step=0.1, key="heat_mass")
        with col2:
            delta_T = st.slider("Temperature change (°C)", 1, 100, 20, step=1)

        Q = mass * c * delta_T
        st.metric("Energy required", f"{Q:.0f} J", delta=f"{Q / 1000:.1f} kJ")

        fig, ax = plt.subplots(figsize=(8, 4))
        materials = list(specific_heat.keys())
        energies = [mass * specific_heat[m] * delta_T for m in materials]
        colors = ["#3b82f6" if m != material else "#ef4444" for m in materials]

        ax.bar(materials, [e / 1000 for e in energies], color=colors, edgecolor="#1e3a5f")
        ax.set_ylabel("Energy needed (kJ)")
        ax.set_title(f"Energy to heat {mass} kg by {delta_T} °C")
        ax.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info(
            f"💡 **Fun fact:** Water needs the most energy to heat up because it has the "
            f"highest specific heat capacity ({specific_heat['Water']} J/kg°C)!"
        )
