"""Cambridge A-Level Chemistry: Organic Chemistry"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulators.utils import nice_axes


def simulate():
    st.subheader("Organic Chemistry")
    st.markdown("_Explore homologous series, functional groups, and reaction pathways._")

    mode = st.radio(
        "Choose a topic",
        ["Homologous Series", "Functional Groups & Isomers", "Reaction Pathways"],
        horizontal=True,
    )

    if mode == "Homologous Series":
        _homologous_series()
    elif mode == "Functional Groups & Isomers":
        _functional_groups()
    else:
        _reaction_pathways()


# -- data --

ALKANES = [
    ("Methane", "CH₄", 1, -161.5, -182.5),
    ("Ethane", "C₂H₆", 2, -88.6, -182.8),
    ("Propane", "C₃H₈", 3, -42.1, -187.7),
    ("Butane", "C₄H₁₀", 4, -0.5, -138.3),
    ("Pentane", "C₅H₁₂", 5, 36.1, -129.7),
    ("Hexane", "C₆H₁₄", 6, 68.7, -95.3),
    ("Heptane", "C₇H₁₆", 7, 98.4, -90.6),
    ("Octane", "C₈H₁₈", 8, 125.7, -56.8),
]

ALCOHOLS = [
    ("Methanol", "CH₃OH", 1, 64.7, -97.6),
    ("Ethanol", "C₂H₅OH", 2, 78.4, -114.1),
    ("Propan-1-ol", "C₃H₇OH", 3, 97.2, -126.2),
    ("Butan-1-ol", "C₄H₉OH", 4, 117.7, -89.5),
    ("Pentan-1-ol", "C₅H₁₁OH", 5, 138.0, -78.2),
]


def _homologous_series():
    st.markdown("### Homologous Series — Trends in Boiling Point")
    st.latex(r"C_nH_{2n+2} \text{ (alkanes)} \qquad C_nH_{2n+1}OH \text{ (alcohols)}")

    series = st.selectbox("Select series", ["Alkanes", "Alcohols"])
    data = ALKANES if series == "Alkanes" else ALCOHOLS

    names = [d[0] for d in data]
    carbons = [d[2] for d in data]
    bps = [d[3] for d in data]
    mps = [d[4] for d in data]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.plot(carbons, bps, "o-", linewidth=2, color="#ef4444",
             markersize=8, label="Boiling point")
    ax1.plot(carbons, mps, "s--", linewidth=2, color="#3b82f6",
             markersize=8, label="Melting point")
    for i, name in enumerate(names):
        ax1.annotate(name, (carbons[i], bps[i]), textcoords="offset points",
                     xytext=(5, 5), fontsize=8)
    nice_axes(ax1, "Number of carbons", "Temperature (°C)",
              f"{series}: BP & MP trends")
    ax1.legend()

    # Mr trend
    if series == "Alkanes":
        mrs = [12 * n + 2 * n + 2 for n in carbons]
    else:
        mrs = [12 * n + 2 * n + 2 + 16 for n in carbons]

    ax2.bar(names, mrs, color="#22c55e", edgecolor="#333")
    ax2.set_ylabel("Relative molecular mass (Mr)")
    ax2.set_title("Molecular Mass")
    ax2.grid(True, alpha=0.3, axis="y")
    plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.info(
        "💡 **Trend:** As chain length increases, London dispersion forces increase, "
        "so more energy is needed to overcome intermolecular forces → higher boiling points."
    )


def _functional_groups():
    st.markdown("### Functional Groups & Structural Isomers")

    groups = {
        "Alkane (C–C, C–H)": {"formula": "CₙH₂ₙ₊₂", "example": "Butane C₄H₁₀",
                               "isomers_4c": 2},
        "Alkene (C=C)": {"formula": "CₙH₂ₙ", "example": "But-1-ene C₄H₈",
                         "isomers_4c": 3},
        "Alcohol (–OH)": {"formula": "CₙH₂ₙ₊₁OH", "example": "Butan-1-ol C₄H₉OH",
                          "isomers_4c": 4},
        "Carboxylic acid (–COOH)": {"formula": "CₙH₂ₙ₊₁COOH",
                                     "example": "Propanoic acid C₂H₅COOH",
                                     "isomers_4c": 1},
        "Halogenoalkane (C–X)": {"formula": "CₙH₂ₙ₊₁X",
                                 "example": "1-chlorobutane C₄H₉Cl",
                                 "isomers_4c": 4},
    }

    selected = st.selectbox("Functional group", list(groups.keys()))
    info = groups[selected]

    c1, c2, c3 = st.columns(3)
    c1.metric("General formula", info["formula"])
    c2.metric("Example", info["example"])
    c3.metric("Structural isomers (4 C)", str(info["isomers_4c"]))

    # Isomer count growth
    carbon_range = list(range(1, 11))
    approx_isomers = {
        "Alkane (C–C, C–H)": [1, 1, 1, 2, 3, 5, 9, 18, 35, 75],
        "Alkene (C=C)": [0, 1, 1, 3, 5, 13, 27, 66, 153, 377],
        "Alcohol (–OH)": [1, 1, 2, 4, 8, 17, 39, 89, 211, 507],
        "Carboxylic acid (–COOH)": [1, 1, 1, 1, 2, 4, 8, 17, 39, 89],
        "Halogenoalkane (C–X)": [1, 1, 2, 4, 8, 17, 39, 89, 211, 507],
    }

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(carbon_range, approx_isomers[selected], color="#8b5cf6", edgecolor="#333")
    ax.set_xlabel("Number of carbons")
    ax.set_ylabel("Number of structural isomers")
    ax.set_title(f"Isomer Count Growth — {selected}")
    ax.set_xticks(carbon_range)
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.info("💡 The number of structural isomers grows exponentially with chain length!")


def _reaction_pathways():
    st.markdown("### Reaction Pathway Map")
    st.markdown(
        "Follow the pathways between functional groups. "
        "Select a starting material and target to see the route."
    )

    pathways = {
        ("Alkane", "Halogenoalkane"): "Free-radical substitution (UV light + halogen)",
        ("Alkene", "Alkane"): "Hydrogenation (H₂ / Ni catalyst, 150°C)",
        ("Alkene", "Alcohol"): "Hydration (steam / H₃PO₄ catalyst, 300°C)",
        ("Alkene", "Halogenoalkane"): "Electrophilic addition (HX or X₂)",
        ("Alkene", "Polymer"): "Addition polymerisation (high pressure, catalyst)",
        ("Alcohol", "Alkene"): "Dehydration (conc. H₂SO₄ or Al₂O₃, heat)",
        ("Alcohol", "Aldehyde"): "Oxidation (acidified K₂Cr₂O₇, distil)",
        ("Alcohol", "Carboxylic acid"): "Oxidation (acidified K₂Cr₂O₇, reflux)",
        ("Alcohol", "Ester"): "Esterification (carboxylic acid + conc. H₂SO₄)",
        ("Aldehyde", "Carboxylic acid"): "Further oxidation (acidified K₂Cr₂O₇)",
        ("Halogenoalkane", "Alcohol"): "Nucleophilic substitution (aq. NaOH, reflux)",
        ("Halogenoalkane", "Alkene"): "Elimination (ethanolic NaOH, reflux)",
    }

    compounds = sorted({c for pair in pathways for c in pair})

    col1, col2 = st.columns(2)
    with col1:
        start = st.selectbox("Starting material", compounds, index=0)
    with col2:
        end = st.selectbox("Target product", compounds, index=1)

    if start == end:
        st.warning("Select different starting material and target.")
        return

    direct = pathways.get((start, end))
    if direct:
        st.success(f"**Direct route:** {start} → {end}")
        st.markdown(f"**Conditions:** {direct}")
    else:
        # Try 2-step route
        found = False
        for (a, b), cond1 in pathways.items():
            if a == start:
                cond2 = pathways.get((b, end))
                if cond2:
                    st.success(f"**2-step route:** {start} → {b} → {end}")
                    st.markdown(f"1. {start} → {b}: {cond1}")
                    st.markdown(f"2. {b} → {end}: {cond2}")
                    found = True
                    break
        if not found:
            st.error(f"No direct or 2-step route found from {start} to {end}.")

    # Pathway network visualisation
    fig, ax = plt.subplots(figsize=(8, 8))
    n = len(compounds)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    positions = {c: (2 * np.cos(a), 2 * np.sin(a)) for c, a in zip(compounds, angles)}

    for (a, b) in pathways:
        xa, ya = positions[a]
        xb, yb = positions[b]
        colour = "#ef4444" if a == start or b == end else "#cbd5e1"
        lw = 2 if a == start or b == end else 0.5
        ax.annotate("", xy=(xb, yb), xytext=(xa, ya),
                    arrowprops=dict(arrowstyle="->", color=colour, lw=lw))

    for c, (x, y) in positions.items():
        face = "#3b82f6" if c == start else "#22c55e" if c == end else "#f1f5f9"
        ax.plot(x, y, "o", markersize=25, color=face, markeredgecolor="#333")
        ax.text(x, y - 0.35, c, ha="center", fontsize=8, fontweight="bold")

    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect("equal")
    ax.set_title("Reaction Pathway Network")
    ax.axis("off")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
