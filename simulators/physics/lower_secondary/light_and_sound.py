"""
Grade 8 — Light & Sound Waves
Cambridge Lower Secondary Science (Stage 9)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("🌊 Light & Sound Waves")
    st.markdown("_Investigate how light reflects, refracts, and how sound travels._")

    mode = st.selectbox(
        "Choose an activity",
        ["Reflection — Mirror Angles", "Refraction — Bending Light", "Sound Waves — Frequency & Pitch"],
    )

    if mode == "Reflection — Mirror Angles":
        st.subheader("🪞 Reflection — Law of Reflection")
        st.latex(r"\theta_i = \theta_r")
        st.markdown("The **angle of incidence** always equals the **angle of reflection**.")

        angle = st.slider("Angle of incidence (°)", 0, 85, 45, step=5)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axhline(y=0, color="#64748b", linewidth=3, label="Mirror")
        ax.plot([0, 0], [0, 5], "k--", alpha=0.5, label="Normal")

        angle_rad = np.radians(angle)
        x_inc = -5 * np.sin(angle_rad)
        y_inc = 5 * np.cos(angle_rad)
        ax.annotate(
            "", xy=(0, 0), xytext=(x_inc, y_inc),
            arrowprops=dict(arrowstyle="->", color="#ef4444", lw=2),
        )

        x_ref = 5 * np.sin(angle_rad)
        y_ref = 5 * np.cos(angle_rad)
        ax.annotate(
            "", xy=(x_ref, y_ref), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=2),
        )

        if angle > 0:
            theta = np.linspace(np.pi / 2 - angle_rad, np.pi / 2, 30)
            ax.plot(1.5 * np.cos(theta), 1.5 * np.sin(theta), color="#ef4444", lw=1.5)
            ax.text(-0.8, 1.8, f"θᵢ = {angle}°", color="#ef4444", fontsize=11)

            theta2 = np.linspace(np.pi / 2, np.pi / 2 + angle_rad, 30)
            ax.plot(1.5 * np.cos(theta2), 1.5 * np.sin(theta2), color="#3b82f6", lw=1.5)
            ax.text(0.3, 1.8, f"θᵣ = {angle}°", color="#3b82f6", fontsize=11)

        ax.set_xlim(-6, 6)
        ax.set_ylim(-1, 6)
        ax.set_aspect("equal")
        ax.legend(loc="upper right")
        ax.set_title("Law of Reflection")
        ax.grid(True, alpha=0.2)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.success(f"✅ Angle of incidence = {angle}° → Angle of reflection = {angle}°")
        st.info("💡 **Real world:** This is how mirrors, periscopes, and kaleidoscopes work!")

    elif mode == "Refraction — Bending Light":
        st.subheader("🔦 Refraction — Snell's Law")
        st.latex(r"n_1 \sin\theta_1 = n_2 \sin\theta_2")

        medium = st.selectbox(
            "Second medium",
            ["Water (n = 1.33)", "Glass (n = 1.50)", "Diamond (n = 2.42)"],
        )
        n_values = {
            "Water (n = 1.33)": 1.33,
            "Glass (n = 1.50)": 1.50,
            "Diamond (n = 2.42)": 2.42,
        }
        n2 = n_values[medium]
        n1 = 1.0  # Air

        angle1 = st.slider("Angle of incidence (°)", 0, 85, 30, step=5, key="refr_angle")
        angle1_rad = np.radians(angle1)
        sin_angle2 = n1 * np.sin(angle1_rad) / n2

        if sin_angle2 <= 1:
            angle2_rad = np.arcsin(sin_angle2)
            angle2 = np.degrees(angle2_rad)

            fig, ax = plt.subplots(figsize=(8, 6))
            ax.axhspan(-6, 0, alpha=0.15, color="#3b82f6",
                        label=f"Medium 2: {medium.split('(')[0].strip()}")
            ax.axhspan(0, 6, alpha=0.05, color="#fbbf24", label="Air (n = 1.00)")
            ax.axhline(y=0, color="#64748b", linewidth=2)
            ax.plot([0, 0], [-5, 5], "k--", alpha=0.4, label="Normal")

            x_inc = -4 * np.sin(angle1_rad)
            y_inc = 4 * np.cos(angle1_rad)
            ax.annotate(
                "", xy=(0, 0), xytext=(x_inc, y_inc),
                arrowprops=dict(arrowstyle="->", color="#ef4444", lw=2),
            )

            x_ref = 4 * np.sin(angle2_rad)
            y_ref = -4 * np.cos(angle2_rad)
            ax.annotate(
                "", xy=(x_ref, y_ref), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=2),
            )

            ax.set_xlim(-5, 5)
            ax.set_ylim(-5, 5)
            ax.set_aspect("equal")
            ax.legend(loc="upper right")
            ax.set_title("Refraction of Light")
            ax.grid(True, alpha=0.2)

            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            c1, c2 = st.columns(2)
            c1.metric("Angle of incidence", f"{angle1}°")
            c2.metric("Angle of refraction", f"{angle2:.1f}°")

            if angle2 < angle1:
                st.info("💡 Light bends **towards** the normal when entering a denser medium.")
            else:
                st.info("💡 Light bends **away from** the normal when entering a less dense medium.")
        else:
            st.warning(
                "⚠️ **Total internal reflection!** The angle is too large — "
                "all light reflects back."
            )

    elif mode == "Sound Waves — Frequency & Pitch":
        st.subheader("🔊 Sound Waves — Frequency & Pitch")
        st.latex(r"v = f \times \lambda")

        col1, col2 = st.columns(2)
        with col1:
            frequency = st.slider("Frequency (Hz)", 20, 2000, 440, step=20)
        with col2:
            v_sound = st.slider("Speed of sound (m/s)", 300, 360, 343, step=1)

        wavelength = v_sound / frequency

        c1, c2, c3 = st.columns(3)
        c1.metric("Frequency", f"{frequency} Hz")
        c2.metric("Wavelength", f"{wavelength:.3f} m")
        c3.metric("Speed", f"{v_sound} m/s")

        note_names = {
            262: "C₄", 294: "D₄", 330: "E₄", 349: "F₄",
            392: "G₄", 440: "A₄", 494: "B₄", 523: "C₅",
        }
        closest_note = min(note_names.keys(), key=lambda n: abs(n - frequency))
        if abs(closest_note - frequency) < 30:
            st.success(f"🎵 This is close to the musical note **{note_names[closest_note]}**!")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        t = np.linspace(0, 3 / frequency, 500)
        wave = np.sin(2 * np.pi * frequency * t)
        ax1.plot(t * 1000, wave, lw=2, color="#2563eb")
        ax1.set_xlabel("Time (ms)")
        ax1.set_ylabel("Amplitude")
        ax1.set_title(f"Sound wave at {frequency} Hz")
        ax1.grid(True, alpha=0.3)

        freqs = [262, 440, 880, frequency]
        labels = ["Low C₄\n(262 Hz)", "Concert A₄\n(440 Hz)", "High A₅\n(880 Hz)", f"Yours\n({frequency} Hz)"]
        colors = ["#60a5fa", "#f59e0b", "#ef4444", "#10b981"]
        ax2.bar(labels, freqs, color=colors, edgecolor="#1e3a5f")
        ax2.set_ylabel("Frequency (Hz)")
        ax2.set_title("Frequency Comparison")
        ax2.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        if frequency < 200:
            st.info("💡 This is a **low pitch** sound — like a bass guitar or thunder!")
        elif frequency < 600:
            st.info("💡 This is a **medium pitch** sound — like a human voice or piano!")
        else:
            st.info("💡 This is a **high pitch** sound — like a whistle or bird song!")
