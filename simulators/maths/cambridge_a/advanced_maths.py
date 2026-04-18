"""Cambridge A Level Maths: Advanced Calculus & Further Pure Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("A Level Mathematics — Further Pure & Mechanics")

    mode = st.radio(
        "Select topic",
        ["Integration Techniques", "Differential Equations", "Vectors & Mechanics"],
        horizontal=True,
    )

    if mode == "Integration Techniques":
        _integration_techniques()
    elif mode == "Differential Equations":
        _differential_equations()
    else:
        _vectors_mechanics()


def _integration_techniques():
    st.latex(r"\int_a^b f(x)\,dx \quad;\quad \text{Trapezium rule: } \approx \tfrac{h}{2}[y_0 + 2(y_1+\cdots+y_{n-1}) + y_n]")

    with st.sidebar.expander("Integration Controls", expanded=True):
        func = st.selectbox("Function f(x)", [
            "x·sin(x)", "x²·eˣ", "ln(x)", "1/√(1+x²)"
        ], key="adv_int_func")
        a_lim = st.slider("Lower limit a", 0.1, 4.0, 0.5, step=0.1, key="adv_int_a")
        b_lim = st.slider("Upper limit b", 1.0, 8.0, 3.0, step=0.1, key="adv_int_b")
        n_trap = st.slider("Trapezium strips n", 2, 50, 6, step=2)

    if a_lim >= b_lim:
        st.warning("Upper limit must be greater than lower limit.")
        return

    x = np.linspace(0.01, 10, 500)

    def f(x_val):
        if func == "x·sin(x)":
            return x_val * np.sin(x_val)
        elif func == "x²·eˣ":
            return x_val**2 * np.exp(x_val)
        elif func == "ln(x)":
            return np.log(np.maximum(x_val, 1e-10))
        else:
            return 1.0 / np.sqrt(1 + x_val**2)

    y = f(x)
    x_fill = np.linspace(a_lim, b_lim, 500)
    y_fill = f(x_fill)

    # Trapezium rule
    h = (b_lim - a_lim) / n_trap
    x_trap = np.linspace(a_lim, b_lim, n_trap + 1)
    y_trap = f(x_trap)
    trap_area = h / 2 * (y_trap[0] + 2 * np.sum(y_trap[1:-1]) + y_trap[-1])

    # Numerical exact
    exact_area = np.trapz(y_fill, x_fill)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(x, y, "b-", lw=2, label=f"f(x) = {func}")
    axes[0].fill_between(x_fill, y_fill, alpha=0.2, color="green")
    axes[0].set_xlim(0, max(b_lim + 1, 5))
    axes[0].set_ylim(min(0, np.min(y_fill) - 1), max(np.max(y_fill) + 1, 5))
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[0].set_title("Exact Area (numerical)")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.25)

    # Draw trapeziums
    axes[1].plot(x, y, "b-", lw=2)
    for i in range(n_trap):
        xs = [x_trap[i], x_trap[i], x_trap[i + 1], x_trap[i + 1]]
        ys = [0, y_trap[i], y_trap[i + 1], 0]
        axes[1].fill(xs, ys, alpha=0.3, color="orange", edgecolor="red", lw=1)
    axes[1].scatter(x_trap, y_trap, color="red", s=30, zorder=3)
    axes[1].set_xlim(0, max(b_lim + 1, 5))
    axes[1].set_ylim(min(0, np.min(y_fill) - 1), max(np.max(y_fill) + 1, 5))
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("y")
    axes[1].set_title(f"Trapezium Rule (n={n_trap})")
    axes[1].grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    error = abs(trap_area - exact_area)
    st.markdown(f"""
