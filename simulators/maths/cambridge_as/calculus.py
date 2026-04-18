"""Cambridge AS Level Maths: Calculus Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Differentiation & Integration (9709)")
    st.latex(r"\frac{d}{dx}[x^n] = nx^{n-1} \quad;\quad \int x^n\,dx = \frac{x^{n+1}}{n+1} + C")

    mode = st.radio(
        "Select topic",
        ["Differentiation", "Integration", "Stationary Points"],
        horizontal=True,
    )

    if mode == "Differentiation":
        _differentiation()
    elif mode == "Integration":
        _integration()
    else:
        _stationary_points()


def _differentiation():
    with st.sidebar.expander("Differentiation Controls", expanded=True):
        func = st.selectbox("Function f(x)", [
            "ax² + bx + c",
            "sin(kx)",
            "eᵏˣ",
            "ln(x)",
        ])
        if func == "ax² + bx + c":
            a = st.slider("a", -5.0, 5.0, 1.0, step=0.5, key="diff_a")
            b = st.slider("b", -10.0, 10.0, -2.0, step=0.5, key="diff_b")
            c = st.slider("c", -10.0, 10.0, 1.0, step=0.5, key="diff_c")
        else:
            k = st.slider("k", 0.5, 5.0, 1.0, step=0.5, key="diff_k")
        x_pt = st.slider("Point x₀ for tangent", -5.0, 5.0, 1.0, step=0.5)

    x = np.linspace(-5, 5, 500)
    x_pos = x[x > 0.01]

    if func == "ax² + bx + c":
        y = a * x**2 + b * x + c
        dy = 2 * a * x + b
        y0 = a * x_pt**2 + b * x_pt + c
        dy0 = 2 * a * x_pt + b
    elif func == "sin(kx)":
        y = np.sin(k * x)
        dy = k * np.cos(k * x)
        y0 = np.sin(k * x_pt)
        dy0 = k * np.cos(k * x_pt)
    elif func == "eᵏˣ":
        y = np.exp(k * x)
        dy = k * np.exp(k * x)
        y0 = np.exp(k * x_pt)
        dy0 = k * np.exp(k * x_pt)
    else:
        y = np.full_like(x, np.nan)
        y[x > 0.01] = np.log(x[x > 0.01])
        dy = np.full_like(x, np.nan)
        dy[x > 0.01] = 1.0 / x[x > 0.01]
        y0 = np.log(x_pt) if x_pt > 0 else 0
        dy0 = 1.0 / x_pt if x_pt > 0 else 0

    tangent = dy0 * (x - x_pt) + y0

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(x, y, "b-", lw=2, label="f(x)")
    axes[0].plot(x, tangent, "r--", lw=1.5, alpha=0.7, label=f"Tangent at x={x_pt:.1f}")
    axes[0].scatter([x_pt], [y0], color="red", s=100, zorder=3)
    axes[0].set_xlim(-5, 5)
    axes[0].set_ylim(-10, 10)
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[0].set_title("f(x) and Tangent Line")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.25)

    axes[1].plot(x, dy, "g-", lw=2, label="f'(x)")
    axes[1].axhline(0, color="k", lw=0.5)
    axes[1].scatter([x_pt], [dy0], color="red", s=100, zorder=3)
    axes[1].set_xlim(-5, 5)
    axes[1].set_ylim(-10, 10)
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("dy/dx")
    axes[1].set_title("Derivative f'(x)")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"**At x = {x_pt}:** f(x₀) = {y0:.3f}, f'(x₀) = {dy0:.3f}, Tangent: y = {dy0:.3f}(x − {x_pt}) + {y0:.3f}")


def _integration():
    with st.sidebar.expander("Integration Controls", expanded=True):
        func = st.selectbox("Function f(x)", ["x²", "sin(x)", "eˣ", "1/x (x>0)"], key="int_func")
        a_lim = st.slider("Lower limit a", -5.0, 4.0, 0.0, step=0.5, key="int_a")
        b_lim = st.slider("Upper limit b", -4.0, 5.0, 2.0, step=0.5, key="int_b")

    if a_lim >= b_lim:
        st.warning("Upper limit must be greater than lower limit.")
        return

    x = np.linspace(-5, 5, 500)

    if func == "x²":
        y = x**2
        area_exact = (b_lim**3 - a_lim**3) / 3
    elif func == "sin(x)":
        y = np.sin(x)
        area_exact = -np.cos(b_lim) + np.cos(a_lim)
    elif func == "eˣ":
        y = np.exp(x)
        area_exact = np.exp(b_lim) - np.exp(a_lim)
    else:
        y = np.where(x > 0.01, 1.0 / x, np.nan)
        a_lim = max(a_lim, 0.1)
        area_exact = np.log(b_lim) - np.log(a_lim)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, "b-", lw=2, label=f"f(x) = {func}")

    x_fill = np.linspace(a_lim, b_lim, 200)
    if func == "x²":
        y_fill = x_fill**2
    elif func == "sin(x)":
        y_fill = np.sin(x_fill)
    elif func == "eˣ":
        y_fill = np.exp(x_fill)
    else:
        y_fill = 1.0 / x_fill

    ax.fill_between(x_fill, y_fill, alpha=0.3, color="green", label=f"Area = {area_exact:.3f}")
    ax.axhline(0, color="k", lw=0.5)
    ax.axvline(a_lim, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(b_lim, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-3, 10)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Definite Integral ∫[{a_lim}, {b_lim}] f(x) dx")
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"**∫ from {a_lim} to {b_lim} of {func} dx = {area_exact:.4f}**")


def _stationary_points():
    st.latex(r"\text{Stationary when } f'(x) = 0 \quad;\quad f''(x) > 0 \Rightarrow \text{min}, \quad f''(x) < 0 \Rightarrow \text{max}")

    with st.sidebar.expander("Stationary Point Controls", expanded=True):
        a = st.slider("a (x³ coefficient)", -2.0, 2.0, 1.0, step=0.5, key="sp_a")
        b = st.slider("b (x² coefficient)", -6.0, 6.0, -3.0, step=0.5, key="sp_b")
        c = st.slider("c (x coefficient)", -10.0, 10.0, 0.0, step=1.0, key="sp_c")
        d = st.slider("d (constant)", -10.0, 10.0, 5.0, step=1.0, key="sp_d")

    x = np.linspace(-5, 5, 500)
    y = a * x**3 + b * x**2 + c * x + d
    dy = 3 * a * x**2 + 2 * b * x + c
    ddy = 6 * a * x + 2 * b

    # Find stationary points (solve 3ax² + 2bx + c = 0)
    disc = (2 * b)**2 - 4 * (3 * a) * c
    stat_points = []
    if a != 0 and disc >= 0:
        x1 = (-2 * b + np.sqrt(disc)) / (6 * a)
        x2 = (-2 * b - np.sqrt(disc)) / (6 * a)
        for xp in [x1, x2]:
            yp = a * xp**3 + b * xp**2 + c * xp + d
            ddyp = 6 * a * xp + 2 * b
            nature = "Minimum" if ddyp > 0 else "Maximum" if ddyp < 0 else "Inflection"
            stat_points.append((xp, yp, nature))

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(x, y, "b-", lw=2, label="f(x)")
    for xp, yp, nature in stat_points:
        color = "green" if nature == "Minimum" else "red" if nature == "Maximum" else "orange"
        axes[0].scatter([xp], [yp], color=color, s=150, zorder=3, label=f"{nature} ({xp:.2f}, {yp:.2f})")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[0].set_title("f(x) with Stationary Points")
    axes[0].legend(fontsize=7)
    axes[0].grid(True, alpha=0.25)

    axes[1].plot(x, dy, "r-", lw=2, label="f'(x)")
    axes[1].axhline(0, color="k", lw=0.8)
    for xp, _, _ in stat_points:
        axes[1].scatter([xp], [0], color="black", s=100, zorder=3)
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("f'(x)")
    axes[1].set_title("First Derivative")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    if stat_points:
        for xp, yp, nature in stat_points:
            st.markdown(f"- **{nature}** at x = {xp:.3f}, y = {yp:.3f}")
    else:
        st.info("No stationary points found in this range.")
