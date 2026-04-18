"""Vectors & 3D Geometry — Advanced Pack (Grades 11–12)."""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("📐 Vectors & 3D Geometry")

    tab1, tab2, tab3 = st.tabs(["Vector Operations", "Dot & Cross Product", "Lines & Planes"])

    with tab1:
        st.markdown("Add, subtract, and scale 3D vectors.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Vector a**")
            ax = st.slider("aₓ", -10.0, 10.0, 3.0, 0.5, key="ax")
            ay = st.slider("aᵧ", -10.0, 10.0, 4.0, 0.5, key="ay")
            az = st.slider("a_z", -10.0, 10.0, 0.0, 0.5, key="az")
        with c2:
            st.markdown("**Vector b**")
            bx = st.slider("bₓ", -10.0, 10.0, -2.0, 0.5, key="bx")
            by = st.slider("bᵧ", -10.0, 10.0, 5.0, 0.5, key="by")
            bz = st.slider("b_z", -10.0, 10.0, 0.0, 0.5, key="bz")

        a = np.array([ax, ay, az])
        b = np.array([bx, by, bz])
        a_plus_b = a + b
        a_minus_b = a - b

        c1, c2, c3 = st.columns(3)
        c1.metric("|a|", f"{np.linalg.norm(a):.2f}")
        c2.metric("|b|", f"{np.linalg.norm(b):.2f}")
        c3.metric("|a + b|", f"{np.linalg.norm(a_plus_b):.2f}")

        # 2D projection plot (XY plane)
        fig, ax_plot = plt.subplots(figsize=(6, 6))
        origin = [0, 0]
        ax_plot.quiver(*origin, ax, ay, angles="xy", scale_units="xy", scale=1,
                       color="blue", label="a", width=0.015)
        ax_plot.quiver(*origin, bx, by, angles="xy", scale_units="xy", scale=1,
                       color="red", label="b", width=0.015)
        ax_plot.quiver(*origin, a_plus_b[0], a_plus_b[1], angles="xy", scale_units="xy",
                       scale=1, color="green", label="a + b", width=0.015)

        all_coords = [ax, ay, bx, by, a_plus_b[0], a_plus_b[1]]
        lim = max(abs(v) for v in all_coords) + 2
        ax_plot.set_xlim(-lim, lim)
        ax_plot.set_ylim(-lim, lim)
        ax_plot.set_aspect("equal")
        ax_plot.grid(True, alpha=0.3)
        ax_plot.axhline(0, color="black", linewidth=0.5)
        ax_plot.axvline(0, color="black", linewidth=0.5)
        ax_plot.legend()
        ax_plot.set_title("XY Plane Projection")
        st.pyplot(fig)
        plt.close(fig)

        st.markdown(
            f"**a + b** = ({a_plus_b[0]:.1f}, {a_plus_b[1]:.1f}, {a_plus_b[2]:.1f})  \n"
            f"**a − b** = ({a_minus_b[0]:.1f}, {a_minus_b[1]:.1f}, {a_minus_b[2]:.1f})"
        )

    with tab2:
        st.markdown("Compute dot product and cross product of two 3D vectors.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Vector u**")
            ux = st.number_input("uₓ", value=1.0, key="ux")
            uy = st.number_input("uᵧ", value=2.0, key="uy")
            uz = st.number_input("u_z", value=3.0, key="uz")
        with c2:
            st.markdown("**Vector v**")
            vx = st.number_input("vₓ", value=4.0, key="vx")
            vy = st.number_input("vᵧ", value=-1.0, key="vy")
            vz = st.number_input("v_z", value=2.0, key="vz")

        u = np.array([ux, uy, uz])
        v = np.array([vx, vy, vz])

        dot = np.dot(u, v)
        cross = np.cross(u, v)
        mag_u = np.linalg.norm(u)
        mag_v = np.linalg.norm(v)

        if mag_u > 0 and mag_v > 0:
            cos_angle = np.clip(dot / (mag_u * mag_v), -1, 1)
            angle_rad = np.arccos(cos_angle)
            angle_deg = np.degrees(angle_rad)
        else:
            angle_deg = 0.0

        c1, c2, c3 = st.columns(3)
        c1.metric("u · v", f"{dot:.2f}")
        c2.metric("u × v", f"({cross[0]:.1f}, {cross[1]:.1f}, {cross[2]:.1f})")
        c3.metric("Angle", f"{angle_deg:.1f}°")

        area = np.linalg.norm(cross)
        st.metric("Parallelogram area |u × v|", f"{area:.2f}")

        st.latex(r"\mathbf{u} \cdot \mathbf{v} = |\mathbf{u}||\mathbf{v}|\cos\theta")
        st.latex(r"|\mathbf{u} \times \mathbf{v}| = |\mathbf{u}||\mathbf{v}|\sin\theta")

    with tab3:
        st.markdown("Equation of a line and distance from a point to a plane.")

        st.markdown("#### Line: **r** = **a** + t**d**")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("Point **a**")
            la = st.number_input("x₀", value=1.0, key="la")
            lb = st.number_input("y₀", value=2.0, key="lb")
            lc = st.number_input("z₀", value=3.0, key="lc")
        with c2:
            st.markdown("Direction **d**")
            da = st.number_input("dₓ", value=2.0, key="da")
            db = st.number_input("dᵧ", value=-1.0, key="db")
            dc = st.number_input("d_z", value=1.0, key="dc")

        st.markdown(
            f"**r** = ({la}, {lb}, {lc}) + t({da}, {db}, {dc})"
        )

        st.markdown("---")
        st.markdown("#### Plane: n₁x + n₂y + n₃z = d")
        c1, c2 = st.columns(2)
        with c1:
            n1 = st.number_input("n₁", value=1.0, key="n1")
            n2 = st.number_input("n₂", value=1.0, key="n2")
            n3 = st.number_input("n₃", value=1.0, key="n3")
        with c2:
            d_val = st.number_input("d", value=6.0, key="d_plane")
            px = st.number_input("Point x", value=0.0, key="px")
            py_val = st.number_input("Point y", value=0.0, key="py_val")
            pz = st.number_input("Point z", value=0.0, key="pz")

        normal = np.array([n1, n2, n3])
        point = np.array([px, py_val, pz])
        mag_n = np.linalg.norm(normal)

        if mag_n > 0:
            dist = abs(np.dot(normal, point) - d_val) / mag_n
            st.metric("Distance from point to plane", f"{dist:.3f}")
            st.latex(
                r"d = \frac{|n_1 x_0 + n_2 y_0 + n_3 z_0 - d|}{|\mathbf{n}|}"
            )
        else:
            st.warning("Normal vector cannot be zero.")