**Numerical integral:** {exact_area:.6f}  
**Trapezium rule ({n_trap} strips):** {trap_area:.6f}  
**Error:** {error:.6f} ({error / abs(exact_area) * 100:.3f}%)
""")


def _differential_equations():
    st.latex(r"\frac{dy}{dx} = f(x, y) \quad;\quad \text{Euler: } y_{n+1} = y_n + h \cdot f(x_n, y_n)")

    with st.sidebar.expander("ODE Controls", expanded=True):
        ode = st.selectbox("Differential equation", [
            "dy/dx = y  (solution: y = Ce^x)",
            "dy/dx = -2y  (decay)",
            "dy/dx = x + y",
            "dy/dx = sin(x) - y",
        ])
        y0 = st.slider("Initial condition y(0)", -3.0, 3.0, 1.0, step=0.5)
        x_max = st.slider("x range", 1.0, 10.0, 5.0, step=0.5)
        n_steps = st.slider("Euler steps", 10, 200, 50, step=10)

    h = x_max / n_steps
    x_euler = np.zeros(n_steps + 1)
    y_euler = np.zeros(n_steps + 1)
    y_euler[0] = y0

    def f_ode(x, y):
        if "dy/dx = y" in ode:
            return y
        elif "dy/dx = -2y" in ode:
            return -2 * y
        elif "dy/dx = x + y" in ode:
            return x + y
        else:
            return np.sin(x) - y

    for i in range(n_steps):
        x_euler[i + 1] = x_euler[i] + h
        y_euler[i + 1] = y_euler[i] + h * f_ode(x_euler[i], y_euler[i])

    # Exact solutions where available
    x_exact = np.linspace(0, x_max, 500)
    if "dy/dx = y" in ode:
        y_exact = y0 * np.exp(x_exact)
    elif "dy/dx = -2y" in ode:
        y_exact = y0 * np.exp(-2 * x_exact)
    else:
        y_exact = None

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_euler, y_euler, "ro-", markersize=3, lw=1.5, label=f"Euler (n={n_steps})")
    if y_exact is not None:
        ax.plot(x_exact, y_exact, "b-", lw=2, label="Exact solution")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Numerical Solution of ODE")
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"**Step size h = {h:.4f}** — Smaller h gives better accuracy but more computation.")


def _vectors_mechanics():
    st.latex(r"\vec{r} = \vec{a} + t\vec{b} \quad;\quad |\vec{v}| = \sqrt{v_x^2 + v_y^2}")

    with st.sidebar.expander("Vectors Controls", expanded=True):
        mode = st.selectbox("Mode", ["2D Vector Addition", "Projectile with Vectors"])

    if mode == "2D Vector Addition":
        with st.sidebar.expander("Vector Components", expanded=True):
            ax_val = st.slider("Vector A: x-component", -10.0, 10.0, 3.0, step=0.5, key="vax")
            ay_val = st.slider("Vector A: y-component", -10.0, 10.0, 4.0, step=0.5, key="vay")
            bx = st.slider("Vector B: x-component", -10.0, 10.0, -1.0, step=0.5, key="vbx")
            by = st.slider("Vector B: y-component", -10.0, 10.0, 2.0, step=0.5, key="vby")

        rx, ry = ax_val + bx, ay_val + by
        mag_a = np.sqrt(ax_val**2 + ay_val**2)
        mag_b = np.sqrt(bx**2 + by**2)
        mag_r = np.sqrt(rx**2 + ry**2)

        fig, ax = plt.subplots(figsize=(8, 7))
        ax.quiver(0, 0, ax_val, ay_val, angles="xy", scale_units="xy", scale=1, color="blue", label=f"A ({ax_val}, {ay_val})")
        ax.quiver(0, 0, bx, by, angles="xy", scale_units="xy", scale=1, color="red", label=f"B ({bx}, {by})")
        ax.quiver(0, 0, rx, ry, angles="xy", scale_units="xy", scale=1, color="green", lw=2, label=f"R ({rx}, {ry})")
        ax.quiver(ax_val, ay_val, bx, by, angles="xy", scale_units="xy", scale=1, color="red", alpha=0.4)
        lim = max(abs(ax_val) + abs(bx), abs(ay_val) + abs(by), 5) + 2
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Vector Addition: R = A + B")
        ax.legend()
        ax.grid(True, alpha=0.25)
        ax.axhline(0, color="k", lw=0.5)
        ax.axvline(0, color="k", lw=0.5)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown(f"|A| = {mag_a:.3f}, |B| = {mag_b:.3f}, |R| = {mag_r:.3f}")
    else:
        with st.sidebar.expander("Projectile Controls", expanded=True):
            v0 = st.slider("Initial speed v₀ (m/s)", 5.0, 50.0, 20.0, step=1.0, key="vp_v0")
            theta_deg = st.slider("Launch angle θ (°)", 10, 80, 45, key="vp_theta")
            g = 9.81

        theta = np.radians(theta_deg)
        vx = v0 * np.cos(theta)
        vy0 = v0 * np.sin(theta)
        T = 2 * vy0 / g
        t = np.linspace(0, T, 300)
        x_pos = vx * t
        y_pos = vy0 * t - 0.5 * g * t**2

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        axes[0].plot(x_pos, y_pos, "b-", lw=2)
        axes[0].set_xlabel("x (m)")
        axes[0].set_ylabel("y (m)")
        axes[0].set_title("Trajectory")
        axes[0].set_aspect("equal", adjustable="box")
        axes[0].grid(True, alpha=0.25)

        vy_arr = vy0 - g * t
        speed = np.sqrt(vx**2 + vy_arr**2)
        axes[1].plot(t, speed, "r-", lw=2, label="|v|")
        axes[1].plot(t, np.full_like(t, vx), "b--", lw=1, label="vx")
        axes[1].plot(t, vy_arr, "g--", lw=1, label="vy")
        axes[1].axhline(0, color="k", lw=0.5)
        axes[1].set_xlabel("Time (s)")
        axes[1].set_ylabel("Velocity (m/s)")
        axes[1].set_title("Velocity Components")
        axes[1].legend()
        axes[1].grid(True, alpha=0.25)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        R = vx * T
        H = vy0**2 / (2 * g)
        st.markdown(f"**Range:** {R:.2f} m, **Max height:** {H:.2f} m, **Time of flight:** {T:.2f} s")
