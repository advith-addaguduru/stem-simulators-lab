"""
Grade 6 — Ratio, Proportion & Percentages
Cambridge Lower Secondary Mathematics (Stage 7)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("⚖️ Ratio, Proportion & Percentages")
    st.markdown("_Visualise ratios, scale quantities, and calculate percentages._")

    mode = st.selectbox(
        "Choose an activity",
        ["Bar-Model Ratios", "Scaling & Proportion", "Percentage Calculator"],
    )

    if mode == "Bar-Model Ratios":
        _bar_model()
    elif mode == "Scaling & Proportion":
        _scaling()
    else:
        _percentages()


def _bar_model():
    st.subheader("📊 Bar-Model Ratios")
    st.markdown("Split a total quantity into parts using a ratio.")

    col1, col2, col3 = st.columns(3)
    with col1:
        total = st.number_input("Total quantity", 1, 10000, 120, step=1)
    with col2:
        a = st.number_input("Part A", 1, 50, 2, step=1)
    with col3:
        b = st.number_input("Part B", 1, 50, 3, step=1)

    parts_sum = a + b
    val_a = total * a / parts_sum
    val_b = total * b / parts_sum

    c1, c2, c3 = st.columns(3)
    c1.metric(f"Ratio", f"{a} : {b}")
    c2.metric("Part A gets", f"{val_a:.1f}")
    c3.metric("Part B gets", f"{val_b:.1f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # Bar model
    ax1.barh(["Part A", "Part B"], [val_a, val_b],
             color=["#3b82f6", "#f97316"], edgecolor="#333", height=0.5)
    ax1.set_xlabel("Quantity")
    ax1.set_title(f"Splitting {total} in ratio {a}:{b}")
    ax1.grid(True, alpha=0.3, axis="x")
    for i, v in enumerate([val_a, val_b]):
        ax1.text(v + total * 0.01, i, f"{v:.1f}", va="center", fontsize=11)

    # Pie chart
    ax2.pie([val_a, val_b], labels=[f"A = {val_a:.1f}", f"B = {val_b:.1f}"],
            colors=["#3b82f6", "#f97316"], autopct="%1.1f%%", startangle=90)
    ax2.set_title("Proportion")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Three-part ratio
    st.markdown("---")
    st.markdown("**Try a 3-part ratio:**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total3 = st.number_input("Total", 1, 10000, 180, step=1, key="t3")
    with col2:
        p1 = st.number_input("Part 1", 1, 50, 1, step=1, key="p1")
    with col3:
        p2 = st.number_input("Part 2", 1, 50, 2, step=1, key="p2")
    with col4:
        p3 = st.number_input("Part 3", 1, 50, 3, step=1, key="p3")

    ps = p1 + p2 + p3
    vals = [total3 * p / ps for p in [p1, p2, p3]]

    fig2, ax = plt.subplots(figsize=(8, 3))
    ax.barh(["Part 1", "Part 2", "Part 3"], vals,
            color=["#3b82f6", "#22c55e", "#f97316"], edgecolor="#333", height=0.5)
    for i, v in enumerate(vals):
        ax.text(v + total3 * 0.01, i, f"{v:.1f}", va="center", fontsize=11)
    ax.set_xlabel("Quantity")
    ax.set_title(f"Splitting {total3} in ratio {p1}:{p2}:{p3}")
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)


def _scaling():
    st.subheader("📐 Scaling & Direct Proportion")
    st.latex(r"y = kx \quad \text{where } k = \frac{y}{x}")

    col1, col2 = st.columns(2)
    with col1:
        x_known = st.number_input("Known x", 0.1, 1000.0, 5.0, step=0.5)
        y_known = st.number_input("Known y", 0.1, 1000.0, 15.0, step=0.5)
    with col2:
        x_new = st.number_input("New x (find y)", 0.1, 1000.0, 8.0, step=0.5)

    k = y_known / x_known
    y_new = k * x_new

    c1, c2, c3 = st.columns(3)
    c1.metric("Constant k", f"{k:.3f}")
    c2.metric("New y", f"{y_new:.2f}")
    c3.metric("Scale factor", f"{x_new / x_known:.2f}×")

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(0, max(x_known, x_new) * 1.5, 100)
    ax.plot(x, k * x, linewidth=2, color="#2563eb", label=f"y = {k:.2f}x")
    ax.plot(x_known, y_known, "o", color="#22c55e", markersize=10, label=f"Known ({x_known}, {y_known})")
    ax.plot(x_new, y_new, "s", color="#ef4444", markersize=10, label=f"New ({x_new}, {y_new:.1f})")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Direct Proportion")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.info("💡 If y is directly proportional to x, the graph is a straight line through the origin!")


def _percentages():
    st.subheader("💯 Percentage Calculator")

    calc_type = st.radio(
        "What to calculate?",
        ["Find % of a number", "Percentage change", "Reverse percentage"],
        horizontal=True,
    )

    if calc_type == "Find % of a number":
        col1, col2 = st.columns(2)
        with col1:
            number = st.number_input("Number", 0.0, 1e6, 250.0, step=1.0)
        with col2:
            pct = st.slider("Percentage (%)", 0, 200, 30)

        result = number * pct / 100
        st.metric(f"{pct}% of {number}", f"{result:.2f}")

        fig, ax = plt.subplots(figsize=(8, 3))
        ax.barh(["Amount"], [number], color="#e2e8f0", edgecolor="#333", height=0.4)
        ax.barh(["Amount"], [result], color="#3b82f6", edgecolor="#333", height=0.4)
        ax.text(result + number * 0.01, 0, f"{result:.1f} ({pct}%)",
                va="center", fontsize=11, color="#2563eb")
        ax.set_xlabel("Value")
        ax.set_title(f"{pct}% of {number}")
        ax.grid(True, alpha=0.3, axis="x")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif calc_type == "Percentage change":
        col1, col2 = st.columns(2)
        with col1:
            original = st.number_input("Original value", 0.01, 1e6, 80.0, step=1.0)
        with col2:
            new_val = st.number_input("New value", 0.0, 1e6, 100.0, step=1.0)

        change = ((new_val - original) / original) * 100
        direction = "increase" if change >= 0 else "decrease"
        st.metric(f"Percentage {direction}", f"{abs(change):.1f}%",
                  delta=f"{change:+.1f}%")

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(["Original", "New"], [original, new_val],
               color=["#94a3b8", "#3b82f6" if change >= 0 else "#ef4444"],
               edgecolor="#333")
        ax.set_ylabel("Value")
        ax.set_title(f"Percentage change: {change:+.1f}%")
        ax.grid(True, alpha=0.3, axis="y")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    else:  # Reverse percentage
        st.markdown("If £X is the price **after** a % change, what was the original?")
        col1, col2 = st.columns(2)
        with col1:
            final = st.number_input("Final value (after change)", 0.01, 1e6, 90.0, step=1.0)
        with col2:
            pct_change = st.number_input("% change applied", -99.0, 500.0, 10.0, step=1.0)

        original = final / (1 + pct_change / 100)
        st.metric("Original value", f"{original:.2f}")
        st.markdown(
            f"Original × {1 + pct_change / 100:.3f} = {final} → Original = {original:.2f}"
        )
