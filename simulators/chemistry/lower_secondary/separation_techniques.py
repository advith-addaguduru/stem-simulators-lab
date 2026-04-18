"""
Grade 7 — Separation Techniques
Cambridge Lower Secondary Science (Stage 8)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("🧫 Separation Techniques")
    st.markdown("_Learn how to separate mixtures using different physical methods._")

    mode = st.selectbox(
        "Choose a technique",
        ["Filtration", "Evaporation & Distillation", "Chromatography"],
    )

    if mode == "Filtration":
        st.subheader("🔬 Filtration")
        st.markdown(
            "Filtration separates an **insoluble solid** from a liquid. "
            "The solid stays in the filter paper (residue) and the liquid passes through (filtrate)."
        )

        col1, col2 = st.columns(2)
        with col1:
            total_mass = st.slider("Total mixture mass (g)", 10, 200, 100, step=10)
        with col2:
            solid_pct = st.slider("Solid content (%)", 1, 80, 20, step=1)

        solid_mass = total_mass * solid_pct / 100
        liquid_mass = total_mass - solid_mass

        c1, c2, c3 = st.columns(3)
        c1.metric("Total mixture", f"{total_mass} g")
        c2.metric("Residue (solid)", f"{solid_mass:.1f} g")
        c3.metric("Filtrate (liquid)", f"{liquid_mass:.1f} g")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        ax1.pie(
            [solid_mass, liquid_mass],
            labels=["Solid (residue)", "Liquid (filtrate)"],
            colors=["#a78bfa", "#60a5fa"],
            autopct="%1.1f%%",
            startangle=90,
        )
        ax1.set_title("Mixture Composition")

        pct_range = np.arange(5, 85, 5)
        ax2.plot(pct_range, total_mass * pct_range / 100, "o-",
                 color="#a78bfa", label="Solid")
        ax2.plot(pct_range, total_mass * (100 - pct_range) / 100, "s-",
                 color="#60a5fa", label="Liquid")
        ax2.axvline(solid_pct, color="red", linestyle="--", alpha=0.6)
        ax2.set_xlabel("Solid content (%)")
        ax2.set_ylabel("Mass (g)")
        ax2.set_title(f"Separation results for {total_mass} g mixture")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info("💡 **Examples:** Sand from salty water, chalk from water, tea leaves from tea.")

    elif mode == "Evaporation & Distillation":
        st.subheader("🌡️ Evaporation & Distillation")
        st.markdown(
            "**Evaporation** — heat a solution to drive off the solvent, leaving the solid behind.\n\n"
            "**Distillation** — heat a mixture and collect the vapour by cooling, separating liquids by boiling point."
        )

        substances = {
            "Water": 100.0,
            "Ethanol": 78.4,
            "Acetone": 56.1,
            "Salt water": 101.5,
            "Methanol": 64.7,
        }

        selected = st.multiselect(
            "Choose substances for the mixture",
            list(substances.keys()),
            default=["Water", "Ethanol"],
        )

        if len(selected) >= 2:
            bps = sorted([(s, substances[s]) for s in selected], key=lambda x: x[1])

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

            names = [b[0] for b in bps]
            temps = [b[1] for b in bps]
            colours = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(bps)))
            ax1.barh(names, temps, color=colours, edgecolor="#333")
            ax1.set_xlabel("Boiling point (°C)")
            ax1.set_title("Boiling Points (collection order →)")
            ax1.grid(True, alpha=0.3, axis="x")

            temp = np.linspace(20, max(temps) + 20, 300)
            ax2.set_xlabel("Temperature (°C)")
            ax2.set_ylabel("Collection")
            ax2.set_title("Distillation Heating Curve")
            collected = np.zeros_like(temp)
            for i, (name, bp) in enumerate(bps):
                ax2.axvline(bp, color=colours[i], linestyle="--",
                            alpha=0.7, label=f"{name} ({bp}°C)")
                collected += np.where(temp >= bp, 1.0 / len(bps), 0)
            ax2.plot(temp, collected * 100, color="#2563eb", linewidth=2)
            ax2.set_ylabel("Fraction collected (%)")
            ax2.legend(fontsize=8)
            ax2.grid(True, alpha=0.3)

            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            st.markdown("**Collection order:** " +
                        " → ".join([f"**{n}** ({t}°C)" for n, t in bps]))
        else:
            st.warning("Select at least 2 substances to compare.")

    else:  # Chromatography
        st.subheader("🎨 Chromatography")
        st.markdown(
            "Chromatography separates the **coloured components** of a mixture. "
            "Each component travels a different distance up the paper."
        )
        st.latex(r"R_f = \frac{\text{Distance moved by substance}}{\text{Distance moved by solvent}}")

        col1, col2 = st.columns(2)
        with col1:
            solvent_dist = st.slider("Solvent front distance (cm)", 5.0, 15.0, 10.0, step=0.5)
        with col2:
            n_spots = st.slider("Number of ink components", 2, 6, 4)

        np.random.seed(42)
        spot_dists = sorted(np.random.uniform(1.0, solvent_dist * 0.95, n_spots))
        rf_values = [d / solvent_dist for d in spot_dists]

        colours_list = ["#ef4444", "#f59e0b", "#22c55e", "#3b82f6", "#8b5cf6", "#ec4899"]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        ax1.axhline(solvent_dist, color="grey", linestyle="--", linewidth=1,
                     label="Solvent front")
        ax1.axhline(0, color="grey", linewidth=2)
        for i, (d, c) in enumerate(zip(spot_dists, colours_list[:n_spots])):
            ax1.plot(0.5, d, "o", markersize=20, color=c, alpha=0.7)
            ax1.annotate(f"  Component {i + 1}: {d:.1f} cm",
                         (0.5, d), fontsize=9, va="center")
        ax1.set_xlim(0, 1)
        ax1.set_ylim(-0.5, solvent_dist + 1)
        ax1.set_ylabel("Distance (cm)")
        ax1.set_title("Chromatogram")
        ax1.set_xticks([])
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis="y")

        ax2.bar([f"C{i + 1}" for i in range(n_spots)], rf_values,
                color=colours_list[:n_spots], edgecolor="#333")
        ax2.set_ylabel("Rf value")
        ax2.set_title("Rf Values")
        ax2.set_ylim(0, 1.05)
        ax2.axhline(1.0, color="grey", linestyle=":", alpha=0.5)
        ax2.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        for i, (d, rf) in enumerate(zip(spot_dists, rf_values)):
            st.markdown(f"- **Component {i + 1}:** distance = {d:.1f} cm → Rf = {rf:.3f}")

        st.info("💡 **Tip:** Substances with the same Rf value in the same solvent are likely the same chemical.")
