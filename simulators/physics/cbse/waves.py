"""CBSE Physics: Waves Simulator"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.subheader("Waves — CBSE Grade 11-12")

    mode = st.radio(
        "Select topic",
        ["Transverse & Longitudinal", "Standing Waves", "Doppler Effect"],
        horizontal=True,
    )

    if mode == "Transverse & Longitudinal":
        _wave_types()
    elif mode == "Standing Waves":
        _standing_waves()
    else:
        _doppler()


def _wave_types():
    st.latex(r"v = f\lambda \quad;\quad y(x,t) = A\sin(kx - \omega t)")

    with st.sidebar.expander("Wave Controls", expanded=True):
        A = st.slider("Amplitude A (m)", 0.1, 2.0, 1.0, step=0.1)
        f = st.slider("Frequency f (Hz)", 0.5, 5.0, 1.0, step=0.1)
        v = st.slider("Wave speed v (m/s)", 1.0, 20.0, 5.0, step=0.5)
        t_now = st.slider("Time t (s)", 0.0, 5.0, 0.0, step=0.1)

    wavelength = v / f
    k = 2 * np.pi / wavelength
    omega = 2 * np.pi * f
    x = np.linspace(0, 5 * wavelength, 500)
    y = A * np.sin(k * x - omega * t_now)

    col1, col2, col3 = st.columns(3)
    col1.metric("Wavelength λ", f"{wavelength:.3f} m")
    col2.metric("Period T", f"{1/f:.3f} s")
    col3.metric("Speed v", f"{v:.1f} m/s")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y, "b-", lw=2)
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel("Position x (m)")
    ax.set_ylabel("Displacement y (m)")
    ax.set_title(f"Transverse Wave at t = {t_now:.1f} s")
    ax.set_ylim(-A * 1.3, A * 1.3)
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"**y(x, t) = {A} sin({k:.2f}x − {omega:.2f}t)**")


def _standing_waves():
    st.latex(r"y(x,t) = 2A\sin(kx)\cos(\omega t) \quad;\quad f_n = \frac{nv}{2L}")

    with st.sidebar.expander("Standing Wave Controls", expanded=True):
        L = st.slider("String length L (m)", 0.5, 5.0, 1.0, step=0.1)
        n = st.slider("Harmonic number n", 1, 8, 1)
        A = st.slider("Amplitude A (m)", 0.1, 1.0, 0.5, step=0.1)
        v = st.slider("Wave speed v (m/s)", 10.0, 100.0, 50.0, step=5.0)
        t_now = st.slider("Time t (s)", 0.0, 1.0, 0.0, step=0.02)

    f_n = n * v / (2 * L)
    wavelength = 2 * L / n
    k = n * np.pi / L
    omega = 2 * np.pi * f_n

    x = np.linspace(0, L, 500)
    y = 2 * A * np.sin(k * x) * np.cos(omega * t_now)

    col1, col2, col3 = st.columns(3)
    col1.metric(f"f_{n} (Hz)", f"{f_n:.2f}")
    col2.metric("λ (m)", f"{wavelength:.3f}")
    col3.metric("Nodes", f"{n + 1}")

    fig, ax = plt.subplots(figsize=(10, 4))
    # Show multiple time snapshots
    for t_snap in np.linspace(0, 1 / f_n, 8, endpoint=False):
        y_snap = 2 * A * np.sin(k * x) * np.cos(omega * t_snap)
        ax.plot(x, y_snap, "b-", alpha=0.15, lw=1)
    ax.plot(x, y, "r-", lw=2, label=f"t = {t_now:.2f} s")
    ax.plot(x, 2 * A * np.sin(k * x), "g--", alpha=0.5, label="Envelope")
    ax.plot(x, -2 * A * np.sin(k * x), "g--", alpha=0.5)
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel("Position x (m)")
    ax.set_ylabel("Displacement y (m)")
    ax.set_title(f"Standing Wave — {n}{'st' if n==1 else 'nd' if n==2 else 'rd' if n==3 else 'th'} Harmonic")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _doppler():
    st.latex(r"f' = f_0 \frac{v \pm v_o}{v \mp v_s}")

    with st.sidebar.expander("Doppler Controls", expanded=True):
        f0 = st.slider("Source frequency f₀ (Hz)", 100, 2000, 440, step=10)
        v_sound = st.slider("Speed of sound v (m/s)", 300, 360, 343, step=1)
        v_s = st.slider("Source speed v_s (m/s)", 0, 200, 30, step=5)
        v_o = st.slider("Observer speed v_o (m/s)", 0, 100, 0, step=5)

    # Source approaching
    f_approach = f0 * (v_sound + v_o) / (v_sound - v_s) if v_s < v_sound else float("inf")
    # Source receding
    f_recede = f0 * (v_sound - v_o) / (v_sound + v_s)

    col1, col2, col3 = st.columns(3)
    col1.metric("f₀ (source)", f"{f0} Hz")
    col2.metric("f (approaching)", f"{f_approach:.1f} Hz")
    col3.metric("f (receding)", f"{f_recede:.1f} Hz")

    speeds = np.linspace(0, min(v_sound * 0.9, 300), 200)
    f_app = f0 * (v_sound + v_o) / (v_sound - speeds)
    f_rec = f0 * (v_sound - v_o) / (v_sound + speeds)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(speeds, f_app, "r-", lw=2, label="Approaching")
    ax.plot(speeds, f_rec, "b-", lw=2, label="Receding")
    ax.axhline(f0, color="gray", linestyle="--", alpha=0.5, label=f"f₀ = {f0} Hz")
    ax.scatter([v_s], [f_approach], color="red", s=100, zorder=3)
    ax.scatter([v_s], [f_recede], color="blue", s=100, zorder=3)
    ax.set_xlabel("Source speed v_s (m/s)")
    ax.set_ylabel("Observed frequency f (Hz)")
    ax.set_title("Doppler Effect")
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"**Shift:** Approaching +{f_approach - f0:.1f} Hz, Receding {f_recede - f0:.1f} Hz")
