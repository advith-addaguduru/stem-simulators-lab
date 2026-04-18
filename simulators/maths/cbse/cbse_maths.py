"""CBSE Maths: Calculus, Trigonometry & Vectors Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Mathematics — CBSE Grade 11-12")

    mode = st.radio(
        "Select topic",
        ["Limits & Derivatives", "Integration", "Vectors & 3D Geometry"],
        horizontal=True,
    )

    if mode == "Limits & Derivatives":
        _limits_derivatives()
    elif mode == "Integration":
        _integration()
    else:
        _vectors()


def _limits_derivatives():
    st.latex(r"\lim_{x \to a} f(x) \quad;\quad f'(x) = \lim_{h \to 0}\frac{f(x+h)-f(x)}{h}")

    with st.sidebar.expander("Derivative Controls", expanded=True):
        func = st.selectbox("Function f(x)", [
            "x² + 3x + 2",
            "sin(x)",
            "eˣ",
            "x³ − 6x² + 9x",
        ], key="cbse_deriv_func")
        x_pt = st.slider("Point x₀", -5.0, 5.0, 1.0, step=0.5, key="cbse_x0")
        show_limit = st.checkbox("Show limit process", value=True)

    x = np.linspace(-5, 5, 500)

    if func == "x² + 3x + 2":
        y = x**2 + 3 * x + 2
        dy = 2 * x + 3
        y0 = x_pt**2 + 3 * x_pt + 2
        dy0 = 2 * x_pt + 3
    elif func == "sin(x)":
        y = np.sin(x)
        dy = np.cos(x)
        y0 = np.sin(x_pt)
        dy0 = np.cos(x_pt)
    elif func == "eˣ":
        y = np.exp(x)
        dy = np.exp(x)
        y0 = np.exp(x_pt)
        dy0 = np.exp(x_pt)
    else:
        y = x**3 - 6 * x**2 + 9 * x
        dy = 3 * x**2 - 12 * x + 9
        y0 = x_pt**3 - 6 * x_pt**2 + 9 * x_pt
        dy0 = 3 * x_pt**2 - 12 * x_pt + 9

    tangent = dy0 * (x - x_pt) + y0

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(x, y, "b-", lw=2, label="f(x)")
    axes[0].plot(x, tangent, "r--", lw=1.5, alpha=0.7, label=f"Tangent at x={x_pt}")
    axes[0].scatter([x_pt], [y0], color="red", s=100, zorder=3)
    axes[0].set_xlim(-5, 5)
    axes[0].set_ylim(min(y0 - 10, -5), max(y0 + 10, 10))
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[0].set_title("f(x) and Tangent")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.25)

    axes[1].plot(x, dy, "g-", lw=2, label="f'(x)")
    axes[1].axhline(0, color="k", lw=0.5)
    axes[1].scatter([x_pt], [dy0], color="red", s=100, zorder=3)
    axes[1].set_xlim(-5, 5)
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("f'(x)")
    axes[1].set_title("Derivative")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    if show_limit:
        st.markdown("**Limit process:** As h → 0:")
        for h in [1.0, 0.1, 0.01, 0.001]:
            if func == "x² + 3x + 2":
                fxh = (x_pt + h)**2 + 3 * (x_pt + h) + 2
            elif func == "sin(x)":
                fxh = np.sin(x_pt + h)
            elif func == "eˣ":
                fxh = np.exp(x_pt + h)
            else:
                fxh = (x_pt + h)**3 - 6 * (x_pt + h)**2 + 9 * (x_pt + h)
            approx = (fxh - y0) / h
            st.write(f"  h = {h}: [f(x₀+h) − f(x₀)]/h = **{approx:.6f}** (exact: {dy0:.6f})")


def _integration():
    st.latex(r"\int_a^b f(x)\,dx = F(b) - F(a)")

    with st.sidebar.expander("Integration Controls", expanded=True):
        func = st.selectbox("Function f(x)", ["x²", "sin(x)", "eˣ", "√x"], key="cbse_int_func")
        a_lim = st.slider("Lower limit a", 0.0, 4.0, 0.0, step=0.5, key="cbse_int_a")
        b_lim = st.slider("Upper limit b", 0.5, 8.0, 3.0, step=0.5, key="cbse_int_b")

    if a_lim >= b_lim:
        st.warning("Upper limit must be greater than lower limit.")
        return

    x = np.linspace(max(0.01, a_lim - 1), b_lim + 1, 500)
    x_fill = np.linspace(max(0.01, a_lim), b_lim, 300)

    if func == "x²":
        y = x**2
        y_fill = x_fill**2
        area = (b_lim**3 - a_lim**3) / 3
        antideriv = "x³/3"
    elif func == "sin(x)":
        y = np.sin(x)
        y_fill = np.sin(x_fill)
        area = -np.cos(b_lim) + np.cos(a_lim)
        antideriv = "−cos(x)"
    elif func == "eˣ":
        y = np.exp(x)
        y_fill = np.exp(x_fill)
        area = np.exp(b_lim) - np.exp(a_lim)
        antideriv = "eˣ"
    else:
        y = np.sqrt(np.maximum(x, 0))
        y_fill = np.sqrt(np.maximum(x_fill, 0))
        area = (2 / 3) * (b_lim**1.5 - max(a_lim, 0)**1.5)
        antideriv = "⅔x^(3/2)"

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, "b-", lw=2, label=f"f(x) = {func}")
    ax.fill_between(x_fill, y_fill, alpha=0.3, color="green", label=f"Area = {area:.4f}")
    ax.axhline(0, color="k", lw=0.5)
    ax.axvline(a_lim, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(b_lim, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Definite Integral of {func}")
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"**∫ {func} dx = {antideriv} + C**")
    st.markdown(f"**∫[{a_lim}, {b_lim}] = {area:.4f}**")


def _vectors():
    st.latex(r"\vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta \quad;\quad |\vec{a} \times \vec{b}| = |\vec{a}||\vec{b}|\sin\theta")

    with st.sidebar.expander("Vector Controls", expanded=True):
        ax_val = st.slider("Vector a: x", -5.0, 5.0, 3.0, step=0.5, key="cbse_vax")
        ay_val = st.slider("Vector a: y", -5.0, 5.0, 1.0, step=0.5, key="cbse_vay")
        bx_val = st.slider("Vector b: x", -5.0, 5.0, 1.0, step=0.5, key="cbse_vbx")
        by_val = st.slider("Vector b: y", -5.0, 5.0, 4.0, step=0.5, key="cbse_vby")

    dot = ax_val * bx_val + ay_val * by_val
    mag_a = np.sqrt(ax_val**2 + ay_val**2)
    mag_b = np.sqrt(bx_val**2 + by_val**2)
    cross_z = ax_val * by_val - ay_val * bx_val

    cos_theta = dot / (mag_a * mag_b) if (mag_a * mag_b) > 0 else 0
    cos_theta = np.clip(cos_theta, -1, 1)
    theta = np.degrees(np.arccos(cos_theta))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("a · b", f"{dot:.2f}")
    col2.metric("|a × b|", f"{abs(cross_z):.2f}")
    col3.metric("Angle θ", f"{theta:.1f}°")
    col4.metric("Area of ||gram", f"{abs(cross_z):.2f}")

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.quiver(0, 0, ax_val, ay_val, angles="xy", scale_units="xy", scale=1, color="blue",
              label=f"a = ({ax_val}, {ay_val})")
    ax.quiver(0, 0, bx_val, by_val, angles="xy", scale_units="xy", scale=1, color="red",
              label=f"b = ({bx_val}, {by_val})")

    # Draw parallelogram
    pgram = plt.Polygon(
        [[0, 0], [ax_val, ay_val], [ax_val + bx_val, ay_val + by_val], [bx_val, by_val]],
        fill=True, alpha=0.15, color="green", edgecolor="green", lw=1, linestyle="--",
    )
    ax.add_patch(pgram)

    lim = max(abs(ax_val) + abs(bx_val), abs(ay_val) + abs(by_val), 3) + 1
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.axhline(0, color="k", lw=0.5)
    ax.axvline(0, color="k", lw=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Vectors — Angle = {theta:.1f}°")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
