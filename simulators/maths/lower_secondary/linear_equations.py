"""
Grade 8 — Linear Equations & Inequalities
Cambridge Lower Secondary Mathematics (Stage 9)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("📊 Linear Equations & Inequalities")
    st.markdown("_Solve equations, graph lines, and shade inequality regions._")

    mode = st.selectbox(
        "Choose an activity",
        ["Equation Solver — Balance Model", "Graph y = mx + c", "Inequalities on a Number Line"],
    )

    if mode == "Equation Solver — Balance Model":
        st.subheader("⚖️ Solve ax + b = c")
        st.latex(r"ax + b = c \quad\Rightarrow\quad x = \frac{c - b}{a}")

        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.number_input("a", -10.0, 10.0, 2.0, step=1.0)
        with col2:
            b = st.number_input("b", -20.0, 20.0, 5.0, step=1.0)
        with col3:
            c = st.number_input("c", -50.0, 50.0, 11.0, step=1.0)

        if a == 0:
            if b == c:
                st.success("**Infinite solutions** — any value of x works!")
            else:
                st.error("**No solution** — the equation is inconsistent.")
        else:
            x_sol = (c - b) / a
            st.success(f"**Solution:** x = ({c} − {b}) ÷ {a} = **{x_sol:.3f}**")

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

            # Balance model
            left_val = a * x_sol + b
            right_val = c
            ax1.barh(["Left side\n(ax + b)", "Right side\n(c)"],
                     [left_val, right_val],
                     color=["#3b82f6", "#22c55e"], edgecolor="#333", height=0.4)
            ax1.set_xlabel("Value")
            ax1.set_title("Balance Model — Both sides equal!")
            ax1.grid(True, alpha=0.3, axis="x")

            # Line graph showing where y = ax + b crosses y = c
            x_vals = np.linspace(x_sol - 5, x_sol + 5, 200)
            y_vals = a * x_vals + b
            ax2.plot(x_vals, y_vals, linewidth=2, color="#2563eb", label=f"y = {a}x + {b}")
            ax2.axhline(c, color="#ef4444", linestyle="--", linewidth=1.5, label=f"y = {c}")
            ax2.plot(x_sol, c, "o", color="#f59e0b", markersize=10, zorder=5)
            ax2.annotate(f"  x = {x_sol:.2f}", (x_sol, c), fontsize=10, color="#f59e0b")
            ax2.set_xlabel("x")
            ax2.set_ylabel("y")
            ax2.set_title("Graphical Solution")
            ax2.legend()
            ax2.grid(True, alpha=0.3)

            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    elif mode == "Graph y = mx + c":
        st.subheader("📈 Graph y = mx + c")
        st.latex(r"y = mx + c")
        st.markdown("**m** is the gradient (slope) and **c** is the y-intercept.")

        col1, col2 = st.columns(2)
        with col1:
            m = st.slider("Gradient m", -5.0, 5.0, 1.0, step=0.5)
        with col2:
            c_val = st.slider("y-intercept c", -10.0, 10.0, 0.0, step=0.5)

        x = np.linspace(-10, 10, 200)
        y = m * x + c_val

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y, linewidth=2, color="#2563eb", label=f"y = {m}x + {c_val}")
        ax.axhline(0, color="black", linewidth=0.5)
        ax.axvline(0, color="black", linewidth=0.5)
        ax.plot(0, c_val, "o", color="#ef4444", markersize=8, label=f"y-intercept = {c_val}")

        if m != 0:
            x_int = -c_val / m
            ax.plot(x_int, 0, "s", color="#22c55e", markersize=8, label=f"x-intercept = {x_int:.2f}")

        ax.set_xlim(-10, 10)
        ax.set_ylim(-15, 15)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Straight Line Graph")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        c1, c2 = st.columns(2)
        c1.metric("Gradient", f"{m}")
        c2.metric("y-intercept", f"{c_val}")

        if m > 0:
            st.info("📈 Positive gradient — the line goes **uphill** from left to right.")
        elif m < 0:
            st.info("📉 Negative gradient — the line goes **downhill** from left to right.")
        else:
            st.info("➡️ Zero gradient — the line is **horizontal**.")

    else:  # Inequalities
        st.subheader("📏 Inequalities on a Number Line")
        st.latex(r"ax + b < c \quad\text{or}\quad ax + b > c")

        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.number_input("a ", -10.0, 10.0, 1.0, step=1.0, key="ineq_a")
        with col2:
            b = st.number_input("b ", -20.0, 20.0, 3.0, step=1.0, key="ineq_b")
        with col3:
            c_val = st.number_input("c ", -50.0, 50.0, 7.0, step=1.0, key="ineq_c")

        ineq_type = st.selectbox("Inequality type", ["<", "≤", ">", "≥"])

        if a == 0:
            st.warning("Set a ≠ 0 for a meaningful inequality.")
        else:
            boundary = (c_val - b) / a
            flip = a < 0

            fig, ax = plt.subplots(figsize=(10, 2))
            num_line = np.linspace(boundary - 10, boundary + 10, 500)
            ax.plot(num_line, np.zeros_like(num_line), "k-", linewidth=1)

            # Determine shading direction
            shade_left = (ineq_type in ["<", "≤"]) != flip
            filled = ineq_type in ["≤", "≥"]

            if shade_left:
                ax.fill_between(num_line, -0.3, 0.3,
                                where=num_line <= boundary, color="#3b82f6", alpha=0.3)
                ax.annotate("", xy=(boundary - 8, 0), xytext=(boundary - 2, 0),
                            arrowprops=dict(arrowstyle="<-", color="#3b82f6", lw=2))
                symbol = "≤" if filled else "<"
            else:
                ax.fill_between(num_line, -0.3, 0.3,
                                where=num_line >= boundary, color="#22c55e", alpha=0.3)
                ax.annotate("", xy=(boundary + 8, 0), xytext=(boundary + 2, 0),
                            arrowprops=dict(arrowstyle="<-", color="#22c55e", lw=2))
                symbol = "≥" if filled else ">"

            marker = "o" if filled else "o"
            face = "#f59e0b" if filled else "white"
            ax.plot(boundary, 0, marker, color="#f59e0b", markerfacecolor=face,
                    markersize=12, markeredgewidth=2, zorder=5)
            ax.annotate(f"  x = {boundary:.2f}", (boundary, 0.05), fontsize=11)

            ax.set_ylim(-0.5, 0.5)
            ax.set_yticks([])
            ax.set_xlabel("x")
            ax.set_title(f"Solution: x {symbol} {boundary:.2f}")
            ax.grid(True, alpha=0.3, axis="x")

            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            circle = "filled ●" if filled else "open ○"
            st.markdown(
                f"**{a}x + {b} {ineq_type} {c_val}** → **x {symbol} {boundary:.2f}** "
                f"({circle} means the boundary is {'included' if filled else 'excluded'})"
            )
