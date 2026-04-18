"""IGCSE Grades 9-10 Chemistry: Bonding & Properties Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Bonding & Properties of Matter")
    st.latex(r"\text{Ionic: } M \rightarrow M^+ + e^- \quad;\quad \text{Covalent: shared pairs}")

    mode = st.radio(
        "Select topic",
        ["Ionic vs Covalent", "Metallic Bonding", "Properties Comparison"],
        horizontal=True,
    )

    if mode == "Ionic vs Covalent":
        _ionic_covalent()
    elif mode == "Metallic Bonding":
        _metallic()
    else:
        _properties_comparison()


def _ionic_covalent():
    with st.sidebar.expander("Bonding Controls", expanded=True):
        bond_type = st.selectbox("Bond type", ["Ionic (NaCl)", "Covalent (H₂O)", "Covalent (CO₂)", "Covalent (CH₄)"])
        show_electrons = st.checkbox("Show electron transfer / sharing", value=True)

    bond_data = {
        "Ionic (NaCl)": {
            "desc": "Na transfers 1 electron to Cl → Na⁺ Cl⁻",
            "electronegativity_diff": 2.23,
            "melting_point": 801,
            "conducts": "When molten or dissolved",
        },
        "Covalent (H₂O)": {
            "desc": "O shares 2 pairs of electrons with 2 H atoms",
            "electronegativity_diff": 1.24,
            "melting_point": 0,
            "conducts": "No (pure water)",
        },
        "Covalent (CO₂)": {
            "desc": "C shares 2 double bonds with 2 O atoms",
            "electronegativity_diff": 0.89,
            "melting_point": -78,
            "conducts": "No",
        },
        "Covalent (CH₄)": {
            "desc": "C shares 4 single bonds with 4 H atoms",
            "electronegativity_diff": 0.35,
            "melting_point": -182,
            "conducts": "No",
        },
    }
    data = bond_data[bond_type]

    col1, col2, col3 = st.columns(3)
    col1.metric("ΔEN", f"{data['electronegativity_diff']:.2f}")
    col2.metric("Melting Point", f"{data['melting_point']} °C")
    col3.metric("Conductivity", data["conducts"])

    fig, ax = plt.subplots(figsize=(8, 5))
    names = list(bond_data.keys())
    en_diffs = [bond_data[n]["electronegativity_diff"] for n in names]
    colors = ["#e74c3c" if d > 1.7 else "#3498db" for d in en_diffs]
    bars = ax.bar(names, en_diffs, color=colors, alpha=0.8)
    ax.axhline(1.7, color="gray", linestyle="--", alpha=0.6, label="Ionic/Covalent boundary ≈ 1.7")
    ax.set_ylabel("Electronegativity Difference")
    ax.set_title("Electronegativity Difference & Bond Type")
    ax.legend()
    ax.grid(True, alpha=0.25, axis="y")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"**{bond_type}:** {data['desc']}")


def _metallic():
    st.markdown("""
    **Metallic bonding** involves a lattice of positive metal ions surrounded by a
    'sea' of delocalised electrons.
    """)

    with st.sidebar.expander("Metallic Bonding Controls", expanded=True):
        metal = st.selectbox("Metal", ["Sodium (Na)", "Iron (Fe)", "Copper (Cu)", "Aluminium (Al)"])

    metal_data = {
        "Sodium (Na)":     {"mp": 98,   "bp": 883,  "density": 0.97, "valence": 1},
        "Iron (Fe)":       {"mp": 1538, "bp": 2862, "density": 7.87, "valence": 2},
        "Copper (Cu)":     {"mp": 1085, "bp": 2562, "density": 8.96, "valence": 2},
        "Aluminium (Al)":  {"mp": 660,  "bp": 2519, "density": 2.70, "valence": 3},
    }
    d = metal_data[metal]

    col1, col2, col3 = st.columns(3)
    col1.metric("Melting Point", f"{d['mp']} °C")
    col2.metric("Boiling Point", f"{d['bp']} °C")
    col3.metric("Density", f"{d['density']} g/cm³")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    metals = list(metal_data.keys())
    mps = [metal_data[m]["mp"] for m in metals]
    densities = [metal_data[m]["density"] for m in metals]

    axes[0].bar(metals, mps, color=["#e74c3c", "#3498db", "#f39c12", "#2ecc71"], alpha=0.8)
    axes[0].set_ylabel("Melting Point (°C)")
    axes[0].set_title("Melting Points")
    axes[0].grid(True, alpha=0.25, axis="y")

    axes[1].bar(metals, densities, color=["#e74c3c", "#3498db", "#f39c12", "#2ecc71"], alpha=0.8)
    axes[1].set_ylabel("Density (g/cm³)")
    axes[1].set_title("Densities")
    axes[1].grid(True, alpha=0.25, axis="y")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**{metal}:**  
- Valence electrons per atom: **{d['valence']}**  
- More delocalised electrons → stronger metallic bond → higher melting point
""")


def _properties_comparison():
    st.markdown("Compare physical properties of ionic, simple covalent, and giant covalent substances.")

    substances = {
        "NaCl (Ionic)":         {"mp": 801,  "bp": 1413, "hardness": 5, "conducts_solid": False, "conducts_liquid": True},
        "H₂O (Simple Cov.)":   {"mp": 0,    "bp": 100,  "hardness": 1, "conducts_solid": False, "conducts_liquid": False},
        "SiO₂ (Giant Cov.)":   {"mp": 1710, "bp": 2230, "hardness": 9, "conducts_solid": False, "conducts_liquid": False},
        "Cu (Metallic)":       {"mp": 1085, "bp": 2562, "hardness": 3, "conducts_solid": True,  "conducts_liquid": True},
    }

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    names = list(substances.keys())
    colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12"]

    axes[0].bar(names, [substances[n]["mp"] for n in names], color=colors, alpha=0.8)
    axes[0].set_ylabel("Temperature (°C)")
    axes[0].set_title("Melting Points")
    axes[0].tick_params(axis="x", rotation=20)
    axes[0].grid(True, alpha=0.25, axis="y")

    axes[1].bar(names, [substances[n]["bp"] for n in names], color=colors, alpha=0.8)
    axes[1].set_ylabel("Temperature (°C)")
    axes[1].set_title("Boiling Points")
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].grid(True, alpha=0.25, axis="y")

    axes[2].bar(names, [substances[n]["hardness"] for n in names], color=colors, alpha=0.8)
    axes[2].set_ylabel("Hardness (Mohs scale)")
    axes[2].set_title("Relative Hardness")
    axes[2].tick_params(axis="x", rotation=20)
    axes[2].grid(True, alpha=0.25, axis="y")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("""
| Property | Ionic | Simple Covalent | Giant Covalent | Metallic |
|----------|-------|-----------------|----------------|----------|
| Melting point | High | Low | Very high | Variable |
| Conductivity (solid) | No | No | No (usually) | Yes |
| Conductivity (liquid/aq) | Yes | No | No | Yes |
| Hardness | Hard but brittle | Soft | Very hard | Malleable |
""")
