"""Acids, Bases & pH — Core STEM Pack (Grades 9–10)."""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


_COMMON = {
    "Hydrochloric acid (HCl)": 1.0,
    "Stomach acid": 1.5,
    "Lemon juice": 2.4,
    "Vinegar": 2.9,
    "Orange juice": 3.5,
    "Tomato juice": 4.2,
    "Black coffee": 5.0,
    "Milk": 6.5,
    "Pure water": 7.0,
    "Blood": 7.4,
    "Baking soda": 8.3,
    "Milk of magnesia": 10.5,
    "Ammonia solution": 11.6,
    "Bleach": 12.5,
    "Sodium hydroxide (NaOH)": 14.0,
}


def simulate():
    st.header("🧪 Acids, Bases & pH")

    tab1, tab2, tab3 = st.tabs(["pH Scale", "Neutralisation", "Indicators"])

    with tab1:
        st.markdown("Explore the pH scale from strong acids (0) to strong bases (14).")

        selected = st.selectbox("Common substance", list(_COMMON.keys()))
        ph_val = _COMMON[selected]

        custom_ph = st.slider("Or set pH manually", 0.0, 14.0, ph_val, 0.1)

        h_conc = 10 ** (-custom_ph)
        oh_conc = 10 ** (custom_ph - 14)

        if custom_ph < 7:
            nature = "Acidic"
            color = "#e74c3c"
        elif custom_ph > 7:
            nature = "Basic (Alkaline)"
            color = "#3498db"
        else:
            nature = "Neutral"
            color = "#2ecc71"

        fig, ax = plt.subplots(figsize=(10, 2))
        gradient = np.linspace(0, 14, 500).reshape(1, -1)
        ax.imshow(gradient, aspect="auto", cmap="RdYlBu", extent=[0, 14, 0, 1])
        ax.axvline(custom_ph, color="black", linewidth=2)
        ax.set_xlabel("pH")
        ax.set_yticks([])
        ax.set_title(f"pH = {custom_ph:.1f} — {nature}")
        st.pyplot(fig)
        plt.close(fig)

        c1, c2, c3 = st.columns(3)
        c1.metric("Nature", nature)
        c2.metric("[H⁺]", f"{h_conc:.2e} mol/L")
        c3.metric("[OH⁻]", f"{oh_conc:.2e} mol/L")

        st.latex(r"\text{pH} = -\log_{10}[\text{H}^+] \qquad [\text{H}^+][\text{OH}^-] = 10^{-14}")

    with tab2:
        st.markdown("Mix an acid and a base to observe neutralisation.")
        c1, c2 = st.columns(2)
        acid_vol = c1.slider("Acid volume (mL)", 0.0, 100.0, 50.0, 1.0)
        acid_conc = c1.slider("Acid conc. (mol/L)", 0.01, 2.0, 0.1, 0.01)
        base_vol = c2.slider("Base volume (mL)", 0.0, 100.0, 0.0, 1.0)
        base_conc = c2.slider("Base conc. (mol/L)", 0.01, 2.0, 0.1, 0.01)

        acid_moles = acid_vol * acid_conc / 1000
        base_moles = base_vol * base_conc / 1000
        total_vol = (acid_vol + base_vol) / 1000

        if total_vol > 0:
            excess = acid_moles - base_moles
            if abs(excess) < 1e-10:
                result_ph = 7.0
            elif excess > 0:
                h_remaining = excess / total_vol
                result_ph = max(0, -np.log10(h_remaining))
            else:
                oh_remaining = -excess / total_vol
                poh = max(0, -np.log10(oh_remaining))
                result_ph = min(14, 14 - poh)
        else:
            result_ph = 7.0

        st.metric("Resulting pH", f"{result_ph:.2f}")
        st.latex(r"\text{Acid} + \text{Base} \rightarrow \text{Salt} + \text{Water}")

        # Titration curve
        volumes = np.linspace(0, 100, 500)
        ph_curve = []
        for v in volumes:
            bm = v * base_conc / 1000
            tv = (acid_vol + v) / 1000
            if tv > 0:
                ex = acid_moles - bm
                if abs(ex) < 1e-10:
                    ph_curve.append(7.0)
                elif ex > 0:
                    hr = ex / tv
                    ph_curve.append(max(0, -np.log10(max(hr, 1e-15))))
                else:
                    ohr = -ex / tv
                    ph_curve.append(min(14, 14 + np.log10(max(ohr, 1e-15))))
            else:
                ph_curve.append(7.0)

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.plot(volumes, ph_curve, "b-", linewidth=2)
        ax2.axhline(7, color="green", linestyle="--", alpha=0.5, label="pH 7")
        ax2.axvline(base_vol, color="red", linestyle="--", alpha=0.5, label="Current volume")
        ax2.set_xlabel("Base volume added (mL)")
        ax2.set_ylabel("pH")
        ax2.set_title("Titration Curve")
        ax2.set_ylim(0, 14)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)
        plt.close(fig2)

    with tab3:
        st.markdown("See which colour an indicator shows at different pH values.")
        ph_test = st.slider("Test pH", 0.0, 14.0, 7.0, 0.1, key="ind_ph")

        indicators = {
            "Litmus": {"acid": ("#e74c3c", "Red"), "base": ("#3498db", "Blue"), "switch": 7.0},
            "Phenolphthalein": {"acid": ("#ffffff", "Colourless"), "base": ("#ff69b4", "Pink"), "switch": 8.2},
            "Methyl orange": {"acid": ("#e74c3c", "Red"), "base": ("#f1c40f", "Yellow"), "switch": 4.4},
            "Universal indicator": {"acid": ("#e74c3c", "Red"), "base": ("#8e44ad", "Purple"), "switch": 7.0},
        }

        cols = st.columns(len(indicators))
        for col, (name, info) in zip(cols, indicators.items()):
            if ph_test < info["switch"]:
                c, label = info["acid"]
            else:
                c, label = info["base"]
            col.markdown(
                f"**{name}**\n\n"
                f'<div style="background:{c};width:60px;height:60px;'
                f'border-radius:50%;margin:auto;border:2px solid #ccc"></div>\n\n'
                f"<center>{label}</center>",
                unsafe_allow_html=True,
            )
