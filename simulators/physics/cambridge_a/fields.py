"""Cambridge A-Level Physics: Fields (Gravitational & Electric)"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulators.utils import nice_axes


G = 6.674e-11  # gravitational constant


def simulate():
    st.subheader("Gravitational & Electric Fields")
    st.latex(
        r"g = \frac{GM}{r^2} \qquad E = \frac{kQ}{r^2} \qquad "
        r"v_{orb} = \sqrt{\frac{GM}{r}}"
    )

    mode = st.radio(
        "Choose a topic",
        ["Gravitational Field", "Electric Field", "Orbital Mechanics"],
        horizontal=True,
    )

    if mode == "Gravitational Field":
        _gravitational()
    elif mode == "Electric Field":
        _electric()
    else:
        _orbital()


def _gravitational():
    st.markdown("### Gravitational Field Strength")

    with st.sidebar.expander("Gravity Controls", expanded=True):
        mass_exp = st.slider("Planet mass (×10²⁴ kg)", 0.1, 20.0, 5.97, step=0.1)
        radius_km = st.slider("Planet radius (km)", 1000, 15000, 6371, step=100)

    mass = mass_exp * 1e24
    radius = radius_km * 1e3

    g_surface = G * mass / radius**2

    c1, c2 = st.columns(2)
    c1.metric("Surface gravity g", f"{g_surface:.2f} m/s²")
    c2.metric("Escape velocity", f"{np.sqrt(2 * G * mass / radius):.0f} m/s")

    r = np.linspace(radius, radius * 5, 300)
    g = G * mass / r**2

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.plot(r / 1e6, g, linewidth=2, color="#2563eb")
    ax1.axvline(radius / 1e6, color="#ef4444", linestyle="--",
                label=f"Surface R = {radius_km} km")
    nice_axes(ax1, "Distance from centre (×10⁶ m)", "g (m/s²)",
              "Gravitational field strength vs distance")
    ax1.legend()

    # Potential
    V = -G * mass / r
    ax2.plot(r / 1e6, V / 1e6, linewidth=2, color="#f97316")
    nice_axes(ax2, "Distance (×10⁶ m)", "Potential (MJ/kg)",
              "Gravitational Potential")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.info(
        f"💡 **Earth comparison:** g = 9.81 m/s². Your planet: g = {g_surface:.2f} m/s² "
        f"({g_surface / 9.81:.2f}× Earth)."
    )


def _electric():
    st.markdown("### Electric Field")
    st.latex(r"E = \frac{kQ}{r^2} \qquad V = \frac{kQ}{r}")

    k = 8.99e9

    with st.sidebar.expander("Electric Field Controls", expanded=True):
        charge_nc = st.slider("Charge Q (nC)", -100, 100, 50, step=5)
        show_field_lines = st.checkbox("Show field lines", value=True)

    Q = charge_nc * 1e-9

    if show_field_lines and Q != 0:
        fig, ax = plt.subplots(figsize=(8, 8))

        n_lines = 12
        for i in range(n_lines):
            angle = 2 * np.pi * i / n_lines
            r_vals = np.linspace(0.02, 0.5, 200)
            x = r_vals * np.cos(angle)
            y = r_vals * np.sin(angle)
            if Q > 0:
                ax.annotate("", xy=(x[-1], y[-1]), xytext=(x[0], y[0]),
                            arrowprops=dict(arrowstyle="->", color="#ef4444", lw=1))
            else:
                ax.annotate("", xy=(x[0], y[0]), xytext=(x[-1], y[-1]),
                            arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=1))
            ax.plot(x, y, color="#ef4444" if Q > 0 else "#3b82f6", linewidth=0.8)

        colour = "#ef4444" if Q > 0 else "#3b82f6"
        sign = "+" if Q > 0 else "−"
        ax.plot(0, 0, "o", markersize=20, color=colour)
        ax.text(0, 0, sign, ha="center", va="center", fontsize=14,
                fontweight="bold", color="white")

        ax.set_xlim(-0.6, 0.6)
        ax.set_ylim(-0.6, 0.6)
        ax.set_aspect("equal")
        ax.set_title(f"Electric Field Lines ({sign}{abs(charge_nc)} nC)")
        ax.grid(True, alpha=0.2)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    if Q != 0:
        r = np.linspace(0.01, 0.5, 300)
        E = k * abs(Q) / r**2
        V = k * Q / r

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.plot(r * 100, E, linewidth=2, color="#2563eb")
        nice_axes(ax1, "Distance (cm)", "E (N/C)", "Electric Field Strength")

        ax2.plot(r * 100, V, linewidth=2, color="#f97316")
        ax2.axhline(0, color="grey", linewidth=0.5)
        nice_axes(ax2, "Distance (cm)", "V (V)", "Electric Potential")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("Set a non-zero charge to see field plots.")


def _orbital():
    st.markdown("### Orbital Mechanics")
    st.latex(r"v_{orb} = \sqrt{\frac{GM}{r}} \qquad T = 2\pi\sqrt{\frac{r^3}{GM}}")

    with st.sidebar.expander("Orbit Controls", expanded=True):
        mass_exp = st.slider("Central mass (×10²⁴ kg) ", 0.1, 20.0, 5.97, step=0.1)
        alt_km = st.slider("Orbital altitude (km)", 200, 50000, 400, step=100)

    mass = mass_exp * 1e24
    r_earth = 6.371e6
    r_orbit = r_earth + alt_km * 1e3

    v_orb = np.sqrt(G * mass / r_orbit)
    period = 2 * np.pi * r_orbit / v_orb

    c1, c2, c3 = st.columns(3)
    c1.metric("Orbital speed", f"{v_orb:.0f} m/s")
    c2.metric("Period", f"{period / 3600:.2f} hours")
    c3.metric("Orbital radius", f"{r_orbit / 1e6:.1f} × 10⁶ m")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Orbit visualisation
    theta = np.linspace(0, 2 * np.pi, 300)
    ax1.plot(r_orbit * np.cos(theta) / 1e6, r_orbit * np.sin(theta) / 1e6,
             linewidth=2, color="#2563eb", label="Orbit")
    earth = plt.Circle((0, 0), r_earth / 1e6, color="#22c55e", alpha=0.5, label="Planet")
    ax1.add_patch(earth)
    ax1.plot(r_orbit / 1e6, 0, "o", color="#ef4444", markersize=8, label="Satellite")
    ax1.set_aspect("equal")
    ax1.set_xlabel("× 10⁶ m")
    ax1.set_ylabel("× 10⁶ m")
    ax1.set_title("Orbit Diagram")
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.2)

    # v and T vs altitude
    alts = np.linspace(200, 50000, 200) * 1e3
    rs = r_earth + alts
    vs = np.sqrt(G * mass / rs)
    ts = 2 * np.pi * rs / vs / 3600  # hours

    ax2.plot(alts / 1e3, vs / 1e3, linewidth=2, color="#2563eb", label="Speed")
    ax2.axvline(alt_km, color="red", linestyle="--", alpha=0.5)
    nice_axes(ax2, "Altitude (km)", "Orbital speed (km/s)", "Speed vs Altitude")
    ax2.legend()

    ax2b = ax2.twinx()
    ax2b.plot(alts / 1e3, ts, linewidth=2, color="#f97316", linestyle="--", label="Period")
    ax2b.set_ylabel("Period (hours)", color="#f97316")
    ax2b.legend(loc="center right")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    if abs(period / 3600 - 24) < 1:
        st.success("🛰️ This is close to a **geostationary orbit** (T ≈ 24 h)!")
