"""IGCSE Grades 9-10 Maths: Functions & Graphs Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Functions & Graphs")
    st.latex(r"y = f(x) \quad;\quad \text{Domain} \rightarrow \text{Range}")

    mode = st.radio(
        "Select topic",
        ["Linear & Quadratic", "Cubic & Reciprocal", "Graph Transformations"],
        horizontal=True,
    )

    if mode == "Linear & Quadratic":
        _linear_quadratic()
    elif mode == "Cubic & Reciprocal":
        _cubic_reciprocal()
    else:
        _transformations()


def _linear_quadratic():
    st.latex(r"y = ax^2 + bx + c \quad;\quad x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}")

    with st.sidebar.expander("Quadratic Controls", expanded=True):
        a = st.slider("a (coefficient of x²)", -5.0, 5.0, 1.0, step=0.5)
        b = st.slider("b (coefficient of x)", -10.0, 10.0, 0.0, step=0.5)
        c = st.slider("c (constant)", -10.0, 10.0, -4.0, step=0.5)

    x = np.linspace(-10, 10, 500)
    y = a * x**2 + b * x + c

    discriminant = b**2 - 4 * a * c
    vertex_x = -b / (2 * a) if a != 0 else 0
    vertex_y = a * vertex_x**2 + b * vertex_x + c

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, "b-", lw=2, label=f"y = {a}x² + {b}x + {c}")
    ax.axhline(0, color="k", lw=0.5)
    ax.axvline(0, color="k", lw=0.5)
    ax.scatter([vertex_x], [vertex_y], color="red", s=100, zorder=3, label=f"Vertex ({vertex_x:.2f}, {vertex_y:.2f})")

    if discriminant >= 0 and a != 0:
        r1 = (-b + np.sqrt(discriminant)) / (2 * a)
        r2 = (-b - np.sqrt(discriminant)) / (2 * a)
        ax.scatter([r1, r2], [0, 0], color="green", s=100, zorder=3, label=f"Roots: {r1:.2f}, {r2:.2f}")

    ax.set_xlim(-10, 10)
    ax.set_ylim(-15, 15)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Quadratic Function")
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    if a != 0:
        st.markdown(f"""
**Vertex:** ({vertex_x:.2f}, {vertex_y:.2f})  
**Discriminant:** b² − 4ac = {discriminant:.2f}  
**Roots:** {"Two real roots" if discriminant > 0 else "One repeated root" if discriminant == 0 else "No real roots"}  
**Shape:** {"U-shaped (minimum)" if a > 0 else "∩-shaped (maximum)"}
""")


def _cubic_reciprocal():
    with st.sidebar.expander("Function Controls", expanded=True):
        func_type = st.selectbox("Function type", ["Cubic: y = ax³ + d", "Reciprocal: y = a/x + d"])
        a = st.slider("a", -3.0, 3.0, 1.0, step=0.5, key="cr_a")
        d = st.slider("d (vertical shift)", -5.0, 5.0, 0.0, step=0.5, key="cr_d")

    x = np.linspace(-5, 5, 500)

    fig, ax = plt.subplots(figsize=(8, 6))

    if "Cubic" in func_type:
        y = a * x**3 + d
        ax.plot(x, y, "b-", lw=2, label=f"y = {a}x³ + {d}")
        ax.set_ylim(-30, 30)
    else:
        x_pos = x[x > 0.1]
        x_neg = x[x < -0.1]
        y_pos = a / x_pos + d
        y_neg = a / x_neg + d
        ax.plot(x_pos, y_pos, "b-", lw=2, label=f"y = {a}/x + {d}")
        ax.plot(x_neg, y_neg, "b-", lw=2)
        ax.axhline(d, color="gray", linestyle="--", alpha=0.5, label=f"Asymptote y = {d}")
        ax.axvline(0, color="gray", linestyle="--", alpha=0.5)
        ax.set_ylim(-15, 15)

    ax.axhline(0, color="k", lw=0.5)
    ax.axvline(0, color="k", lw=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(func_type.split(":")[0] + " Function")
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _transformations():
    st.latex(r"y = f(x) \rightarrow y = af(x+b) + c")

    with st.sidebar.expander("Transformation Controls", expanded=True):
        base = st.selectbox("Base function f(x)", ["x²", "sin(x)", "|x|"])
        a_scale = st.slider("Vertical stretch a", -3.0, 3.0, 1.0, step=0.5)
        h_shift = st.slider("Horizontal shift b", -5.0, 5.0, 0.0, step=0.5)
        v_shift = st.slider("Vertical shift c", -5.0, 5.0, 0.0, step=0.5)

    x = np.linspace(-10, 10, 500)

    if base == "x²":
        y_orig = x**2
        y_trans = a_scale * (x + h_shift) ** 2 + v_shift
    elif base == "sin(x)":
        y_orig = np.sin(x)
        y_trans = a_scale * np.sin(x + h_shift) + v_shift
    else:
        y_orig = np.abs(x)
        y_trans = a_scale * np.abs(x + h_shift) + v_shift

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y_orig, "b--", lw=1.5, alpha=0.5, label=f"Original: y = {base}")
    ax.plot(x, y_trans, "r-", lw=2, label=f"Transformed")
    ax.axhline(0, color="k", lw=0.5)
    ax.axvline(0, color="k", lw=0.5)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Graph Transformations")
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**Transformations applied:**
- Vertical stretch: **×{a_scale}** {'(reflected in x-axis)' if a_scale < 0 else ''}
- Horizontal shift: **{-h_shift:+.1f}** units {'right' if h_shift < 0 else 'left' if h_shift > 0 else ''}
- Vertical shift: **{v_shift:+.1f}** units {'up' if v_shift > 0 else 'down' if v_shift < 0 else ''}
""")
