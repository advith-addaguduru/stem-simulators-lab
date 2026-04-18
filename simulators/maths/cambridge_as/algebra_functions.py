"""Cambridge AS Level Maths: Algebra & Functions Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Algebra & Functions (9709)")
    st.latex(r"f(x), \quad f^{-1}(x), \quad |f(x)|, \quad \text{Partial Fractions}")

    mode = st.radio(
        "Select topic",
        ["Quadratics & Inequalities", "Functions & Inverses", "Partial Fractions"],
        horizontal=True,
    )

    if mode == "Quadratics & Inequalities":
        _quadratics()
    elif mode == "Functions & Inverses":
        _functions_inverses()
    else:
        _partial_fractions()


def _quadratics():
    st.latex(r"ax^2 + bx + c = 0 \quad;\quad \Delta = b^2 - 4ac")

    with st.sidebar.expander("Quadratic Controls", expanded=True):
        a = st.slider("a", -5.0, 5.0, 1.0, step=0.5, key="qa")
        b = st.slider("b", -10.0, 10.0, -2.0, step=0.5, key="qb")
        c = st.slider("c", -10.0, 10.0, -3.0, step=0.5, key="qc")
        show_completing = st.checkbox("Show completed square form", value=True)

    if a == 0:
        st.warning("a cannot be zero for a quadratic.")
        return

    x = np.linspace(-10, 10, 500)
    y = a * x**2 + b * x + c
    disc = b**2 - 4 * a * c
    vx = -b / (2 * a)
    vy = a * vx**2 + b * vx + c

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, "b-", lw=2)
    ax.axhline(0, color="k", lw=0.5)
    ax.axvline(0, color="k", lw=0.5)
    ax.scatter([vx], [vy], color="red", s=120, zorder=3, label=f"Vertex ({vx:.2f}, {vy:.2f})")

    if disc > 0:
        r1 = (-b + np.sqrt(disc)) / (2 * a)
        r2 = (-b - np.sqrt(disc)) / (2 * a)
        ax.scatter([r1, r2], [0, 0], color="green", s=100, zorder=3)
        ax.annotate(f"x={r1:.2f}", (r1, 0), textcoords="offset points", xytext=(5, 10))
        ax.annotate(f"x={r2:.2f}", (r2, 0), textcoords="offset points", xytext=(5, 10))

    # Shade inequality region y > 0
    ax.fill_between(x, y, 0, where=(y > 0), alpha=0.1, color="green", label="f(x) > 0")
    ax.fill_between(x, y, 0, where=(y < 0), alpha=0.1, color="red", label="f(x) < 0")

    ax.set_xlim(-10, 10)
    ax.set_ylim(min(-10, vy - 5), max(10, vy + 5))
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    ax.set_title("Quadratic with Inequality Regions")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    if show_completing and a != 0:
        p = b / (2 * a)
        q = c - b**2 / (4 * a)
        st.latex(rf"y = {a}(x {'+' if p >= 0 else ''}{p:.2f})^2 {'+' if q >= 0 else ''}{q:.2f}")

    st.markdown(f"**Discriminant Δ = {disc:.2f}** → {'Two distinct real roots' if disc > 0 else 'Repeated root' if disc == 0 else 'No real roots'}")


def _functions_inverses():
    with st.sidebar.expander("Function Controls", expanded=True):
        func_choice = st.selectbox("Function", [
            "f(x) = 2x + 3",
            "f(x) = x² (x ≥ 0)",
            "f(x) = eˣ",
            "f(x) = ln(x)",
        ])

    x = np.linspace(-5, 5, 500)
    x_pos = x[x > 0.01]

    fig, ax = plt.subplots(figsize=(8, 7))
    ax.plot([-10, 10], [-10, 10], "k--", alpha=0.3, label="y = x")

    if func_choice == "f(x) = 2x + 3":
        y = 2 * x + 3
        y_inv = (x - 3) / 2
        ax.plot(x, y, "b-", lw=2, label="f(x) = 2x + 3")
        ax.plot(x, y_inv, "r-", lw=2, label="f⁻¹(x) = (x-3)/2")
    elif func_choice == "f(x) = x² (x ≥ 0)":
        x_nn = x[x >= 0]
        y = x_nn**2
        y_inv = np.sqrt(x_pos)
        ax.plot(x_nn, y, "b-", lw=2, label="f(x) = x²")
        ax.plot(x_pos, y_inv, "r-", lw=2, label="f⁻¹(x) = √x")
    elif func_choice == "f(x) = eˣ":
        y = np.exp(x)
        y_inv = np.log(x_pos)
        ax.plot(x, y, "b-", lw=2, label="f(x) = eˣ")
        ax.plot(x_pos, y_inv, "r-", lw=2, label="f⁻¹(x) = ln(x)")
    else:
        y = np.log(x_pos)
        y_inv = np.exp(x)
        ax.plot(x_pos, y, "b-", lw=2, label="f(x) = ln(x)")
        ax.plot(x, y_inv, "r-", lw=2, label="f⁻¹(x) = eˣ")

    ax.axhline(0, color="k", lw=0.5)
    ax.axvline(0, color="k", lw=0.5)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Function & Its Inverse (reflection in y = x)")
    ax.legend()
    ax.grid(True, alpha=0.25)
    ax.set_aspect("equal")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("**Key property:** f(f⁻¹(x)) = x and f⁻¹(f(x)) = x. The graph of f⁻¹ is a reflection of f in the line y = x.")


def _partial_fractions():
    st.latex(r"\frac{px + q}{(ax+b)(cx+d)} = \frac{A}{ax+b} + \frac{B}{cx+d}")

    with st.sidebar.expander("Partial Fractions Controls", expanded=True):
        p = st.number_input("Numerator: p (coefficient of x)", -10.0, 10.0, 3.0, step=1.0)
        q = st.number_input("Numerator: q (constant)", -10.0, 10.0, 5.0, step=1.0)
        a_val = st.number_input("Denominator factor 1: a", -5.0, 5.0, 1.0, step=1.0, key="pf_a")
        b_val = st.number_input("Denominator factor 1: b", -10.0, 10.0, 1.0, step=1.0, key="pf_b")
        c_val = st.number_input("Denominator factor 2: c", -5.0, 5.0, 1.0, step=1.0, key="pf_c")
        d_val = st.number_input("Denominator factor 2: d", -10.0, 10.0, -2.0, step=1.0, key="pf_d")

    # Solve for A and B using cover-up
    root1 = -b_val / a_val if a_val != 0 else 0
    root2 = -d_val / c_val if c_val != 0 else 0

    denom_at_root1 = c_val * root1 + d_val
    denom_at_root2 = a_val * root2 + b_val

    A = (p * root1 + q) / denom_at_root1 if denom_at_root1 != 0 else 0
    B = (p * root2 + q) / denom_at_root2 if denom_at_root2 != 0 else 0

    st.success(f"**A = {A:.3f}, B = {B:.3f}**")

    x = np.linspace(-5, 5, 1000)
    denom1 = a_val * x + b_val
    denom2 = c_val * x + d_val
    full = np.where(np.abs(denom1 * denom2) > 0.01, (p * x + q) / (denom1 * denom2), np.nan)
    part = np.where(np.abs(denom1) > 0.01, A / denom1, np.nan) + np.where(np.abs(denom2) > 0.01, B / denom2, np.nan)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, full, "b-", lw=2, label="Original fraction", alpha=0.7)
    ax.plot(x, part, "r--", lw=2, label="Sum of partial fractions")
    ax.axhline(0, color="k", lw=0.5)
    ax.set_ylim(-10, 10)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Partial Fractions Verification")
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
