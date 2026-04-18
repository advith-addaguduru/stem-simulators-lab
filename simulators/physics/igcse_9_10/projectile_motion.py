"""Projectile Motion — Core STEM Pack (Grades 9–10)."""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("🎯 Projectile Motion")

    tab1, tab2 = st.tabs(["Trajectory", "Range vs Angle"])

    with tab1:
        st.markdown("Launch a projectile and trace its parabolic path.")
        c1, c2, c3 = st.columns(3)
        v0 = c1.slider("Launch speed (m/s)", 5.0, 100.0, 30.0, 1.0)
        angle_deg = c2.slider("Launch angle (°)", 5.0, 85.0, 45.0, 1.0)
        g = c3.slider("Gravity (m/s²)", 1.0, 20.0, 9.81, 0.01)

        angle = np.radians(angle_deg)
        t_flight = 2 * v0 * np.sin(angle) / g
        max_height = (v0 * np.sin(angle)) ** 2 / (2 * g)
        horiz_range = v0**2 * np.sin(2 * angle) / g

        t = np.linspace(0, t_flight, 300)
        x = v0 * np.cos(angle) * t
        y = v0 * np.sin(angle) * t - 0.5 * g * t**2

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x, y, "b-", linewidth=2)
        ax.set_xlabel("Horizontal distance (m)")
        ax.set_ylabel("Height (m)")
        ax.set_title("Projectile Trajectory")
        ax.set_ylim(bottom=0)
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)

        m1, m2, m3 = st.columns(3)
        m1.metric("Range", f"{horiz_range:.1f} m")
        m2.metric("Max Height", f"{max_height:.1f} m")
        m3.metric("Flight Time", f"{t_flight:.2f} s")

        st.latex(r"x = v_0 \cos\theta \cdot t \qquad y = v_0 \sin\theta \cdot t - \tfrac{1}{2}g t^2")

    with tab2:
        st.markdown("See how launch angle affects horizontal range.")
        v_fixed = st.slider("Speed (m/s)", 10.0, 80.0, 40.0, 1.0, key="v_range")
        g2 = 9.81
        angles = np.linspace(0, 90, 200)
        ranges = v_fixed**2 * np.sin(2 * np.radians(angles)) / g2

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.plot(angles, ranges, "r-", linewidth=2)
        ax2.axvline(45, color="gray", linestyle="--", alpha=0.5, label="45°")
        ax2.set_xlabel("Launch Angle (°)")
        ax2.set_ylabel("Range (m)")
        ax2.set_title("Range vs Launch Angle")
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)
        plt.close(fig2)

        st.info("Maximum range occurs at **45°** (when launch and landing heights are equal).")
