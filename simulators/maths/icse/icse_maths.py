"""ICSE Maths: Algebra, Geometry & Statistics Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Mathematics — ICSE Grade 10-12")

    mode = st.radio(
        "Select topic",
        ["Quadratic Equations", "Circle Geometry", "Statistics & Probability"],
        horizontal=True,
    )

    if mode == "Quadratic Equations":
        _quadratics()
    elif mode == "Circle Geometry":
        _circle_geometry()
    else:
        _statistics()


def _quadratics():
    st.latex(r"ax^2 + bx + c = 0 \quad;\quad x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")

    with st.sidebar.expander("Quadratic Controls", expanded=True):
        a = st.slider("a", -5.0, 5.0, 1.0, step=0.5, key="icse_qa")
        b = st.slider("b", -10.0, 10.0, -3.0, step=0.5, key="icse_qb")
        c = st.slider("c", -10.0, 10.0, 2.0, step=0.5, key="icse_qc")

    if a == 0:
        st.warning("a cannot be zero for a quadratic.")
        return

    x = np.linspace(-10, 10, 500)
    y = a * x**2 + b * x + c
    disc = b**2 - 4 * a * c
    vx = -b / (2 * a)
    vy = a * vx**2 + b * vx + c

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, "b-", lw=2, label=f"y = {a}x² + {b}x + {c}")
    ax.axhline(0, color="k", lw=0.5)
    ax.axvline(0, color="k", lw=0.5)
    ax.scatter([vx], [vy], color="red", s=120, zorder=3, label=f"Vertex ({vx:.2f}, {vy:.2f})")

    root_info = ""
    if disc > 0:
        r1 = (-b + np.sqrt(disc)) / (2 * a)
        r2 = (-b - np.sqrt(disc)) / (2 * a)
        ax.scatter([r1, r2], [0, 0], color="green", s=100, zorder=3)
        ax.annotate(f"x={r1:.2f}", (r1, 0), textcoords="offset points", xytext=(5, 10), fontsize=9)
        ax.annotate(f"x={r2:.2f}", (r2, 0), textcoords="offset points", xytext=(5, 10), fontsize=9)
        root_info = f"Two real roots: x = {r1:.4f} and x = {r2:.4f}"
    elif disc == 0:
        r = -b / (2 * a)
        ax.scatter([r], [0], color="green", s=100, zorder=3)
        root_info = f"Repeated root: x = {r:.4f}"
    else:
        root_info = "No real roots (discriminant < 0)"

    ax.set_xlim(-10, 10)
    ax.set_ylim(min(-10, vy - 5), max(10, vy + 5))
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Quadratic Function")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**Discriminant:** Δ = b² − 4ac = {disc:.2f}  
**{root_info}**  
**Sum of roots:** −b/a = {-b/a:.4f}  
**Product of roots:** c/a = {c/a:.4f}
""")


