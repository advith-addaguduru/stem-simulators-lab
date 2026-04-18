"""Grade 7 — Magnets & Electromagnets
Cambridge Lower Secondary Science (Stage 8)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("🧲 Magnets & Electromagnets")
    st.markdown("_Explore magnetic fields, compasses, and electromagnet strength._")

    mode = st.selectbox(
        "Choose an activity",
        ["Magnetic Field Lines", "Compass Needle", "Electromagnet Strength"],
    )

    if mode == "Magnetic Field Lines":
        _field_lines()
    elif mode == "Compass Needle":
        _compass()
    else:
        _electromagnet()


def _field_lines():
    st.subheader("🧭 Bar Magnet Field Lines")
    st.markdown(
        "Magnetic field lines go from **North** (N) to **South** (S) "
        "outside the magnet. They never cross."
    )

    with st.sidebar.expander("Field Controls", expanded=True):
        strength = st.slider("Magnet strength", 1, 10, 5)
        n_lines = st.slider("Number of field lines", 6, 20, 12, step=2)

    fig, ax = plt.subplots(figsize=(8, 8))

    # Dipole field: place +m at x=-0.5 and -m at x=+0.5
    mx = 0.5
    m = strength * 0.5

    x = np.linspace(-3, 3, 200)
    y = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(x, y)

    r1 = np.sqrt((X + mx)**2 + Y**2)
    r2 = np.sqrt((X - mx)**2 + Y**2)
    r1 = np.maximum(r1, 0.15)
    r2 = np.maximum(r2, 0.15)

    Bx = m * (X + mx) / r1**3 - m * (X - mx) / r2**3
    By = m * Y / r1**3 - m * Y / r2**3

    # Streamplot for field lines
    ax.streamplot(X, Y, Bx, By, color="#3b82f6", linewidth=1, density=1.5,
                  arrowsize=1.2, arrowstyle="->")

    # Draw magnets
    from matplotlib.patches import FancyBboxPatch
    bar = FancyBboxPatch((-mx - 0.3, -0.15), 2 * mx + 0.6, 0.3,
                          boxstyle="round,pad=0.05", facecolor="#d1d5db",
                          edgecolor="#333", linewidth=2)
    ax.add_patch(bar)
    ax.fill_between([-mx - 0.3, 0], -0.15, 0.15, color="#ef4444", alpha=0.5)
    ax.fill_between([0, mx + 0.3], -0.15, 0.15, color="#3b82f6", alpha=0.5)
    ax.text(-mx / 2 - 0.15, 0, "N", ha="center", va="center",
            fontsize=14, fontweight="bold", color="white")
    ax.text(mx / 2 + 0.15, 0, "S", ha="center", va="center",
            fontsize=14, fontweight="bold", color="white")

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.set_title("Bar Magnet Field Lines")
    ax.grid(True, alpha=0.1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.info("💡 The field is strongest where the lines are closest together — near the poles!")


def _compass():
    st.subheader("🧭 Compass Near a Magnet")
    st.markdown("See how a compass needle aligns with the magnetic field at different positions.")

    col1, col2 = st.columns(2)
    with col1:
        cx = st.slider("Compass x position", -2.5, 2.5, 1.5, step=0.25)
    with col2:
        cy = st.slider("Compass y position", -2.5, 2.5, 0.5, step=0.25)

    mx = 0.5
    m = 3.0

    r1 = np.sqrt((cx + mx)**2 + cy**2)
    r2 = np.sqrt((cx - mx)**2 + cy**2)
    r1 = max(r1, 0.2)
    r2 = max(r2, 0.2)

    Bx = m * (cx + mx) / r1**3 - m * (cx - mx) / r2**3
    By = m * cy / r1**3 - m * cy / r2**3
    angle = np.degrees(np.arctan2(By, Bx))
    B_mag = np.sqrt(Bx**2 + By**2)

    c1, c2 = st.columns(2)
    c1.metric("Field direction", f"{angle:.1f}°")
    c2.metric("Field strength (relative)", f"{B_mag:.2f}")

    fig, ax = plt.subplots(figsize=(8, 8))

    # Magnet
    ax.fill_between([-mx - 0.2, 0], -0.1, 0.1, color="#ef4444", alpha=0.6)
    ax.fill_between([0, mx + 0.2], -0.1, 0.1, color="#3b82f6", alpha=0.6)
    ax.text(-mx / 2, 0, "N", ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(mx / 2, 0, "S", ha="center", va="center", fontsize=12, fontweight="bold")

    # Compass needle
    needle_len = 0.3
    dx = needle_len * np.cos(np.radians(angle))
    dy = needle_len * np.sin(np.radians(angle))
    ax.annotate("", xy=(cx + dx, cy + dy), xytext=(cx - dx, cy - dy),
                arrowprops=dict(arrowstyle="-|>", color="#ef4444", lw=2.5))
    ax.plot(cx, cy, "o", markersize=8, color="#333")
    circle = plt.Circle((cx, cy), 0.35, fill=False, color="#333", linewidth=1.5)
    ax.add_patch(circle)

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.set_title(f"Compass at ({cx}, {cy}) — pointing {angle:.1f}°")
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _electromagnet():
    st.subheader("⚡ Electromagnet Strength")
    st.markdown(
        "An electromagnet is made by wrapping a coil of wire around an iron core. "
        "Its strength depends on **current** and **number of turns**."
    )

    with st.sidebar.expander("Electromagnet Controls", expanded=True):
        current = st.slider("Current I (A)", 0.1, 5.0, 1.0, step=0.1)
        turns = st.slider("Number of turns N", 10, 500, 100, step=10)
        core_length = st.slider("Core length L (cm)", 5.0, 30.0, 10.0, step=1.0)

    # Solenoid field B = μ₀ N I / L
    mu_0 = 4 * np.pi * 1e-7
    L = core_length / 100
    B = mu_0 * turns * current / L * 1000  # mT

    c1, c2, c3 = st.columns(3)
    c1.metric("Magnetic field B", f"{B:.2f} mT")
    c2.metric("Turns per metre", f"{turns / L:.0f}")
    c3.metric("Ampere-turns", f"{turns * current:.0f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # B vs current
    i_range = np.linspace(0, 5, 100)
    b_range = mu_0 * turns * i_range / L * 1000
    ax1.plot(i_range, b_range, linewidth=2, color="#2563eb")
    ax1.axvline(current, color="red", linestyle="--", alpha=0.5, label=f"I = {current} A")
    ax1.set_xlabel("Current (A)")
    ax1.set_ylabel("B (mT)")
    ax1.set_title(f"B vs Current (N = {turns})")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # B vs turns
    n_range = np.arange(10, 510, 10)
    b_n = mu_0 * n_range * current / L * 1000
    ax2.plot(n_range, b_n, linewidth=2, color="#22c55e")
    ax2.axvline(turns, color="red", linestyle="--", alpha=0.5, label=f"N = {turns}")
    ax2.set_xlabel("Number of turns")
    ax2.set_ylabel("B (mT)")
    ax2.set_title(f"B vs Turns (I = {current} A)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.info(
        "💡 **To make an electromagnet stronger:** increase the current, "
        "add more turns, or use a soft iron core!"
    )
