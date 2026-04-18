"""Cambridge A Level Chemistry: Kinetics, Equilibrium & Organic Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("A Level Chemistry — Advanced Topics")

    mode = st.radio(
        "Select topic",
        ["Advanced Kinetics", "Equilibrium & Kp", "Electrochemistry"],
        horizontal=True,
    )

    if mode == "Advanced Kinetics":
        _advanced_kinetics()
    elif mode == "Equilibrium & Kp":
        _equilibrium_kp()
    else:
        _electrochemistry()


def _advanced_kinetics():
    st.latex(r"\text{Rate} = k[A]^m[B]^n \quad;\quad t_{1/2} = \frac{\ln 2}{k} \text{ (1st order)}")

    with st.sidebar.expander("Kinetics Controls", expanded=True):
        order = st.selectbox("Reaction order", ["Zero order", "First order", "Second order"])
        k = st.slider("Rate constant k", 0.01, 2.0, 0.1, step=0.01)
        C0 = st.slider("Initial concentration [A]₀ (mol/dm³)", 0.1, 5.0, 1.0, step=0.1)
        t_max = st.slider("Time range (s)", 5.0, 100.0, 30.0, step=5.0)

    t = np.linspace(0, t_max, 500)

    if order == "Zero order":
        C = np.maximum(C0 - k * t, 0)
        half_life = C0 / (2 * k)
        rate_eq = f"Rate = k = {k:.3f} mol/(dm³·s)"
    elif order == "First order":
        C = C0 * np.exp(-k * t)
        half_life = np.log(2) / k
        rate_eq = f"Rate = k[A], k = {k:.3f} s⁻¹"
    else:
        C = C0 / (1 + C0 * k * t)
        half_life = 1 / (k * C0)
        rate_eq = f"Rate = k[A]², k = {k:.3f} dm³/(mol·s)"

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    # [A] vs t
    axes[0].plot(t, C, "b-", lw=2)
    axes[0].axhline(C0 / 2, color="gray", linestyle="--", alpha=0.5)
    axes[0].axvline(half_life, color="red", linestyle="--", alpha=0.5, label=f"t½ = {half_life:.2f} s")
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("[A] (mol/dm³)")
    axes[0].set_title(f"[A] vs Time — {order}")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.25)

    # Rate vs [A]
    conc_range = np.linspace(0.01, C0, 200)
    if order == "Zero order":
        rate = np.full_like(conc_range, k)
    elif order == "First order":
        rate = k * conc_range
    else:
        rate = k * conc_range**2

    axes[1].plot(conc_range, rate, "r-", lw=2)
    axes[1].set_xlabel("[A] (mol/dm³)")
    axes[1].set_ylabel("Rate (mol/(dm³·s))")
    axes[1].set_title("Rate vs [A]")
    axes[1].grid(True, alpha=0.25)

    # ln[A] vs t for first order check
    axes[2].plot(t, np.log(np.maximum(C, 1e-10)), "g-", lw=2)
    axes[2].set_xlabel("Time (s)")
    axes[2].set_ylabel("ln[A]")
    axes[2].set_title("ln[A] vs Time")
    axes[2].grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**{rate_eq}**  
**Half-life:** {half_life:.3f} s  
**Key:** {'Constant half-life (independent of [A])' if order == 'First order' else 'Half-life depends on [A]₀'}
""")


