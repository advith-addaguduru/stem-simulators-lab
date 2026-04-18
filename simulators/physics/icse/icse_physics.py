"""ICSE Physics: Motion, Energy & Optics Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Physics — ICSE Grade 10-12")

    mode = st.radio(
        "Select topic",
        ["Motion & Work-Energy", "Refraction & Lenses", "Current Electricity"],
        horizontal=True,
    )

    if mode == "Motion & Work-Energy":
        _work_energy()
    elif mode == "Refraction & Lenses":
        _refraction_lenses()
    else:
        _current_electricity()


def _work_energy():
    st.latex(r"W = Fd\cos\theta \quad;\quad KE = \tfrac{1}{2}mv^2 \quad;\quad PE = mgh")

    with st.sidebar.expander("Work-Energy Controls", expanded=True):
        m = st.slider("Mass m (kg)", 0.5, 20.0, 5.0, step=0.5)
        v = st.slider("Velocity v (m/s)", 0.0, 30.0, 10.0, step=0.5)
        h = st.slider("Height h (m)", 0.0, 50.0, 10.0, step=1.0)
        g = 9.81

    KE = 0.5 * m * v**2
    PE = m * g * h
    TE = KE + PE

    col1, col2, col3 = st.columns(3)
    col1.metric("Kinetic Energy", f"{KE:.1f} J")
    col2.metric("Potential Energy", f"{PE:.1f} J")
    col3.metric("Total Energy", f"{TE:.1f} J")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Energy bar chart
    axes[0].bar(["KE", "PE", "Total"], [KE, PE, TE],
                color=["#e74c3c", "#3498db", "#2ecc71"], alpha=0.8)
    axes[0].set_ylabel("Energy (J)")
    axes[0].set_title("Energy Distribution")
    axes[0].grid(True, alpha=0.25, axis="y")

    # KE vs velocity
    v_range = np.linspace(0, 30, 200)
    KE_range = 0.5 * m * v_range**2
    axes[1].plot(v_range, KE_range, "r-", lw=2)
    axes[1].scatter([v], [KE], color="blue", s=100, zorder=3, label=f"v = {v} m/s")
    axes[1].set_xlabel("Velocity (m/s)")
    axes[1].set_ylabel("Kinetic Energy (J)")
    axes[1].set_title("KE vs Velocity")
    axes[1].legend()
    axes[1].grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Free-fall energy conservation
    st.markdown(f"""
