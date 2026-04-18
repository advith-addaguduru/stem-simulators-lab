"""CBSE Chemistry: Equilibrium, Kinetics & Thermodynamics Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Chemistry — CBSE Grade 11-12")

    mode = st.radio(
        "Select topic",
        ["Chemical Equilibrium", "Acids, Bases & pH", "Thermodynamics"],
        horizontal=True,
    )

    if mode == "Chemical Equilibrium":
        _equilibrium()
    elif mode == "Acids, Bases & pH":
        _acids_bases()
    else:
        _thermodynamics()


def _equilibrium():
    st.latex(r"K_c = \frac{[C]^c[D]^d}{[A]^a[B]^b} \quad;\quad Q_c \lessgtr K_c")

    with st.sidebar.expander("Equilibrium Controls", expanded=True):
        c_A = st.slider("[A] (mol/dm³)", 0.1, 5.0, 1.0, step=0.1, key="cbse_cA")
        c_B = st.slider("[B] (mol/dm³)", 0.1, 5.0, 1.0, step=0.1, key="cbse_cB")
        c_C = st.slider("[C] (mol/dm³)", 0.1, 5.0, 0.5, step=0.1, key="cbse_cC")
        c_D = st.slider("[D] (mol/dm³)", 0.1, 5.0, 0.5, step=0.1, key="cbse_cD")
        Kc = st.number_input("Kc (target)", 0.01, 100.0, 4.0, step=0.1)

    Qc = (c_C * c_D) / (c_A * c_B + 1e-10)

    if abs(Qc - Kc) < 0.01:
        status = "At equilibrium ⚖️"
    elif Qc < Kc:
        status = "Q < K → Forward reaction favoured →"
    else:
        status = "Q > K → Reverse reaction favoured ←"

    col1, col2, col3 = st.columns(3)
    col1.metric("Qc", f"{Qc:.4f}")
    col2.metric("Kc", f"{Kc:.4f}")
    col3.metric("Direction", status.split("→")[0].split("←")[0].strip())

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    species = ["[A]", "[B]", "[C]", "[D]"]
    concs = [c_A, c_B, c_C, c_D]
    colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12"]
    axes[0].bar(species, concs, color=colors, alpha=0.8)
    axes[0].set_ylabel("Concentration (mol/dm³)")
    axes[0].set_title("Current Concentrations")
    axes[0].grid(True, alpha=0.25, axis="y")

    Qc_range = np.linspace(0.01, 20, 200)
    axes[1].axvline(Kc, color="red", lw=2, linestyle="--", label=f"Kc = {Kc}")
    axes[1].axvline(Qc, color="blue", lw=2, label=f"Qc = {Qc:.3f}")
    axes[1].fill_betweenx([0, 1], 0, Kc, alpha=0.1, color="blue", label="Forward favoured")
    axes[1].fill_betweenx([0, 1], Kc, 20, alpha=0.1, color="red", label="Reverse favoured")
    axes[1].set_xlabel("Reaction Quotient Q")
    axes[1].set_title("Q vs K Comparison")
    axes[1].set_ylim(0, 1)
    axes[1].set_yticks([])
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.25, axis="x")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"**{status}**")


def _acids_bases():
    st.latex(r"pH = -\log_{10}[H^+] \quad;\quad pOH = -\log_{10}[OH^-] \quad;\quad pH + pOH = 14")

    with st.sidebar.expander("pH Controls", expanded=True):
        acid_type = st.selectbox("Substance", [
            "Strong acid (HCl)",
            "Strong base (NaOH)",
            "Weak acid (CH₃COOH)",
            "Buffer solution",
        ])
        concentration = st.slider("Concentration (mol/dm³)", 0.001, 1.0, 0.1, step=0.01)

    if acid_type == "Strong acid (HCl)":
        H_conc = concentration
        pH = -np.log10(H_conc)
    elif acid_type == "Strong base (NaOH)":
        OH_conc = concentration
        pOH = -np.log10(OH_conc)
        pH = 14 - pOH
    elif acid_type == "Weak acid (CH₃COOH)":
        Ka = 1.8e-5
        H_conc = np.sqrt(Ka * concentration)
        pH = -np.log10(H_conc)
    else:
        Ka = 1.8e-5
        with st.sidebar.expander("Buffer Controls"):
            conj_base = st.slider("Conjugate base conc (mol/dm³)", 0.01, 1.0, 0.1, step=0.01)
        pH = -np.log10(Ka) + np.log10(conj_base / concentration)

    col1, col2, col3 = st.columns(3)
    col1.metric("pH", f"{pH:.2f}")
    col2.metric("pOH", f"{14 - pH:.2f}")
    col3.metric("Nature", "Acidic" if pH < 7 else "Basic" if pH > 7 else "Neutral")

    fig, ax = plt.subplots(figsize=(10, 3))
    pH_scale = np.linspace(0, 14, 200)
    colors_scale = plt.cm.RdYlBu(pH_scale / 14)
    for i in range(len(pH_scale) - 1):
        ax.barh(0, pH_scale[i + 1] - pH_scale[i], left=pH_scale[i], height=0.5,
                color=colors_scale[i])
    ax.axvline(pH, color="black", lw=3, label=f"pH = {pH:.2f}")
    ax.axvline(7, color="gray", lw=1, linestyle="--", alpha=0.5)
    ax.set_xlim(0, 14)
    ax.set_xlabel("pH")
    ax.set_yticks([])
    ax.set_title("pH Scale")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _thermodynamics():
    st.latex(r"\Delta G = \Delta H - T\Delta S \quad;\quad \Delta G < 0 \Rightarrow \text{spontaneous}")

    with st.sidebar.expander("Thermodynamics Controls", expanded=True):
        delta_H = st.slider("ΔH (kJ/mol)", -500.0, 500.0, -100.0, step=10.0)
        delta_S = st.slider("ΔS (J/(mol·K))", -300.0, 300.0, 50.0, step=10.0)
        T = st.slider("Temperature T (K)", 200, 600, 298, step=10)

    delta_G = delta_H - T * delta_S / 1000  # convert ΔS to kJ

    spontaneous = delta_G < 0
    T_crossover = (delta_H * 1000) / delta_S if delta_S != 0 else None

    col1, col2, col3 = st.columns(3)
    col1.metric("ΔG (kJ/mol)", f"{delta_G:.1f}")
    col2.metric("Spontaneous?", "Yes ✅" if spontaneous else "No ❌")
    if T_crossover and T_crossover > 0:
        col3.metric("T crossover", f"{T_crossover:.0f} K")

    T_range = np.linspace(100, 800, 300)
    delta_G_range = delta_H - T_range * delta_S / 1000

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(T_range, delta_G_range, "b-", lw=2)
    ax.axhline(0, color="k", lw=1)
    ax.fill_between(T_range, delta_G_range, 0, where=(delta_G_range < 0),
                    alpha=0.2, color="green", label="Spontaneous (ΔG < 0)")
    ax.fill_between(T_range, delta_G_range, 0, where=(delta_G_range > 0),
                    alpha=0.2, color="red", label="Non-spontaneous (ΔG > 0)")
    ax.scatter([T], [delta_G], color="black", s=100, zorder=3, label=f"T = {T} K")
    if T_crossover and 100 < T_crossover < 800:
        ax.axvline(T_crossover, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("ΔG (kJ/mol)")
    ax.set_title("Gibbs Free Energy vs Temperature")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**At T = {T} K:**
- ΔG = ΔH − TΔS = {delta_H:.1f} − {T} × {delta_S/1000:.3f} = **{delta_G:.1f} kJ/mol**
- Reaction is **{'spontaneous' if spontaneous else 'non-spontaneous'}**
""")
