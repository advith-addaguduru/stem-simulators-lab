"""Maths: Coordinate Geometry - Distance and Line Equations"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def simulate():
    st.subheader("Coordinate Geometry: Points, Lines & Distances")
    st.latex(r"d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2} \quad;\quad y = mx + c")
    
    mode = st.radio("Select tool", ["Distance & Midpoint", "Line Equations", "Intersection"], horizontal=True)
    
    if mode == "Distance & Midpoint":
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Point 1:**")
            x1 = st.number_input("x₁", -10.0, 10.0, 1.0, key='x1')
            y1 = st.number_input("y₁", -10.0, 10.0, 2.0, key='y1')
        
        with col2:
            st.write("**Point 2:**")
            x2 = st.number_input("x₂", -10.0, 10.0, 4.0, key='x2')
            y2 = st.number_input("y₂", -10.0, 10.0, 6.0, key='y2')
        
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        col1, col2 = st.columns(2)
        col1.metric("Distance", f"{distance:.3f}")
        col2.metric("Midpoint", f"({mid_x:.2f}, {mid_y:.2f})")
        
        # Plot
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.scatter([x1, x2], [y1, y2], s=200, c=['blue', 'red'], zorder=3)
        ax.plot([x1, x2], [y1, y2], 'k--', alpha=0.5)
        ax.scatter([mid_x], [mid_y], s=150, c='green', marker='s', zorder=3, label='Midpoint')
        ax.set_xlim(-11, 11)
        ax.set_ylim(-11, 11)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'Distance = {distance:.3f}')
        ax.legend()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    
    elif mode == "Line Equations":
        st.write("**Two-point form or Slope-intercept form**")
        
        form = st.radio("Input method", ["Two points", "Slope & Intercept"], horizontal=True)
        
        if form == "Two points":
            col1, col2 = st.columns(2)
            with col1:
                x1 = st.number_input("x₁", -10.0, 10.0, 1.0, key='x1_line')
                y1 = st.number_input("y₁", -10.0, 10.0, 2.0, key='y1_line')
            with col2:
                x2 = st.number_input("x₂", -10.0, 10.0, 4.0, key='x2_line')
                y2 = st.number_input("y₂", -10.0, 10.0, 6.0, key='y2_line')
            
            if x2 != x1:
                m = (y2 - y1) / (x2 - x1)
                c = y1 - m * x1
            else:
                m = float('inf')
                c = x1
        else:
            m = st.slider("Slope (m)", -5.0, 5.0, 1.0, step=0.1)
            c = st.slider("Y-intercept (c)", -10.0, 10.0, 2.0, step=0.5)
        
        col1, col2 = st.columns(2)
        if m != float('inf'):
            col1.metric("Slope (m)", f"{m:.3f}")
            col2.metric("Y-intercept (c)", f"{c:.3f}")
            st.write(f"**Equation: y = {m:.2f}x + {c:.2f}**")
            
            # Plot
            fig, ax = plt.subplots(figsize=(8, 8))
            x = np.linspace(-10, 10, 100)
            y = m * x + c
            ax.plot(x, y, 'b-', linewidth=2, label=f'y = {m:.2f}x + {c:.2f}')
            ax.scatter([0], [c], color='red', s=100, zorder=3, label='Y-intercept')
            ax.set_xlim(-10, 10)
            ax.set_ylim(-20, 20)
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.legend()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.write(f"**Vertical line: x = {c:.2f}**")
    
    else:  # Intersection
        st.write("**Find intersection of two lines**")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Line 1:**")
            m1 = st.slider("Slope m₁", -5.0, 5.0, 1.0, step=0.1, key='m1')
            c1 = st.slider("Intercept c₁", -10.0, 10.0, 2.0, step=0.5, key='c1')
        
        with col2:
            st.write("**Line 2:**")
            m2 = st.slider("Slope m₂", -5.0, 5.0, 2.0, step=0.1, key='m2')
            c2 = st.slider("Intercept c₂", -10.0, 10.0, -1.0, step=0.5, key='c2')
        
        if m1 != m2:
            x_int = (c2 - c1) / (m1 - m2)
            y_int = m1 * x_int + c1
            st.metric("Intersection point", f"({x_int:.3f}, {y_int:.3f})")
            
            # Plot
            fig, ax = plt.subplots(figsize=(8, 8))
            x = np.linspace(-10, 10, 100)
            y1 = m1 * x + c1
            y2 = m2 * x + c2
            ax.plot(x, y1, 'b-', linewidth=2, label=f'y = {m1:.2f}x + {c1:.2f}')
            ax.plot(x, y2, 'r-', linewidth=2, label=f'y = {m2:.2f}x + {c2:.2f}')
            ax.scatter([x_int], [y_int], color='green', s=200, zorder=3, label=f'Intersection ({x_int:.2f}, {y_int:.2f})')
            ax.set_xlim(-10, 10)
            ax.set_ylim(-20, 20)
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.warning("Lines are parallel! No intersection point.")
