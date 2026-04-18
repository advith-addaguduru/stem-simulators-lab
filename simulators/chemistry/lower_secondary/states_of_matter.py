"""
Grade 6 — States of Matter
Cambridge Lower Secondary Science (Stage 7)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("🧊 States of Matter")
    st.markdown("_Discover how temperature changes solids, liquids, and gases._")

    mode = st.selectbox(
        "Choose an activity",
        ["Particle Model", "Heating Curve", "Density Comparison"],
    )

    if mode == "Particle Model":
        st.subheader("🔵 Particle Arrangement")
        st.markdown(
            "In a **solid**, particles vibrate in fixed positions. "
            "In a **liquid**, particles slide past each other. "
            "In a **gas**, particles fly around freely."
        )

        state = st.radio("Choose a state", ["Solid", "Liquid", "Gas"], horizontal=True)

        fig, ax = plt.subplots(figsize=(6, 6))
        np.random.seed(42)

        if state == "Solid":
            xs, ys = np.meshgrid(np.arange(0.5, 5.5, 0.8), np.arange(0.5, 5.5, 0.8))
            xs = xs.ravel() + np.random.normal(0, 0.05, xs.size)
            ys = ys.ravel() + np.random.normal(0, 0.05, ys.size)
            color, title = "#3b82f6", "Solid — particles vibrate in fixed positions"
        elif state == "Liquid":
            xs = np.random.uniform(0.5, 5.5, 36)
            ys = np.random.uniform(0.5, 3.5, 36)
            color, title = "#22c55e", "Liquid — particles slide past each other"
        else:
            xs = np.random.uniform(0.2, 5.8, 20)
            ys = np.random.uniform(0.2, 5.8, 20)
            color, title = "#ef4444", "Gas — particles move freely in all directions"

        ax.scatter(xs, ys, s=200, c=color, alpha=0.8, edgecolor="#1e3a5f")
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 6)
        ax.set_aspect("equal")
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_linewidth(2)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        props = {
            "Solid": ("Fixed", "Vibrate on the spot", "High", "Fixed"),
            "Liquid": ("Close but random", "Slide past each other", "Medium–high", "Takes shape of container"),
            "Gas": ("Far apart & random", "Move fast in all directions", "Very low", "Fills entire container"),
        }
        arr, move, dens, shape = props[state]
        st.markdown(
            f"| Property | {state} |\n|---|---|\n"
            f"| Arrangement | {arr} |\n| Movement | {move} |\n"
            f"| Density | {dens} |\n| Shape | {shape} |"
        )

    elif mode == "Heating Curve":
        st.subheader("📈 Heating Curve of Water")
        st.markdown("See how water's temperature changes as energy is added.")

        energy_input = st.slider("Energy supplied (kJ)", 0, 500, 250, step=10)

        # Simplified heating curve for water (0→100→100→steam)
        fig, ax = plt.subplots(figsize=(10, 5))

        segments_e = [0, 42, 42 + 226, 42 + 226 + 21, 42 + 226 + 21 + 200]
        segments_t = [0, 100, 100, 200, 200]
        e_plot = np.array(segments_e) / max(segments_e) * 500
        ax.plot(e_plot, segments_t, lw=3, color="#2563eb")

        # Marker for current energy
        if energy_input <= e_plot[1]:
            temp_now = (energy_input / e_plot[1]) * 100 if e_plot[1] > 0 else 0
            phase = "Solid → Liquid (Heating ice/water)"
        elif energy_input <= e_plot[2]:
            temp_now = 100
            phase = "Melting / Boiling (Phase change — temp stays constant!)"
        elif energy_input <= e_plot[3]:
            frac = (energy_input - e_plot[2]) / max(e_plot[3] - e_plot[2], 1)
            temp_now = 100 + frac * 100
            phase = "Liquid → Gas (Heating steam)"
        else:
            temp_now = 200
            phase = "Superheated gas"

        ax.scatter([energy_input], [temp_now], color="red", s=120, zorder=5)
        ax.axhline(y=100, color="#94a3b8", ls="--", alpha=0.5, label="Boiling point (100 °C)")
        ax.set_xlabel("Energy supplied (kJ)")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Heating Curve")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.metric("Temperature", f"{temp_now:.0f} °C")
        st.info(f"📌 **Phase:** {phase}")
        st.info(
            "💡 **Key idea:** During a phase change (melting or boiling), "
            "the temperature stays constant even though energy is being added!"
        )

    elif mode == "Density Comparison":
        st.subheader("⚖️ Density Comparison")
        st.latex(r"\rho = \frac{m}{V}")

        materials = {
            "Air": 1.2, "Wood (oak)": 750, "Water": 1000, "Aluminium": 2700,
            "Iron": 7870, "Gold": 19300,
        }

        selected = st.multiselect(
            "Choose materials to compare",
            list(materials.keys()),
            default=["Air", "Water", "Iron", "Gold"],
        )

        if selected:
            fig, ax = plt.subplots(figsize=(8, 4))
            densities = [materials[m] for m in selected]
            colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(selected)))

            ax.barh(selected, densities, color=colors, edgecolor="#1e3a5f")
            ax.set_xlabel("Density (kg/m³)")
            ax.set_title("Material Densities")
            ax.grid(True, alpha=0.3, axis="x")

            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            st.info(
                "💡 Objects with density **less than water (1000 kg/m³)** float. "
                "Objects with density **greater than water** sink!"
            )
        else:
            st.warning("Select at least one material to compare.")
