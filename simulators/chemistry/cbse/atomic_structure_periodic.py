"""CBSE Class 11 Chemistry: Atomic Structure & Periodic Table"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulators.utils import nice_axes


def simulate():
    st.subheader("Atomic Structure & Periodic Table")
    st.latex(
        r"n, \ell, m_\ell, m_s \qquad "
        r"\text{Aufbau: } 1s\,2s\,2p\,3s\,3p\,4s\,3d\dots"
    )

    mode = st.radio(
        "Choose a topic",
        ["Quantum Numbers & Orbitals", "Electron Configuration", "Periodic Trends"],
        horizontal=True,
    )

    if mode == "Quantum Numbers & Orbitals":
        _quantum_numbers()
    elif mode == "Electron Configuration":
        _electron_config()
    else:
        _periodic_trends()


SUBSHELL_NAMES = {0: "s", 1: "p", 2: "d", 3: "f"}

AUFBAU_ORDER = [
    (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (3, 2),
    (4, 1), (5, 0), (4, 2), (5, 1), (6, 0), (4, 3), (5, 2),
    (6, 1), (7, 0), (5, 3), (6, 2),
]


def _quantum_numbers():
    st.markdown("### Quantum Numbers")
    st.markdown(
        "- **n** (principal): shell number (1, 2, 3, ...)\n"
        "- **ℓ** (angular momentum): subshell (0=s, 1=p, 2=d, 3=f)\n"
        "- **mₗ** (magnetic): orbital orientation (−ℓ to +ℓ)\n"
        "- **mₛ** (spin): +½ or −½"
    )

    col1, col2 = st.columns(2)
    with col1:
        n = st.slider("Principal quantum number n", 1, 7, 3)
    with col2:
        l_max = min(n - 1, 3)
        l_val = st.slider("Angular momentum ℓ", 0, l_max, min(1, l_max))

    ml_range = list(range(-l_val, l_val + 1))
    max_electrons = 2 * (2 * l_val + 1)

    c1, c2, c3 = st.columns(3)
    c1.metric("Subshell", f"{n}{SUBSHELL_NAMES[l_val]}")
    c2.metric("mₗ values", f"{ml_range}")
    c3.metric("Max electrons", f"{max_electrons}")

    # Orbital shape visualisation (radial probability)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    r = np.linspace(0, 30, 500)
    a0 = 1  # Bohr radius units

    # Simplified radial distribution for s orbitals
    if l_val == 0:
        if n == 1:
            psi_r = 2 * np.exp(-r / a0)
        elif n == 2:
            psi_r = (1 / (2 * np.sqrt(2))) * (2 - r / a0) * np.exp(-r / (2 * a0))
        elif n == 3:
            psi_r = (2 / (81 * np.sqrt(3))) * (27 - 18 * r / a0 + 2 * (r / a0)**2) * np.exp(-r / (3 * a0))
        else:
            psi_r = (r / a0)**(n - 1) * np.exp(-r / (n * a0))
            psi_r /= np.max(np.abs(psi_r)) + 1e-30
    else:
        psi_r = (r / a0)**l_val * np.exp(-r / (n * a0))
        psi_r /= np.max(np.abs(psi_r)) + 1e-30

    P_r = 4 * np.pi * r**2 * psi_r**2
    P_r /= np.max(P_r) + 1e-30

    ax1.plot(r, P_r, linewidth=2, color="#8b5cf6")
    ax1.fill_between(r, P_r, alpha=0.2, color="#8b5cf6")
    nice_axes(ax1, "r / a₀", "Radial probability",
              f"Radial Distribution: {n}{SUBSHELL_NAMES[l_val]}")

    # Orbital box diagram
    ml_labels = [str(m) for m in ml_range]
    ax2.set_xlim(-0.5, len(ml_range) - 0.5)
    ax2.set_ylim(-0.5, 1.5)
    for i, ml in enumerate(ml_range):
        ax2.add_patch(plt.Rectangle((i - 0.4, 0), 0.8, 0.8,
                                     fill=False, edgecolor="#333", linewidth=2))
        ax2.text(i, -0.3, f"mₗ={ml}", ha="center", fontsize=9)
        ax2.annotate("↑", (i - 0.1, 0.2), fontsize=14, ha="center", color="#ef4444")
        ax2.annotate("↓", (i + 0.1, 0.2), fontsize=14, ha="center", color="#3b82f6")
    ax2.set_title(f"{n}{SUBSHELL_NAMES[l_val]} Orbital Boxes (filled)")
    ax2.axis("off")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _electron_config():
    st.markdown("### Electron Configuration (Aufbau Principle)")

    z = st.slider("Atomic number Z", 1, 36, 11)

    elements = {
        1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O",
        9: "F", 10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",
        16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca", 21: "Sc", 22: "Ti",
        23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu",
        30: "Zn", 31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br", 36: "Kr",
    }

    st.metric("Element", f"{elements.get(z, '?')} (Z = {z})")

    # Build configuration
    config = []
    remaining = z
    for n, l in AUFBAU_ORDER:
        if remaining <= 0:
            break
        max_e = 2 * (2 * l + 1)
        e = min(remaining, max_e)
        config.append((n, l, e))
        remaining -= e

    config_str = " ".join(f"{n}{SUBSHELL_NAMES[l]}{'⁰¹²³⁴⁵⁶⁷⁸⁹ⁱ⁰¹²³⁴'[e] if e < 10 else str(e)}"
                          for n, l, e in config)
    # Simpler notation
    config_plain = " ".join(f"{n}{SUBSHELL_NAMES[l]}{e}" for n, l, e in config)
    st.code(config_plain)

    # Visualisation
    fig, ax = plt.subplots(figsize=(10, 4))

    x_pos = 0
    colours = {"s": "#3b82f6", "p": "#22c55e", "d": "#f97316", "f": "#8b5cf6"}

    for n, l, e in config:
        label = f"{n}{SUBSHELL_NAMES[l]}"
        max_e = 2 * (2 * l + 1)
        ax.bar(x_pos, e, color=colours[SUBSHELL_NAMES[l]], edgecolor="#333",
               width=0.7)
        ax.bar(x_pos, max_e - e, bottom=e, color="#f1f5f9", edgecolor="#333",
               width=0.7, alpha=0.5)
        ax.text(x_pos, -0.5, label, ha="center", fontsize=9, fontweight="bold")
        ax.text(x_pos, e / 2, str(e), ha="center", va="center",
                fontsize=10, color="white", fontweight="bold")
        x_pos += 1

    ax.set_ylabel("Electrons")
    ax.set_title(f"Electron Configuration of {elements.get(z, '?')} (Z = {z})")
    ax.set_xticks([])
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _periodic_trends():
    st.markdown("### Periodic Trends")

    trend = st.selectbox(
        "Select a trend",
        ["Atomic radius", "Ionisation energy", "Electronegativity"],
    )

    # Approximate data for elements 1-20
    z_range = list(range(1, 21))
    symbols = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
               "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca"]

    data = {
        "Atomic radius": {
            "values": [53, 31, 167, 112, 87, 77, 75, 73, 71, 69,
                       190, 145, 118, 111, 98, 88, 79, 71, 243, 194],
            "unit": "pm",
            "colour": "#3b82f6",
        },
        "Ionisation energy": {
            "values": [1312, 2373, 520, 900, 801, 1086, 1402, 1314, 1681, 2081,
                       496, 738, 577, 786, 1012, 1000, 1251, 1521, 419, 590],
            "unit": "kJ/mol",
            "colour": "#ef4444",
        },
        "Electronegativity": {
            "values": [2.20, 0, 0.98, 1.57, 2.04, 2.55, 3.04, 3.44, 3.98, 0,
                       0.93, 1.31, 1.61, 1.90, 2.19, 2.58, 3.16, 0, 0.82, 1.00],
            "unit": "Pauling",
            "colour": "#22c55e",
        },
    }

    d = data[trend]
    vals = d["values"]

    fig, ax = plt.subplots(figsize=(12, 5))

    # Colour by period
    period_colours = []
    for z in z_range:
        if z <= 2:
            period_colours.append("#60a5fa")
        elif z <= 10:
            period_colours.append("#34d399")
        else:
            period_colours.append("#fb923c")

    bars = ax.bar(symbols, vals, color=period_colours, edgecolor="#333")
    ax.set_xlabel("Element")
    ax.set_ylabel(f"{trend} ({d['unit']})")
    ax.set_title(f"{trend} across the first 20 elements")
    ax.grid(True, alpha=0.3, axis="y")

    # Mark period boundaries
    for boundary in [2, 10]:
        ax.axvline(boundary - 0.5, color="grey", linestyle=":", linewidth=1)

    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    if trend == "Atomic radius":
        st.info("💡 Atomic radius **decreases** across a period (more protons pull electrons in) "
                "and **increases** down a group (more shells).")
    elif trend == "Ionisation energy":
        st.info("💡 Ionisation energy **increases** across a period (stronger nuclear charge) "
                "and **decreases** down a group (outer electrons further from nucleus).")
    else:
        st.info("💡 Electronegativity **increases** across a period and **decreases** down a group. "
                "Noble gases have no electronegativity (they don't form bonds easily).")