def _equilibrium_kp():
    st.latex(r"K_p = \frac{p_C^c \cdot p_D^d}{p_A^a \cdot p_B^b} \quad;\quad p_i = x_i \cdot P_{total}")

    with st.sidebar.expander("Kp Controls", expanded=True):
        P_total = st.slider("Total pressure (atm)", 0.5, 10.0, 1.0, step=0.5)
        n_A = st.slider("Moles of A at equilibrium", 0.1, 5.0, 1.0, step=0.1)
        n_B = st.slider("Moles of B at equilibrium", 0.1, 5.0, 1.0, step=0.1)
        n_C = st.slider("Moles of C at equilibrium", 0.1, 5.0, 0.5, step=0.1)
        n_D = st.slider("Moles of D at equilibrium", 0.1, 5.0, 0.5, step=0.1)

    n_total = n_A + n_B + n_C + n_D
    x_A, x_B, x_C, x_D = n_A / n_total, n_B / n_total, n_C / n_total, n_D / n_total
    p_A, p_B, p_C, p_D = x_A * P_total, x_B * P_total, x_C * P_total, x_D * P_total
    Kp = (p_C * p_D) / (p_A * p_B) if (p_A * p_B) > 0 else 0

    col1, col2 = st.columns(2)
    col1.metric("Kp", f"{Kp:.4f}")
    col2.metric("Total Pressure", f"{P_total} atm")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    species = ["A", "B", "C", "D"]
    mole_fracs = [x_A, x_B, x_C, x_D]
    partial_ps = [p_A, p_B, p_C, p_D]

    axes[0].bar(species, mole_fracs, color=["#3498db", "#e74c3c", "#2ecc71", "#f39c12"], alpha=0.8)
    axes[0].set_ylabel("Mole Fraction")
    axes[0].set_title("Mole Fractions")
    axes[0].grid(True, alpha=0.25, axis="y")

    axes[1].bar(species, partial_ps, color=["#3498db", "#e74c3c", "#2ecc71", "#f39c12"], alpha=0.8)
    axes[1].set_ylabel("Partial Pressure (atm)")
    axes[1].set_title("Partial Pressures")
    axes[1].grid(True, alpha=0.25, axis="y")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**Kp = (p_C × p_D) / (p_A × p_B) = ({p_C:.3f} × {p_D:.3f}) / ({p_A:.3f} × {p_B:.3f}) = {Kp:.4f}**

**Effect of pressure:** If Δn(gas) > 0, increasing pressure shifts equilibrium to fewer moles side.
""")


def _electrochemistry():
    st.latex(r"E^\circ_{cell} = E^\circ_{cathode} - E^\circ_{anode} \quad;\quad \Delta G = -nFE^\circ")

    with st.sidebar.expander("Electrochemistry Controls", expanded=True):
        cathode = st.selectbox("Cathode (reduction)", [
            "Cu²⁺/Cu (+0.34 V)",
            "Ag⁺/Ag (+0.80 V)",
            "Fe³⁺/Fe²⁺ (+0.77 V)",
            "Cl₂/Cl⁻ (+1.36 V)",
        ])
        anode = st.selectbox("Anode (oxidation)", [
            "Zn²⁺/Zn (−0.76 V)",
            "Fe²⁺/Fe (−0.44 V)",
            "Pb²⁺/Pb (−0.13 V)",
            "H⁺/H₂ (0.00 V)",
        ])
        n_electrons = st.slider("Electrons transferred (n)", 1, 4, 2)

    E_cathode_map = {"Cu²⁺/Cu (+0.34 V)": 0.34, "Ag⁺/Ag (+0.80 V)": 0.80,
                     "Fe³⁺/Fe²⁺ (+0.77 V)": 0.77, "Cl₂/Cl⁻ (+1.36 V)": 1.36}
    E_anode_map = {"Zn²⁺/Zn (−0.76 V)": -0.76, "Fe²⁺/Fe (−0.44 V)": -0.44,
                   "Pb²⁺/Pb (−0.13 V)": -0.13, "H⁺/H₂ (0.00 V)": 0.00}

    E_cathode = E_cathode_map[cathode]
    E_anode = E_anode_map[anode]
    E_cell = E_cathode - E_anode

    F = 96485  # C/mol
    delta_G = -n_electrons * F * E_cell

    feasible = E_cell > 0

    col1, col2, col3 = st.columns(3)
    col1.metric("E°cell", f"{E_cell:.2f} V")
    col2.metric("ΔG°", f"{delta_G/1e3:.2f} kJ/mol")
    col3.metric("Feasible?", "Yes ✅" if feasible else "No ❌")

    fig, ax = plt.subplots(figsize=(8, 5))
    half_cells = [anode.split("(")[0].strip(), cathode.split("(")[0].strip()]
    potentials = [E_anode, E_cathode]
    colors = ["#e74c3c", "#2ecc71"]
    ax.barh(half_cells, potentials, color=colors, alpha=0.8)
    ax.axvline(0, color="k", lw=1)
    ax.set_xlabel("Standard Electrode Potential E° (V)")
    ax.set_title(f"Cell EMF = {E_cell:.2f} V")
    ax.grid(True, alpha=0.25, axis="x")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**Cell reaction is {'spontaneous (feasible)' if feasible else 'non-spontaneous'}**  
**E°cell = E°cathode − E°anode = {E_cathode:.2f} − ({E_anode:.2f}) = {E_cell:.2f} V**
""")
