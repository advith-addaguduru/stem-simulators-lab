"""ICSE Chemistry: Acids, Bases, Salts & Organic Chemistry Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Chemistry — ICSE Grade 10-12")

    mode = st.radio(
        "Select topic",
        ["Acids, Bases & Salts", "Periodic Table Trends", "Organic Chemistry Basics"],
        horizontal=True,
    )

    if mode == "Acids, Bases & Salts":
        _acids_bases_salts()
    elif mode == "Periodic Table Trends":
        _periodic_trends()
    else:
        _organic_basics()


def _acids_bases_salts():
    st.latex(r"pH = -\log_{10}[H^+] \quad;\quad \text{Acid + Base} \rightarrow \text{Salt + Water}")

    with st.sidebar.expander("pH & Titration Controls", expanded=True):
        experiment = st.selectbox("Experiment", ["pH Calculator", "Titration Curve"])

    if experiment == "pH Calculator":
        acid_base = st.sidebar.selectbox("Type", [
            "HCl (strong acid)", "NaOH (strong base)",
            "CH₃COOH (weak acid)", "NH₃ (weak base)"
        ])
        conc = st.sidebar.slider("Concentration (mol/dm³)", 0.001, 1.0, 0.1, step=0.001)

        if acid_base == "HCl (strong acid)":
            pH = -np.log10(conc)
        elif acid_base == "NaOH (strong base)":
            pH = 14 + np.log10(conc)
        elif acid_base == "CH₃COOH (weak acid)":
            Ka = 1.8e-5
            H = np.sqrt(Ka * conc)
            pH = -np.log10(H)
        else:
            Kb = 1.8e-5
            OH = np.sqrt(Kb * conc)
            pOH = -np.log10(OH)
            pH = 14 - pOH

        col1, col2 = st.columns(2)
        col1.metric("pH", f"{pH:.2f}")
        col2.metric("Nature", "Acidic" if pH < 7 else "Basic" if pH > 7 else "Neutral")

        fig, ax = plt.subplots(figsize=(10, 2.5))
        pH_scale = np.linspace(0, 14, 300)
        colors_scale = plt.cm.RdYlBu(pH_scale / 14)
        for i in range(len(pH_scale) - 1):
            ax.barh(0, pH_scale[i + 1] - pH_scale[i], left=pH_scale[i],
                    height=0.5, color=colors_scale[i])
        ax.axvline(pH, color="black", lw=3, label=f"pH = {pH:.2f}")
        ax.axvline(7, color="gray", lw=1, linestyle="--", alpha=0.5)
        ax.set_xlim(0, 14)
        ax.set_xlabel("pH")
        ax.set_yticks([])
        ax.set_title("pH Scale")
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    else:  # Titration curve
        with st.sidebar.expander("Titration Controls", expanded=True):
            acid_conc = st.slider("Acid conc (mol/dm³)", 0.05, 1.0, 0.1, step=0.05, key="icse_ac")
            acid_vol = st.slider("Acid volume (cm³)", 10, 50, 25, step=5, key="icse_av")
            base_conc = st.slider("Base conc (mol/dm³)", 0.05, 1.0, 0.1, step=0.05, key="icse_bc")

        vol_base = np.linspace(0, acid_vol * 2, 500)
        moles_acid = acid_conc * acid_vol / 1000
        moles_base = base_conc * vol_base / 1000

        pH_values = []
        for mb in moles_base:
            excess_acid = moles_acid - mb
            total_vol = (acid_vol + vol_base[0]) / 1000  # approximate
            total_vol_actual = (acid_vol / 1000) + (mb / base_conc if base_conc > 0 else 0)
            if total_vol_actual == 0:
                total_vol_actual = 1e-6
            if excess_acid > 1e-10:
                H = excess_acid / total_vol_actual
                pH_values.append(-np.log10(max(H, 1e-14)))
            elif excess_acid < -1e-10:
                OH = -excess_acid / total_vol_actual
                pOH = -np.log10(max(OH, 1e-14))
                pH_values.append(14 - pOH)
            else:
                pH_values.append(7.0)

        equiv_vol = moles_acid / base_conc * 1000

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(vol_base, pH_values, "b-", lw=2)
        ax.axhline(7, color="gray", linestyle="--", alpha=0.5, label="pH 7")
        ax.axvline(equiv_vol, color="red", linestyle="--", alpha=0.5,
                   label=f"Equivalence: {equiv_vol:.1f} cm³")
        ax.set_xlabel("Volume of base added (cm³)")
        ax.set_ylabel("pH")
        ax.set_title("Acid-Base Titration Curve")
        ax.set_ylim(0, 14)
        ax.legend()
        ax.grid(True, alpha=0.25)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown(f"**Equivalence point:** {equiv_vol:.1f} cm³ of base needed")


def _periodic_trends():
    st.markdown("Explore trends across Period 3 (Na → Ar) of the Periodic Table.")

    elements = ["Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"]
    atomic_radii = [186, 160, 143, 117, 110, 104, 99, 71]  # pm
    ionisation_e = [496, 738, 578, 786, 1012, 1000, 1251, 1521]  # kJ/mol
    electronegativity = [0.93, 1.31, 1.61, 1.90, 2.19, 2.58, 3.16, 0]  # Pauling

    with st.sidebar.expander("Trend Controls", expanded=True):
        prop = st.selectbox("Property", [
            "Atomic Radius", "First Ionisation Energy", "Electronegativity"
        ])

    if prop == "Atomic Radius":
        values = atomic_radii
        ylabel = "Atomic Radius (pm)"
        trend = "Decreases across the period (more protons, same shell)"
    elif prop == "First Ionisation Energy":
        values = ionisation_e
        ylabel = "1st Ionisation Energy (kJ/mol)"
        trend = "Generally increases across the period (stronger nuclear attraction)"
    else:
        values = electronegativity
        ylabel = "Electronegativity (Pauling)"
        trend = "Increases across the period (Ar has no value — noble gas)"

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(elements)))
    ax.bar(elements, values, color=colors, alpha=0.8)
    ax.plot(elements, values, "ro-", lw=1.5, markersize=6)
    ax.set_ylabel(ylabel)
    ax.set_title(f"Period 3: {prop}")
    ax.grid(True, alpha=0.25, axis="y")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"**Trend:** {trend}")


def _organic_basics():
    st.latex(r"\text{Alkanes: } C_nH_{2n+2} \quad;\quad \text{Alkenes: } C_nH_{2n}")

    with st.sidebar.expander("Organic Chemistry Controls", expanded=True):
        family = st.selectbox("Homologous series", ["Alkanes", "Alkenes", "Alcohols"])
        n_carbon = st.slider("Number of carbons n", 1, 10, 4)

    if family == "Alkanes":
        formula = f"C{n_carbon}H{2*n_carbon+2}" if n_carbon > 1 else "CH₄"
        general = "CₙH₂ₙ₊₂"
        mr = 12 * n_carbon + (2 * n_carbon + 2)
        bp_data = [-162, -89, -42, -0.5, 36, 69, 98, 126, 151, 174]
        names = ["Methane", "Ethane", "Propane", "Butane", "Pentane",
                 "Hexane", "Heptane", "Octane", "Nonane", "Decane"]
    elif family == "Alkenes":
        if n_carbon < 2:
            st.warning("Alkenes need at least 2 carbons.")
            n_carbon = 2
        formula = f"C{n_carbon}H{2*n_carbon}"
        general = "CₙH₂ₙ"
        mr = 12 * n_carbon + 2 * n_carbon
        bp_data = [None, -104, -47, -6, 30, 63, 94, 121, 147, 171]
        names = ["—", "Ethene", "Propene", "Butene", "Pentene",
                 "Hexene", "Heptene", "Octene", "Nonene", "Decene"]
    else:
        formula = f"C{n_carbon}H{2*n_carbon+1}OH"
        general = "CₙH₂ₙ₊₁OH"
        mr = 12 * n_carbon + (2 * n_carbon + 1) + 17
        bp_data = [65, 78, 97, 117, 138, 157, 176, 195, 214, 231]
        names = ["Methanol", "Ethanol", "Propanol", "Butanol", "Pentanol",
                 "Hexanol", "Heptanol", "Octanol", "Nonanol", "Decanol"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Formula", formula)
    col2.metric("Mr", f"{mr}")
    col3.metric("Name", names[n_carbon - 1] if n_carbon <= len(names) else "—")

    # Boiling point trend
    valid_bps = [(i + 1, bp) for i, bp in enumerate(bp_data) if bp is not None]
    ns, bps = zip(*valid_bps)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ns, bps, "bo-", lw=2, label=f"{family} boiling points")
    if n_carbon <= len(bp_data) and bp_data[n_carbon - 1] is not None:
        ax.scatter([n_carbon], [bp_data[n_carbon - 1]], color="red", s=150, zorder=3,
                   label=f"n={n_carbon}: {bp_data[n_carbon-1]}°C")
    ax.set_xlabel("Number of carbons (n)")
    ax.set_ylabel("Boiling Point (°C)")
    ax.set_title(f"{family} ({general}) — Boiling Point Trend")
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**Trend:** Boiling point increases with chain length due to stronger van der Waals forces.  
**General formula:** {general}
""")
