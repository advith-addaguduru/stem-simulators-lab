"""IGCSE Grades 9-10 Physics: Electricity & Circuits Simulator"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulators.utils import nice_axes


def simulate():
    st.subheader("Electricity & Circuits")
    st.latex(r"V = IR \qquad P = IV \qquad R_s = R_1+R_2 \qquad \frac{1}{R_p}=\frac{1}{R_1}+\frac{1}{R_2}")

    mode = st.radio(
        "Choose a topic",
        ["Ohm's Law & V-I Graphs", "Series & Parallel Resistors", "Potential Divider"],
        horizontal=True,
    )

    if mode == "Ohm's Law & V-I Graphs":
        _ohms_law()
    elif mode == "Series & Parallel Resistors":
        _series_parallel()
    else:
        _potential_divider()


def _ohms_law():
    st.markdown("### Ohm's Law")

    with st.sidebar.expander("Ohm's Law Controls", expanded=True):
        resistance = st.slider("Resistance R (Ω)", 1.0, 100.0, 10.0, step=1.0)
        v_max = st.slider("Max voltage (V)", 5.0, 50.0, 12.0, step=1.0)
        component = st.selectbox(
            "Component type",
            ["Ohmic resistor", "Filament lamp", "Diode"],
        )

    v = np.linspace(0, v_max, 200)

    if component == "Ohmic resistor":
        i = v / resistance
    elif component == "Filament lamp":
        # Non-linear: resistance increases with temperature
        i = v / (resistance * (1 + 0.005 * v**2))
    else:  # Diode
        i_forward = np.where(v > 0.6, (v - 0.6) / (resistance * 0.1), 0)
        i = i_forward

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.plot(v, i, linewidth=2, color="#2563eb")
    nice_axes(ax1, "Voltage (V)", "Current (A)", f"V-I Characteristic: {component}")

    power = v * i
    ax2.fill_between(v, power, alpha=0.3, color="#f97316")
    ax2.plot(v, power, linewidth=2, color="#f97316")
    nice_axes(ax2, "Voltage (V)", "Power (W)", "Power Dissipation")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    mid_v = v_max / 2
    mid_i = np.interp(mid_v, v, i)
    c1, c2, c3 = st.columns(3)
    c1.metric("Voltage", f"{mid_v:.1f} V")
    c2.metric("Current", f"{mid_i:.3f} A")
    c3.metric("Power", f"{mid_v * mid_i:.2f} W")


def _series_parallel():
    st.markdown("### Series & Parallel Resistor Networks")

    with st.sidebar.expander("Resistor Controls", expanded=True):
        r1 = st.slider("R₁ (Ω)", 1.0, 100.0, 10.0, step=1.0)
        r2 = st.slider("R₂ (Ω)", 1.0, 100.0, 20.0, step=1.0)
        r3 = st.slider("R₃ (Ω)", 1.0, 100.0, 30.0, step=1.0)
        supply_v = st.slider("Supply voltage (V)", 1.0, 24.0, 12.0, step=0.5)

    r_series = r1 + r2 + r3
    r_parallel = 1 / (1/r1 + 1/r2 + 1/r3)

    i_series = supply_v / r_series
    i_par_1 = supply_v / r1
    i_par_2 = supply_v / r2
    i_par_3 = supply_v / r3
    i_par_total = i_par_1 + i_par_2 + i_par_3

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**⛓ Series**")
        st.metric("Total R", f"{r_series:.1f} Ω")
        st.metric("Current (all)", f"{i_series:.3f} A")
        st.metric("V across R₁", f"{i_series * r1:.2f} V")
        st.metric("V across R₂", f"{i_series * r2:.2f} V")
        st.metric("V across R₃", f"{i_series * r3:.2f} V")

    with col2:
        st.markdown("**🔀 Parallel**")
        st.metric("Total R", f"{r_parallel:.2f} Ω")
        st.metric("Total current", f"{i_par_total:.3f} A")
        st.metric("I through R₁", f"{i_par_1:.3f} A")
        st.metric("I through R₂", f"{i_par_2:.3f} A")
        st.metric("I through R₃", f"{i_par_3:.3f} A")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    labels = ["R₁", "R₂", "R₃"]
    vals = [r1, r2, r3]
    series_v = [i_series * r for r in vals]
    ax1.bar(labels, series_v, color=["#3b82f6", "#22c55e", "#f97316"], edgecolor="#333")
    ax1.set_ylabel("Voltage (V)")
    ax1.set_title(f"Series: Voltage drops (total = {supply_v} V)")
    ax1.grid(True, alpha=0.3, axis="y")

    par_i = [i_par_1, i_par_2, i_par_3]
    ax2.bar(labels, par_i, color=["#3b82f6", "#22c55e", "#f97316"], edgecolor="#333")
    ax2.set_ylabel("Current (A)")
    ax2.set_title(f"Parallel: Branch currents (total = {i_par_total:.3f} A)")
    ax2.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _potential_divider():
    st.markdown("### Potential Divider")
    st.latex(r"V_{out} = V_{in} \times \frac{R_2}{R_1 + R_2}")

    with st.sidebar.expander("Divider Controls", expanded=True):
        v_in = st.slider("Input voltage Vᵢₙ (V)", 1.0, 24.0, 9.0, step=0.5)
        r1 = st.slider("R₁ (Ω) ", 1.0, 100.0, 10.0, step=1.0)
        r2 = st.slider("R₂ (Ω) ", 1.0, 100.0, 20.0, step=1.0)

    v_out = v_in * r2 / (r1 + r2)
    i = v_in / (r1 + r2)

    c1, c2, c3 = st.columns(3)
    c1.metric("Vout", f"{v_out:.2f} V")
    c2.metric("Current", f"{i:.3f} A")
    c3.metric("Ratio R₂/(R₁+R₂)", f"{r2 / (r1 + r2):.3f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # Vary R2 and show Vout
    r2_range = np.linspace(1, 100, 200)
    v_out_range = v_in * r2_range / (r1 + r2_range)
    ax1.plot(r2_range, v_out_range, linewidth=2, color="#2563eb")
    ax1.axvline(r2, color="red", linestyle="--", alpha=0.7, label=f"R₂ = {r2}")
    ax1.axhline(v_out, color="green", linestyle="--", alpha=0.7, label=f"Vout = {v_out:.2f}")
    nice_axes(ax1, "R₂ (Ω)", "Vout (V)", f"Vout vs R₂ (R₁ = {r1} Ω, Vᵢₙ = {v_in} V)")
    ax1.legend()

    ax2.bar(["V across R₁", "V across R₂"], [v_in - v_out, v_out],
            color=["#f97316", "#22c55e"], edgecolor="#333")
    ax2.set_ylabel("Voltage (V)")
    ax2.set_title("Voltage Distribution")
    ax2.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
