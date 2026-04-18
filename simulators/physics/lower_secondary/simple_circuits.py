"""
Grade 6 — Simple Circuits & Electricity
Cambridge Lower Secondary Science (Stage 7)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("🔋 Simple Circuits & Electricity")
    st.markdown("_Build circuits and discover how electricity flows._")

    mode = st.selectbox(
        "Choose an activity",
        ["Battery & Bulb Circuit", "Conductors vs Insulators", "Series & Parallel"],
    )

    if mode == "Battery & Bulb Circuit":
        st.subheader("💡 Battery & Bulb Circuit")
        st.latex(r"V = I \times R")
        st.markdown(
            "A battery pushes electric current through a circuit. "
            "The **voltage** (V) drives the current, and **resistance** (R) opposes it."
        )

        col1, col2 = st.columns(2)
        with col1:
            voltage = st.slider("Battery voltage (V)", 1.0, 12.0, 3.0, step=0.5)
        with col2:
            resistance = st.slider("Bulb resistance (Ω)", 1.0, 50.0, 10.0, step=1.0)

        current = voltage / resistance
        power = voltage * current

        c1, c2, c3 = st.columns(3)
        c1.metric("Current", f"{current:.2f} A")
        c2.metric("Power", f"{power:.2f} W")
        brightness = min(power / 5.0, 1.0)
        c3.metric("Brightness", f"{brightness * 100:.0f}%")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        voltages = np.linspace(0, 12, 50)
        currents = voltages / resistance
        ax1.plot(voltages, currents, linewidth=2, color="#2563eb")
        ax1.axvline(voltage, color="red", linestyle="--", alpha=0.7, label=f"V = {voltage}")
        ax1.axhline(current, color="green", linestyle="--", alpha=0.7, label=f"I = {current:.2f}")
        ax1.set_xlabel("Voltage (V)")
        ax1.set_ylabel("Current (A)")
        ax1.set_title(f"V-I Graph (R = {resistance} Ω)")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        resistances = [5, 10, 20, 30, 50]
        powers = [voltage**2 / r for r in resistances]
        colours = ["#f59e0b" if r != resistance else "#2563eb" for r in resistances]
        ax2.bar([f"{r}Ω" for r in resistances], powers, color=colours, edgecolor="#1e3a5f")
        ax2.set_ylabel("Power (W)")
        ax2.set_title(f"Power at {voltage} V for different resistances")
        ax2.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info("💡 **Did you know?** A standard AA battery is 1.5 V. Your phone charger supplies 5 V!")

    elif mode == "Conductors vs Insulators":
        st.subheader("🔌 Conductors vs Insulators")
        st.markdown(
            "**Conductors** allow electricity to flow easily. "
            "**Insulators** block the flow of electricity."
        )

        materials = {
            "Copper wire": {"resistance": 0.02, "type": "Conductor"},
            "Aluminium foil": {"resistance": 0.03, "type": "Conductor"},
            "Iron nail": {"resistance": 0.10, "type": "Conductor"},
            "Graphite (pencil)": {"resistance": 5.0, "type": "Conductor"},
            "Rubber band": {"resistance": 1e6, "type": "Insulator"},
            "Plastic ruler": {"resistance": 1e8, "type": "Insulator"},
            "Glass rod": {"resistance": 1e10, "type": "Insulator"},
            "Dry wood": {"resistance": 1e7, "type": "Insulator"},
        }

        selected = st.multiselect(
            "Select materials to test",
            list(materials.keys()),
            default=["Copper wire", "Rubber band", "Aluminium foil", "Glass rod"],
        )

        if selected:
            fig, ax = plt.subplots(figsize=(10, 5))
            resistances = [materials[m]["resistance"] for m in selected]
            types = [materials[m]["type"] for m in selected]
            colours = ["#22c55e" if t == "Conductor" else "#ef4444" for t in types]

            ax.barh(selected, [np.log10(r) for r in resistances], color=colours, edgecolor="#333")
            ax.set_xlabel("Resistance (log₁₀ Ω)")
            ax.set_title("Material Resistance Comparison")
            ax.grid(True, alpha=0.3, axis="x")

            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            st.markdown("🟢 **Green** = Conductor &nbsp;&nbsp; 🔴 **Red** = Insulator")
        else:
            st.warning("Select at least one material to compare.")

    else:  # Series & Parallel
        st.subheader("🔗 Series & Parallel Circuits")
        st.markdown("Compare how bulbs behave in **series** and **parallel** arrangements.")

        col1, col2 = st.columns(2)
        with col1:
            battery_v = st.slider("Battery voltage (V)", 1.0, 12.0, 6.0, step=0.5)
        with col2:
            num_bulbs = st.slider("Number of bulbs", 1, 5, 3)

        bulb_r = 10.0

        series_r = bulb_r * num_bulbs
        series_i = battery_v / series_r
        series_v_each = battery_v / num_bulbs
        series_p_each = series_i * series_v_each

        parallel_r = bulb_r / num_bulbs
        parallel_i_total = battery_v / parallel_r
        parallel_i_each = battery_v / bulb_r
        parallel_p_each = parallel_i_each * battery_v

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**⛓ Series Circuit**")
            st.metric("Total resistance", f"{series_r:.1f} Ω")
            st.metric("Current (same for all)", f"{series_i:.2f} A")
            st.metric("Voltage per bulb", f"{series_v_each:.2f} V")
            st.metric("Power per bulb", f"{series_p_each:.2f} W")

        with col2:
            st.markdown("**🔀 Parallel Circuit**")
            st.metric("Total resistance", f"{parallel_r:.1f} Ω")
            st.metric("Current per bulb", f"{parallel_i_each:.2f} A")
            st.metric("Voltage per bulb", f"{battery_v:.2f} V")
            st.metric("Power per bulb", f"{parallel_p_each:.2f} W")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        bulbs = range(1, num_bulbs + 1)
        ax1.bar(bulbs, [series_p_each] * num_bulbs, color="#60a5fa", label="Series")
        ax1.bar([b + 0.3 for b in bulbs], [parallel_p_each] * num_bulbs,
                color="#f97316", label="Parallel")
        ax1.set_xlabel("Bulb number")
        ax1.set_ylabel("Power (W)")
        ax1.set_title("Power per Bulb")
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis="y")

        n_range = range(1, 6)
        ax2.plot(list(n_range), [bulb_r * n for n in n_range], "o-",
                 color="#2563eb", label="Series", linewidth=2)
        ax2.plot(list(n_range), [bulb_r / n for n in n_range], "s-",
                 color="#f97316", label="Parallel", linewidth=2)
        ax2.set_xlabel("Number of bulbs")
        ax2.set_ylabel("Total resistance (Ω)")
        ax2.set_title("How resistance changes")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info(
            "💡 **Key difference:** In series, the current is the same through every bulb "
            "but each gets less voltage. In parallel, every bulb gets full voltage!"
        )