**Energy conservation (free fall from h = {h} m, starting at rest):**
- At top: KE = 0, PE = {m*g*h:.1f} J
- At bottom: KE = {m*g*h:.1f} J, PE = 0
- Speed at bottom: v = √(2gh) = **{np.sqrt(2*g*h):.2f} m/s**
""")


def _refraction_lenses():
    st.latex(r"n_1\sin\theta_1 = n_2\sin\theta_2 \quad;\quad \frac{1}{f} = \frac{1}{v} - \frac{1}{u}")

    with st.sidebar.expander("Lens Controls", expanded=True):
        lens_type = st.selectbox("Lens type", ["Convex (converging)", "Concave (diverging)"])
        f = st.slider("Focal length |f| (cm)", 5.0, 30.0, 15.0, step=1.0)
        u = st.slider("Object distance u (cm)", 5.0, 60.0, 30.0, step=1.0)
        obj_height = st.slider("Object height (cm)", 1.0, 10.0, 3.0, step=0.5)

    if lens_type == "Convex (converging)":
        f_val = f
    else:
        f_val = -f

    u_val = -u  # Convention: object on left

    try:
        v_val = 1 / (1 / f_val + 1 / u_val)  # 1/v = 1/f - 1/u → 1/v = 1/f + 1/u_val
    except ZeroDivisionError:
        v_val = float("inf")

    magnification = v_val / u_val if u_val != 0 else 0
    image_height = magnification * obj_height

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Image distance v", f"{v_val:.1f} cm")
    col2.metric("Magnification", f"{magnification:.2f}")
    col3.metric("Image height", f"{abs(image_height):.1f} cm")
    nature = "Real, Inverted" if v_val > 0 and lens_type == "Convex (converging)" else "Virtual, Upright"
    col4.metric("Nature", nature)

    # Ray diagram
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axhline(0, color="k", lw=1)  # Principal axis
    ax.axvline(0, color="k", lw=0.5)  # Lens

    # Lens representation
    lens_h = max(abs(obj_height), abs(image_height), 5) + 2
    if "Convex" in lens_type:
        ax.annotate("", xy=(0, lens_h), xytext=(0, -lens_h),
                    arrowprops=dict(arrowstyle="<->", color="blue", lw=2))
    else:
        ax.plot([0, 0], [-lens_h, lens_h], "b-", lw=2)

    # Focal points
    ax.scatter([f_val, -f_val], [0, 0], color="green", s=50, zorder=3)
    ax.text(f_val, -1, "F", ha="center", fontsize=9, color="green")
    ax.text(-f_val, -1, "F'", ha="center", fontsize=9, color="green")

    # Object
    ax.annotate("", xy=(u_val, obj_height), xytext=(u_val, 0),
                arrowprops=dict(arrowstyle="->", color="red", lw=2))
    ax.text(u_val, obj_height + 0.5, "Object", ha="center", fontsize=8, color="red")

    # Image
    if abs(v_val) < 200:
        ax.annotate("", xy=(v_val, -image_height), xytext=(v_val, 0),
                    arrowprops=dict(arrowstyle="->", color="purple", lw=2))
        ax.text(v_val, -image_height - 1, "Image", ha="center", fontsize=8, color="purple")

    lim_x = max(abs(u_val), abs(v_val) if abs(v_val) < 200 else abs(u_val), 20) + 5
    ax.set_xlim(-lim_x, lim_x)
    ax.set_ylim(-lens_h - 2, lens_h + 2)
    ax.set_xlabel("Distance (cm)")
    ax.set_ylabel("Height (cm)")
    ax.set_title(f"{lens_type} Lens — Ray Diagram")
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _current_electricity():
    st.latex(r"V = IR \quad;\quad R = \frac{\rho L}{A} \quad;\quad P = VI")

    with st.sidebar.expander("Resistance Controls", expanded=True):
        rho = st.slider("Resistivity ρ (×10⁻⁸ Ω·m)", 1.0, 50.0, 1.7, step=0.1)
        L = st.slider("Wire length L (m)", 0.1, 10.0, 1.0, step=0.1)
        d = st.slider("Wire diameter d (mm)", 0.1, 3.0, 1.0, step=0.1)
        V_supply = st.slider("Supply voltage V (V)", 1.0, 24.0, 6.0, step=0.5)

    rho_SI = rho * 1e-8
    A = np.pi * (d * 1e-3 / 2) ** 2
    R = rho_SI * L / A
    I = V_supply / R
    P = V_supply * I

    col1, col2, col3 = st.columns(3)
    col1.metric("Resistance R", f"{R:.4f} Ω")
    col2.metric("Current I", f"{I:.4f} A")
    col3.metric("Power P", f"{P:.4f} W")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # R vs L
    L_range = np.linspace(0.1, 10, 200)
    R_range = rho_SI * L_range / A
    axes[0].plot(L_range, R_range, "b-", lw=2)
    axes[0].scatter([L], [R], color="red", s=100, zorder=3)
    axes[0].set_xlabel("Length (m)")
    axes[0].set_ylabel("Resistance (Ω)")
    axes[0].set_title("R vs Length (constant diameter)")
    axes[0].grid(True, alpha=0.25)

    # V-I characteristic
    I_range = np.linspace(0, V_supply / R * 1.5, 200)
    V_range = I_range * R
    axes[1].plot(I_range, V_range, "r-", lw=2)
    axes[1].scatter([I], [V_supply], color="blue", s=100, zorder=3)
    axes[1].set_xlabel("Current I (A)")
    axes[1].set_ylabel("Voltage V (V)")
    axes[1].set_title(f"V-I Characteristic (R = {R:.4f} Ω)")
    axes[1].grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
