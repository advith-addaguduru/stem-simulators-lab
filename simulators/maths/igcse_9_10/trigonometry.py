"""IGCSE Grades 9-10 Maths: Trigonometry Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Trigonometry")
    st.latex(r"\sin\theta = \frac{\text{opp}}{\text{hyp}} \quad;\quad \cos\theta = \frac{\text{adj}}{\text{hyp}} \quad;\quad \tan\theta = \frac{\text{opp}}{\text{adj}}")

    mode = st.radio(
        "Select topic",
        ["Right-Angle Triangle", "Trig Graphs", "Sine & Cosine Rules"],
        horizontal=True,
    )

    if mode == "Right-Angle Triangle":
        _right_angle()
    elif mode == "Trig Graphs":
        _trig_graphs()
    else:
        _sine_cosine_rules()


def _right_angle():
    with st.sidebar.expander("Triangle Controls", expanded=True):
        angle_deg = st.slider("Angle θ (degrees)", 5, 85, 30)
        hyp = st.slider("Hypotenuse (cm)", 1.0, 20.0, 10.0, step=0.5)

    theta = np.radians(angle_deg)
    opp = hyp * np.sin(theta)
    adj = hyp * np.cos(theta)

    col1, col2, col3 = st.columns(3)
    col1.metric("Opposite", f"{opp:.3f} cm")
    col2.metric("Adjacent", f"{adj:.3f} cm")
    col3.metric("Hypotenuse", f"{hyp:.3f} cm")

    fig, ax = plt.subplots(figsize=(7, 6))
    triangle = plt.Polygon([[0, 0], [adj, 0], [adj, opp]], fill=False, edgecolor="blue", lw=2)
    ax.add_patch(triangle)
    ax.text(adj / 2, -0.5, f"adj = {adj:.2f}", ha="center", fontsize=10, color="green")
    ax.text(adj + 0.3, opp / 2, f"opp = {opp:.2f}", ha="left", fontsize=10, color="red")
    ax.text(adj / 2 - 0.5, opp / 2 + 0.3, f"hyp = {hyp:.2f}", ha="center", fontsize=10, color="blue", rotation=angle_deg)
    ax.text(1.0, 0.3, f"θ = {angle_deg}°", fontsize=12, color="purple")
    ax.set_xlim(-1, max(adj, hyp) + 2)
    ax.set_ylim(-1, max(opp, hyp) + 1)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)
    ax.set_title("Right-Angle Triangle")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""
**Trigonometric ratios for θ = {angle_deg}°:**
- sin({angle_deg}°) = {np.sin(theta):.4f}
- cos({angle_deg}°) = {np.cos(theta):.4f}
- tan({angle_deg}°) = {np.tan(theta):.4f}
""")


def _trig_graphs():
    with st.sidebar.expander("Trig Graph Controls", expanded=True):
        func = st.multiselect("Functions", ["sin(x)", "cos(x)", "tan(x)"], default=["sin(x)"])
        amplitude = st.slider("Amplitude A", 0.5, 3.0, 1.0, step=0.5)
        period_factor = st.slider("Period factor (1/n)", 0.5, 3.0, 1.0, step=0.5)
        x_range = st.slider("x range (degrees)", 180, 720, 360, step=90)

    x_deg = np.linspace(0, x_range, 1000)
    x_rad = np.radians(x_deg)

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = {"sin(x)": "#3498db", "cos(x)": "#e74c3c", "tan(x)": "#2ecc71"}

    for f in func:
        if f == "sin(x)":
            y = amplitude * np.sin(period_factor * x_rad)
        elif f == "cos(x)":
            y = amplitude * np.cos(period_factor * x_rad)
        else:
            y = amplitude * np.tan(period_factor * x_rad)
            y = np.where(np.abs(y) > 10, np.nan, y)
        ax.plot(x_deg, y, lw=2, label=f"y = {amplitude}·{f.replace('x', f'{period_factor}x')}", color=colors[f])

    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel("Angle (degrees)")
    ax.set_ylabel("y")
    ax.set_title("Trigonometric Functions")
    ax.legend()
    ax.grid(True, alpha=0.25)
    if "tan(x)" in func:
        ax.set_ylim(-10, 10)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _sine_cosine_rules():
    st.latex(r"\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C}")
    st.latex(r"a^2 = b^2 + c^2 - 2bc\cos A")

    with st.sidebar.expander("Triangle Controls", expanded=True):
        b = st.slider("Side b (cm)", 1.0, 20.0, 8.0, step=0.5)
        c = st.slider("Side c (cm)", 1.0, 20.0, 6.0, step=0.5)
        A_deg = st.slider("Included angle A (degrees)", 10, 170, 60)

    A_rad = np.radians(A_deg)
    a = np.sqrt(b**2 + c**2 - 2 * b * c * np.cos(A_rad))

    sin_B = b * np.sin(A_rad) / a
    sin_B = np.clip(sin_B, -1, 1)
    B_deg = np.degrees(np.arcsin(sin_B))
    C_deg = 180 - A_deg - B_deg

    col1, col2, col3 = st.columns(3)
    col1.metric("Side a", f"{a:.3f} cm")
    col2.metric("Angle B", f"{B_deg:.1f}°")
    col3.metric("Angle C", f"{C_deg:.1f}°")

    # Draw triangle
    Ax, Ay = 0, 0
    Bx, By = c, 0
    Cx, Cy = b * np.cos(A_rad), b * np.sin(A_rad)

    fig, ax = plt.subplots(figsize=(8, 6))
    triangle = plt.Polygon([[Ax, Ay], [Bx, By], [Cx, Cy]], fill=False, edgecolor="blue", lw=2)
    ax.add_patch(triangle)
    ax.scatter([Ax, Bx, Cx], [Ay, By, Cy], color="red", s=80, zorder=3)
    ax.text(Ax - 0.5, Ay - 0.5, f"A={A_deg}°", fontsize=10, color="purple")
    ax.text(Bx + 0.3, By - 0.5, f"B={B_deg:.1f}°", fontsize=10, color="purple")
    ax.text(Cx + 0.3, Cy + 0.3, f"C={C_deg:.1f}°", fontsize=10, color="purple")
    ax.text((Ax + Bx) / 2, (Ay + By) / 2 - 0.7, f"c={c}", ha="center", fontsize=10)
    ax.text((Ax + Cx) / 2 - 0.7, (Ay + Cy) / 2, f"b={b}", ha="center", fontsize=10)
    ax.text((Bx + Cx) / 2 + 0.5, (By + Cy) / 2, f"a={a:.2f}", ha="center", fontsize=10)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)
    ax.set_title("Non-Right Triangle (Sine & Cosine Rules)")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    area = 0.5 * b * c * np.sin(A_rad)
    st.markdown(f"**Area = ½ × b × c × sin(A) = {area:.3f} cm²**")
