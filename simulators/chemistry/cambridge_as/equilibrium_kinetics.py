"""
Cambridge AS Chemistry — Equilibrium, Kinetics & Thermochemistry
================================================================
Simulators for Cambridge AS Level Chemistry (9701).
Extracted from inline definitions for clean modular architecture.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from simulators.utils import nice_axes


def simulate_equilibrium():
    """Equilibrium Constant Kc and Le Chatelier's Principle."""
    st.subheader("⚖️ Equilibrium Constant Kc")
    st.latex(r"K_c = \frac{[C][D]}{[A][B]} \quad \text{for} \quad aA + bB \rightleftharpoons cC + dD")

    with st.sidebar.expander("Equilibrium Controls", expanded=True):
        c_A_init = st.number_input("Initial [A] (mol/dm³)", 0.0, 10.0, 1.0, step=0.1)
        c_B_init = st.number_input("Initial [B] (mol/dm³)", 0.0, 10.0, 1.0, step=0.1)
        Kc = st.number_input("Kc value", 0.01, 100.0, 4.0, step=0.1)
        x = st.slider("Extent of reaction x (mol/dm³)", 0.0, min(c_A_init, c_B_init), 0.3, step=0.05)

    c_A_eq = c_A_init - x
    c_B_eq = c_B_init - x
    c_C_eq = x
    c_D_eq = x

    Kc_actual = (c_C_eq * c_D_eq) / (c_A_eq * c_B_eq + 1e-10)

    conditions = st.multiselect(
        "Apply Le Chatelier stress",
        ["Increase temperature", "Increase pressure", "Remove product"],
        default=[],
    )

    shift = ""
    if "Increase temperature" in conditions:
        shift = "Right (exothermic)" if Kc > 2 else "Left (endothermic)"
    if "Increase pressure" in conditions:
        shift = "Left (fewer moles)" if shift == "" else shift
    if "Remove product" in conditions:
        shift = "Right (to restore equilibrium)"

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    substances = ["[A]", "[B]", "[C]", "[D]"]
    initial = [c_A_init, c_B_init, 0, 0]
    equilibrium = [c_A_eq, c_B_eq, c_C_eq, c_D_eq]

    x_pos = np.arange(len(substances))
    width = 0.35
    ax[0].bar(x_pos - width / 2, initial, width, label="Initial", alpha=0.8)
    ax[0].bar(x_pos + width / 2, equilibrium, width, label="Equilibrium", alpha=0.8)
    ax[0].set_ylabel("Concentration (mol/dm³)")
    ax[0].set_xticks(x_pos)
    ax[0].set_xticklabels(substances)
    ax[0].legend()
    ax[0].grid(True, alpha=0.25)
    ax[0].set_title("Concentrations at Equilibrium")

    shift_direction = {
        "Right (exothermic)": 0.7,
        "Left (endothermic)": 0.3,
        "Right (to restore equilibrium)": 0.7,
        "Left (fewer moles)": 0.3,
    }
    position = shift_direction.get(shift, 0.5)

    ax[1].barh(["Equilibrium\nPosition"], [1], color="lightblue")
    ax[1].scatter([position], [0], s=300, color="red", marker="v", zorder=3)
    ax[1].set_xlim([0, 1])
    ax[1].set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax[1].set_xticklabels(["Reactants\ndominate", "", "Equal", "", "Products\ndominate"])
    ax[1].set_title("Equilibrium Position")
    ax[1].invert_yaxis()

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**Equilibrium concentrations:**
- [A] = {c_A_eq:.3f} mol/dm³
- [B] = {c_B_eq:.3f} mol/dm³
- [C] = {c_C_eq:.3f} mol/dm³
- [D] = {c_D_eq:.3f} mol/dm³

**Kc (actual) = {Kc_actual:.3f}** vs **Kc (target) = {Kc:.3f}**

