"""Climate Modelling — Cross-Disciplinary Enrichment Pack."""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("🌍 Climate Modelling")

    tab1, tab2 = st.tabs(["Energy Balance Model", "Greenhouse Effect"])

    with tab1:
        st.markdown(
            "A zero-dimensional energy-balance model: the Earth receives solar "
            "radiation and emits thermal (infrared) radiation. Adjust parameters "
            "to see how equilibrium temperature changes."
        )
        c1, c2 = st.columns(2)
        S = c1.slider("Solar constant S (W/m²)", 1000.0, 1600.0, 1361.0, 1.0)
        albedo = c2.slider("Albedo α (reflectivity)", 0.0, 1.0, 0.30, 0.01)
        emissivity = st.slider("Effective emissivity ε", 0.1, 1.0, 0.612, 0.001)

        sigma = 5.670374419e-8  # Stefan-Boltzmann constant

        # Equilibrium temperature: S(1-α)/4 = εσT⁴
        T_eq = ((S * (1 - albedo)) / (4 * emissivity * sigma)) ** 0.25
        T_eq_C = T_eq - 273.15

        # Time evolution from initial temperature
        C = 4e8  # Heat capacity J/(m²·K) ~ ocean mixed layer
        T0 = 250.0  # initial temperature K
        dt = 3.154e7  # 1 year in seconds
        n_years = 200
        T_arr = np.zeros(n_years)
        T_arr[0] = T0

        for i in range(1, n_years):
            power_in = S * (1 - albedo) / 4
            power_out = emissivity * sigma * T_arr[i - 1] ** 4
            dT = (power_in - power_out) * dt / C
            T_arr[i] = T_arr[i - 1] + dT

        years = np.arange(n_years)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        ax1.plot(years, T_arr - 273.15, "b-", linewidth=2)
        ax1.axhline(T_eq_C, color="red", linestyle="--", label=f"Equilibrium {T_eq_C:.1f} °C")
        ax1.set_xlabel("Time (years)")
        ax1.set_ylabel("Temperature (°C)")
        ax1.set_title("Temperature Evolution")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Energy budget bar chart
        absorbed = S * (1 - albedo) / 4
        emitted = emissivity * sigma * T_eq**4
        ax2.bar(["Absorbed Solar", "Emitted IR"], [absorbed, emitted],
                color=["#f39c12", "#e74c3c"], alpha=0.7)
        ax2.set_ylabel("Power (W/m²)")
        ax2.set_title("Equilibrium Energy Budget")
        ax2.grid(True, alpha=0.3, axis="y")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        c1, c2, c3 = st.columns(3)
        c1.metric("Equilibrium T", f"{T_eq_C:.1f} °C")
        c2.metric("Absorbed power", f"{absorbed:.1f} W/m²")
        c3.metric("Without greenhouse", f"{((S*(1-albedo))/(4*sigma))**0.25 - 273.15:.1f} °C")

        st.latex(r"\frac{S(1-\alpha)}{4} = \varepsilon \sigma T^4")

    with tab2:
        st.markdown(
            "Model the greenhouse effect by adding atmospheric layers that "
            "absorb and re-emit infrared radiation."
        )
        n_layers = st.slider("Number of atmospheric layers", 0, 5, 1)
        S2 = 1361.0
        a2 = 0.30

        # With n absorbing layers, surface temperature:
        # T_surface = T_eff * (n+1)^(1/4)
        T_eff = ((S2 * (1 - a2)) / (4 * sigma)) ** 0.25
        T_surface = T_eff * (n_layers + 1) ** 0.25
        T_surface_C = T_surface - 273.15

        layers_range = np.arange(0, 6)
        T_surfaces = T_eff * (layers_range + 1) ** 0.25 - 273.15

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.bar(layers_range, T_surfaces, color=["#3498db" if i != n_layers else "#e74c3c"
                                                   for i in layers_range], alpha=0.8)
        ax2.set_xlabel("Number of atmospheric layers")
        ax2.set_ylabel("Surface temperature (°C)")
        ax2.set_title("Greenhouse Effect — Layer Model")
        ax2.grid(True, alpha=0.3, axis="y")
        st.pyplot(fig2)
        plt.close(fig2)

        st.metric("Surface temperature", f"{T_surface_C:.1f} °C")

        st.info(
            f"With **0 layers** (no atmosphere): {T_eff - 273.15:.1f} °C — "
            f"far below freezing!  \n"
            f"Earth's actual average is ≈ 15 °C, demonstrating the warming "
            f"effect of greenhouse gases."
        )

        st.latex(r"T_{\text{surface}} = T_{\text{eff}} \cdot (n+1)^{1/4}")
