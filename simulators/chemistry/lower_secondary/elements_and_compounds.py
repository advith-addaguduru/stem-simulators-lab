"""
Grade 7 — Elements & Compounds
Cambridge Lower Secondary Science (Stage 8)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# First 20 elements with basic data
ELEMENTS = {
    1: ("H", "Hydrogen", "Non-metal", 1.008),
    2: ("He", "Helium", "Noble gas", 4.003),
    3: ("Li", "Lithium", "Metal", 6.941),
    4: ("Be", "Beryllium", "Metal", 9.012),
    5: ("B", "Boron", "Metalloid", 10.81),
    6: ("C", "Carbon", "Non-metal", 12.01),
    7: ("N", "Nitrogen", "Non-metal", 14.01),
    8: ("O", "Oxygen", "Non-metal", 16.00),
    9: ("F", "Fluorine", "Non-metal", 19.00),
    10: ("Ne", "Neon", "Noble gas", 20.18),
    11: ("Na", "Sodium", "Metal", 22.99),
    12: ("Mg", "Magnesium", "Metal", 24.31),
    13: ("Al", "Aluminium", "Metal", 26.98),
    14: ("Si", "Silicon", "Metalloid", 28.09),
    15: ("P", "Phosphorus", "Non-metal", 30.97),
    16: ("S", "Sulfur", "Non-metal", 32.07),
    17: ("Cl", "Chlorine", "Non-metal", 35.45),
    18: ("Ar", "Argon", "Noble gas", 39.95),
    19: ("K", "Potassium", "Metal", 19.10),
    20: ("Ca", "Calcium", "Metal", 40.08),
}


def simulate():
    st.header("🔬 Elements & Compounds")
    st.markdown("_Understand atoms, elements, and how they combine into compounds._")

    mode = st.selectbox(
        "Choose an activity",
        ["Periodic Table Explorer", "Elements vs Compounds", "Word Equations"],
    )

    if mode == "Periodic Table Explorer":
        st.subheader("🧪 First 20 Elements")
        st.markdown("Click through the first 20 elements of the periodic table.")

        z = st.slider("Atomic number (Z)", 1, 20, 1)
        sym, name, category, mass = ELEMENTS[z]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Symbol", sym)
        c2.metric("Name", name)
        c3.metric("Category", category)
        c4.metric("Atomic mass", f"{mass:.3f}")

        # Mini periodic table visual
        fig, ax = plt.subplots(figsize=(10, 4))
        type_colors = {"Metal": "#60a5fa", "Non-metal": "#f87171", "Noble gas": "#a78bfa", "Metalloid": "#fbbf24"}

        for num, (s, n, cat, m) in ELEMENTS.items():
            row = 0 if num <= 2 else (1 if num <= 10 else 2)
            if num <= 2:
                col_pos = 0 if num == 1 else 7
            elif num <= 10:
                col_pos = (num - 3) % 8
            else:
                col_pos = (num - 11) % 8

            fc = type_colors.get(cat, "#d1d5db")
            ec = "#1e3a5f" if num == z else "#94a3b8"
            lw = 3 if num == z else 1
            rect = plt.Rectangle((col_pos, -row), 0.9, 0.9, facecolor=fc, edgecolor=ec, linewidth=lw)
            ax.add_patch(rect)
            ax.text(col_pos + 0.45, -row + 0.55, s, ha="center", va="center",
                    fontweight="bold" if num == z else "normal", fontsize=9)
            ax.text(col_pos + 0.45, -row + 0.2, str(num), ha="center", va="center", fontsize=6, color="#6b7280")

        ax.set_xlim(-0.2, 8.2)
        ax.set_ylim(-2.5, 1.2)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title("First 20 Elements — Mini Periodic Table")

        # Legend
        for i, (cat, col) in enumerate(type_colors.items()):
            ax.add_patch(plt.Rectangle((i * 2, -2.3), 0.3, 0.3, facecolor=col, edgecolor="#1e3a5f"))
            ax.text(i * 2 + 0.4, -2.15, cat, va="center", fontsize=7)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif mode == "Elements vs Compounds":
        st.subheader("🧩 Elements vs Compounds")

        st.markdown("""
