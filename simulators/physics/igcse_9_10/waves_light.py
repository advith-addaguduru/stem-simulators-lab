"""IGCSE Grades 9-10 Physics: Waves & Light Simulator"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulators.utils import nice_axes


def simulate():
    st.subheader("Waves & Light")
    st.latex(r"v = f\lambda \qquad n = \frac{\sin\theta_i}{\sin\theta_r}")

    mode = st.radio(
        "Choose a topic",
        ["Wave Properties", "Reflection & Refraction", "Total Internal Reflection"],
        horizontal=True,
    )

    if mode == "Wave Properties":
        _wave_properties()
    elif mode == "Reflection & Refraction":
        _refraction()
    else:
        _tir()


def _wave_properties():
    st.markdown("### Transverse & Longitudinal Waves")

    with st.sidebar.expander("Wave Controls", expanded=True):
        frequency = st.slider("Frequency f (Hz)", 0.5, 5.0, 1.0, step=0.25)
        wavelength = st.slider("Wavelength λ (m)", 0.5, 5.0, 2.0, step=0.25)
        amplitude = st.slider("Amplitude A (m)", 0.2, 2.0, 1.0, step=0.1)

    velocity = frequency * wavelength
    period = 1 / frequency
    c1, c2, c3 = st.columns(3)
    c1.metric("Wave speed v", f"{velocity:.2f} m/s")
    c2.metric("Period T", f"{period:.2f} s")
    c3.metric("v = fλ", f"{frequency} × {wavelength} = {velocity:.2f}")

    x = np.linspace(0, 10, 500)
    t = 0
    k = 2 * np.pi / wavelength
    omega = 2 * np.pi * frequency
    y = amplitude * np.sin(k * x - omega * t)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    ax1.plot(x, y, linewidth=2, color="#2563eb")
    ax1.axhline(0, color="grey", linewidth=0.5)

    ax1.annotate("", xy=(wavelength, amplitude * 0.8), xytext=(0, amplitude * 0.8),
                 arrowprops=dict(arrowstyle="<->", color="#ef4444", lw=2))
    ax1.text(wavelength / 2, amplitude * 0.9, f"λ = {wavelength} m",
             ha="center", color="#ef4444", fontsize=10)

    ax1.annotate("", xy=(-0.2, amplitude), xytext=(-0.2, 0),
                 arrowprops=dict(arrowstyle="<->", color="#22c55e", lw=2))
    ax1.text(-0.5, amplitude / 2, f"A = {amplitude}", ha="right",
             color="#22c55e", fontsize=10)

    nice_axes(ax1, "Position (m)", "Displacement (m)", "Transverse Wave")

    # Longitudinal wave representation
    n_particles = 80
    x_eq = np.linspace(0.2, 9.8, n_particles)
    displacement = 0.3 * np.sin(k * x_eq)
    x_displaced = x_eq + displacement

    ax2.scatter(x_displaced, np.zeros(n_particles), c=displacement,
                cmap="coolwarm", s=30, edgecolor="none")
    ax2.set_xlim(0, 10)
    ax2.set_ylim(-0.5, 0.5)
    ax2.set_yticks([])
    ax2.set_xlabel("Position (m)")
    ax2.set_title("Longitudinal Wave (compressions & rarefactions)")
    ax2.grid(True, alpha=0.3, axis="x")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _refraction():
    st.markdown("### Snell's Law — Refraction")
    st.latex(r"n_1 \sin\theta_i = n_2 \sin\theta_r")

    with st.sidebar.expander("Refraction Controls", expanded=True):
        n1 = st.slider("Refractive index n₁", 1.0, 2.5, 1.0, step=0.1)
        n2 = st.slider("Refractive index n₂", 1.0, 2.5, 1.5, step=0.1)
        angle_i = st.slider("Angle of incidence (°)", 0, 89, 30)

    theta_i = np.radians(angle_i)
    sin_r = n1 * np.sin(theta_i) / n2

    fig, ax = plt.subplots(figsize=(6, 8))

    # Interface
    ax.axhline(0, color="grey", linewidth=2)
    ax.axvline(0, color="grey", linewidth=0.5, linestyle="--", label="Normal")
    ax.fill_between([-5, 5], 0, 5, color="#e0f2fe", alpha=0.5)
    ax.fill_between([-5, 5], -5, 0, color="#dbeafe", alpha=0.8)
    ax.text(3.5, 4, f"n₁ = {n1}", fontsize=12, color="#2563eb")
    ax.text(3.5, -4.5, f"n₂ = {n2}", fontsize=12, color="#2563eb")

    # Incident ray
    ray_len = 4.5
    xi = -ray_len * np.sin(theta_i)
    yi = ray_len * np.cos(theta_i)
    ax.annotate("", xy=(0, 0), xytext=(xi, yi),
                arrowprops=dict(arrowstyle="-|>", color="#ef4444", lw=2))

    if sin_r <= 1:
        theta_r = np.arcsin(sin_r)
        angle_r = np.degrees(theta_r)

        xr = ray_len * np.sin(theta_r)
        yr = -ray_len * np.cos(theta_r)
        ax.annotate("", xy=(xr, yr), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color="#22c55e", lw=2))

        # Angle arcs
        arc_i = np.linspace(np.pi / 2 - theta_i, np.pi / 2, 50)
        ax.plot(1.5 * np.cos(arc_i), 1.5 * np.sin(arc_i), color="#ef4444")
        ax.text(0.3, 1.8, f"θᵢ = {angle_i}°", color="#ef4444", fontsize=10)

        arc_r = np.linspace(-np.pi / 2, -np.pi / 2 + theta_r, 50)
        ax.plot(1.5 * np.cos(arc_r), 1.5 * np.sin(arc_r), color="#22c55e")
        ax.text(0.3, -2.2, f"θᵣ = {angle_r:.1f}°", color="#22c55e", fontsize=10)

        c1, c2, c3 = st.columns(3)
        c1.metric("Angle of incidence", f"{angle_i}°")
        c2.metric("Angle of refraction", f"{angle_r:.1f}°")
        c3.metric("Speed ratio", f"{n2 / n1:.2f}")
    else:
        # Total internal reflection
        ax.text(0, -2, "TOTAL INTERNAL\nREFLECTION", ha="center",
                fontsize=14, color="#ef4444", fontweight="bold")
        xr = ray_len * np.sin(theta_i)
        yr = ray_len * np.cos(theta_i)
        ax.annotate("", xy=(xr, yr), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color="#f59e0b", lw=2, linestyle="--"))

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Ray Diagram")
    ax.legend()
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _tir():
    st.markdown("### Total Internal Reflection")
    st.latex(r"\sin\theta_c = \frac{n_2}{n_1} \quad (n_1 > n_2)")

    with st.sidebar.expander("TIR Controls", expanded=True):
        n1 = st.slider("Denser medium n₁ ", 1.2, 2.5, 1.5, step=0.1)
        n2_tir = st.slider("Less dense medium n₂ ", 1.0, 2.4, 1.0, step=0.1)

    if n1 <= n2_tir:
        st.warning("n₁ must be greater than n₂ for TIR to occur.")
        return

    critical_angle = np.degrees(np.arcsin(n2_tir / n1))
    st.success(f"**Critical angle** θc = {critical_angle:.1f}°")

    fig, ax = plt.subplots(figsize=(10, 4))

    angles = np.arange(0, 90, 1)
    refracted = []
    for a in angles:
        sin_r = n1 * np.sin(np.radians(a)) / n2_tir
        if sin_r <= 1:
            refracted.append(np.degrees(np.arcsin(sin_r)))
        else:
            refracted.append(np.nan)

    ax.plot(angles, refracted, linewidth=2, color="#2563eb", label="Refracted angle")
    ax.axvline(critical_angle, color="#ef4444", linestyle="--", linewidth=2,
               label=f"Critical angle = {critical_angle:.1f}°")
    ax.fill_between(angles, 0, 90, where=[a > critical_angle for a in angles],
                    alpha=0.15, color="#ef4444", label="TIR region")
    nice_axes(ax, "Angle of incidence (°)", "Angle of refraction (°)",
              f"TIR Diagram (n₁ = {n1}, n₂ = {n2_tir})")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 95)
    ax.legend()

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.info(
        "💡 **Applications:** optical fibres (communication), prisms in binoculars, "
        "diamond sparkle (high n → small θc)."
    )
