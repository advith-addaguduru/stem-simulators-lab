"""
Grade 6 — Number Patterns & Sequences
Cambridge Lower Secondary Mathematics (Stage 7)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("🔢 Number Patterns & Sequences")
    st.markdown("_Spot patterns in numbers and predict what comes next._")

    mode = st.selectbox(
        "Choose an activity",
        ["Arithmetic Sequences", "Geometric Sequences", "Equation Solver"],
    )

    if mode == "Arithmetic Sequences":
        st.subheader("➕ Arithmetic Sequences")
        st.latex(r"a_n = a_1 + (n - 1) \times d")
        st.markdown("Each term is found by **adding** a common difference **d**.")

        col1, col2, col3 = st.columns(3)
        with col1:
            a1 = st.number_input("First term (a₁)", value=2, step=1)
        with col2:
            d = st.number_input("Common difference (d)", value=3, step=1)
        with col3:
            n_terms = st.slider("Number of terms", 3, 20, 8)

        terms = [a1 + i * d for i in range(n_terms)]

        st.markdown("**Sequence:** " + ", ".join(str(t) for t in terms) + ", ...")

        c1, c2 = st.columns(2)
        c1.metric(f"Term {n_terms}", terms[-1])
        c2.metric("Sum of all terms", sum(terms))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Plot sequence
        ax1.plot(range(1, n_terms + 1), terms, "o-", color="#2563eb", markersize=8, lw=2)
        ax1.set_xlabel("Term number (n)")
        ax1.set_ylabel("Value")
        ax1.set_title("Arithmetic Sequence")
        ax1.grid(True, alpha=0.3)

        # Differences bar chart
        diffs = [terms[i + 1] - terms[i] for i in range(len(terms) - 1)]
        ax2.bar(range(1, len(diffs) + 1), diffs, color="#60a5fa", edgecolor="#2563eb")
        ax2.set_xlabel("Between terms")
        ax2.set_ylabel("Difference")
        ax2.set_title(f"Common difference = {d}")
        ax2.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.info("💡 **Pattern:** The graph of an arithmetic sequence is always a straight line!")

    elif mode == "Geometric Sequences":
        st.subheader("✖️ Geometric Sequences")
        st.latex(r"a_n = a_1 \times r^{(n-1)}")
        st.markdown("Each term is found by **multiplying** by a common ratio **r**.")

        col1, col2, col3 = st.columns(3)
        with col1:
            a1 = st.number_input("First term (a₁)", value=2.0, step=1.0, key="geo_a1")
        with col2:
            r = st.number_input("Common ratio (r)", value=2.0, step=0.5, min_value=0.1, max_value=5.0)
        with col3:
            n_terms = st.slider("Number of terms", 3, 12, 6, key="geo_n")

        terms = [a1 * r ** i for i in range(n_terms)]

        st.markdown("**Sequence:** " + ", ".join(f"{t:.1f}" for t in terms) + ", ...")

        c1, c2 = st.columns(2)
        c1.metric(f"Term {n_terms}", f"{terms[-1]:.1f}")
        c2.metric("Sum of all terms", f"{sum(terms):.1f}")

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(range(1, n_terms + 1), terms, "s-", color="#ef4444", markersize=8, lw=2)
        ax.set_xlabel("Term number (n)")
        ax.set_ylabel("Value")
        ax.set_title("Geometric Sequence")
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        if r > 1:
            st.info("💡 **Pattern:** When r > 1, the sequence grows exponentially — it curves upward!")
        elif r == 1:
            st.info("💡 **Pattern:** When r = 1, every term is the same!")
        else:
            st.info("💡 **Pattern:** When r < 1, the terms get smaller and approach zero!")

    elif mode == "Equation Solver":
        st.subheader("🔍 Simple Equation Solver")
        st.latex(r"ax + b = c")
        st.markdown("Find the value of **x** that makes the equation true.")

        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.number_input("a (coefficient of x)", value=2, step=1, key="eq_a")
        with col2:
            b = st.number_input("b (constant on left)", value=3, step=1, key="eq_b")
        with col3:
            c_val = st.number_input("c (right side)", value=11, step=1, key="eq_c")

        st.markdown(f"**Equation:** {a}x + {b} = {c_val}")

        if a == 0:
            if b == c_val:
                st.success("✅ Any value of x works (the equation is always true)!")
            else:
                st.error("❌ No solution exists (the equation is never true).")
        else:
            x = (c_val - b) / a
            st.markdown("**Solution steps:**")
            st.markdown(f"1. Subtract {b} from both sides: {a}x = {c_val} − {b} = {c_val - b}")
            st.markdown(f"2. Divide both sides by {a}: x = {c_val - b} / {a} = **{x:.2f}**")

            st.metric("x =", f"{x:.2f}")

            # Check visualization
            fig, ax = plt.subplots(figsize=(8, 4))
            x_range = np.linspace(x - 5, x + 5, 100)
            y_left = a * x_range + b
            y_right = np.full_like(x_range, c_val)

            ax.plot(x_range, y_left, lw=2, label=f"y = {a}x + {b}", color="#2563eb")
            ax.axhline(y=c_val, color="#ef4444", lw=2, ls="--", label=f"y = {c_val}")
            ax.scatter([x], [c_val], color="#10b981", s=120, zorder=5, label=f"Solution: x = {x:.2f}")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title("Graphical Solution")
            ax.legend()
            ax.grid(True, alpha=0.3)

            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            st.info("💡 **Check:** The solution is where the two lines cross!")
