"""Cambridge AS Level Physics: Mechanics, Waves, Electricity, Deformation Simulators"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulators.utils import nice_axes

G_DEFAULT = 9.81


def _two_col_plot(fig, caption=None):
    c1, c2 = st.columns([3, 2])
    with c1:
        st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    if caption:
        with c2:
            st.markdown(caption)


def sim_kinematics_dynamics():
    st.subheader("1) Kinematics & Dynamics")
    st.latex(r"s(t) = s_0 + ut + \tfrac{1}{2}at^2 \quad;\quad v(t) = u + at")

    with st.sidebar.expander("Kinematics & Dynamics — Controls", expanded=True):
        s0 = st.number_input("Initial position s₀ (m)", 0.0, 1e6, 0.0, step=0.1)
        u = st.number_input("Initial velocity u (m/s)", -1e4, 1e4, 5.0, step=0.1)
        a_mode = st.radio("Set acceleration by", ["Direct (a)", "Force & Mass (F, m)"], horizontal=True)
        if a_mode == "Direct (a)":
            a = st.number_input("Acceleration a (m/s²)", -1e3, 1e3, 1.0, step=0.1)
        else:
            F = st.number_input("Net force F (N)", -1e6, 1e6, 10.0)
            m = st.number_input("Mass m (kg)", 0.1, 1e6, 2.0, step=0.1)
            a = F / m
            st.caption(f"Computed acceleration a = {a:.4g} m/s² from F = ma")

        T = st.slider("Total time (s)", 1.0, 60.0, 10.0, step=0.5)
        N = st.slider("Time resolution (points)", 50, 2000, 400, step=50)

    t = np.linspace(0, T, N)
    s = s0 + u * t + 0.5 * a * t**2
    v = u + a * t
    a_arr = np.full_like(t, a)

    fig, axs = plt.subplots(3, 1, figsize=(8, 10), sharex=True)
    axs[0].plot(t, s, color="#1f77b4"); nice_axes(axs[0], "t (s)", "s (m)", "Displacement–time")
    axs[1].plot(t, v, color="#ff7f0e"); nice_axes(axs[1], "t (s)", "v (m/s)", "Velocity–time")
    axs[2].plot(t, a_arr, color="#2ca02c"); nice_axes(axs[2], "t (s)", "a (m/s²)", "Acceleration–time")
    plt.tight_layout()

    _two_col_plot(fig, caption=(
        f"**Summary**  \n"
        f"- Final velocity: **{v[-1]:.3g} m/s**  \n"
        f"- Displacement after {T:.2f}s: **{s[-1]-s0:.3g} m**  \n"
        f"- Using equations of motion under constant acceleration."
    ))


def sim_projectile():
    st.subheader("2) Projectile Motion (no air resistance)")
    st.latex(r"""\begin{aligned}
    x(t)&=v_0\cos\theta\ t,\quad y(t)=v_0\sin\theta\ t-\tfrac{1}{2}gt^2\\
    T&=\frac{2v_0\sin\theta}{g},\quad R=\frac{v_0^2\sin 2\theta}{g},\quad H=\frac{v_0^2\sin^2\theta}{2g}
    \end{aligned}""")

    with st.sidebar.expander("Projectile — Controls", expanded=True):
        v0 = st.slider("Initial speed v₀ (m/s)", 1.0, 200.0, 30.0)
        theta_deg = st.slider("Launch angle θ (deg)", 1, 89, 45)
        g = st.slider("Gravity g (m/s²)", 1.0, 20.0, G_DEFAULT)
        N = st.slider("Trajectory resolution", 50, 1000, 400, step=50)

    theta = np.radians(theta_deg)
    T = 2 * v0 * np.sin(theta) / g
    t = np.linspace(0, T, N)
    x = v0 * np.cos(theta) * t
    y = v0 * np.sin(theta) * t - 0.5 * g * t**2

    R = (v0**2 * np.sin(2 * theta)) / g
    H = (v0**2 * (np.sin(theta))**2) / (2 * g)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(x, y, lw=2)
    ax.axhline(0, color="k", lw=0.8)
    ax.scatter([0, R / 2, R], [0, H, 0], color=["green", "orange", "red"], zorder=3)
    nice_axes(ax, "x (m)", "y (m)", "Trajectory")
    ax.set_aspect("equal", adjustable="box")
    plt.tight_layout()

    _two_col_plot(fig, caption=(
        f"**Time of flight:** {T:.3g} s  \n"
        f"**Range:** {R:.3g} m  \n"
        f"**Max height:** {H:.3g} m"
    ))


def sim_forces_density_pressure():
    st.subheader("3) Forces, Density & Pressure")
    st.latex(r"p=\rho g h \quad;\quad F_b=\rho_{\text{fluid}} g V \quad;\quad W=mg")

    with st.sidebar.expander("Forces/Density/Pressure — Controls", expanded=True):
        rho_fl = st.slider("Fluid density ρ_fluid (kg/m³)", 100.0, 20000.0, 1000.0, step=10.0)
        rho_obj = st.slider("Object density ρ_object (kg/m³)", 100.0, 20000.0, 800.0, step=10.0)
        V = st.number_input("Object volume V (m³)", 1e-6, 10.0, 0.01, step=0.001, format="%.6f")
        g = st.slider("g (m/s²)", 1.0, 20.0, G_DEFAULT)
        A = st.number_input("Area for pressure calc A (m²)", 1e-6, 100.0, 0.01, step=0.001, format="%.6f")
        h_max = st.slider("Max depth for pressure plot h_max (m)", 0.1, 100.0, 10.0)

    m = rho_obj * V
    W = m * g
    Fb = rho_fl * g * V
    net = Fb - W

    float_state = "floats (net upward)" if net > 0 else ("sinks (net downward)" if net < 0 else "neutrally buoyant")

    h = np.linspace(0, h_max, 200)
    p = rho_fl * g * h

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(h, p, color="#1f77b4")
    nice_axes(ax, "Depth h (m)", "Gauge pressure p (Pa)", "Hydrostatic pressure")
    plt.tight_layout()

    _two_col_plot(fig, caption=(
        f"**Weight (W):** {W:.3g} N  \n"
        f"**Buoyant force (F_b):** {Fb:.3g} N  \n"
        f"**Net force:** {net:.3g} N → Object **{float_state}**  \n"
        f"**Pressure at depth {h_max:.2f} m:** {p[-1]:.3g} Pa  \n"
        f"**Force on area A at that depth:** {p[-1]*A:.3g} N"
    ))


def sim_waves_superposition():
    st.subheader("4) Waves & Superposition")
    st.latex(r"y(x,t) = A_1\sin(k_1 x - \omega_1 t) + A_2\sin(k_2 x - \omega_2 t + \phi)")

    with st.sidebar.expander("Waves — Controls", expanded=True):
        L = st.slider("Spatial length (m)", 1.0, 20.0, 10.0)
        N_x = st.slider("Spatial resolution (points)", 100, 3000, 800, step=100)
        A1 = st.slider("A₁ (m)", 0.0, 2.0, 1.0, step=0.05)
        f1 = st.slider("f₁ (Hz)", 0.1, 10.0, 1.0, step=0.1)
        A2 = st.slider("A₂ (m)", 0.0, 2.0, 1.0, step=0.05)
        f2 = st.slider("f₂ (Hz)", 0.1, 10.0, 1.0, step=0.1)
        phi_deg = st.slider("Phase φ (deg)", 0, 360, 0, step=5)
        v = st.slider("Wave speed v (m/s)", 0.1, 20.0, 5.0, step=0.1)
        t_now = st.slider("Time t (s)", 0.0, 10.0, 0.5, step=0.05)
        standing = st.checkbox("Show standing wave (A₁=A₂, f₁=f₂, opposite directions)")

    x = np.linspace(0, L, N_x)

    if standing:
        A2 = A1
        f2 = f1
        k = 2 * np.pi * f1 / v
        w = 2 * np.pi * f1
        y = 2 * A1 * np.sin(k * x) * np.cos(w * t_now)
        label_sum = "Standing wave: y = 2A sin(kx) cos(ωt)"
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(x, y, lw=2, label=label_sum)
        nice_axes(ax, "x (m)", "y (m)", "Standing wave pattern")
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        phi = np.radians(phi_deg)
        k1 = 2 * np.pi * f1 / v
        w1 = 2 * np.pi * f1
        k2 = 2 * np.pi * f2 / v
        w2 = 2 * np.pi * f2
        y1 = A1 * np.sin(k1 * x - w1 * t_now)
        y2 = A2 * np.sin(k2 * x - w2 * t_now + phi)
        y = y1 + y2

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(x, y1, alpha=0.7, label="Wave 1")
        ax.plot(x, y2, alpha=0.7, label="Wave 2")
        ax.plot(x, y, lw=2, label="Superposition (sum)")
        nice_axes(ax, "x (m)", "y (m)", "Superposition at time t")
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


def _series_equiv(Rs):
    return np.sum(Rs)


def _parallel_equiv(Rs):
    inv = np.sum([1.0 / r for r in Rs if r > 0])
    return np.inf if inv == 0 else 1.0 / inv


def sim_dc_circuits():
    st.subheader("5) Electricity & D.C. Circuits (Ohmic)")
    st.latex(r"I=\frac{\mathcal{E}}{R_\text{eq}+r}\quad;\quad V_\text{terminal}=\mathcal{E}-Ir")

    with st.sidebar.expander("D.C. Circuits — Controls", expanded=True):
        E = st.slider("Cell EMF 𝓔 (V)", 0.1, 100.0, 12.0)
        r = st.slider("Internal resistance r (Ω)", 0.0, 20.0, 1.0, step=0.1)
        config = st.radio("Load configuration", ["Series", "Parallel"], horizontal=True)
        R1 = st.slider("R₁ (Ω)", 0.1, 1000.0, 50.0, step=0.1)
        R2 = st.slider("R₂ (Ω)", 0.1, 1000.0, 100.0, step=0.1)
        R3 = st.slider("R₃ (Ω)", 0.1, 1000.0, 200.0, step=0.1)

    Rs = np.array([R1, R2, R3])
    Req = _series_equiv(Rs) if config == "Series" else _parallel_equiv(Rs)
    I = E / (Req + r) if np.isfinite(Req) else 0.0
    V_term = E - I * r
    P_load = I**2 * Req
    P_internal = I**2 * r
    eff = 100.0 * P_load / (P_load + P_internal) if (P_load + P_internal) > 0 else 0.0

    st.markdown(f"""
