"""IGCSE Grades 9-10 Chemistry: Reaction Types Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Reaction Types & Equations")
    st.latex(r"\text{Reactants} \rightarrow \text{Products}")

    mode = st.radio(
        "Select topic",
        ["Reaction Types", "Balancing Equations", "Rates of Reaction"],
        horizontal=True,
    )

    if mode == "Reaction Types":
        _reaction_types()
    elif mode == "Balancing Equations":
        _balancing()
    else:
        _rates()


def _reaction_types():
    with st.sidebar.expander("Reaction Type Controls", expanded=True):
        rxn = st.selectbox("Reaction", [
            "Combustion: CH₄ + 2O₂ → CO₂ + 2H₂O",
            "Neutralisation: HCl + NaOH → NaCl + H₂O",
            "Decomposition: CaCO₃ → CaO + CO₂",
            "Displacement: Zn + CuSO₄ → ZnSO₄ + Cu",
            "Redox: 2Mg + O₂ → 2MgO",
        ])

    rxn_info = {
        "Combustion: CH₄ + 2O₂ → CO₂ + 2H₂O": {
            "type": "Combustion", "energy": "Exothermic",
            "delta_h": -890, "desc": "Fuel reacts with oxygen, releasing heat and light.",
        },
        "Neutralisation: HCl + NaOH → NaCl + H₂O": {
            "type": "Neutralisation", "energy": "Exothermic",
            "delta_h": -57, "desc": "Acid + Base → Salt + Water. pH moves towards 7.",
        },
        "Decomposition: CaCO₃ → CaO + CO₂": {
            "type": "Thermal Decomposition", "energy": "Endothermic",
            "delta_h": 178, "desc": "One compound breaks down into simpler substances on heating.",
        },
        "Displacement: Zn + CuSO₄ → ZnSO₄ + Cu": {
            "type": "Displacement", "energy": "Exothermic",
            "delta_h": -219, "desc": "More reactive metal displaces less reactive metal from solution.",
        },
        "Redox: 2Mg + O₂ → 2MgO": {
            "type": "Redox (Oxidation)", "energy": "Exothermic",
            "delta_h": -1204, "desc": "Mg is oxidised (loses electrons), O is reduced (gains electrons).",
        },
    }
    info = rxn_info[rxn]

    col1, col2, col3 = st.columns(3)
    col1.metric("Type", info["type"])
    col2.metric("Energy Change", info["energy"])
    col3.metric("ΔH", f"{info['delta_h']} kJ/mol")

    # Energy diagram
    fig, ax = plt.subplots(figsize=(8, 5))
    dh = info["delta_h"]
    reactant_e = 100
    product_e = reactant_e + dh / 10  # scaled

    ax.plot([0, 1], [reactant_e, reactant_e], "b-", lw=3, label="Reactants")
    ax.plot([2, 3], [product_e, product_e], "r-", lw=3, label="Products")

    peak = max(reactant_e, product_e) + 20
    xs = np.linspace(0.5, 2.5, 100)
    ys = reactant_e + (peak - reactant_e) * np.sin(np.pi * (xs - 0.5) / 2) ** 2
    # Adjust right side to land on product_e
    mid = len(xs) // 2
    ys[mid:] = peak - (peak - product_e) * np.sin(np.pi * (xs[mid:] - xs[mid]) / (xs[-1] - xs[mid])) ** 2

    ax.plot(xs, ys, "k--", alpha=0.6)
    ax.annotate("", xy=(3.2, product_e), xytext=(3.2, reactant_e),
                arrowprops=dict(arrowstyle="<->", color="green", lw=2))
    ax.text(3.4, (reactant_e + product_e) / 2, f"ΔH={dh}\nkJ/mol", fontsize=10, color="green")

    ax.set_ylabel("Energy")
    ax.set_xticks([0.5, 2.5])
    ax.set_xticklabels(["Reactants", "Products"])
    ax.set_title(f"Energy Profile: {info['type']} Reaction")
    ax.legend()
    ax.grid(True, alpha=0.25, axis="y")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"**{info['desc']}**")


def _balancing():
    st.markdown("Explore how atoms are conserved in balanced equations.")

    with st.sidebar.expander("Balancing Controls", expanded=True):
        equation = st.selectbox("Equation to balance", [
            "H₂ + O₂ → H₂O",
            "Fe + O₂ → Fe₂O₃",
            "N₂ + H₂ → NH₃",
        ])

    balanced = {
        "H₂ + O₂ → H₂O": {
            "balanced": "2H₂ + O₂ → 2H₂O",
            "reactant_atoms": {"H": 4, "O": 2},
            "product_atoms": {"H": 4, "O": 2},
            "coefficients": [2, 1, 2],
        },
        "Fe + O₂ → Fe₂O₃": {
            "balanced": "4Fe + 3O₂ → 2Fe₂O₃",
            "reactant_atoms": {"Fe": 4, "O": 6},
            "product_atoms": {"Fe": 4, "O": 6},
            "coefficients": [4, 3, 2],
        },
        "N₂ + H₂ → NH₃": {
            "balanced": "N₂ + 3H₂ → 2NH₃",
            "reactant_atoms": {"N": 2, "H": 6},
            "product_atoms": {"N": 2, "H": 6},
            "coefficients": [1, 3, 2],
        },
    }
    data = balanced[equation]

    st.success(f"**Balanced:** {data['balanced']}")

    fig, ax = plt.subplots(figsize=(8, 5))
    elements = list(data["reactant_atoms"].keys())
    x = np.arange(len(elements))
    width = 0.35
    ax.bar(x - width / 2, [data["reactant_atoms"][e] for e in elements], width,
           label="Reactants", color="#3498db", alpha=0.8)
    ax.bar(x + width / 2, [data["product_atoms"][e] for e in elements], width,
           label="Products", color="#e74c3c", alpha=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(elements)
    ax.set_ylabel("Number of Atoms")
    ax.set_title("Atom Conservation (Balanced)")
    ax.legend()
    ax.grid(True, alpha=0.25, axis="y")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("**Law of Conservation of Mass:** atoms are neither created nor destroyed in a chemical reaction.")


def _rates():
    st.latex(r"\text{Rate} = \frac{\text{Change in amount}}{\text{Time taken}}")

    with st.sidebar.expander("Rate Controls", expanded=True):
        temp = st.slider("Temperature (°C)", 20, 80, 25, step=5)
        concentration = st.slider("Concentration (mol/dm³)", 0.1, 2.0, 1.0, step=0.1)
        surface_area = st.selectbox("Surface area", ["Powder (large)", "Lumps (small)"])
        catalyst = st.checkbox("Catalyst present", value=False)

    # Simple rate model
    base_rate = 0.5
    rate = base_rate * concentration
    rate *= 2 ** ((temp - 25) / 10)  # doubles every 10°C
    if surface_area == "Powder (large)":
        rate *= 2.0
    if catalyst:
        rate *= 3.0

    t = np.linspace(0, 20, 200)
    product = 100 * (1 - np.exp(-rate * t / 20))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t, product, "b-", lw=2, label=f"Rate factor: {rate:.2f}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Product formed (%)")
    ax.set_title("Effect of Conditions on Rate")
    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**Factors affecting rate:**
- Temperature: **{temp}°C** — higher T → faster particles → more collisions
- Concentration: **{concentration} mol/dm³** — more particles → more collisions
- Surface area: **{surface_area}** — more exposed surface → more collisions
- Catalyst: **{'Yes' if catalyst else 'No'}** — lowers activation energy

**Relative rate: {rate:.2f}×** compared to baseline
""")
