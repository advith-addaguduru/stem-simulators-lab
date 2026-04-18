"""CBSE Physics: Electricity & Magnetism Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Electricity & Magnetism — CBSE Grade 12")

    mode = st.radio(
        "Select topic",
        ["Coulomb's Law & Electric Field", "Ohm's Law & Circuits", "Electromagnetic Induction"],
        horizontal=True,
    )

    if mode == "Coulomb's Law & Electric Field":
        _coulomb()
    elif mode == "Ohm's Law & Circuits":
        _ohm_circuits()
    else:
        _em_induction()


def _coulomb():
    st.latex(r"F = \frac{1}{4\pi\varepsilon_0}\frac{q_1 q_2}{r^2} \quad;\quad E = \frac{F}{q}")

    with st.sidebar.expander("Coulomb's Law Controls", expanded=True):
        q1 = st.slider("Charge q₁ (μC)", -10.0, 10.0, 1.0, step=0.5)
        q2 = st.slider("Charge q₂ (μC)", -10.0, 10.0, -1.0, step=0.5)
        r = st.slider("Separation r (cm)", 1.0, 50.0, 10.0, step=1.0)

    k = 8.99e9
    q1_C = q1 * 1e-6
    q2_C = q2 * 1e-6
    r_m = r * 1e-2
    F = k * q1_C * q2_C / r_m**2
    E1 = k * abs(q1_C) / r_m**2

    col1, col2, col3 = st.columns(3)
    col1.metric("Force F", f"{F:.4e} N")
    col2.metric("Type", "Attractive" if F < 0 else "Repulsive")
    col3.metric("E at r", f"{E1:.4e} N/C")

    r_arr = np.linspace(1, 50, 200) * 1e-2
    F_arr = k * q1_C * q2_C / r_arr**2
    E_arr = k * abs(q1_C) / r_arr**2

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(r_arr * 100, F_arr, "b-", lw=2)
    axes[0].scatter([r], [F], color="red", s=100, zorder=3)
    axes[0].set_xlabel("Distance r (cm)")
    axes[0].set_ylabel("Force F (N)")
    axes[0].set_title("Coulomb's Law: F vs r")
    axes[0].grid(True, alpha=0.25)

    axes[1].plot(r_arr * 100, E_arr, "r-", lw=2)
    axes[1].scatter([r], [E1], color="blue", s=100, zorder=3)
    axes[1].set_xlabel("Distance r (cm)")
    axes[1].set_ylabel("Electric Field E (N/C)")
    axes[1].set_title("Electric Field due to q₁")
    axes[1].grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _ohm_circuits():
    st.latex(r"V = IR \quad;\quad P = IV = I^2R = \frac{V^2}{R}")

    with st.sidebar.expander("Circuit Controls", expanded=True):
        V = st.slider("EMF (V)", 1.0, 24.0, 12.0, step=0.5)
        R1 = st.slider("R₁ (Ω)", 1.0, 100.0, 10.0, step=1.0)
        R2 = st.slider("R₂ (Ω)", 1.0, 100.0, 20.0, step=1.0)
        config = st.radio("Configuration", ["Series", "Parallel"], horizontal=True)

    if config == "Series":
        R_eq = R1 + R2
        I_total = V / R_eq
        V1 = I_total * R1
        V2 = I_total * R2
        I1 = I2 = I_total
    else:
        R_eq = (R1 * R2) / (R1 + R2)
        I_total = V / R_eq
        I1 = V / R1
        I2 = V / R2
        V1 = V2 = V

    P_total = V * I_total

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("R_eq (Ω)", f"{R_eq:.2f}")
    col2.metric("I_total (A)", f"{I_total:.3f}")
    col3.metric("P_total (W)", f"{P_total:.3f}")
    col4.metric("Config", config)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    labels = ["R₁", "R₂"]
    voltages = [V1, V2]
    currents = [I1, I2]
    colors = ["#3498db", "#e74c3c"]

    axes[0].bar(labels, voltages, color=colors, alpha=0.8)
    axes[0].set_ylabel("Voltage (V)")
    axes[0].set_title(f"Voltage Distribution ({config})")
    axes[0].grid(True, alpha=0.25, axis="y")

    axes[1].bar(labels, currents, color=colors, alpha=0.8)
    axes[1].set_ylabel("Current (A)")
    axes[1].set_title(f"Current Distribution ({config})")
    axes[1].grid(True, alpha=0.25, axis="y")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**{config} Circuit:**
- R₁ = {R1} Ω → V₁ = {V1:.2f} V, I₁ = {I1:.3f} A, P₁ = {V1*I1:.3f} W
- R₂ = {R2} Ω → V₂ = {V2:.2f} V, I₂ = {I2:.3f} A, P₂ = {V2*I2:.3f} W
""")


def _em_induction():
    st.latex(r"\mathcal{E} = -N\frac{d\Phi}{dt} \quad;\quad \Phi = BA\cos\theta")

    with st.sidebar.expander("EM Induction Controls", expanded=True):
        N = st.slider("Number of turns N", 1, 200, 50, step=10)
        B = st.slider("Magnetic field B (T)", 0.01, 1.0, 0.1, step=0.01)
        A = st.slider("Loop area A (cm²)", 1.0, 100.0, 25.0, step=5.0) / 1e4
        omega = st.slider("Angular velocity ω (rad/s)", 1.0, 100.0, 10.0, step=1.0)

    t = np.linspace(0, 2 * np.pi / omega * 3, 500)
    flux = N * B * A * np.cos(omega * t)
    emf = N * B * A * omega * np.sin(omega * t)
    emf_max = N * B * A * omega

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(t, flux * 1e3, "b-", lw=2)
    axes[0].set_ylabel("Flux linkage NΦ (mWb)")
    axes[0].set_title("Magnetic Flux Linkage vs Time")
    axes[0].grid(True, alpha=0.25)

    axes[1].plot(t, emf, "r-", lw=2)
    axes[1].axhline(emf_max, color="gray", linestyle="--", alpha=0.5, label=f"ε_max = {emf_max:.3f} V")
    axes[1].axhline(-emf_max, color="gray", linestyle="--", alpha=0.5)
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Induced EMF ε (V)")
    axes[1].set_title("Faraday's Law — Induced EMF")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**Peak EMF:** ε_max = NBAω = {N} × {B} × {A*1e4:.0f}×10⁻⁴ × {omega} = **{emf_max:.4f} V**  
**Frequency:** f = ω/2π = **{omega/(2*np.pi):.2f} Hz**
""")
