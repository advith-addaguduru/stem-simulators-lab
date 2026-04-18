"""Coding & Mathematics — Cross-Disciplinary Enrichment Pack."""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def simulate():
    st.header("💻 Coding & Mathematics")

    tab1, tab2, tab3 = st.tabs(["Sorting Visualiser", "Fibonacci & Golden Ratio", "Fractal Explorer"])

    with tab1:
        st.markdown("Compare sorting algorithms step-by-step.")
        n_elements = st.slider("Array size", 5, 50, 20, 1)
        algo = st.radio("Algorithm", ["Bubble Sort", "Selection Sort", "Insertion Sort"],
                        horizontal=True)

        arr = list(np.random.randint(1, 100, n_elements))

        def bubble_sort(a):
            a = a.copy()
            steps = [a.copy()]
            comps = 0
            for i in range(len(a)):
                for j in range(len(a) - i - 1):
                    comps += 1
                    if a[j] > a[j + 1]:
                        a[j], a[j + 1] = a[j + 1], a[j]
                        steps.append(a.copy())
            return steps, comps

        def selection_sort(a):
            a = a.copy()
            steps = [a.copy()]
            comps = 0
            for i in range(len(a)):
                min_idx = i
                for j in range(i + 1, len(a)):
                    comps += 1
                    if a[j] < a[min_idx]:
                        min_idx = j
                if min_idx != i:
                    a[i], a[min_idx] = a[min_idx], a[i]
                    steps.append(a.copy())
            return steps, comps

        def insertion_sort(a):
            a = a.copy()
            steps = [a.copy()]
            comps = 0
            for i in range(1, len(a)):
                key = a[i]
                j = i - 1
                while j >= 0 and a[j] > key:
                    comps += 1
                    a[j + 1] = a[j]
                    j -= 1
                comps += 1
                a[j + 1] = key
                steps.append(a.copy())
            return steps, comps

        sorters = {
            "Bubble Sort": bubble_sort,
            "Selection Sort": selection_sort,
            "Insertion Sort": insertion_sort,
        }

        steps, comparisons = sorters[algo](arr)

        step_idx = st.slider("Step", 0, len(steps) - 1, len(steps) - 1, 1)

        fig, ax = plt.subplots(figsize=(10, 4))
        colors = ["#3498db" if i >= len(steps[step_idx]) - step_idx else "#2ecc71"
                  for i in range(len(steps[step_idx]))]
        ax.bar(range(len(steps[step_idx])), steps[step_idx], color="#3498db", alpha=0.8)
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        ax.set_title(f"{algo} — Step {step_idx}/{len(steps)-1}")
        ax.grid(True, alpha=0.3, axis="y")
        st.pyplot(fig)
        plt.close(fig)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total steps", len(steps) - 1)
        c2.metric("Comparisons", comparisons)
        c3.metric("Time complexity", "O(n²)")

    with tab2:
        st.markdown("Explore the Fibonacci sequence and its connection to the golden ratio.")
        n_terms = st.slider("Number of terms", 5, 40, 15, 1)

        fib = [0, 1]
        for i in range(2, n_terms):
            fib.append(fib[-1] + fib[-2])

        ratios = [fib[i] / fib[i - 1] if fib[i - 1] > 0 else 0 for i in range(2, len(fib))]
        phi = (1 + np.sqrt(5)) / 2

        fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(12, 4))

        ax2a.plot(range(n_terms), fib, "bo-", markersize=5, linewidth=1.5)
        ax2a.set_xlabel("n")
        ax2a.set_ylabel("F(n)")
        ax2a.set_title("Fibonacci Sequence")
        ax2a.grid(True, alpha=0.3)

        ax2b.plot(range(2, n_terms), ratios, "ro-", markersize=5, linewidth=1.5, label="F(n)/F(n-1)")
        ax2b.axhline(phi, color="gold", linestyle="--", linewidth=2, label=f"φ = {phi:.6f}")
        ax2b.set_xlabel("n")
        ax2b.set_ylabel("Ratio")
        ax2b.set_title("Convergence to Golden Ratio")
        ax2b.legend()
        ax2b.grid(True, alpha=0.3)

        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

        st.metric("Golden ratio φ", f"{phi:.10f}")
        st.latex(r"\varphi = \frac{1 + \sqrt{5}}{2} \approx 1.618")

        # Golden spiral
        st.markdown("#### Golden Spiral")
        fig3, ax3 = plt.subplots(figsize=(6, 6))
        x0, y0 = 0, 0
        for i in range(min(n_terms - 1, 12)):
            size = fib[i + 1] if i + 1 < len(fib) else fib[-1]
            if size == 0:
                continue
            rect = plt.Rectangle((x0, y0), size, size, fill=False,
                                 edgecolor="#3498db", linewidth=1.5)
            ax3.add_patch(rect)

            theta = np.linspace(0, np.pi / 2, 50)
            r = size
            if i % 4 == 0:
                cx, cy = x0 + size, y0 + size
                arc_x = cx - r * np.cos(theta)
                arc_y = cy - r * np.sin(theta)
            elif i % 4 == 1:
                cx, cy = x0, y0 + size
                arc_x = cx + r * np.sin(theta)
                arc_y = cy - r * np.cos(theta)
            elif i % 4 == 2:
                cx, cy = x0, y0
                arc_x = cx + r * np.cos(theta)
                arc_y = cy + r * np.sin(theta)
            else:
                cx, cy = x0 + size, y0
                arc_x = cx - r * np.sin(theta)
                arc_y = cy + r * np.cos(theta)

            ax3.plot(arc_x, arc_y, "r-", linewidth=2)

            if i % 4 == 0:
                x0 += size
            elif i % 4 == 1:
                y0 += size
            elif i % 4 == 2:
                x0 -= fib[i + 2] if i + 2 < len(fib) else size
            else:
                y0 -= fib[i + 2] if i + 2 < len(fib) else size

        ax3.set_aspect("equal")
        ax3.set_title("Golden Spiral")
        ax3.grid(True, alpha=0.2)
        st.pyplot(fig3)
        plt.close(fig3)

    with tab3:
        st.markdown("Generate fractal patterns using iterative mathematics.")
        fractal_type = st.radio("Fractal", ["Mandelbrot Set", "Sierpinski Triangle"],
                                horizontal=True)

        if fractal_type == "Mandelbrot Set":
            c1, c2 = st.columns(2)
            x_center = c1.slider("x center", -2.0, 1.0, -0.5, 0.01)
            y_center = c2.slider("y center", -1.5, 1.5, 0.0, 0.01)
            zoom = st.slider("Zoom level", 0.1, 50.0, 1.0, 0.1)

            res = 300
            x_range = 2.0 / zoom
            y_range = 2.0 / zoom
            x = np.linspace(x_center - x_range, x_center + x_range, res)
            y = np.linspace(y_center - y_range, y_center + y_range, res)
            X, Y = np.meshgrid(x, y)
            C = X + 1j * Y

            Z = np.zeros_like(C)
            M = np.zeros(C.shape, dtype=int)
            max_iter = 80

            for i in range(max_iter):
                mask = np.abs(Z) <= 2
                Z[mask] = Z[mask] ** 2 + C[mask]
                M[mask] = i + 1

            fig4, ax4 = plt.subplots(figsize=(7, 7))
            ax4.imshow(M, extent=[x.min(), x.max(), y.min(), y.max()],
                       cmap="hot", origin="lower")
            ax4.set_xlabel("Re")
            ax4.set_ylabel("Im")
            ax4.set_title("Mandelbrot Set")
            st.pyplot(fig4)
            plt.close(fig4)

            st.latex(r"z_{n+1} = z_n^2 + c")

        else:  # Sierpinski Triangle
            n_points = st.slider("Points to plot", 1000, 50000, 10000, 1000)

            vertices = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2]])
            point = np.random.rand(2)
            points = np.zeros((n_points, 2))

            for i in range(n_points):
                vertex = vertices[np.random.randint(3)]
                point = (point + vertex) / 2
                points[i] = point

            fig5, ax5 = plt.subplots(figsize=(7, 6))
            ax5.scatter(points[:, 0], points[:, 1], s=0.1, c="blue", alpha=0.5)
            ax5.set_aspect("equal")
            ax5.set_title("Sierpinski Triangle (Chaos Game)")
            ax5.axis("off")
            st.pyplot(fig5)
            plt.close(fig5)

            st.info("The Sierpinski triangle emerges from a simple rule: "
                    "repeatedly move halfway toward a randomly chosen vertex.")
