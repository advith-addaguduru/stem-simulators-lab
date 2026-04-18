"""
Grade 8 — Statistics & Probability
Cambridge Lower Secondary Mathematics (Stage 9)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("📊 Statistics & Probability")
    st.markdown("_Collect data, draw charts, and calculate probability._")

    mode = st.selectbox(
        "Choose an activity",
        ["Mean, Median & Mode", "Probability Simulator", "Chart Builder"],
    )

    if mode == "Mean, Median & Mode":
        st.subheader("📈 Mean, Median & Mode")

        st.markdown("Enter your data set (comma-separated numbers):")
        data_input = st.text_input("Data", value="4, 7, 2, 9, 4, 6, 4, 8, 3, 5")

        try:
            data = [float(x.strip()) for x in data_input.split(",") if x.strip()]
        except ValueError:
            st.error("Please enter valid numbers separated by commas.")
            return

        if len(data) < 2:
            st.warning("Enter at least 2 numbers.")
            return

        data_sorted = sorted(data)
        mean = np.mean(data)
        median = np.median(data)

        # Mode calculation
        from collections import Counter
        counts = Counter(data)
        max_count = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_count]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Mean", f"{mean:.2f}")
        c2.metric("Median", f"{median:.1f}")
        c3.metric("Mode", ", ".join(f"{m:.0f}" for m in modes))
        c4.metric("Range", f"{max(data) - min(data):.1f}")

        st.markdown(f"**Sorted data:** {', '.join(f'{x:.0f}' for x in data_sorted)}")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Dot plot
        ax1.plot(range(1, len(data_sorted) + 1), data_sorted, "o-", color="#2563eb", markersize=8)
        ax1.axhline(y=mean, color="#ef4444", ls="--", lw=2, label=f"Mean = {mean:.1f}")
        ax1.axhline(y=median, color="#22c55e", ls="--", lw=2, label=f"Median = {median:.1f}")
        ax1.set_xlabel("Position")
        ax1.set_ylabel("Value")
        ax1.set_title("Data Points (sorted)")
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)

        # Frequency chart
        unique_vals = sorted(set(data))
        freqs = [data.count(v) for v in unique_vals]
        ax2.bar([str(int(v)) for v in unique_vals], freqs, color="#60a5fa", edgecolor="#2563eb")
        ax2.set_xlabel("Value")
        ax2.set_ylabel("Frequency")
        ax2.set_title("Frequency Chart")
        ax2.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info(
            "💡 **Mean** = sum ÷ count | **Median** = middle value | "
            "**Mode** = most frequent | **Range** = highest − lowest"
        )

    elif mode == "Probability Simulator":
        st.subheader("🎲 Probability Simulator")
        st.latex(r"P(\text{event}) = \frac{\text{favourable outcomes}}{\text{total outcomes}}")

        experiment = st.radio("Experiment", ["Coin Flip", "Dice Roll", "Card Draw"], horizontal=True)

        n_trials = st.slider("Number of trials", 10, 1000, 100, step=10)

        if experiment == "Coin Flip":
            results = np.random.choice(["Heads", "Tails"], size=n_trials)
            heads = np.sum(results == "Heads")
            tails = n_trials - heads

            c1, c2 = st.columns(2)
            c1.metric("Heads", f"{heads} ({100 * heads / n_trials:.1f}%)")
            c2.metric("Tails", f"{tails} ({100 * tails / n_trials:.1f}%)")

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            ax1.bar(["Heads", "Tails"], [heads, tails], color=["#3b82f6", "#f59e0b"], edgecolor="#1e3a5f")
            ax1.set_ylabel("Count")
            ax1.set_title("Results")
            ax1.grid(True, alpha=0.3, axis="y")

            # Running proportion
            running = np.cumsum(results == "Heads") / np.arange(1, n_trials + 1)
            ax2.plot(running, color="#2563eb", lw=1.5)
            ax2.axhline(y=0.5, color="#ef4444", ls="--", label="Expected (0.5)")
            ax2.set_xlabel("Number of flips")
            ax2.set_ylabel("Proportion of heads")
            ax2.set_title("Convergence to 0.5")
            ax2.legend()
            ax2.grid(True, alpha=0.3)

            expected = "P(Heads) = 1/2 = 0.5"

        elif experiment == "Dice Roll":
            results = np.random.randint(1, 7, size=n_trials)
            counts = [np.sum(results == i) for i in range(1, 7)]

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            ax1.bar(range(1, 7), counts, color="#60a5fa", edgecolor="#2563eb")
            ax1.axhline(y=n_trials / 6, color="#ef4444", ls="--", lw=2, label=f"Expected ≈ {n_trials / 6:.0f}")
            ax1.set_xlabel("Dice face")
            ax1.set_ylabel("Count")
            ax1.set_title("Dice Roll Results")
            ax1.legend()
            ax1.grid(True, alpha=0.3, axis="y")

            ax2.pie(counts, labels=[f"{i}" for i in range(1, 7)],
                    autopct="%1.1f%%", colors=plt.cm.Set3(np.linspace(0, 1, 6)))
            ax2.set_title("Distribution")

            expected = "P(any face) = 1/6 ≈ 0.167"

        else:  # Card Draw
            suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
            results = np.random.choice(suits, size=n_trials)
            counts = [np.sum(results == s) for s in suits]

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            colors_suit = ["#ef4444", "#f59e0b", "#374151", "#3b82f6"]
            ax1.bar(suits, counts, color=colors_suit, edgecolor="#1e3a5f")
            ax1.axhline(y=n_trials / 4, color="#22c55e", ls="--", lw=2, label=f"Expected ≈ {n_trials / 4:.0f}")
            ax1.set_ylabel("Count")
            ax1.set_title("Card Suit Draws")
            ax1.legend()
            ax1.grid(True, alpha=0.3, axis="y")

            ax2.pie(counts, labels=suits, autopct="%1.1f%%", colors=colors_suit)
            ax2.set_title("Distribution")

            expected = "P(any suit) = 1/4 = 0.25"

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown(f"**Theoretical probability:** {expected}")
        st.info("💡 **Law of Large Numbers:** The more trials you do, the closer the results get to the theoretical probability!")

    elif mode == "Chart Builder":
        st.subheader("📊 Chart Builder")
        st.markdown("Enter category names and values to build your own chart.")

        n_cats = st.slider("Number of categories", 2, 8, 4)

        categories = []
        values = []
        cols = st.columns(n_cats)
        for i, col in enumerate(cols):
            with col:
                cat = st.text_input(f"Name {i + 1}", value=f"Cat {i + 1}", key=f"cat_{i}")
                val = st.number_input(f"Value {i + 1}", value=float(i + 1) * 10, step=1.0, key=f"val_{i}")
                categories.append(cat)
                values.append(val)

        chart_type = st.radio("Chart type", ["Bar Chart", "Pie Chart", "Horizontal Bar"], horizontal=True)

        fig, ax = plt.subplots(figsize=(8, 5))
        colors = plt.cm.Set2(np.linspace(0, 1, n_cats))

        if chart_type == "Bar Chart":
            ax.bar(categories, values, color=colors, edgecolor="#1e3a5f")
            ax.set_ylabel("Value")
            ax.grid(True, alpha=0.3, axis="y")
        elif chart_type == "Pie Chart":
            if all(v >= 0 for v in values) and sum(values) > 0:
                ax.pie(values, labels=categories, autopct="%1.1f%%", colors=colors)
            else:
                st.warning("Pie charts need positive values.")
                return
        else:
            ax.barh(categories, values, color=colors, edgecolor="#1e3a5f")
            ax.set_xlabel("Value")
            ax.grid(True, alpha=0.3, axis="x")

        ax.set_title("Your Custom Chart")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.metric("Total", f"{sum(values):.1f}")
        st.info("💡 **Tip:** Bar charts are great for comparing categories. Pie charts show proportions of a whole.")