| | Element | Compound |
|---|---|---|
| **Made of** | One type of atom | Two or more types of atoms bonded together |
| **Can be broken down?** | No (by chemical means) | Yes (by chemical reactions) |
| **Examples** | Oxygen (O₂), Iron (Fe) | Water (H₂O), Carbon dioxide (CO₂) |
| **On the periodic table?** | Yes | No |
""")

        substance = st.selectbox(
            "Explore a substance",
            ["Oxygen (O₂) — Element", "Water (H₂O) — Compound",
             "Iron (Fe) — Element", "Carbon Dioxide (CO₂) — Compound",
             "Sodium Chloride (NaCl) — Compound"],
        )

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 4)
        ax.set_aspect("equal")
        ax.axis("off")

        if "O₂" in substance:
            ax.add_patch(plt.Circle((2, 2), 0.5, color="#ef4444", alpha=0.8))
            ax.add_patch(plt.Circle((3, 2), 0.5, color="#ef4444", alpha=0.8))
            ax.text(2, 2, "O", ha="center", va="center", fontweight="bold", color="white")
            ax.text(3, 2, "O", ha="center", va="center", fontweight="bold", color="white")
            ax.set_title("Oxygen molecule (O₂) — 2 oxygen atoms bonded")
        elif "H₂O" in substance:
            ax.add_patch(plt.Circle((2, 2), 0.5, color="#ef4444", alpha=0.8))
            ax.add_patch(plt.Circle((3.2, 2.8), 0.35, color="#3b82f6", alpha=0.8))
            ax.add_patch(plt.Circle((3.2, 1.2), 0.35, color="#3b82f6", alpha=0.8))
            ax.text(2, 2, "O", ha="center", va="center", fontweight="bold", color="white")
            ax.text(3.2, 2.8, "H", ha="center", va="center", fontweight="bold", color="white")
            ax.text(3.2, 1.2, "H", ha="center", va="center", fontweight="bold", color="white")
            ax.set_title("Water molecule (H₂O) — 1 oxygen + 2 hydrogen atoms")
        elif "Fe" in substance:
            for r in range(3):
                for c_pos in range(4):
                    ax.add_patch(plt.Circle((1 + c_pos, 1 + r), 0.4, color="#94a3b8", alpha=0.8))
                    ax.text(1 + c_pos, 1 + r, "Fe", ha="center", va="center", fontsize=7, fontweight="bold")
            ax.set_title("Iron (Fe) — all atoms are the same element")
        elif "CO₂" in substance:
            ax.add_patch(plt.Circle((2.5, 2), 0.5, color="#374151", alpha=0.8))
            ax.add_patch(plt.Circle((1.3, 2), 0.45, color="#ef4444", alpha=0.8))
            ax.add_patch(plt.Circle((3.7, 2), 0.45, color="#ef4444", alpha=0.8))
            ax.text(2.5, 2, "C", ha="center", va="center", fontweight="bold", color="white")
            ax.text(1.3, 2, "O", ha="center", va="center", fontweight="bold", color="white")
            ax.text(3.7, 2, "O", ha="center", va="center", fontweight="bold", color="white")
            ax.set_title("Carbon dioxide (CO₂) — 1 carbon + 2 oxygen atoms")
        else:
            ax.add_patch(plt.Circle((2, 2), 0.5, color="#a78bfa", alpha=0.8))
            ax.add_patch(plt.Circle((3.2, 2), 0.45, color="#22c55e", alpha=0.8))
            ax.text(2, 2, "Na", ha="center", va="center", fontweight="bold", color="white")
            ax.text(3.2, 2, "Cl", ha="center", va="center", fontweight="bold", color="white")
            ax.set_title("Sodium chloride (NaCl) — 1 sodium + 1 chlorine")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif mode == "Word Equations":
        st.subheader("📝 Word Equations")
        st.markdown("A **word equation** shows the reactants and products of a chemical reaction.")

        reactions = {
            "Iron + Oxygen → Iron Oxide (rusting)": ("Iron reacts with oxygen in the air to form rust (iron oxide).", "Slow reaction, needs moisture"),
            "Magnesium + Hydrochloric Acid → Magnesium Chloride + Hydrogen": ("A metal reacts with an acid to produce a salt and hydrogen gas.", "Fizzing / bubbling observed"),
            "Calcium Carbonate + Acid → Calcium Chloride + Water + CO₂": ("Limestone reacts with acid — this is how caves form!", "Effervescence (bubbles)"),
            "Methane + Oxygen → Carbon Dioxide + Water": ("Burning natural gas — the main reaction in a gas stove.", "Exothermic — gives off heat and light"),
        }

        selected_rxn = st.selectbox("Choose a reaction", list(reactions.keys()))
        explanation, observation = reactions[selected_rxn]

        st.markdown(f"### {selected_rxn}")
        st.markdown(f"**Explanation:** {explanation}")
        st.markdown(f"**What you'd observe:** {observation}")

        parts = selected_rxn.split("→")
        reactants = [r.strip() for r in parts[0].split("+")]
        products_raw = parts[1].split("(")[0] if "(" in parts[1] else parts[1]
        products = [p.strip() for p in products_raw.split("+")]

        fig, ax = plt.subplots(figsize=(10, 3))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 3)
        ax.axis("off")

        # Reactants
        for i, r in enumerate(reactants):
            x = 1 + i * 1.8
            ax.add_patch(plt.FancyBboxPatch((x - 0.7, 1), 1.4, 1, boxstyle="round,pad=0.1",
                                            facecolor="#dbeafe", edgecolor="#2563eb", linewidth=2))
            ax.text(x, 1.5, r, ha="center", va="center", fontsize=8, fontweight="bold")

        # Arrow
        ax.annotate("", xy=(5.5, 1.5), xytext=(4.5, 1.5),
                    arrowprops=dict(arrowstyle="-|>", color="#374151", lw=2))

        # Products
        for i, p in enumerate(products):
            x = 6.5 + i * 1.8
            ax.add_patch(plt.FancyBboxPatch((x - 0.7, 1), 1.4, 1, boxstyle="round,pad=0.1",
                                            facecolor="#dcfce7", edgecolor="#16a34a", linewidth=2))
            ax.text(x, 1.5, p, ha="center", va="center", fontsize=8, fontweight="bold")

        ax.set_title("Reaction Diagram", fontsize=12)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info("💡 **Key rule:** Atoms are never created or destroyed — they just rearrange!")
