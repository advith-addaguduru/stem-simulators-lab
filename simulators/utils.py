"""Shared utility functions for STEM simulators."""
import matplotlib.pyplot as plt


def nice_axes(ax, xlab, ylab, title=None):
    """Apply consistent formatting to a matplotlib axes object."""
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    if title:
        ax.set_title(title)
    ax.grid(True, alpha=0.25)


def close_fig(fig):
    """Close a matplotlib figure to free memory in long-running Streamlit processes."""
    plt.close(fig)
