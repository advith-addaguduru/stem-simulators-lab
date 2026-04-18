"""
Grade 7 — Geometry & Measurement
Cambridge Lower Secondary Mathematics (Stage 8)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def simulate():
    st.header("📏 Geometry & Measurement")
    st.markdown("_Explore shapes, angles, area, and volume._")

    mode = st.selectbox(
        "Choose an activity",
        ["Area of Shapes", "Angles in Polygons", "Volume of 3D Shapes"],
    )

    if mode == "Area of Shapes":
        st.subheader("📐 Area of Shapes")

        shape = st.radio("Shape", ["Rectangle", "Triangle", "Circle", "Trapezium"], horizontal=True)

        if shape == "Rectangle":
            st.latex(r"A = l \times w")
            col1, col2 = st.columns(2)
            with col1:
                length = st.slider("Length (cm)", 1, 20, 8)
            with col2:
                width = st.slider("Width (cm)", 1, 20, 5)
            area = length * width

            fig, ax = plt.subplots(figsize=(6, 4))
            rect = patches.Rectangle((0, 0), length, width, linewidth=2,
                                     edgecolor="#2563eb", facecolor="#dbeafe")
            ax.add_patch(rect)
            ax.set_xlim(-1, length + 2)
            ax.set_ylim(-1, width + 2)
            ax.set_aspect("equal")
            ax.text(length / 2, -0.5, f"{length} cm", ha="center", fontsize=11)
            ax.text(-0.7, width / 2, f"{width} cm", ha="center", fontsize=11, rotation=90)
            ax.set_title(f"Rectangle — Area = {area} cm²")
            ax.grid(True, alpha=0.2)

        elif shape == "Triangle":
            st.latex(r"A = \frac{1}{2} \times b \times h")
            col1, col2 = st.columns(2)
            with col1:
                base = st.slider("Base (cm)", 1, 20, 10)
            with col2:
                height = st.slider("Height (cm)", 1, 20, 6, key="tri_h")
            area = 0.5 * base * height

            fig, ax = plt.subplots(figsize=(6, 4))
            triangle = plt.Polygon([(0, 0), (base, 0), (base / 2, height)],
                                   facecolor="#dcfce7", edgecolor="#16a34a", lw=2)
            ax.add_patch(triangle)
            ax.plot([base / 2, base / 2], [0, height], "k--", alpha=0.5)
            ax.set_xlim(-1, base + 2)
            ax.set_ylim(-1, height + 2)
            ax.set_aspect("equal")
            ax.text(base / 2, -0.5, f"{base} cm", ha="center", fontsize=11)
            ax.text(base / 2 + 0.3, height / 2, f"{height} cm", fontsize=11)
            ax.set_title(f"Triangle — Area = {area:.1f} cm²")
            ax.grid(True, alpha=0.2)

        elif shape == "Circle":
            st.latex(r"A = \pi r^2")
            radius = st.slider("Radius (cm)", 1, 15, 5)
            area = np.pi * radius ** 2

            fig, ax = plt.subplots(figsize=(6, 6))
            circle = plt.Circle((0, 0), radius, facecolor="#ede9fe", edgecolor="#7c3aed", lw=2)
            ax.add_patch(circle)
            ax.plot([0, radius], [0, 0], "k-", lw=2)
            ax.text(radius / 2, 0.3, f"r = {radius} cm", ha="center", fontsize=11)
            ax.set_xlim(-radius - 2, radius + 2)
            ax.set_ylim(-radius - 2, radius + 2)
            ax.set_aspect("equal")
            ax.set_title(f"Circle — Area = {area:.1f} cm²")
            ax.grid(True, alpha=0.2)

        else:  # Trapezium
            st.latex(r"A = \frac{1}{2}(a + b) \times h")
            col1, col2, col3 = st.columns(3)
            with col1:
                a_top = st.slider("Top side a (cm)", 1, 15, 4)
            with col2:
                b_bot = st.slider("Bottom side b (cm)", 1, 20, 10)
            with col3:
                height = st.slider("Height (cm)", 1, 15, 6, key="trap_h")
            area = 0.5 * (a_top + b_bot) * height

            fig, ax = plt.subplots(figsize=(6, 4))
            offset = (b_bot - a_top) / 2
            trap = plt.Polygon(
                [(offset, height), (offset + a_top, height), (b_bot, 0), (0, 0)],
                facecolor="#fef3c7", edgecolor="#d97706", lw=2,
            )
            ax.add_patch(trap)
            ax.set_xlim(-1, b_bot + 2)
            ax.set_ylim(-1, height + 2)
            ax.set_aspect("equal")
            ax.text(b_bot / 2, -0.5, f"b = {b_bot} cm", ha="center", fontsize=11)
            ax.text(offset + a_top / 2, height + 0.3, f"a = {a_top} cm", ha="center", fontsize=11)
            ax.set_title(f"Trapezium — Area = {area:.1f} cm²")
            ax.grid(True, alpha=0.2)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.metric("Area", f"{area:.1f} cm²")

    elif mode == "Angles in Polygons":
        st.subheader("🔺 Angles in Polygons")
        st.latex(r"\text{Sum of interior angles} = (n - 2) \times 180°")

        n_sides = st.slider("Number of sides (n)", 3, 12, 4)

        angle_sum = (n_sides - 2) * 180
        each_angle = angle_sum / n_sides

        c1, c2, c3 = st.columns(3)
        c1.metric("Sides", n_sides)
        c2.metric("Angle sum", f"{angle_sum}°")
        c3.metric("Each angle (regular)", f"{each_angle:.1f}°")

        names = {3: "Triangle", 4: "Quadrilateral", 5: "Pentagon", 6: "Hexagon",
                 7: "Heptagon", 8: "Octagon", 9: "Nonagon", 10: "Decagon",
                 11: "Hendecagon", 12: "Dodecagon"}

        st.markdown(f"**Shape:** {names.get(n_sides, f'{n_sides}-gon')}")

        fig, ax = plt.subplots(figsize=(6, 6))
        angles = np.linspace(0, 2 * np.pi, n_sides, endpoint=False) + np.pi / 2
        xs = np.cos(angles)
        ys = np.sin(angles)
        polygon = plt.Polygon(list(zip(xs, ys)), facecolor="#dbeafe", edgecolor="#2563eb", lw=2)
        ax.add_patch(polygon)

        for i in range(n_sides):
            ax.text(xs[i] * 1.15, ys[i] * 1.15, f"{each_angle:.0f}°", ha="center",
                    va="center", fontsize=8, color="#2563eb", fontweight="bold")

        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect("equal")
        ax.set_title(f"Regular {names.get(n_sides, f'{n_sides}-gon')}")
        ax.axis("off")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info(f"💡 A regular {names.get(n_sides, 'polygon')} has {n_sides} equal sides and {n_sides} equal angles of {each_angle:.1f}° each.")

    elif mode == "Volume of 3D Shapes":
        st.subheader("📦 Volume of 3D Shapes")

        shape3d = st.radio("Shape", ["Cuboid", "Cylinder", "Sphere", "Cone"], horizontal=True)

        if shape3d == "Cuboid":
            st.latex(r"V = l \times w \times h")
            c1, c2, c3 = st.columns(3)
            with c1:
                l = st.slider("Length (cm)", 1, 15, 5, key="cub_l")
            with c2:
                w = st.slider("Width (cm)", 1, 15, 4, key="cub_w")
            with c3:
                h = st.slider("Height (cm)", 1, 15, 6, key="cub_h")
            volume = l * w * h
            sa = 2 * (l * w + l * h + w * h)

        elif shape3d == "Cylinder":
            st.latex(r"V = \pi r^2 h")
            c1, c2 = st.columns(2)
            with c1:
                r = st.slider("Radius (cm)", 1, 10, 4, key="cyl_r")
            with c2:
                h = st.slider("Height (cm)", 1, 20, 8, key="cyl_h")
            volume = np.pi * r ** 2 * h
            sa = 2 * np.pi * r * (r + h)

        elif shape3d == "Sphere":
            st.latex(r"V = \frac{4}{3}\pi r^3")
            r = st.slider("Radius (cm)", 1, 10, 5, key="sph_r")
            volume = (4 / 3) * np.pi * r ** 3
            sa = 4 * np.pi * r ** 2

        else:  # Cone
            st.latex(r"V = \frac{1}{3}\pi r^2 h")
            c1, c2 = st.columns(2)
            with c1:
                r = st.slider("Radius (cm)", 1, 10, 4, key="cone_r")
            with c2:
                h = st.slider("Height (cm)", 1, 20, 10, key="cone_h")
            volume = (1 / 3) * np.pi * r ** 2 * h
            slant = np.sqrt(r ** 2 + h ** 2)
            sa = np.pi * r * (r + slant)

        c1, c2 = st.columns(2)
        c1.metric("Volume", f"{volume:.1f} cm³")
        c2.metric("Surface Area", f"{sa:.1f} cm²")

        # Comparison chart
        fig, ax = plt.subplots(figsize=(8, 4))
        shapes_data = {
            "Cuboid (5×4×6)": 5 * 4 * 6,
            "Cylinder (r=4,h=8)": np.pi * 16 * 8,
            "Sphere (r=5)": (4 / 3) * np.pi * 125,
            "Cone (r=4,h=10)": (1 / 3) * np.pi * 16 * 10,
        }
        colors = ["#60a5fa", "#34d399", "#a78bfa", "#fbbf24"]

        ax.bar(list(shapes_data.keys()), list(shapes_data.values()), color=colors, edgecolor="#1e3a5f")
        ax.set_ylabel("Volume (cm³)")
        ax.set_title("Volume Comparison of Common 3D Shapes")
        ax.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info("💡 **Challenge:** Which shape holds the most water for the same surface area? (Hint: it's the sphere!)")
