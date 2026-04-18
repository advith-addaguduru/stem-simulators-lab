"""CBSE Class 12 Physics: Optics Simulator"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulators.utils import nice_axes


def simulate():
    st.subheader("Optics — Ray & Wave")
    st.latex(
        r"\frac{1}{f} = \frac{1}{v} - \frac{1}{u} \qquad "
        r"d\sin\theta = n\lambda"
    )

    mode = st.radio(
        "Choose a topic",
        ["Mirror & Lens Ray Diagrams", "Young's Double Slit", "Single-Slit Diffraction"],
        horizontal=True,
    )

    if mode == "Mirror & Lens Ray Diagrams":
        _lens()
    elif mode == "Young's Double Slit":
        _double_slit()
    else:
        _single_slit()


def _lens():
    st.markdown("### Thin Lens / Mirror Equation")
    st.latex(r"\frac{1}{f} = \frac{1}{v} - \frac{1}{u}")

    with st.sidebar.expander("Lens Controls", expanded=True):
        optic = st.selectbox("Optical element", ["Convex lens", "Concave lens",
                                                  "Concave mirror", "Convex mirror"])
        f_mag = st.slider("|Focal length| (cm)", 5.0, 30.0, 10.0, step=1.0)
        u = st.slider("Object distance u (cm)", 5.0, 60.0, 25.0, step=1.0)
        h_obj = st.slider("Object height (cm)", 1.0, 10.0, 3.0, step=0.5)

    if optic in ("Convex lens", "Concave mirror"):
        f = f_mag
    else:
        f = -f_mag

    # Sign convention: for lenses u is negative (real object on left)
    # Using 1/v = 1/f + 1/u with real-is-positive for lenses
    u_signed = -u  # object on left
    denom = 1 / f - 1 / abs(u)
    if abs(denom) < 1e-10:
        st.warning("Object is at the focal point — image at infinity!")
        return

    v = 1 / denom
    magnification = v / u
    h_img = magnification * h_obj

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Image distance v", f"{abs(v):.1f} cm")
    c2.metric("Magnification", f"{abs(magnification):.2f}×")
    c3.metric("Image height", f"{abs(h_img):.1f} cm")
    nature = "Real, inverted" if v > 0 else "Virtual, upright"
    c4.metric("Nature", nature)

    fig, ax = plt.subplots(figsize=(10, 5))

    # Axis
    ax.axhline(0, color="grey", linewidth=0.5)
    ax.axvline(0, color="#2563eb", linewidth=2, label=f"{optic}")

    # Focal points
    ax.plot(f, 0, "x", color="#ef4444", markersize=10, markeredgewidth=2, label="F")
    ax.plot(-f, 0, "x", color="#ef4444", markersize=10, markeredgewidth=2)

    # Object
    ax.annotate("", xy=(-u, h_obj), xytext=(-u, 0),
                arrowprops=dict(arrowstyle="-|>", color="#22c55e", lw=2))
    ax.text(-u, h_obj + 0.3, "Object", ha="center", fontsize=9, color="#22c55e")

    # Image
    ax.annotate("", xy=(v, -h_img if v > 0 else h_img), xytext=(v, 0),
                arrowprops=dict(arrowstyle="-|>", color="#f97316", lw=2))
    ax.text(v, (-h_img if v > 0 else h_img) + 0.3, "Image", ha="center",
            fontsize=9, color="#f97316")

    # Rays (simplified 2-ray construction)
    # Ray parallel to axis → through F
    ax.plot([-u, 0], [h_obj, h_obj], "--", color="#3b82f6", linewidth=1)
    ax.plot([0, max(v, 30)], [h_obj, h_obj - h_obj * max(v, 30) / f], "--",
            color="#3b82f6", linewidth=1)

    ax.set_xlim(-u - 10, max(abs(v), 30) + 5)
    y_max = max(h_obj, abs(h_img)) + 2
    ax.set_ylim(-y_max, y_max)
    ax.set_xlabel("Distance (cm)")
    ax.set_ylabel("Height (cm)")
    ax.set_title("Ray Diagram")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # v vs u graph
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    u_range = np.linspace(f + 0.5, 60, 200)
    v_range = 1 / (1 / f - 1 / u_range)
    ax2.plot(u_range, v_range, linewidth=2, color="#2563eb")
    ax2.axvline(u, color="red", linestyle="--", alpha=0.5, label=f"u = {u}")
    ax2.axhline(0, color="grey", linewidth=0.5)
    nice_axes(ax2, "Object distance u (cm)", "Image distance v (cm)", "v vs u graph")
    ax2.legend()

    plt.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)


def _double_slit():
    st.markdown("### Young's Double-Slit Experiment")
    st.latex(r"\Delta y = \frac{\lambda D}{d}")

    with st.sidebar.expander("Double Slit Controls", expanded=True):
        wavelength_nm = st.slider("Wavelength λ (nm)", 380, 750, 550, step=10)
        d_mm = st.slider("Slit separation d (mm)", 0.1, 2.0, 0.5, step=0.1)
        D_m = st.slider("Screen distance D (m)", 0.5, 5.0, 2.0, step=0.1)

    lam = wavelength_nm * 1e-9
    d = d_mm * 1e-3
    D = D_m

    fringe_spacing = lam * D / d * 1e3  # mm

    c1, c2 = st.columns(2)
    c1.metric("Fringe spacing Δy", f"{fringe_spacing:.2f} mm")
    c2.metric("Central bright fringe", "0 mm")

    y = np.linspace(-10, 10, 1000) * 1e-3  # metres
    path_diff = d * y / D
    intensity = (np.cos(np.pi * path_diff / lam))**2

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Colour from wavelength
    def _wl_to_rgb(wl):
        if 380 <= wl < 440:
            return (-(wl - 440) / 60, 0, 1)
        elif 440 <= wl < 490:
            return (0, (wl - 440) / 50, 1)
        elif 490 <= wl < 510:
            return (0, 1, -(wl - 510) / 20)
        elif 510 <= wl < 580:
            return ((wl - 510) / 70, 1, 0)
        elif 580 <= wl < 645:
            return (1, -(wl - 645) / 65, 0)
        else:
            return (1, 0, 0)

    rgb = _wl_to_rgb(wavelength_nm)

    ax1.plot(y * 1e3, intensity, linewidth=2, color=rgb)
    ax1.fill_between(y * 1e3, intensity, alpha=0.2, color=rgb)
    nice_axes(ax1, "Position on screen (mm)", "Relative intensity",
              f"Interference Pattern (λ = {wavelength_nm} nm)")

    # Fringe pattern as image
    pattern = np.tile(intensity, (50, 1))
    ax2.imshow(pattern, cmap="gray", aspect="auto",
               extent=[-10, 10, 0, 1])
    ax2.set_xlabel("Position (mm)")
    ax2.set_yticks([])
    ax2.set_title("Screen Pattern")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _single_slit():
    st.markdown("### Single-Slit Diffraction")
    st.latex(r"I(\theta) = I_0 \left(\frac{\sin\beta}{\beta}\right)^2 \quad \beta = \frac{\pi a \sin\theta}{\lambda}")

    with st.sidebar.expander("Diffraction Controls", expanded=True):
        wavelength_nm = st.slider("Wavelength λ (nm) ", 380, 750, 550, step=10)
        a_mm = st.slider("Slit width a (mm)", 0.05, 1.0, 0.2, step=0.05)

    lam = wavelength_nm * 1e-9
    a = a_mm * 1e-3

    theta = np.linspace(-0.03, 0.03, 1000)
    beta = np.pi * a * np.sin(theta) / lam
    intensity = np.where(np.abs(beta) < 1e-10, 1.0, (np.sin(beta) / beta)**2)

    first_min = np.degrees(np.arcsin(lam / a)) if lam / a <= 1 else None

    if first_min:
        st.metric("First minimum at", f"±{first_min:.4f}°")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.plot(np.degrees(theta), intensity, linewidth=2, color="#8b5cf6")
    ax1.fill_between(np.degrees(theta), intensity, alpha=0.2, color="#8b5cf6")
    if first_min:
        ax1.axvline(first_min, color="#ef4444", linestyle="--", alpha=0.7, label=f"1st min: {first_min:.4f}°")
        ax1.axvline(-first_min, color="#ef4444", linestyle="--", alpha=0.7)
    nice_axes(ax1, "Angle θ (degrees)", "Relative intensity",
              f"Diffraction Pattern (a = {a_mm} mm)")
    ax1.legend(fontsize=9)

    # Pattern image
    pattern = np.tile(intensity, (50, 1))
    ax2.imshow(pattern, cmap="inferno", aspect="auto",
               extent=[np.degrees(theta[0]), np.degrees(theta[-1]), 0, 1])
    ax2.set_xlabel("Angle (degrees)")
    ax2.set_yticks([])
    ax2.set_title("Diffraction Pattern on Screen")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