def _circle_geometry():
    st.latex(r"(x - h)^2 + (y - k)^2 = r^2 \quad;\quad A = \pi r^2 \quad;\quad C = 2\pi r")

    with st.sidebar.expander("Circle Controls", expanded=True):
        h = st.slider("Centre x (h)", -5.0, 5.0, 0.0, step=0.5, key="icse_ch")
        k = st.slider("Centre y (k)", -5.0, 5.0, 0.0, step=0.5, key="icse_ck")
        r = st.slider("Radius r", 0.5, 5.0, 3.0, step=0.5, key="icse_cr")
        show_tangent = st.checkbox("Show tangent at a point", value=True)
        if show_tangent:
            t_angle = st.slider("Tangent point angle (°)", 0, 360, 45, step=15)

    area = np.pi * r**2
    circumference = 2 * np.pi * r

    col1, col2, col3 = st.columns(3)
    col1.metric("Area", f"{area:.2f}")
    col2.metric("Circumference", f"{circumference:.2f}")
    col3.metric("Equation", f"(x−{h})²+(y−{k})²={r**2:.1f}")

    theta = np.linspace(0, 2 * np.pi, 200)
    cx = h + r * np.cos(theta)
    cy = k + r * np.sin(theta)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(cx, cy, "b-", lw=2, label=f"r = {r}")
    ax.scatter([h], [k], color="red", s=80, zorder=3, label=f"Centre ({h}, {k})")

    if show_tangent:
        t_rad = np.radians(t_angle)
        px = h + r * np.cos(t_rad)
        py = k + r * np.sin(t_rad)
        ax.scatter([px], [py], color="green", s=80, zorder=3, label=f"Point ({px:.2f}, {py:.2f})")

        # Tangent line (perpendicular to radius)
        tang_dx = -np.sin(t_rad)
        tang_dy = np.cos(t_rad)
        t_len = 3
        ax.plot([px - t_len * tang_dx, px + t_len * tang_dx],
                [py - t_len * tang_dy, py + t_len * tang_dy],
                "g--", lw=1.5, label="Tangent")
        # Radius to point
        ax.plot([h, px], [k, py], "r--", lw=1, alpha=0.5)

    lim = max(abs(h) + r, abs(k) + r) + 2
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.axhline(0, color="k", lw=0.5)
    ax.axvline(0, color="k", lw=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Circle Geometry")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _statistics():
    st.latex(r"\bar{x} = \frac{\sum x_i}{n} \quad;\quad \sigma = \sqrt{\frac{\sum(x_i - \bar{x})^2}{n}}")

    with st.sidebar.expander("Statistics Controls", expanded=True):
        data_type = st.selectbox("Data set", ["Custom", "Exam Scores", "Heights"])
        if data_type == "Custom":
            data_str = st.text_input("Enter data (comma-separated)", "5, 8, 12, 15, 7, 10, 9, 11, 13, 6")
            try:
                data = [float(x.strip()) for x in data_str.split(",")]
            except ValueError:
                st.error("Invalid input. Enter comma-separated numbers.")
                return
        elif data_type == "Exam Scores":
            data = [45, 62, 78, 85, 91, 55, 72, 68, 88, 73, 60, 82, 77, 95, 50]
        else:
            data = [155, 162, 170, 158, 175, 168, 160, 172, 165, 180, 163, 177, 169, 171, 166]

    data = np.array(data)
    n = len(data)
    mean = np.mean(data)
    median = np.median(data)
    std = np.std(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean", f"{mean:.2f}")
    col2.metric("Median", f"{median:.2f}")
    col3.metric("Std Dev", f"{std:.2f}")
    col4.metric("IQR", f"{iqr:.2f}")

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    axes[0].hist(data, bins="auto", color="#3498db", alpha=0.8, edgecolor="black")
    axes[0].axvline(mean, color="red", linestyle="--", lw=2, label=f"Mean = {mean:.1f}")
    axes[0].axvline(median, color="green", linestyle="--", lw=2, label=f"Median = {median:.1f}")
    axes[0].set_xlabel("Value")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("Histogram")
    axes[0].legend(fontsize=7)
    axes[0].grid(True, alpha=0.25, axis="y")

    axes[1].boxplot(data, vert=True)
    axes[1].set_ylabel("Value")
    axes[1].set_title("Box Plot")
    axes[1].grid(True, alpha=0.25, axis="y")

    sorted_data = np.sort(data)
    cumulative = np.arange(1, n + 1) / n * 100
    axes[2].plot(sorted_data, cumulative, "bo-", lw=2, markersize=4)
    axes[2].set_xlabel("Value")
    axes[2].set_ylabel("Cumulative %")
    axes[2].set_title("Cumulative Frequency")
    axes[2].grid(True, alpha=0.25)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**Summary Statistics:**
- n = {n}, Range = {np.ptp(data):.2f}
- Q1 = {q1:.2f}, Q3 = {q3:.2f}, IQR = {iqr:.2f}
- Variance = {std**2:.2f}
""")