**Le Chatelier Response:** {shift if shift else "No stress applied"}
""")


def simulate_rate_reaction():
    """Rate of Reaction and Arrhenius Equation."""
    st.subheader("⏱️ Rate of Reaction")
    st.latex(r"v = k[A]^m[B]^n \quad;\quad k = Ae^{-E_a/RT}")

    with st.sidebar.expander("Rate Reaction Controls", expanded=True):
        temp_choice = st.radio("Temperature", ["Variable", "298K (default)"], horizontal=True)
        if temp_choice == "Variable":
            T = st.slider("Temperature (K)", 250, 400, 298, step=5)
        else:
            T = 298

        Ea = st.slider("Activation Energy Ea (kJ/mol)", 10.0, 200.0, 50.0, step=5.0)
        A = st.slider(
            "Pre-exponential factor A (s⁻¹)", 1e10, 1e15, 1e13, step=1e12, format="%.1e"
        )
        conc = st.slider("Concentration [A] (mol/dm³)", 0.01, 2.0, 1.0, step=0.1)

    R = 8.314
    k = A * np.exp(-Ea * 1000 / (R * T))
    rate = k * (conc ** 1.0)

    temps = np.linspace(250, 400, 100)
    k_temps = A * np.exp(-Ea * 1000 / (R * temps))

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    inv_temps = 1000 / temps
    ax[0].semilogy(inv_temps, k_temps, lw=2)
    ax[0].scatter([1000 / T], [k], color="red", s=100, zorder=3)
    nice_axes(ax[0], "1000/T (K⁻¹)", "Rate constant k (s⁻¹)", "Arrhenius Plot")

    ax[1].plot([0, 1], [0, Ea], "ko-", lw=2, label="Energy barrier")
    ax[1].plot([1, 2], [Ea, Ea - 50], "ko-", lw=2)
    ax[1].fill_between([0, 0.05], 0, Ea, alpha=0.3, color="blue", label="Reactants")
    ax[1].fill_between([1.95, 2], 0, Ea - 50, alpha=0.3, color="green", label="Products")
    ax[1].annotate(
        "", xy=(0.5, Ea), xytext=(0.5, 0), arrowprops=dict(arrowstyle="<->", color="red")
    )
    ax[1].text(0.55, Ea / 2, f"Ea = {Ea:.0f}\nkJ/mol", fontsize=10)
    ax[1].set_ylabel("Energy (kJ/mol)")
    ax[1].set_xticks([])
    ax[1].set_title("Reaction Energy Diagram")
    ax[1].legend()
    ax[1].grid(True, alpha=0.25, axis="y")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**At T = {T} K:**
- Rate constant k = {k:.3e} s⁻¹
- Rate v = {rate:.3e} mol/(dm³·s)

**Rule of Thumb:** Rate approximately doubles every 10 °C temperature increase
""")


def simulate_thermochemistry():
    """Enthalpy Changes and Hess's Law."""
    st.subheader("🔥 Thermochemistry")
    st.latex(r"\Delta H = \sum \Delta H_f(\text{products}) - \sum \Delta H_f(\text{reactants})")

    with st.sidebar.expander("Thermochemistry Controls", expanded=True):
        reaction = st.selectbox(
            "Reaction",
            ["C + O₂ → CO₂", "N₂ + 3H₂ → 2NH₃", "Custom"],
            key="thermo_select",
        )

        if reaction == "C + O₂ → CO₂":
            delta_H = -393.5
            rxn_name = "Combustion of Carbon"
            desc = "C(s) + O₂(g) → CO₂(g)"
        elif reaction == "N₂ + 3H₂ → 2NH₃":
            delta_H = -92.4
            rxn_name = "Haber Process"
            desc = "N₂(g) + 3H₂(g) → 2NH₃(g)"
        else:
            delta_H = st.slider("ΔH (kJ/mol)", -500.0, 200.0, -100.0, step=10.0)
            rxn_name = "Custom Reaction"
            desc = "A → B"

        moles = st.number_input("Moles of reaction", 0.1, 10.0, 1.0, step=0.1)

    total_H = delta_H * moles

    fig, ax = plt.subplots(figsize=(8, 6))

    if delta_H < 0:
        ax.barh("Exothermic", -delta_H, color="red", alpha=0.7)
        thermo_type = "**EXOTHERMIC** (releases heat)"
    else:
        ax.barh("Endothermic", delta_H, color="blue", alpha=0.7)
        thermo_type = "**ENDOTHERMIC** (absorbs heat)"

    ax.set_xlabel("ΔH (kJ/mol)")
    ax.set_title(f"{rxn_name}: ΔH = {delta_H:.1f} kJ/mol")
    ax.grid(True, alpha=0.25, axis="x")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**Reaction:** {desc}
**Type:** {thermo_type}

**ΔH = {delta_H:.1f} kJ/mol**
**For {moles} mol: Total ΔH = {total_H:.1f} kJ**

**Bond energy approach:** Bonds broken (endothermic) − Bonds formed (exothermic)
""")
