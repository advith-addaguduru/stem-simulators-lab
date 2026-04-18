"""Cambridge A Level Physics: Thermal Physics & Oscillations Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("A Level Physics — Thermal Physics & Oscillations")

    mode = st.radio(
        "Select topic",
        ["Thermal Physics", "Damped Oscillations", "Circular Motion"],
        horizontal=True,
    )

    if mode == "Thermal Physics":
        _thermal()
    elif mode == "Damped Oscillations":
        _damped_oscillations()
    else:
        _circular_motion()


def _thermal():
    st.latex(r"pV = nRT \quad;\quad E_k = \tfrac{3}{2}k_BT \quad;\quad \Delta U = q + w")

    with st.sidebar.expander("Thermal Physics Controls", expanded=True):
        n = st.slider("Moles n", 0.1, 5.0, 1.0, step=0.1)
        process = st.selectbox("Thermodynamic process", [
            "Isothermal (constant T)",
            "Isobaric (constant P)",
            "Isochoric (constant V)",
            "Adiabatic",
        ])
        T1 = st.slider("Initial temperature T₁ (K)", 200, 600, 300, step=10)
        V1 = st.slider("Initial volume V₁ (L)", 1.0, 50.0, 10.0, step=1.0)

    R = 8.314
    P1 = n * R * T1 / (V1 * 1e-3)  # Pa
    gamma = 5 / 3  # monatomic ideal gas

    V = np.linspace(max(V1 * 0.2, 0.5), V1 * 3, 500) * 1e-3  # m³

    if process == "Isothermal (constant T)":
        P = n * R * T1 / V
        label = f"Isothermal T={T1} K"
    elif process == "Isobaric (constant P)":
        P = np.full_like(V, P1)
        label = f"Isobaric P={P1:.0f} Pa"
    elif process == "Isochoric (constant V)":
        T_range = np.linspace(200, 600, 500)
        P_iso = n * R * T_range / (V1 * 1e-3)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(T_range, P_iso / 1e3, "b-", lw=2)
        ax.scatter([T1], [P1 / 1e3], color="red", s=100, zorder=3)
        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel("Pressure (kPa)")
        ax.set_title(f"Isochoric Process (V = {V1} L)")
        ax.grid(True, alpha=0.25)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown(f"**P₁ = {P1/1e3:.2f} kPa at T = {T1} K, V = {V1} L**")
        return
    else:
        P = P1 * (V1 * 1e-3 / V) ** gamma
        label = f"Adiabatic γ={gamma:.2f}"

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(V * 1e3, P / 1e3, "b-", lw=2, label=label)
    ax.scatter([V1], [P1 / 1e3], color="red", s=100, zorder=3, label=f"State 1 ({V1} L, {P1/1e3:.1f} kPa)")
    ax.set_xlabel("Volume (L)")
    ax.set_ylabel("Pressure (kPa)")
    ax.set_title("P–V Diagram")
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    Ek = 1.5 * 1.381e-23 * T1
    st.markdown(f"""
**State 1:** P = {P1/1e3:.2f} kPa, V = {V1} L, T = {T1} K  
**Mean KE per molecule:** {Ek:.4e} J  
**Internal energy (monatomic):** U = {1.5 * n * R * T1:.1f} J
""")


def _damped_oscillations():
    st.latex(r"x(t) = A_0 e^{-\gamma t}\cos(\omega' t + \phi) \quad;\quad \omega' = \sqrt{\omega_0^2 - \gamma^2}")

    with st.sidebar.expander("Damped Oscillation Controls", expanded=True):
        A0 = st.slider("Initial amplitude A₀ (m)", 0.1, 2.0, 1.0, step=0.1)
        f0 = st.slider("Natural frequency f₀ (Hz)", 0.5, 5.0, 1.0, step=0.1)
        gamma = st.slider("Damping coefficient γ (s⁻¹)", 0.0, 5.0, 0.3, step=0.1)
        t_max = st.slider("Duration (s)", 2.0, 20.0, 10.0, step=1.0)

    omega0 = 2 * np.pi * f0
    t = np.linspace(0, t_max, 1000)

    if gamma < omega0:
        omega_d = np.sqrt(omega0**2 - gamma**2)
        x = A0 * np.exp(-gamma * t) * np.cos(omega_d * t)
        regime = "Underdamped"
    elif gamma == omega0:
        x = A0 * (1 + omega0 * t) * np.exp(-gamma * t)
        regime = "Critically damped"
    else:
        beta = np.sqrt(gamma**2 - omega0**2)
        x = A0 * np.exp(-gamma * t) * np.cosh(beta * t)
        regime = "Overdamped"

    envelope = A0 * np.exp(-gamma * t)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, x, "b-", lw=2, label=f"x(t) — {regime}")
    ax.plot(t, envelope, "r--", alpha=0.5, label="Envelope")
    ax.plot(t, -envelope, "r--", alpha=0.5)
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Displacement (m)")
    ax.set_title(f"Damped Oscillation — {regime}")
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    Q = omega0 / (2 * gamma) if gamma > 0 else float("inf")
    st.markdown(f"""
**Regime:** {regime}  
**Quality factor Q:** {Q:.2f}  
**Energy half-life:** {np.log(2) / (2 * gamma):.3f} s (approx)
""" if gamma > 0 else f"**Regime:** Undamped (no energy loss)")


def _circular_motion():
    st.latex(r"a_c = \frac{v^2}{r} = \omega^2 r \quad;\quad F_c = \frac{mv^2}{r}")

    with st.sidebar.expander("Circular Motion Controls", expanded=True):
        m = st.slider("Mass m (kg)", 0.1, 10.0, 1.0, step=0.1)
        r = st.slider("Radius r (m)", 0.5, 10.0, 2.0, step=0.5)
        v = st.slider("Speed v (m/s)", 1.0, 30.0, 5.0, step=0.5)

    omega = v / r
    T = 2 * np.pi / omega
    ac = v**2 / r
    Fc = m * ac

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("ω (rad/s)", f"{omega:.3f}")
    col2.metric("Period T (s)", f"{T:.3f}")
    col3.metric("a_c (m/s²)", f"{ac:.3f}")
    col4.metric("F_c (N)", f"{Fc:.3f}")

    theta = np.linspace(0, 2 * np.pi, 200)
    x_circle = r * np.cos(theta)
    y_circle = r * np.sin(theta)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(x_circle, y_circle, "b-", lw=2)
    axes[0].scatter([r], [0], color="red", s=150, zorder=3, label="Object")
    axes[0].annotate("", xy=(0, 0), xytext=(r, 0),
                     arrowprops=dict(arrowstyle="<-", color="green", lw=2))
    axes[0].text(r / 2, -0.5, f"r = {r} m", ha="center", color="green")
    axes[0].annotate("", xy=(r, 1.5), xytext=(r, 0),
                     arrowprops=dict(arrowstyle="->", color="blue", lw=2))
    axes[0].text(r + 0.3, 0.7, f"v = {v} m/s", color="blue")
    axes[0].set_aspect("equal")
    axes[0].set_title("Circular Path")
    axes[0].grid(True, alpha=0.25)
    axes[0].legend()

    radii = np.linspace(0.5, 10, 100)
    Fc_curve = m * v**2 / radii
    axes[1].plot(radii, Fc_curve, "r-", lw=2)
    axes[1].scatter([r], [Fc], color="blue", s=100, zorder=3, label="Current")
    axes[1].set_xlabel("Radius (m)")
    axes[1].set_ylabel("Centripetal Force (N)")
    axes[1].set_title("F_c vs Radius (constant v)")
    axes[1].legend()
    axes[1].grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
