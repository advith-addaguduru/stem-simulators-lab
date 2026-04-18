"""Cambridge A-Level Maths: Statistics & Probability"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from simulators.utils import nice_axes


def simulate():
    st.subheader("Statistics & Probability")
    st.latex(
        r"X \sim N(\mu,\sigma^2) \qquad X \sim B(n,p) \qquad "
        r"Z = \frac{X - \mu}{\sigma}"
    )

    mode = st.radio(
        "Choose a topic",
        ["Normal Distribution", "Binomial Distribution", "Hypothesis Testing"],
        horizontal=True,
    )

    if mode == "Normal Distribution":
        _normal()
    elif mode == "Binomial Distribution":
        _binomial()
    else:
        _hypothesis_testing()


def _normal():
    st.markdown("### Normal Distribution")

    with st.sidebar.expander("Normal Controls", expanded=True):
        mu = st.slider("Mean μ", -10.0, 10.0, 0.0, step=0.5)
        sigma = st.slider("Std dev σ", 0.1, 5.0, 1.0, step=0.1)
        x_val = st.slider("Find P(X < x)", mu - 4 * sigma, mu + 4 * sigma, mu, step=0.1)

    z = (x_val - mu) / sigma
    prob = stats.norm.cdf(x_val, mu, sigma)

    c1, c2, c3 = st.columns(3)
    c1.metric("P(X < x)", f"{prob:.4f}")
    c2.metric("Z-score", f"{z:.3f}")
    c3.metric("P(X > x)", f"{1 - prob:.4f}")

    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 400)
    pdf = stats.norm.pdf(x, mu, sigma)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.plot(x, pdf, linewidth=2, color="#2563eb")
    ax1.fill_between(x, pdf, where=x <= x_val, alpha=0.3, color="#3b82f6",
                     label=f"P(X < {x_val:.1f}) = {prob:.4f}")
    ax1.axvline(mu, color="grey", linestyle="--", alpha=0.5)
    ax1.axvline(x_val, color="#ef4444", linestyle="--", linewidth=1.5)
    nice_axes(ax1, "X", "Probability density",
              f"N({mu}, {sigma}²)")
    ax1.legend(fontsize=9)

    # Standard normal comparison
    z_vals = np.linspace(-4, 4, 400)
    ax2.plot(z_vals, stats.norm.pdf(z_vals, 0, 1), linewidth=2, color="#22c55e")
    ax2.fill_between(z_vals, stats.norm.pdf(z_vals, 0, 1),
                     where=z_vals <= z, alpha=0.3, color="#22c55e")
    ax2.axvline(z, color="#ef4444", linestyle="--", linewidth=1.5,
                label=f"z = {z:.2f}")
    nice_axes(ax2, "Z", "Probability density", "Standard Normal Z")
    ax2.legend()

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("**68-95-99.7 Rule:**")
    for k, pct in [(1, 68.27), (2, 95.45), (3, 99.73)]:
        st.markdown(f"- P(μ − {k}σ < X < μ + {k}σ) = {pct}%")


def _binomial():
    st.markdown("### Binomial Distribution")
    st.latex(r"P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}")

    with st.sidebar.expander("Binomial Controls", expanded=True):
        n = st.slider("Number of trials n", 1, 50, 10)
        p = st.slider("Probability of success p", 0.01, 0.99, 0.5, step=0.01)
        target_k = st.slider("Find P(X ≤ k)", 0, n, n // 2)

    mean = n * p
    var = n * p * (1 - p)
    cum_prob = stats.binom.cdf(target_k, n, p)

    c1, c2, c3 = st.columns(3)
    c1.metric("E(X) = np", f"{mean:.2f}")
    c2.metric("Var(X) = np(1−p)", f"{var:.2f}")
    c3.metric(f"P(X ≤ {target_k})", f"{cum_prob:.4f}")

    k_vals = np.arange(0, n + 1)
    pmf = stats.binom.pmf(k_vals, n, p)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    colours = ["#3b82f6" if k <= target_k else "#cbd5e1" for k in k_vals]
    ax1.bar(k_vals, pmf, color=colours, edgecolor="#333", alpha=0.8)
    ax1.axvline(mean, color="#ef4444", linestyle="--", label=f"μ = {mean:.1f}")
    nice_axes(ax1, "k", "P(X = k)", f"B({n}, {p})")
    ax1.legend()

    # CDF
    cdf = stats.binom.cdf(k_vals, n, p)
    ax2.step(k_vals, cdf, linewidth=2, color="#22c55e", where="mid")
    ax2.axhline(cum_prob, color="#ef4444", linestyle="--", alpha=0.5)
    ax2.axvline(target_k, color="#ef4444", linestyle="--", alpha=0.5)
    nice_axes(ax2, "k", "P(X ≤ k)", "Cumulative Distribution")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Normal approximation validity
    if n * p >= 5 and n * (1 - p) >= 5:
        st.info(
            f"✅ Normal approximation is valid (np = {n * p:.1f} ≥ 5, "
            f"n(1−p) = {n * (1 - p):.1f} ≥ 5). "
            f"X ≈ N({mean:.1f}, {var:.2f})"
        )
    else:
        st.warning("⚠️ Normal approximation not appropriate (np or n(1−p) < 5).")


def _hypothesis_testing():
    st.markdown("### One-sample Z-test for the Mean")
    st.latex(r"Z = \frac{\bar{X} - \mu_0}{\sigma / \sqrt{n}}")

    with st.sidebar.expander("Test Controls", expanded=True):
        mu_0 = st.number_input("Null hypothesis μ₀", value=50.0, step=1.0)
        x_bar = st.number_input("Sample mean x̄", value=52.5, step=0.5)
        sigma = st.number_input("Population σ", value=10.0, min_value=0.1, step=0.5)
        n = st.number_input("Sample size n", value=30, min_value=2, step=1)
        alpha = st.selectbox("Significance level α", [0.01, 0.05, 0.10], index=1)
        tail = st.radio("Test type", ["Two-tailed", "One-tailed (right)", "One-tailed (left)"])

    se = sigma / np.sqrt(n)
    z_stat = (x_bar - mu_0) / se

    if tail == "Two-tailed":
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        z_crit = stats.norm.ppf(1 - alpha / 2)
        reject = abs(z_stat) > z_crit
    elif tail == "One-tailed (right)":
        p_value = 1 - stats.norm.cdf(z_stat)
        z_crit = stats.norm.ppf(1 - alpha)
        reject = z_stat > z_crit
    else:
        p_value = stats.norm.cdf(z_stat)
        z_crit = -stats.norm.ppf(1 - alpha)
        reject = z_stat < z_crit

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Z-statistic", f"{z_stat:.3f}")
    c2.metric("p-value", f"{p_value:.4f}")
    c3.metric("Critical z", f"±{abs(z_crit):.3f}" if tail == "Two-tailed" else f"{z_crit:.3f}")
    c4.metric("Decision", "Reject H₀" if reject else "Do not reject")

    fig, ax = plt.subplots(figsize=(10, 5))
    z_range = np.linspace(-4, 4, 400)
    pdf = stats.norm.pdf(z_range, 0, 1)
    ax.plot(z_range, pdf, linewidth=2, color="#2563eb")

    if tail == "Two-tailed":
        ax.fill_between(z_range, pdf, where=np.abs(z_range) >= z_crit,
                        alpha=0.3, color="#ef4444", label=f"Rejection region (α = {alpha})")
    elif tail == "One-tailed (right)":
        ax.fill_between(z_range, pdf, where=z_range >= z_crit,
                        alpha=0.3, color="#ef4444", label=f"Rejection region (α = {alpha})")
    else:
        ax.fill_between(z_range, pdf, where=z_range <= z_crit,
                        alpha=0.3, color="#ef4444", label=f"Rejection region (α = {alpha})")

    ax.axvline(z_stat, color="#f59e0b", linewidth=2, linestyle="--",
               label=f"Z = {z_stat:.3f}")
    nice_axes(ax, "Z", "Density", f"Hypothesis Test: {tail}")
    ax.legend()

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    if reject:
        st.error(f"**Reject H₀** at α = {alpha}. p-value ({p_value:.4f}) < α ({alpha}).")
    else:
        st.success(f"**Do not reject H₀** at α = {alpha}. p-value ({p_value:.4f}) ≥ α ({alpha}).")