**Equivalent resistance (R_eq):** `{Req:.3g} Ω`  
**Circuit current (I):** `{I:.3g} A`  
**Terminal voltage:** `{V_term:.3g} V`  
**Power in load:** `{P_load:.3g} W` • **Power lost internally:** `{P_internal:.3g} W` • **Efficiency:** `{eff:.1f}%`
""")

    fig, ax = plt.subplots(figsize=(7, 5))
    R_exts = np.linspace(1, 1000, 200)
    I_curve = E / (R_exts + r)
    V_term_curve = E - I_curve * r
    ax.plot(I_curve, V_term_curve, label="V–I (varying load)")
    ax.scatter([I], [V_term], color="red", zorder=3, label="Current setup")
    nice_axes(ax, "Current I (A)", "Terminal voltage V (V)", "Load line")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("**Per‑resistor values**")
    if config == "Series":
        V_drop = I * Rs
        tab = {f"R{i+1} (Ω)": Rs[i] for i in range(3)}
        st.write({**tab,
                  "Current I (A)": float(I),
                  "Voltage drops (V)": [float(v) for v in V_drop]})
    else:
        V_each = V_term
        I_branch = V_each / Rs
        tab = {f"R{i+1} (Ω)": Rs[i] for i in range(3)}
        st.write({**tab,
                  "Branch V (V)": float(V_each),
                  "Branch currents (A)": [float(i) for i in I_branch]})


def sim_deformation_solids():
    st.subheader("6) Deformation of Solids (Hooke's Law, Young's Modulus)")
    st.latex(r"\sigma=\frac{F}{A},\quad \varepsilon=\frac{\Delta L}{L_0},\quad E=\frac{\sigma}{\varepsilon}=\frac{FL_0}{A\Delta L}")

    with st.sidebar.expander("Deformation — Controls", expanded=True):
        material = st.selectbox("Material (preset E)", ["Custom", "Steel", "Aluminium", "Copper", "Nylon"])
        E_map = {"Steel": 200e9, "Aluminium": 70e9, "Copper": 110e9, "Nylon": 2.5e9}
        if material == "Custom":
            E = st.number_input("Young's modulus E (Pa)", 1e6, 1e12, 100e9, step=1e9, format="%.3e")
        else:
            E = E_map[material]
            st.caption(f"Using E ≈ {E:.3e} Pa for {material}")

        L0 = st.number_input("Original length L₀ (m)", 0.001, 100.0, 1.0, step=0.01)
        A = st.number_input("Cross-sectional area A (m²)", 1e-8, 1.0, 1e-4, step=1e-6, format="%.1e")
        Fmax = st.slider("Max force for plot (N)", 1.0, 2e5, 1e4, step=100.0)

    F = np.linspace(0, Fmax, 300)
    sigma = F / A
    deltaL = (F * L0) / (E * A)
    eps = deltaL / L0

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].plot(eps, sigma, lw=2)
    nice_axes(ax[0], "Strain ε", "Stress σ (Pa)", "Stress–strain (linear elastic)")
    ax[1].plot(F, deltaL * 1000, lw=2)
    nice_axes(ax[1], "Force F (N)", "Extension ΔL (mm)", "Force–extension")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    F_pick = st.slider("Show values at force F* (N)", 0.0, float(Fmax), float(0.25 * Fmax))
    sigma_star = F_pick / A
    deltaL_star = (F_pick * L0) / (E * A)
    eps_star = deltaL_star / L0
    U_elastic = 0.5 * F_pick * deltaL_star

    st.markdown(f"""
**At F = {F_pick:.3g} N:**  
• Stress **σ = {sigma_star:.3e} Pa**  • Strain **ε = {eps_star:.3e}**  
• Extension **ΔL = {deltaL_star*1000:.3g} mm**  
• Elastic energy **U = {U_elastic:.3g} J**
""")
