"""Probability & Data Analysis — Core STEM Pack (Grades 9–10)."""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("🎲 Probability & Data Analysis")

    tab1, tab2, tab3 = st.tabs(["Dice Simulator", "Probability Tree", "Data Analysis"])

    with tab1:
        st.markdown("Roll dice and compare experimental vs theoretical probability.")
        c1, c2 = st.columns(2)
        n_dice = c1.selectbox("Number of dice", [1, 2, 3], index=1)
        n_rolls = c2.slider("Number of rolls", 10, 10000, 500, 10)

        rolls = np.random.randint(1, 7, size=(n_rolls, n_dice))
        totals = rolls.sum(axis=1)

        min_val = n_dice
        max_val = 6 * n_dice
        bins = np.arange(min_val, max_val + 2) - 0.5
        counts, _ = np.histogram(totals, bins=bins)
        freqs = counts / n_rolls

        # Theoretical (brute force for small n_dice)
        if n_dice <= 3:
            from itertools import product
            all_combos = list(product(range(1, 7), repeat=n_dice))
            theo_totals = [sum(c) for c in all_combos]
            theo_counts = np.zeros(max_val - min_val + 1)
            for t in theo_totals:
                theo_counts[t - min_val] += 1
            theo_probs = theo_counts / len(all_combos)
        else:
            theo_probs = np.ones(max_val - min_val + 1) / (max_val - min_val + 1)

        x_vals = np.arange(min_val, max_val + 1)
        fig, ax = plt.subplots(figsize=(8, 4))
        width = 0.35
        ax.bar(x_vals - width / 2, freqs, width, label="Experimental", alpha=0.7, color="#3498db")
        ax.bar(x_vals + width / 2, theo_probs, width, label="Theoretical", alpha=0.7, color="#e74c3c")
        ax.set_xlabel("Sum of dice")
        ax.set_ylabel("Probability")
        ax.set_title(f"Rolling {n_dice} {'die' if n_dice == 1 else 'dice'} — {n_rolls} trials")
        ax.legend()
        ax.grid(True, alpha=0.3, axis="y")
        st.pyplot(fig)
        plt.close(fig)

        st.latex(r"P(\text{event}) = \frac{\text{favourable outcomes}}{\text{total outcomes}}")

    with tab2:
        st.markdown("Two-stage probability with replacement.")
        c1, c2 = st.columns(2)
        p_a = c1.slider("P(A) — first event", 0.0, 1.0, 0.5, 0.01)
        p_b = c2.slider("P(B) — second event", 0.0, 1.0, 0.3, 0.01)

        p_both = p_a * p_b
        p_a_not_b = p_a * (1 - p_b)
        p_not_a_b = (1 - p_a) * p_b
        p_neither = (1 - p_a) * (1 - p_b)

        st.markdown("#### Outcomes")
        cols = st.columns(4)
        cols[0].metric("A ∩ B", f"{p_both:.4f}")
        cols[1].metric("A ∩ B'", f"{p_a_not_b:.4f}")
        cols[2].metric("A' ∩ B", f"{p_not_a_b:.4f}")
        cols[3].metric("A' ∩ B'", f"{p_neither:.4f}")

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        labels = ["A ∩ B", "A ∩ B'", "A' ∩ B", "A' ∩ B'"]
        values = [p_both, p_a_not_b, p_not_a_b, p_neither]
        colors = ["#3498db", "#2ecc71", "#e74c3c", "#95a5a6"]
        ax2.bar(labels, values, color=colors, alpha=0.8)
        ax2.set_ylabel("Probability")
        ax2.set_title("Probability Tree Outcomes")
        ax2.set_ylim(0, 1)
        ax2.grid(True, alpha=0.3, axis="y")
        st.pyplot(fig2)
        plt.close(fig2)

        st.latex(r"P(A \cap B) = P(A) \times P(B) \quad \text{(independent events)}")

    with tab3:
        st.markdown("Enter data values to compute statistics.")
        data_str = st.text_input(
            "Data (comma-separated)",
            value="4, 7, 2, 9, 5, 7, 3, 8, 7, 6",
        )
        try:
            data = np.array([float(x.strip()) for x in data_str.split(",") if x.strip()])
        except ValueError:
            st.error("Please enter valid numbers separated by commas.")
            return

        if len(data) == 0:
            st.warning("No data entered.")
            return

        mean = np.mean(data)
        median = np.median(data)
        from collections import Counter
        counts = Counter(data)
        mode_val = max(counts, key=counts.get)
        data_range = np.ptp(data)
        std_dev = np.std(data, ddof=1) if len(data) > 1 else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Mean", f"{mean:.2f}")
        c2.metric("Median", f"{median:.2f}")
        c3.metric("Mode", f"{mode_val:.2f}")

        c4, c5 = st.columns(2)
        c4.metric("Range", f"{data_range:.2f}")
        c5.metric("Std Dev", f"{std_dev:.2f}")

        fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(10, 4))
        ax3a.hist(data, bins="auto", color="#3498db", alpha=0.7, edgecolor="white")
        ax3a.axvline(mean, color="red", linestyle="--", label=f"Mean={mean:.1f}")
        ax3a.axvline(median, color="green", linestyle="--", label=f"Median={median:.1f}")
        ax3a.set_title("Histogram")
        ax3a.legend(fontsize=8)
        ax3a.grid(True, alpha=0.3)

        ax3b.boxplot(data, vert=True)
        ax3b.set_title("Box Plot")
        ax3b.grid(True, alpha=0.3)

        fig3.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)
