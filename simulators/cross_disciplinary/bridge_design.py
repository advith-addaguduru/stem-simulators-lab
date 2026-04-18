"""Bridge Design Challenge — Cross-Disciplinary Enrichment Pack."""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


_MATERIALS = {
    "Steel": {"E": 200e9, "density": 7850, "color": "#3498db", "max_stress": 250e6},
    "Aluminium": {"E": 69e9, "density": 2700, "color": "#95a5a6", "max_stress": 70e6},
    "Wood (Oak)": {"E": 12e9, "density": 600, "color": "#8B4513", "max_stress": 40e6},
    "Concrete": {"E": 30e9, "density": 2400, "color": "#7f8c8d", "max_stress": 5e6},
}


def simulate():
    st.header("🌉 Bridge Design Challenge")

    tab1, tab2 = st.tabs(["Beam Bridge", "Truss Analysis"])

    with tab1:
        st.markdown(
            "Design a simply-supported beam bridge and test it under load. "
            "Adjust material, dimensions, and loading to see deflection and stress."
        )
        c1, c2 = st.columns(2)
        material = c1.selectbox("Material", list(_MATERIALS.keys()))
        span = c2.slider("Span length (m)", 2.0, 50.0, 10.0, 0.5)

        c3, c4 = st.columns(2)
        width = c3.slider("Beam width (m)", 0.1, 2.0, 0.5, 0.05)
        height = c4.slider("Beam height (m)", 0.1, 2.0, 0.3, 0.05)

        load = st.slider("Uniformly distributed load (kN/m)", 1.0, 200.0, 20.0, 1.0)

        mat = _MATERIALS[material]
        E = mat["E"]
        I = width * height**3 / 12  # Second moment of area
        q = load * 1000  # N/m
        beam_weight = mat["density"] * width * height * 9.81  # N/m
        total_q = q + beam_weight

        # Maximum deflection at midspan for UDL
        delta_max = 5 * total_q * span**4 / (384 * E * I)
        # Maximum bending stress
        M_max = total_q * span**2 / 8
        sigma_max = M_max * (height / 2) / I

        # Deflection curve
        x = np.linspace(0, span, 300)
        delta = total_q * x * (span**3 - 2 * span * x**2 + x**3) / (24 * E * I)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={"height_ratios": [3, 1]})

        # Bridge shape with deflection (exaggerated)
        scale = min(span / (10 * max(abs(delta_max), 1e-6)), 500)
        ax1.fill_between(x, -delta * scale, -delta * scale + height * scale * 0.1,
                         color=mat["color"], alpha=0.7)
        ax1.plot(x, -delta * scale, "k-", linewidth=1.5)
        ax1.plot([0, 0], [-0.5, 0.5], "k^", markersize=12)
        ax1.plot([span, span], [-0.5, 0.5], "k^", markersize=12)
        ax1.set_title(f"{material} Beam Bridge — Deflection (exaggerated)")
        ax1.set_xlabel("Position along span (m)")
        ax1.set_ylabel("Deflection (scaled)")
        ax1.grid(True, alpha=0.3)

        # Bending moment diagram
        M = total_q * x * (span - x) / 2
        ax2.fill_between(x, M / 1000, alpha=0.3, color="red")
        ax2.plot(x, M / 1000, "r-", linewidth=1.5)
        ax2.set_xlabel("Position (m)")
        ax2.set_ylabel("BM (kN·m)")
        ax2.set_title("Bending Moment Diagram")
        ax2.grid(True, alpha=0.3)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        # Metrics
        safe = sigma_max < mat["max_stress"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Max deflection", f"{delta_max*1000:.1f} mm")
        c2.metric("Max stress", f"{sigma_max/1e6:.1f} MPa")
        c3.metric("Status", "✅ Safe" if safe else "⚠️ Over-stressed")

        if not safe:
            st.warning(
                f"Maximum stress ({sigma_max/1e6:.1f} MPa) exceeds the "
                f"material limit ({mat['max_stress']/1e6:.0f} MPa). "
                "Increase beam height or choose a stronger material."
            )

        st.latex(r"\delta_{max} = \frac{5qL^4}{384EI}, \quad \sigma_{max} = \frac{M_{max} \cdot c}{I}")

    with tab2:
        st.markdown("Analyse forces in a simple Warren truss.")
        n_panels = st.slider("Number of panels", 2, 8, 4, 1)
        panel_len = st.slider("Panel length (m)", 1.0, 5.0, 2.0, 0.5, key="tpl")
        truss_h = st.slider("Truss height (m)", 0.5, 5.0, 2.0, 0.5, key="th")
        pt_load = st.slider("Point load at each top joint (kN)", 1.0, 100.0, 10.0, 1.0)

        # Simple truss geometry
        total_span = n_panels * panel_len
        reaction = (n_panels * pt_load) / 2  # Symmetric loading

        fig3, ax3 = plt.subplots(figsize=(10, 4))

        # Draw bottom chord
        for i in range(n_panels):
            x0 = i * panel_len
            ax3.plot([x0, x0 + panel_len], [0, 0], "b-", linewidth=2)

        # Draw top chord and diagonals
        for i in range(n_panels):
            x0 = i * panel_len
            mid = x0 + panel_len / 2
            # Top point
            ax3.plot([x0, mid], [0, truss_h], "b-", linewidth=2)
            ax3.plot([mid, x0 + panel_len], [truss_h, 0], "b-", linewidth=2)
            if i > 0:
                prev_mid = (i - 1) * panel_len + panel_len / 2
                ax3.plot([prev_mid, mid], [truss_h, truss_h], "b-", linewidth=2)

        # Joints
        for i in range(n_panels + 1):
            ax3.plot(i * panel_len, 0, "ko", markersize=6)
        for i in range(n_panels):
            ax3.plot(i * panel_len + panel_len / 2, truss_h, "ko", markersize=6)

        # Load arrows
        for i in range(n_panels):
            mid = i * panel_len + panel_len / 2
            ax3.annotate("", xy=(mid, truss_h), xytext=(mid, truss_h + 1),
                         arrowprops=dict(arrowstyle="->", color="red", lw=2))
            ax3.text(mid, truss_h + 1.1, f"{pt_load} kN", ha="center", fontsize=8, color="red")

        # Reactions
        ax3.annotate("", xy=(0, -0.3), xytext=(0, -1),
                     arrowprops=dict(arrowstyle="->", color="green", lw=2))
        ax3.text(0, -1.2, f"R={reaction:.0f} kN", ha="center", fontsize=9, color="green")
        ax3.annotate("", xy=(total_span, -0.3), xytext=(total_span, -1),
                     arrowprops=dict(arrowstyle="->", color="green", lw=2))
        ax3.text(total_span, -1.2, f"R={reaction:.0f} kN", ha="center", fontsize=9, color="green")

        ax3.set_xlim(-1, total_span + 1)
        ax3.set_ylim(-2, truss_h + 2)
        ax3.set_aspect("equal")
        ax3.set_title(f"Warren Truss — {n_panels} panels")
        ax3.grid(True, alpha=0.2)
        st.pyplot(fig3)
        plt.close(fig3)

        st.metric("Total load", f"{n_panels * pt_load:.0f} kN")
        st.metric("Each reaction", f"{reaction:.0f} kN")
