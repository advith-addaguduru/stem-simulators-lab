"""IGCSE Grades 9-10 Chemistry: Atomic Structure Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Atomic Structure")
    st.latex(r"\text{Mass number } A = Z + N \quad;\quad \text{Atomic number } Z = \text{protons}")

    mode = st.radio(
        "Select topic",
        ["Atom Builder", "Isotopes & Relative Atomic Mass", "Electron Configuration"],
        horizontal=True,
    )

    if mode == "Atom Builder":
        _atom_builder()
    elif mode == "Isotopes & Relative Atomic Mass":
        _isotopes()
    else:
        _electron_config()


def _atom_builder():
    with st.sidebar.expander("Atom Builder Controls", expanded=True):
        protons = st.slider("Protons (Z)", 1, 20, 6)
        neutrons = st.slider("Neutrons (N)", 0, 30, 6)
        electrons = st.slider("Electrons", 0, 20, 6)

    mass_number = protons + neutrons
    charge = protons - electrons
    charge_str = "neutral" if charge == 0 else (f"+{charge}" if charge > 0 else str(charge))

    element_map = {
        1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O",
        9: "F", 10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",
        16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca",
    }
    symbol = element_map.get(protons, "?")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Element", symbol)
    col2.metric("Mass Number (A)", mass_number)
    col3.metric("Atomic Number (Z)", protons)
    col4.metric("Charge", charge_str)

    # Visual representation
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Atom: {symbol}-{mass_number}")

    # Nucleus
    nucleus = plt.Circle((0, 0), 0.8, color="gold", alpha=0.7, zorder=2)
    ax.add_patch(nucleus)
    ax.text(0, 0, f"{protons}p\n{neutrons}n", ha="center", va="center", fontsize=9, fontweight="bold")

    # Electron shells
    shells = [2, 8, 8, 2]
    remaining = electrons
    radii = [1.8, 2.8, 3.8, 4.6]
    colors = ["#3498db", "#2ecc71", "#e74c3c", "#9b59b6"]
    for i, (capacity, r) in enumerate(zip(shells, radii)):
        if remaining <= 0:
            break
        n_in_shell = min(remaining, capacity)
        remaining -= n_in_shell
        circle = plt.Circle((0, 0), r, fill=False, color=colors[i], linestyle="--", alpha=0.5)
        ax.add_patch(circle)
        angles = np.linspace(0, 2 * np.pi, n_in_shell, endpoint=False)
        for angle in angles:
            ex, ey = r * np.cos(angle), r * np.sin(angle)
            ax.plot(ex, ey, "o", color=colors[i], markersize=6, zorder=3)

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**Particle Summary:**
- Protons: **{protons}** (positive charge)
- Neutrons: **{neutrons}** (no charge)
- Electrons: **{electrons}** (negative charge)
- Net charge: **{charge_str}**
- {'This is an **ion**.' if charge != 0 else 'This is a **neutral atom**.'}
""")


def _isotopes():
    st.latex(r"A_r = \frac{\sum (\text{mass} \times \text{abundance})}{100}")

    with st.sidebar.expander("Isotope Controls", expanded=True):
        element = st.selectbox("Element", ["Carbon", "Chlorine", "Bromine", "Custom"])

    if element == "Carbon":
        masses = [12, 13]
        abundances = [98.9, 1.1]
        names = ["¹²C", "¹³C"]
    elif element == "Chlorine":
        masses = [35, 37]
        abundances = [75.77, 24.23]
        names = ["³⁵Cl", "³⁷Cl"]
    elif element == "Bromine":
        masses = [79, 81]
        abundances = [50.7, 49.3]
        names = ["⁷⁹Br", "⁸¹Br"]
    else:
        with st.sidebar.expander("Custom Isotopes", expanded=True):
            n_isotopes = st.slider("Number of isotopes", 2, 4, 2)
            masses, abundances, names = [], [], []
            for i in range(n_isotopes):
                m = st.number_input(f"Mass {i+1}", 1.0, 300.0, float(12 + i), key=f"iso_m{i}")
                a = st.number_input(f"Abundance {i+1} (%)", 0.0, 100.0, 100.0 / n_isotopes, key=f"iso_a{i}")
                masses.append(m)
                abundances.append(a)
                names.append(f"Isotope {i+1}")

    Ar = sum(m * a for m, a in zip(masses, abundances)) / sum(abundances)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(names, abundances, color=["#3498db", "#e74c3c", "#2ecc71", "#9b59b6"][: len(names)], alpha=0.8)
    ax.set_ylabel("Relative Abundance (%)")
    ax.set_title(f"Isotope Distribution — Relative Atomic Mass = {Ar:.2f}")
    ax.grid(True, alpha=0.25, axis="y")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"**Relative Atomic Mass (Aᵣ) = {Ar:.2f}**")


def _electron_config():
    with st.sidebar.expander("Electron Configuration Controls", expanded=True):
        Z = st.slider("Atomic number Z", 1, 20, 11)

    element_map = {
        1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O",
        9: "F", 10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",
        16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca",
    }
    symbol = element_map.get(Z, "?")

    shells = []
    remaining = Z
    for cap in [2, 8, 8, 2]:
        if remaining <= 0:
            break
        n = min(remaining, cap)
        shells.append(n)
        remaining -= n

    config_str = ".".join(str(s) for s in shells)

    col1, col2 = st.columns(2)
    col1.metric("Element", f"{symbol} (Z={Z})")
    col2.metric("Configuration", config_str)

    fig, ax = plt.subplots(figsize=(8, 4))
    shell_labels = [f"Shell {i+1}" for i in range(len(shells))]
    capacities = [2, 8, 8, 2][: len(shells)]
    ax.bar(shell_labels, capacities, color="lightgray", alpha=0.5, label="Capacity")
    ax.bar(shell_labels, shells, color="#3498db", alpha=0.8, label="Electrons")
    ax.set_ylabel("Number of electrons")
    ax.set_title(f"Electron Configuration of {symbol}: {config_str}")
    ax.legend()
    ax.grid(True, alpha=0.25, axis="y")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Valence info
    valence = shells[-1] if shells else 0
    group_guess = valence if valence <= 4 else 8 - valence if valence < 8 else 0
    st.markdown(f"""
**Valence electrons:** {valence}  
**Electron configuration:** {config_str}  
**Likely group:** {valence} (for simple elements up to Z=20)
""")
