"""Epidemiology Simulator (SIR Model) — Cross-Disciplinary Enrichment Pack."""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


def simulate():
    st.header("🦠 Epidemiology — SIR Model")

    tab1, tab2 = st.tabs(["SIR Dynamics", "Herd Immunity"])

    with tab1:
        st.markdown(
            "The **SIR model** divides a population into Susceptible (S), "
            "Infected (I), and Recovered (R) compartments."
        )
        c1, c2, c3 = st.columns(3)
        N = c1.slider("Population N", 1000, 1_000_000, 100_000, 1000)
        beta = c2.slider("Transmission rate β (per day)", 0.01, 1.0, 0.3, 0.01)
        gamma = c3.slider("Recovery rate γ (per day)", 0.01, 1.0, 0.1, 0.01)

        I0 = st.slider("Initial infected", 1, max(N // 100, 1), max(N // 1000, 1), 1)
        days = st.slider("Simulation days", 30, 365, 160, 5)

        R0 = beta / gamma

        def sir_model(y, _t, _N, _beta, _gamma):
            S, I, R = y
            dSdt = -_beta * S * I / _N
            dIdt = _beta * S * I / _N - _gamma * I
            dRdt = _gamma * I
            return [dSdt, dIdt, dRdt]

        t = np.linspace(0, days, days * 10)
        y0 = [N - I0, I0, 0]
        solution = odeint(sir_model, y0, t, args=(N, beta, gamma))
        S, I, R = solution.T

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        ax1.plot(t, S, "b-", linewidth=2, label="Susceptible")
        ax1.plot(t, I, "r-", linewidth=2, label="Infected")
        ax1.plot(t, R, "g-", linewidth=2, label="Recovered")
        ax1.set_xlabel("Days")
        ax1.set_ylabel("Population")
        ax1.set_title("SIR Model")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # New infections per day
        new_infections = beta * S * I / N
        ax2.plot(t, new_infections, "r-", linewidth=2)
        ax2.set_xlabel("Days")
        ax2.set_ylabel("New infections / day")
        ax2.set_title("Epidemic Curve")
        ax2.grid(True, alpha=0.3)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        peak_infected = int(np.max(I))
        peak_day = int(t[np.argmax(I)])
        total_infected = int(R[-1])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("R₀", f"{R0:.2f}")
        c2.metric("Peak infected", f"{peak_infected:,}")
        c3.metric("Peak day", f"Day {peak_day}")
        c4.metric("Total affected", f"{total_infected:,}")

        if R0 > 1:
            st.warning(f"R₀ = {R0:.2f} > 1 — the disease will spread through the population.")
        else:
            st.success(f"R₀ = {R0:.2f} < 1 — the outbreak will die out naturally.")

        st.latex(
            r"\frac{dS}{dt} = -\frac{\beta S I}{N}, \quad "
            r"\frac{dI}{dt} = \frac{\beta S I}{N} - \gamma I, \quad "
            r"\frac{dR}{dt} = \gamma I"
        )
        st.latex(r"R_0 = \frac{\beta}{\gamma}")

    with tab2:
        st.markdown(
            "**Herd immunity** is reached when enough of the population is immune "
            "so that the disease cannot spread effectively."
        )
        c1, c2 = st.columns(2)
        beta_h = c1.slider("β", 0.05, 1.0, 0.4, 0.01, key="beta_h")
        gamma_h = c2.slider("γ", 0.01, 1.0, 0.1, 0.01, key="gamma_h")
        R0_h = beta_h / gamma_h

        vacc_pct = st.slider("Vaccination coverage (%)", 0, 100, 0, 1)

        # Effective R = R0 * (1 - vaccination fraction)
        R_eff = R0_h * (1 - vacc_pct / 100)
        herd_threshold = max(0, 1 - 1 / R0_h) * 100 if R0_h > 1 else 0

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        vacc_range = np.linspace(0, 100, 200)
        R_eff_range = R0_h * (1 - vacc_range / 100)
        ax2.plot(vacc_range, R_eff_range, "b-", linewidth=2)
        ax2.axhline(1, color="red", linestyle="--", label="R_eff = 1 (threshold)")
        ax2.axvline(vacc_pct, color="green", linestyle="--", alpha=0.5, label=f"Current: {vacc_pct}%")
        if R0_h > 1:
            ax2.axvline(herd_threshold, color="orange", linestyle=":", alpha=0.7,
                        label=f"Herd immunity: {herd_threshold:.0f}%")
        ax2.set_xlabel("Vaccination coverage (%)")
        ax2.set_ylabel("Effective R₀")
        ax2.set_title("Vaccination & Herd Immunity")
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(bottom=0)
        st.pyplot(fig2)
        plt.close(fig2)

        c1, c2, c3 = st.columns(3)
        c1.metric("Basic R₀", f"{R0_h:.2f}")
        c2.metric("Effective R₀", f"{R_eff:.2f}")
        c3.metric("Herd immunity threshold", f"{herd_threshold:.0f}%")

        if R_eff < 1:
            st.success("Disease cannot spread — herd immunity achieved!")
        else:
            needed = herd_threshold - vacc_pct
            st.info(f"Need {needed:.0f}% more coverage to reach herd immunity.")

        st.latex(r"R_{\text{eff}} = R_0 (1 - p), \quad p_{\text{herd}} = 1 - \frac{1}{R_0}")
