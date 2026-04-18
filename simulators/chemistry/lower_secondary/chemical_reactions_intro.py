"""
Grade 8 — Chemical Reactions Explorer
Cambridge Lower Secondary Science (Stage 9)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("🧪 Chemical Reactions Explorer")
    st.markdown("_Watch what happens when substances react and form new materials._")

    mode = st.selectbox(
        "Choose an activity",
        ["Types of Chemical Reactions", "Conservation of Mass", "Reaction Speed Factors"],
    )

    if mode == "Types of Chemical Reactions":
        st.subheader("🔄 Types of Chemical Reactions")

        rxn_type = st.radio(
            "Reaction type",
            ["Combustion", "Neutralisation", "Decomposition", "Displacement"],
            horizontal=True,
        )

        info = {
            "Combustion": {
                "eq": "Fuel + Oxygen → Carbon Dioxide + Water",
                "example": "Methane + O₂ → CO₂ + H₂O",
                "desc": "A substance burns in oxygen, releasing heat and light.",
                "sign": "Flame, heat, light produced",
                "color": "#ef4444",
            },
            "Neutralisation": {
                "eq": "Acid + Base → Salt + Water",
                "example": "HCl + NaOH → NaCl + H₂O",
                "desc": "An acid reacts with a base to form a salt and water.",
                "sign": "Temperature change, pH moves to 7",
                "color": "#8b5cf6",
            },
            "Decomposition": {
                "eq": "Compound → Element A + Element B",
                "example": "CaCO₃ → CaO + CO₂ (heated)",
                "desc": "A compound breaks down into simpler substances.",
                "sign": "Gas produced, colour change",
                "color": "#f59e0b",
            },
            "Displacement": {
                "eq": "Metal A + Salt of Metal B → Salt of Metal A + Metal B",
                "example": "Zn + CuSO₄ → ZnSO₄ + Cu",
                "desc": "A more reactive metal displaces a less reactive one from its compound.",
                "sign": "Colour change, solid forms",
                "color": "#22c55e",
            },
        }

        data = info[rxn_type]

        st.markdown(f"**General equation:** {data['eq']}")
        st.markdown(f"**Example:** {data['example']}")
        st.markdown(f"**What happens:** {data['desc']}")
        st.markdown(f"**Signs of reaction:** {data['sign']}")

        fig, ax = plt.subplots(figsize=(8, 3))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 3)
        ax.axis("off")

        ax.add_patch(plt.FancyBboxPatch((0.5, 0.8), 3, 1.4, boxstyle="round,pad=0.2",
                                        facecolor="#dbeafe", edgecolor="#2563eb", lw=2))
        ax.text(2, 1.5, "REACTANTS", ha="center", va="center", fontweight="bold", fontsize=11)

        ax.annotate("", xy=(5.2, 1.5), xytext=(4, 1.5),
                    arrowprops=dict(arrowstyle="-|>", color=data["color"], lw=3))
        ax.text(4.6, 2, rxn_type, ha="center", fontsize=9, color=data["color"], fontweight="bold")

        ax.add_patch(plt.FancyBboxPatch((5.5, 0.8), 3, 1.4, boxstyle="round,pad=0.2",
                                        facecolor="#dcfce7", edgecolor="#16a34a", lw=2))
        ax.text(7, 1.5, "PRODUCTS", ha="center", va="center", fontweight="bold", fontsize=11)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif mode == "Conservation of Mass":
        st.subheader("⚖️ Conservation of Mass")
        st.latex(r"\text{Total mass of reactants} = \text{Total mass of products}")
        st.markdown("Atoms are **never created or destroyed** during a chemical reaction.")

        st.markdown("#### Try an example")
        reaction = st.selectbox("Reaction", [
            "C + O₂ → CO₂",
            "2H₂ + O₂ → 2H₂O",
            "N₂ + 3H₂ → 2NH₃",
        ])

        mass_data = {
            "C + O₂ → CO₂": {"reactants": {"C": 12, "O₂": 32}, "products": {"CO₂": 44}},
            "2H₂ + O₂ → 2H₂O": {"reactants": {"2H₂": 4, "O₂": 32}, "products": {"2H₂O": 36}},
            "N₂ + 3H₂ → 2NH₃": {"reactants": {"N₂": 28, "3H₂": 6}, "products": {"2NH₃": 34}},
        }
        data = mass_data[reaction]

        r_total = sum(data["reactants"].values())
        p_total = sum(data["products"].values())

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Reactants
        labels_r = list(data["reactants"].keys())
        vals_r = list(data["reactants"].values())
        ax1.bar(labels_r, vals_r, color="#60a5fa", edgecolor="#1e3a5f")
        ax1.set_ylabel("Mass (g)")
        ax1.set_title(f"Reactants — Total: {r_total} g")
        ax1.grid(True, alpha=0.3, axis="y")

        # Products
        labels_p = list(data["products"].keys())
        vals_p = list(data["products"].values())
        ax2.bar(labels_p, vals_p, color="#4ade80", edgecolor="#166534")
        ax2.set_ylabel("Mass (g)")
        ax2.set_title(f"Products — Total: {p_total} g")
        ax2.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        if r_total == p_total:
            st.success(f"✅ Mass is conserved! Reactants ({r_total} g) = Products ({p_total} g)")
        else:
            st.info(f"Reactants ({r_total} g) = Products ({p_total} g) — mass is conserved!")

    elif mode == "Reaction Speed Factors":
        st.subheader("⏩ Factors Affecting Reaction Speed")
        st.markdown("Several factors can speed up or slow down a chemical reaction.")

        factor = st.radio(
            "Factor",
            ["Temperature", "Concentration", "Surface Area", "Catalyst"],
            horizontal=True,
        )

        # Simple simulation of reaction progress
        fig, ax = plt.subplots(figsize=(8, 5))
        t = np.linspace(0, 10, 200)

        if factor == "Temperature":
            low = 1 - np.exp(-0.3 * t)
            high = 1 - np.exp(-0.8 * t)
            ax.plot(t, low * 100, label="Low temperature", lw=2, color="#3b82f6")
            ax.plot(t, high * 100, label="High temperature", lw=2, color="#ef4444")
            explanation = "Higher temperature → particles move faster → more collisions → faster reaction"
        elif factor == "Concentration":
            dilute = 1 - np.exp(-0.3 * t)
            concentrated = 1 - np.exp(-0.7 * t)
            ax.plot(t, dilute * 100, label="Dilute solution", lw=2, color="#3b82f6")
            ax.plot(t, concentrated * 100, label="Concentrated solution", lw=2, color="#ef4444")
            explanation = "Higher concentration → more particles in same volume → more collisions → faster"
        elif factor == "Surface Area":
            lump = 1 - np.exp(-0.25 * t)
            powder = 1 - np.exp(-0.7 * t)
            ax.plot(t, lump * 100, label="Large lump", lw=2, color="#3b82f6")
            ax.plot(t, powder * 100, label="Fine powder", lw=2, color="#ef4444")
            explanation = "Smaller pieces → more surface exposed → more collisions → faster reaction"
        else:  # Catalyst
            without = 1 - np.exp(-0.3 * t)
            with_cat = 1 - np.exp(-0.9 * t)
            ax.plot(t, without * 100, label="Without catalyst", lw=2, color="#3b82f6")
            ax.plot(t, with_cat * 100, label="With catalyst", lw=2, color="#ef4444")
            explanation = "A catalyst lowers the activation energy → reaction happens faster without being used up"

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Reaction progress (%)")
        ax.set_title(f"Effect of {factor} on Reaction Speed")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info(f"💡 **{factor}:** {explanation}")
