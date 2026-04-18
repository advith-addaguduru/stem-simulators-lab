"""
Grade 6 — Forces & Motion Basics
Cambridge Lower Secondary Science (Stage 7)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("🚀 Forces & Motion Basics")
    st.markdown("_Explore how forces make things move, stop, and change direction._")

    mode = st.selectbox(
        "Choose an activity",
        ["Speed Calculator", "Force & Acceleration", "Friction Explorer"],
    )

    if mode == "Speed Calculator":
        st.subheader("🏎️ Speed Calculator")
        st.latex(r"\text{Speed} = \frac{\text{Distance}}{\text{Time}}")

        col1, col2 = st.columns(2)
        with col1:
            distance = st.slider("Distance (metres)", 1, 500, 100, step=10)
        with col2:
            time_val = st.slider("Time (seconds)", 1, 60, 10, step=1)

        speed = distance / time_val

        st.metric("Speed", f"{speed:.1f} m/s")
        st.caption(f"That's about {speed * 3.6:.1f} km/h!")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        t = np.linspace(0, time_val, 100)
        d = speed * t
        ax1.plot(t, d, linewidth=2, color="#2563eb")
        ax1.fill_between(t, d, alpha=0.1, color="#2563eb")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Distance (m)")
        ax1.set_title("Distance–Time Graph")
        ax1.grid(True, alpha=0.3)

        time_options = [t_val for t_val in [5, 10, 20, 30, 60] if t_val <= 60]
        speeds = [distance / t_val for t_val in time_options]
        ax2.bar(
            [f"{t_val}s" for t_val in time_options],
            speeds,
            color="#60a5fa",
            edgecolor="#2563eb",
        )
        ax2.set_ylabel("Speed (m/s)")
        ax2.set_title(f"Speed for {distance} m at different times")
        ax2.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info("💡 **Did you know?** A cheetah runs at about 30 m/s — the fastest land animal!")

    elif mode == "Force & Acceleration":
        st.subheader("💪 Force & Acceleration")
        st.latex(r"F = m \times a")
        st.markdown(
            "A **force** causes a mass to **accelerate** (speed up, slow down, or change direction)."
        )

        col1, col2 = st.columns(2)
        with col1:
            mass = st.slider("Mass (kg)", 1, 100, 10, step=1)
        with col2:
            force = st.slider("Applied Force (N)", 0, 500, 50, step=10)

        acceleration = force / max(mass, 1)

        c1, c2, c3 = st.columns(3)
        c1.metric("Force", f"{force} N")
        c2.metric("Mass", f"{mass} kg")
        c3.metric("Acceleration", f"{acceleration:.2f} m/s²")

        fig, ax = plt.subplots(figsize=(8, 4))
        masses = np.linspace(1, 100, 50)
        accs = force / masses
        ax.plot(masses, accs, linewidth=2, color="#2563eb")
        ax.scatter(
            [mass], [acceleration], color="red", s=100, zorder=5,
            label=f"Your object ({mass} kg)",
        )
        ax.set_xlabel("Mass (kg)")
        ax.set_ylabel("Acceleration (m/s²)")
        ax.set_title(f"Acceleration vs Mass for {force} N force")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info("💡 **Tip:** Increasing mass decreases acceleration for the same force!")

    elif mode == "Friction Explorer":
        st.subheader("🏔️ Friction Explorer")
        st.markdown(
            "**Friction** is a force that opposes motion. Different surfaces have different friction."
        )

        surface = st.select_slider(
            "Surface type",
            options=["Ice", "Polished Wood", "Concrete", "Grass", "Sand"],
        )
        friction_coefficients = {
            "Ice": 0.03, "Polished Wood": 0.2, "Concrete": 0.6,
            "Grass": 0.35, "Sand": 0.5,
        }
        mu = friction_coefficients[surface]

        mass = st.slider("Object mass (kg)", 1, 50, 10, step=1, key="friction_mass")
        applied_force = st.slider("Push force (N)", 0, 200, 50, step=5)

        g = 9.81
        friction_force = mu * mass * g
        net_force = max(applied_force - friction_force, 0)
        acceleration = net_force / mass if net_force > 0 else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Friction Force", f"{friction_force:.1f} N")
        c2.metric("Net Force", f"{net_force:.1f} N")
        c3.metric("Acceleration", f"{acceleration:.2f} m/s²")

        if net_force == 0:
            st.warning("⚠️ Friction is too strong! The object doesn't move. Push harder!")
        else:
            st.success(f"✅ The object accelerates at {acceleration:.2f} m/s²")

        fig, ax = plt.subplots(figsize=(8, 4))
        surfaces = list(friction_coefficients.keys())
        forces = [friction_coefficients[s] * mass * g for s in surfaces]
        colors = ["#60a5fa" if s != surface else "#ef4444" for s in surfaces]

        ax.barh(surfaces, forces, color=colors, edgecolor="#1e3a5f")
        ax.axvline(
            x=applied_force, color="#22c55e", linestyle="--", linewidth=2,
            label=f"Your push: {applied_force} N",
        )
        ax.set_xlabel("Friction Force (N)")
        ax.set_title(f"Friction forces for a {mass} kg object")
        ax.legend()
        ax.grid(True, alpha=0.3, axis="x")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info(
            "💡 **Real world:** Car brakes use friction to stop. "
            "Ice has very low friction — that's why ice skating is slippery!"
        )
