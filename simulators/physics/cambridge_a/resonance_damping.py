"""Resonance & Damped Oscillations — Advanced Pack (Grades 11–12)."""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("🔔 Resonance & Damped Oscillations")

    tab1, tab2 = st.tabs(["Damped Oscillation", "Forced Oscillation & Resonance"])

    with tab1:
        st.markdown("Observe how damping reduces the amplitude of oscillations over time.")
        c1, c2, c3 = st.columns(3)
        A0 = c1.slider("Initial amplitude (m)", 0.1, 5.0, 2.0, 0.1)
        omega = c2.slider("Natural frequency ω₀ (rad/s)", 1.0, 20.0, 5.0, 0.5)
        gamma = c3.slider("Damping coefficient γ (s⁻¹)", 0.0, 5.0, 0.5, 0.05)

        t = np.linspace(0, 10, 1000)

        if gamma < omega:
            # Under-damped
            omega_d = np.sqrt(omega**2 - gamma**2)
            x = A0 * np.exp(-gamma * t) * np.cos(omega_d * t)
            regime = "Under-damped"
        elif abs(gamma - omega) < 0.01:
            # Critically damped
            x = A0 * (1 + omega * t) * np.exp(-gamma * t)
            regime = "Critically damped"
        else:
            # Over-damped
            r1 = -gamma + np.sqrt(gamma**2 - omega**2)
            r2 = -gamma - np.sqrt(gamma**2 - omega**2)
            x = A0 * (np.exp(r1 * t) + np.exp(r2 * t)) / 2
            regime = "Over-damped"

        envelope = A0 * np.exp(-gamma * t)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(t, x, "b-", linewidth=1.5, label="Displacement")
        if gamma > 0 and gamma < omega:
            ax.plot(t, envelope, "r--", alpha=0.5, label="Envelope")
            ax.plot(t, -envelope, "r--", alpha=0.5)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Displacement (m)")
        ax.set_title(f"Damped Oscillation — {regime}")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)

        st.latex(r"x(t) = A_0 \, e^{-\gamma t} \cos(\omega_d t), \quad \omega_d = \sqrt{\omega_0^2 - \gamma^2}")

        m1, m2 = st.columns(2)
        m1.metric("Regime", regime)
        if gamma > 0:
            m2.metric("Half-life", f"{np.log(2)/gamma:.2f} s")

    with tab2:
        st.markdown("Drive an oscillator at varying frequencies and observe resonance.")
        c1, c2, c3 = st.columns(3)
        omega_0 = c1.slider("Natural freq ω₀ (rad/s)", 1.0, 20.0, 10.0, 0.5, key="w0_res")
        gamma_r = c2.slider("Damping γ (s⁻¹)", 0.1, 5.0, 0.5, 0.1, key="g_res")
        F0 = c3.slider("Driving force amplitude F₀", 0.1, 10.0, 1.0, 0.1)

        omega_drive = np.linspace(0.1, 2.5 * omega_0, 500)
        # Steady-state amplitude: A = F0 / sqrt((omega_0^2 - omega^2)^2 + (2*gamma*omega)^2)
        A_resp = F0 / np.sqrt((omega_0**2 - omega_drive**2)**2 + (2 * gamma_r * omega_drive)**2)

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.plot(omega_drive, A_resp, "b-", linewidth=2)
        ax2.axvline(omega_0, color="red", linestyle="--", alpha=0.6, label=f"ω₀ = {omega_0}")

        # Plot for different damping values
        for g_val, c, ls in [(0.2, "#2ecc71", ":"), (1.0, "#e67e22", "-."), (3.0, "#95a5a6", "--")]:
            if abs(g_val - gamma_r) > 0.05:
                A_g = F0 / np.sqrt((omega_0**2 - omega_drive**2)**2 + (2 * g_val * omega_drive)**2)
                ax2.plot(omega_drive, A_g, color=c, linestyle=ls, alpha=0.5, label=f"γ = {g_val}")

        ax2.set_xlabel("Driving frequency ω (rad/s)")
        ax2.set_ylabel("Amplitude (m)")
        ax2.set_title("Resonance Curve")
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)
        plt.close(fig2)

        omega_res = np.sqrt(max(omega_0**2 - 2 * gamma_r**2, 0.01))
        st.metric("Resonance frequency ω_res", f"{omega_res:.2f} rad/s")

        st.latex(
            r"A(\omega) = \frac{F_0}{\sqrt{(\omega_0^2-\omega^2)^2 + (2\gamma\omega)^2}}"
        )
        st.info("At resonance, the driving frequency matches the system's natural frequency, "
                "producing maximum amplitude. Higher damping flattens and broadens the peak.")
