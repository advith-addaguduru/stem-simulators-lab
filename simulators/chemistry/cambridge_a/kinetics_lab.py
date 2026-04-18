"""Chemical Kinetics Laboratory — Advanced Pack (Grades 11–12)."""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("⏱️ Chemical Kinetics Laboratory")

    tab1, tab2, tab3 = st.tabs(["Reaction Orders", "Arrhenius Plot", "Half-Life"])

    with tab1:
        st.markdown("Compare zero, first, and second order reaction kinetics.")
        c1, c2, c3 = st.columns(3)
        A0 = c1.slider("Initial conc. [A]₀ (mol/L)", 0.1, 5.0, 1.0, 0.1)
        k_val = c2.slider("Rate constant k", 0.01, 2.0, 0.5, 0.01)
        order = c3.radio("Reaction order", [0, 1, 2], horizontal=True)

        t_max = 10.0
        t = np.linspace(0, t_max, 500)

        if order == 0:
            # [A] = [A]₀ - kt
            conc = np.maximum(A0 - k_val * t, 0)
            rate_eq = r"[\text{A}] = [\text{A}]_0 - kt"
            unit = "mol L⁻¹ s⁻¹"
        elif order == 1:
            # [A] = [A]₀ * exp(-kt)
            conc = A0 * np.exp(-k_val * t)
            rate_eq = r"[\text{A}] = [\text{A}]_0 \, e^{-kt}"
            unit = "s⁻¹"
        else:
            # 1/[A] = 1/[A]₀ + kt
            conc = 1.0 / (1.0 / A0 + k_val * t)
            rate_eq = r"\frac{1}{[\text{A}]} = \frac{1}{[\text{A}]_0} + kt"
            unit = "L mol⁻¹ s⁻¹"

        fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))

        # [A] vs t
        axes[0].plot(t, conc, "b-", linewidth=2)
        axes[0].set_xlabel("Time (s)")
        axes[0].set_ylabel("[A] (mol/L)")
        axes[0].set_title("[A] vs Time")
        axes[0].grid(True, alpha=0.3)

        # ln[A] vs t (diagnostic for 1st order)
        ln_conc = np.log(np.maximum(conc, 1e-12))
        axes[1].plot(t, ln_conc, "r-", linewidth=2)
        axes[1].set_xlabel("Time (s)")
        axes[1].set_ylabel("ln[A]")
        axes[1].set_title("ln[A] vs Time")
        axes[1].grid(True, alpha=0.3)
        if order == 1:
            axes[1].set_facecolor("#f0fff0")

        # 1/[A] vs t (diagnostic for 2nd order)
        inv_conc = 1.0 / np.maximum(conc, 1e-12)
        axes[2].plot(t, inv_conc, "g-", linewidth=2)
        axes[2].set_xlabel("Time (s)")
        axes[2].set_ylabel("1/[A]")
        axes[2].set_title("1/[A] vs Time")
        axes[2].grid(True, alpha=0.3)
        if order == 2:
            axes[2].set_facecolor("#f0fff0")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.info(f"The highlighted (green background) plot is linear for order {order}.")
        st.latex(rate_eq)
        st.caption(f"Rate constant unit: {unit}")

    with tab2:
        st.markdown("Plot ln(k) vs 1/T to determine activation energy.")
        c1, c2 = st.columns(2)
        Ea = c1.slider("Activation energy Ea (kJ/mol)", 10.0, 200.0, 80.0, 1.0)
        A_pre = c2.slider("Pre-exponential factor A (×10⁶)", 0.1, 100.0, 10.0, 0.1)

        Ea_J = Ea * 1000
        R = 8.314
        T_range = np.linspace(200, 600, 300)
        k_arr = (A_pre * 1e6) * np.exp(-Ea_J / (R * T_range))

        fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(10, 4))

        ax2a.plot(T_range, k_arr, "b-", linewidth=2)
        ax2a.set_xlabel("Temperature (K)")
        ax2a.set_ylabel("Rate constant k")
        ax2a.set_title("k vs Temperature")
        ax2a.grid(True, alpha=0.3)

        inv_T = 1.0 / T_range
        ln_k = np.log(k_arr)
        ax2b.plot(inv_T * 1000, ln_k, "r-", linewidth=2)
        ax2b.set_xlabel("1000/T (K⁻¹)")
        ax2b.set_ylabel("ln(k)")
        ax2b.set_title("Arrhenius Plot")
        ax2b.grid(True, alpha=0.3)

        # Slope annotation
        slope = -Ea_J / R
        ax2b.annotate(
            f"slope = −Ea/R = {slope:.0f} K",
            xy=(inv_T[150] * 1000, ln_k[150]),
            fontsize=9, color="red",
        )

        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

        st.latex(r"k = A \, e^{-E_a / RT} \qquad \ln k = \ln A - \frac{E_a}{R} \cdot \frac{1}{T}")

    with tab3:
        st.markdown("Half-life for different reaction orders.")
        A0_hl = st.slider("Initial conc. (mol/L)", 0.1, 5.0, 1.0, 0.1, key="hl_a0")
        k_hl = st.slider("Rate constant k", 0.01, 2.0, 0.3, 0.01, key="hl_k")

        # Half-lives
        hl_0 = A0_hl / (2 * k_hl)
        hl_1 = np.log(2) / k_hl
        hl_2 = 1 / (k_hl * A0_hl)

        c1, c2, c3 = st.columns(3)
        c1.metric("Zero order t½", f"{hl_0:.2f} s")
        c2.metric("First order t½", f"{hl_1:.2f} s")
        c3.metric("Second order t½", f"{hl_2:.2f} s")

        st.markdown(
            "| Order | Half-life formula | Depends on [A]₀? |\n"
            "|-------|------------------|-------------------|\n"
            "| 0 | t½ = [A]₀ / 2k | Yes |\n"
            "| 1 | t½ = ln2 / k | No |\n"
            "| 2 | t½ = 1 / (k[A]₀) | Yes |"
        )
