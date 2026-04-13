#!/usr/bin/env python3
"""
Laboratorio: Multi-Armed Bandits (imágenes para las notas)

Uso:
    cd clase/17_multi_armed_bandits
    python3 lab_bandits.py

Genera 27 imágenes en:
    clase/17_multi_armed_bandits/images/

Dependencias: numpy, matplotlib, scipy
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import numpy as np
from scipy import stats

# ---------------------------------------------------------------------------
# Shared styling
# ---------------------------------------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 11

COLORS = {
    "blue":   "#2E86AB",
    "red":    "#E94F37",
    "green":  "#27AE60",
    "gray":   "#7F8C8D",
    "orange": "#F39C12",
    "purple": "#8E44AD",
    "light":  "#ECF0F1",
    "dark":   "#2C3E50",
    "teal":   "#1ABC9C",
    "pink":   "#E91E8C",
}

# Arm-specific colors (consistent across all figures)
ARM_COLORS = [COLORS["red"], COLORS["orange"], COLORS["blue"]]
ARM_LABELS = ["Brazo A", "Brazo B", "Brazo C"]

ROOT = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

np.random.seed(42)

# Canonical problems
BERNOULLI_MUS = [0.3, 0.5, 0.7]
GAUSSIAN_MUS = [1.0, 2.0, 3.0]
GAUSSIAN_SIGMA = 1.5
T_HORIZON = 1000
N_RUNS = 200


def _save(fig, name: str) -> None:
    out = IMAGES_DIR / name
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"✓  {out.name}")


# ---------------------------------------------------------------------------
# Bandit simulation helpers
# ---------------------------------------------------------------------------

def _pull_bernoulli(mus, arm, rng):
    """Pull arm from Bernoulli bandit, return reward 0 or 1."""
    return 1 if rng.random() < mus[arm] else 0


def _pull_gaussian(mus, sigma, arm, rng):
    """Pull arm from Gaussian bandit, return continuous reward."""
    return rng.normal(mus[arm], sigma)


def _run_epsilon_greedy(mus, T, eps, seed, reward_type="bernoulli", sigma=1.5):
    """Run epsilon-greedy on a bandit problem.

    Returns: arms_pulled, rewards, cumulative_regret
    """
    rng = np.random.RandomState(seed)
    K = len(mus)
    mu_star = max(mus)
    Q = np.zeros(K)
    N = np.zeros(K, dtype=int)
    arms_pulled = np.zeros(T, dtype=int)
    rewards = np.zeros(T)
    cum_regret = np.zeros(T)

    for t in range(T):
        if rng.random() < eps:
            a = rng.randint(K)
        else:
            a = np.argmax(Q)

        if reward_type == "bernoulli":
            r = _pull_bernoulli(mus, a, rng)
        else:
            r = _pull_gaussian(mus, sigma, a, rng)

        N[a] += 1
        Q[a] += (r - Q[a]) / N[a]
        arms_pulled[t] = a
        rewards[t] = r
        cum_regret[t] = (cum_regret[t - 1] if t > 0 else 0) + (mu_star - mus[a])

    return arms_pulled, rewards, cum_regret


def _run_ucb1(mus, T, seed, reward_type="bernoulli", sigma=1.5):
    """Run UCB1 on a bandit problem.

    Returns: arms_pulled, rewards, cumulative_regret, ucb_values_history
    """
    rng = np.random.RandomState(seed)
    K = len(mus)
    mu_star = max(mus)
    Q = np.zeros(K)
    N = np.zeros(K, dtype=int)
    arms_pulled = np.zeros(T, dtype=int)
    rewards = np.zeros(T)
    cum_regret = np.zeros(T)
    ucb_history = np.zeros((T, K))
    q_history = np.zeros((T, K))

    for t in range(T):
        if t < K:
            a = t
        else:
            ucb_vals = Q + np.sqrt(2 * np.log(t) / np.maximum(N, 1))
            a = np.argmax(ucb_vals)

        if reward_type == "bernoulli":
            r = _pull_bernoulli(mus, a, rng)
        else:
            r = _pull_gaussian(mus, sigma, a, rng)

        N[a] += 1
        Q[a] += (r - Q[a]) / N[a]
        arms_pulled[t] = a
        rewards[t] = r
        cum_regret[t] = (cum_regret[t - 1] if t > 0 else 0) + (mu_star - mus[a])
        ucb_history[t] = Q + np.sqrt(2 * np.log(t + 1) / np.maximum(N, 1))
        q_history[t] = Q.copy()

    return arms_pulled, rewards, cum_regret, ucb_history, q_history


def _run_klucb(mus, T, seed, reward_type="bernoulli"):
    """Run KL-UCB on a Bernoulli bandit problem.

    Returns: arms_pulled, rewards, cumulative_regret
    """
    rng = np.random.RandomState(seed)
    K = len(mus)
    mu_star = max(mus)
    Q = np.zeros(K)
    N = np.zeros(K, dtype=int)
    arms_pulled = np.zeros(T, dtype=int)
    rewards = np.zeros(T)
    cum_regret = np.zeros(T)

    def _kl_bernoulli(p, q):
        """KL divergence between Bernoulli(p) and Bernoulli(q)."""
        p = np.clip(p, 1e-10, 1 - 1e-10)
        q = np.clip(q, 1e-10, 1 - 1e-10)
        return p * np.log(p / q) + (1 - p) * np.log((1 - p) / (1 - q))

    def _kl_ucb_bound(p_hat, n_i, t):
        """Find q that maximizes: q s.t. KL(p_hat, q) <= log(t)/n_i."""
        if n_i == 0:
            return 1.0
        threshold = np.log(t) / n_i
        lo, hi = p_hat, 1.0
        for _ in range(32):
            mid = (lo + hi) / 2
            if _kl_bernoulli(p_hat, mid) <= threshold:
                lo = mid
            else:
                hi = mid
        return lo

    for t in range(T):
        if t < K:
            a = t
        else:
            kl_vals = np.array([_kl_ucb_bound(Q[i], N[i], t) for i in range(K)])
            a = np.argmax(kl_vals)

        r = _pull_bernoulli(mus, a, rng)
        N[a] += 1
        Q[a] += (r - Q[a]) / N[a]
        arms_pulled[t] = a
        rewards[t] = r
        cum_regret[t] = (cum_regret[t - 1] if t > 0 else 0) + (mu_star - mus[a])

    return arms_pulled, rewards, cum_regret


def _run_thompson(mus, T, seed, reward_type="bernoulli", sigma=1.5):
    """Run Thompson Sampling on a bandit problem.

    Returns: arms_pulled, rewards, cumulative_regret, alpha_history, beta_history
    """
    rng = np.random.RandomState(seed)
    K = len(mus)
    mu_star = max(mus)
    arms_pulled = np.zeros(T, dtype=int)
    rewards = np.zeros(T)
    cum_regret = np.zeros(T)

    if reward_type == "bernoulli":
        alpha = np.ones(K)
        beta_param = np.ones(K)
        alpha_hist = np.zeros((T + 1, K))
        beta_hist = np.zeros((T + 1, K))
        alpha_hist[0] = alpha.copy()
        beta_hist[0] = beta_param.copy()

        for t in range(T):
            theta = np.array([rng.beta(alpha[i], beta_param[i]) for i in range(K)])
            a = np.argmax(theta)
            r = _pull_bernoulli(mus, a, rng)
            alpha[a] += r
            beta_param[a] += 1 - r
            arms_pulled[t] = a
            rewards[t] = r
            cum_regret[t] = (cum_regret[t - 1] if t > 0 else 0) + (mu_star - mus[a])
            alpha_hist[t + 1] = alpha.copy()
            beta_hist[t + 1] = beta_param.copy()

        return arms_pulled, rewards, cum_regret, alpha_hist, beta_hist
    else:
        # Normal-Normal conjugacy (known sigma)
        mu_prior = np.zeros(K)
        sigma_prior = np.ones(K) * 10.0  # vague prior
        n_obs = np.zeros(K, dtype=int)
        sum_obs = np.zeros(K)
        mu_post_hist = np.zeros((T + 1, K))
        sigma_post_hist = np.zeros((T + 1, K))
        mu_post_hist[0] = mu_prior.copy()
        sigma_post_hist[0] = sigma_prior.copy()

        for t in range(T):
            theta = np.array([rng.normal(mu_prior[i], sigma_prior[i]) for i in range(K)])
            a = np.argmax(theta)
            r = _pull_gaussian(mus, sigma, a, rng)
            n_obs[a] += 1
            sum_obs[a] += r
            # Posterior from scratch: Normal-Normal conjugacy with original prior
            total_prec = 1.0 / (10.0 ** 2) + n_obs[a] / (sigma ** 2)
            sigma_prior[a] = 1.0 / np.sqrt(total_prec)
            mu_prior[a] = (0.0 / (10.0 ** 2) + sum_obs[a] / (sigma ** 2)) / total_prec

            arms_pulled[t] = a
            rewards[t] = r
            cum_regret[t] = (cum_regret[t - 1] if t > 0 else 0) + (mu_star - mus[a])
            mu_post_hist[t + 1] = mu_prior.copy()
            sigma_post_hist[t + 1] = sigma_prior.copy()

        return arms_pulled, rewards, cum_regret, mu_post_hist, sigma_post_hist


def _run_exp3(mus, T, seed, gamma=None, reward_type="bernoulli", sigma=1.5,
              adversarial_rewards=None):
    """Run EXP3 on a bandit problem.

    Args:
        adversarial_rewards: if provided, shape (T, K) of adversarial rewards
                             overriding stochastic pulls.

    Returns: arms_pulled, rewards, cumulative_regret, weight_history
    """
    rng = np.random.RandomState(seed)
    K = len(mus)
    mu_star = max(mus)
    if gamma is None:
        gamma = min(1.0, np.sqrt(K * np.log(K) / max(T, 1)))
    w = np.ones(K)
    arms_pulled = np.zeros(T, dtype=int)
    rewards = np.zeros(T)
    cum_regret = np.zeros(T)
    weight_hist = np.zeros((T + 1, K))
    weight_hist[0] = w.copy()

    for t in range(T):
        # Compute mixed strategy
        w_sum = np.sum(w)
        p = (1 - gamma) * (w / w_sum) + gamma / K

        # Sample arm from distribution p
        a = rng.choice(K, p=p)

        # Get reward
        if adversarial_rewards is not None:
            r = adversarial_rewards[t, a]
        elif reward_type == "bernoulli":
            r = _pull_bernoulli(mus, a, rng)
        else:
            r = _pull_gaussian(mus, sigma, a, rng)

        # Importance-weighted reward estimate
        r_hat = r / p[a]

        # Update weight (only for the pulled arm)
        w[a] *= np.exp(gamma * r_hat / K)

        # Prevent overflow
        w = w / np.max(w) * 1e6 if np.max(w) > 1e10 else w

        arms_pulled[t] = a
        rewards[t] = r
        if adversarial_rewards is not None:
            cum_regret[t] = (cum_regret[t - 1] if t > 0 else 0) + \
                            (np.max(adversarial_rewards[t]) - adversarial_rewards[t, a])
        else:
            cum_regret[t] = (cum_regret[t - 1] if t > 0 else 0) + (mu_star - mus[a])
        weight_hist[t + 1] = w.copy()

    return arms_pulled, rewards, cum_regret, weight_hist


def _run_multi(runner, mus, T, n_runs, reward_type="bernoulli", sigma=1.5,
               **kwargs):
    """Run an algorithm n_runs times, return matrix of cumulative regrets."""
    all_regrets = np.zeros((n_runs, T))
    all_arms = np.zeros((n_runs, T), dtype=int)
    for run in range(n_runs):
        result = runner(mus, T, seed=run, reward_type=reward_type,
                        sigma=sigma, **kwargs)
        all_arms[run] = result[0]
        all_regrets[run] = result[2]
    return all_arms, all_regrets


# ---------------------------------------------------------------------------
# Section 01 figures
# ---------------------------------------------------------------------------

def plot_26_reward_distributions():
    """Side-by-side comparison of common reward distributions for bandits."""
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))

    # --- Bernoulli ---
    ax = axes[0]
    p = 0.7
    ax.bar([0, 1], [1 - p, p], color=[COLORS["red"], COLORS["blue"]],
           width=0.5, edgecolor=COLORS["dark"], linewidth=1.2)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["0 (fracaso)", "1 (éxito)"], fontsize=9)
    ax.set_ylabel("Probabilidad", fontsize=10)
    ax.set_title("Bernoulli($p=0.7$)", fontsize=12, fontweight="bold")
    ax.set_ylim(0, 1.0)
    ax.text(0.5, 0.85, "$r \\in \\{0, 1\\}$", ha="center", fontsize=10,
            transform=ax.transAxes, color=COLORS["gray"])

    # --- Gaussian ---
    ax = axes[1]
    x = np.linspace(-3, 7, 300)
    mu, sigma = 2.0, 1.5
    y = stats.norm.pdf(x, mu, sigma)
    ax.plot(x, y, color=COLORS["blue"], linewidth=2.5)
    ax.fill_between(x, y, alpha=0.2, color=COLORS["blue"])
    ax.axvline(mu, color=COLORS["dark"], linestyle="--", alpha=0.6, linewidth=1)
    ax.set_title(f"Normal($\\mu={mu},\\sigma={sigma}$)", fontsize=12,
                 fontweight="bold")
    ax.set_xlabel("$r$", fontsize=10)
    ax.text(0.5, 0.85, "$r \\in (-\\infty, \\infty)$", ha="center", fontsize=10,
            transform=ax.transAxes, color=COLORS["gray"])

    # --- Poisson ---
    ax = axes[2]
    lam = 3.0
    k = np.arange(0, 12)
    pmf = stats.poisson.pmf(k, lam)
    ax.bar(k, pmf, color=COLORS["green"], edgecolor=COLORS["dark"],
           linewidth=0.8, width=0.7)
    ax.axvline(lam, color=COLORS["dark"], linestyle="--", alpha=0.6, linewidth=1)
    ax.set_title(f"Poisson($\\lambda={lam:.0f}$)", fontsize=12,
                 fontweight="bold")
    ax.set_xlabel("$r$", fontsize=10)
    ax.text(0.5, 0.85, "$r \\in \\{0,1,2,\\ldots\\}$", ha="center", fontsize=10,
            transform=ax.transAxes, color=COLORS["gray"])

    # --- Exponential ---
    ax = axes[3]
    rate = 0.5
    x = np.linspace(0, 8, 300)
    y = stats.expon.pdf(x, scale=1 / rate)
    ax.plot(x, y, color=COLORS["orange"], linewidth=2.5)
    ax.fill_between(x, y, alpha=0.2, color=COLORS["orange"])
    ax.axvline(1 / rate, color=COLORS["dark"], linestyle="--", alpha=0.6,
               linewidth=1)
    ax.set_title(f"Exponencial($\\lambda={rate}$)", fontsize=12,
                 fontweight="bold")
    ax.set_xlabel("$r$", fontsize=10)
    ax.text(0.5, 0.85, "$r \\in [0, \\infty)$", ha="center", fontsize=10,
            transform=ax.transAxes, color=COLORS["gray"])

    fig.suptitle("Distribuciones de recompensa comunes en bandidos",
                 fontsize=14, fontweight="bold", y=1.04)
    fig.tight_layout()
    _save(fig, "26_reward_distributions.png")


def plot_27_kl_divergence():
    """KL divergence: asymmetry and behavior for Bernoulli distributions."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # --- Left panel: KL(p, q) as heatmap showing asymmetry ---
    ax = axes[0]
    n = 200
    p_vals = np.linspace(0.01, 0.99, n)
    q_vals = np.linspace(0.01, 0.99, n)
    P, Q = np.meshgrid(p_vals, q_vals)
    KL = P * np.log(P / Q) + (1 - P) * np.log((1 - P) / (1 - Q))
    KL = np.clip(KL, 0, 3)  # clip for display

    im = ax.contourf(P, Q, KL, levels=20, cmap="YlOrRd")
    fig.colorbar(im, ax=ax, label="KL$(p \\| q)$", shrink=0.85)

    # Show asymmetry: mark two specific points with p+q != 1
    p1, q1 = 0.3, 0.8
    p2, q2 = 0.8, 0.3
    kl1 = p1 * np.log(p1 / q1) + (1 - p1) * np.log((1 - p1) / (1 - q1))
    kl2 = p2 * np.log(p2 / q2) + (1 - p2) * np.log((1 - p2) / (1 - q2))
    ax.plot(p1, q1, "o", color=COLORS["blue"], markersize=10, zorder=5)
    ax.plot(p2, q2, "s", color=COLORS["green"], markersize=10, zorder=5)
    ax.annotate(f"KL(0.3 || 0.8) = {kl1:.3f}",
                xy=(p1, q1), xytext=(0.05, 0.90),
                fontsize=10, color=COLORS["blue"], fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=COLORS["blue"]))
    ax.annotate(f"KL(0.8 || 0.3) = {kl2:.3f}",
                xy=(p2, q2), xytext=(0.42, 0.18),
                fontsize=10, color=COLORS["green"], fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=COLORS["green"]))
    ax.plot([0, 1], [0, 1], "--", color=COLORS["gray"], alpha=0.5,
            linewidth=1)
    ax.set_xlabel("$p$", fontsize=12)
    ax.set_ylabel("$q$", fontsize=12)
    ax.set_title("KL$(p \\| q)$ para Bernoulli — asimetría",
                 fontsize=12, fontweight="bold")

    # --- Right panel: KL(p, q*) as function of p, fixed q* = 0.7 ---
    ax = axes[1]
    q_star = 0.7
    p_range = np.linspace(0.01, 0.99, 300)
    # Remove q_star itself to avoid log(0)
    mask = np.abs(p_range - q_star) > 0.005
    p_plot = p_range[mask]
    kl_vals = p_plot * np.log(p_plot / q_star) + \
              (1 - p_plot) * np.log((1 - p_plot) / (1 - q_star))

    ax.plot(p_plot, kl_vals, color=COLORS["blue"], linewidth=2.5)
    ax.axvline(q_star, color=COLORS["gray"], linestyle="--", alpha=0.6,
               linewidth=1)
    ax.text(q_star + 0.02, 1.5, f"$q = \\mu^{{∗}} = {q_star}$", fontsize=10,
            color=COLORS["gray"])

    # Mark canonical problem points
    for mu_i, label, color in [(0.3, "A", COLORS["red"]),
                                (0.5, "B", COLORS["orange"])]:
        kl_i = mu_i * np.log(mu_i / q_star) + \
               (1 - mu_i) * np.log((1 - mu_i) / (1 - q_star))
        ax.plot(mu_i, kl_i, "o", color=color, markersize=10, zorder=5)
        ax.annotate(f"Brazo {label}\nKL = {kl_i:.3f}",
                    xy=(mu_i, kl_i),
                    xytext=(mu_i - 0.12, kl_i + 0.35),
                    fontsize=10, color=color, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=color))

    ax.set_xlabel("$\\mu_i$ (media del brazo subóptimo)", fontsize=11)
    ax.set_ylabel("KL$(\\mu_i \\| \\mu^{∗})$", fontsize=11)
    ax.set_title(f"KL Bernoulli con $\\mu^{{∗}} = {q_star}$\n"
                 "— más cerca del óptimo → KL menor → más difícil distinguir",
                 fontsize=11, fontweight="bold")
    ax.set_ylim(0, 3)
    ax.set_xlim(0, 1)

    fig.tight_layout()
    _save(fig, "27_kl_divergence.png")


def plot_01_slot_machines():
    """Three slot machines with hidden probabilities."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.set_aspect("equal")
    ax.axis("off")

    for i, (mu, color, label) in enumerate(zip(BERNOULLI_MUS, ARM_COLORS,
                                                ["A", "B", "C"])):
        cx = 2 + i * 3.5
        # Machine body
        body = mpatches.FancyBboxPatch((cx - 0.8, 0.5), 1.6, 3.0,
                                        boxstyle="round,pad=0.15",
                                        facecolor=color, alpha=0.85,
                                        edgecolor=COLORS["dark"], linewidth=2)
        ax.add_patch(body)
        # Screen area
        screen = mpatches.FancyBboxPatch((cx - 0.55, 2.2), 1.1, 0.9,
                                          boxstyle="round,pad=0.08",
                                          facecolor="white", alpha=0.9,
                                          edgecolor=COLORS["dark"], linewidth=1)
        ax.add_patch(screen)
        # Question mark (hidden probability)
        ax.text(cx, 2.65, "?", ha="center", va="center",
                fontsize=28, fontweight="bold", color=COLORS["dark"])
        # Label
        ax.text(cx, 4.0, f"Brazo {label}", ha="center", va="center",
                fontsize=13, fontweight="bold", color="white")
        # Hidden probability (shown faintly below)
        ax.text(cx, 0.15, f"μ{label} = {mu}", ha="center", va="center",
                fontsize=10, color=COLORS["gray"], style="italic")
        # Lever (circle on right side)
        lever = plt.Circle((cx + 0.95, 1.5), 0.12, color=COLORS["dark"],
                           zorder=5)
        ax.add_patch(lever)
        ax.plot([cx + 0.95, cx + 0.95], [1.62, 2.2], color=COLORS["dark"],
                linewidth=3, zorder=4)

    # Title
    ax.text(6, 4.8, "Problema canónico: 3 brazos Bernoulli",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color=COLORS["dark"])
    ax.text(6, -0.3, "(el agente NO conoce estas probabilidades)",
            ha="center", va="center", fontsize=10, color=COLORS["gray"],
            style="italic")

    _save(fig, "01_slot_machines.png")


def plot_02_gaussian_densities():
    """Three overlapping Gaussian density curves."""
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.linspace(-4, 8, 500)

    for i, (mu, color, label) in enumerate(zip(GAUSSIAN_MUS, ARM_COLORS,
                                                ARM_LABELS)):
        y = stats.norm.pdf(x, mu, GAUSSIAN_SIGMA)
        ax.plot(x, y, color=color, linewidth=2.5, label=f"{label}: μ={mu}")
        ax.fill_between(x, y, alpha=0.15, color=color)
        ax.axvline(mu, color=color, linestyle="--", alpha=0.5, linewidth=1)

    ax.set_xlabel("Recompensa $r$", fontsize=12)
    ax.set_ylabel("Densidad $p(r)$", fontsize=12)
    ax.set_title("Problema canónico: 3 brazos Gaussianos "
                 "(μ = 1.0, 2.0, 3.0;  σ = 1.5)", fontsize=13)
    ax.legend(fontsize=11, loc="upper right")
    ax.set_xlim(-4, 8)

    # Annotate overlap
    ax.annotate("Las distribuciones se\nsolapan significativamente\n→ difícil distinguir brazos",
                xy=(2.0, 0.12), xytext=(5.5, 0.2),
                fontsize=9, color=COLORS["gray"],
                arrowprops=dict(arrowstyle="->", color=COLORS["gray"]),
                bbox=dict(boxstyle="round,pad=0.3", facecolor=COLORS["light"],
                          edgecolor=COLORS["gray"]))

    _save(fig, "02_gaussian_densities.png")


def plot_03_explore_exploit_spectrum():
    """Conceptual exploration-exploitation spectrum."""
    fig, ax = plt.subplots(figsize=(13, 4))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(0, 4)
    ax.axis("off")

    # Gradient bar
    for i in range(200):
        x = 1 + i * 8 / 200
        ratio = i / 200
        r1, g1, b1 = mcolors.to_rgb(COLORS["blue"])
        r2, g2, b2 = mcolors.to_rgb(COLORS["green"])
        c = (r1 + ratio * (r2 - r1), g1 + ratio * (g2 - g1),
             b1 + ratio * (b2 - b1))
        ax.add_patch(mpatches.Rectangle((x, 1.5), 8 / 200, 0.8,
                                         facecolor=c, edgecolor="none"))

    # Labels — placed outside the gradient bar to avoid overlap
    ax.text(0.4, 1.9, "Exploración\npura", ha="center", va="center",
            fontsize=11, fontweight="bold", color=COLORS["blue"])
    ax.text(9.6, 1.9, "Explotación\npura", ha="center", va="center",
            fontsize=11, fontweight="bold", color=COLORS["green"])
    ax.text(5, 1.9, "Balance\nóptimo", ha="center", va="center",
            fontsize=12, fontweight="bold", color="white")

    # Descriptions
    ax.text(0.4, 0.8, "Probar todo por igual\n→ mucha información\n→ poco reward",
            ha="center", va="center", fontsize=9, color=COLORS["gray"])
    ax.text(9.6, 0.8, "Siempre el mejor actual\n→ máximo reward inmediato\n→ riesgo de error",
            ha="center", va="center", fontsize=9, color=COLORS["gray"])
    ax.text(5, 0.6, "Algoritmos de bandidos:\nexplorar lo suficiente,\nexplotar lo aprendido",
            ha="center", va="center", fontsize=10, color=COLORS["dark"],
            bbox=dict(boxstyle="round,pad=0.4", facecolor=COLORS["light"],
                      edgecolor=COLORS["dark"]))

    # Arrow
    ax.annotate("", xy=(9, 2.6), xytext=(1, 2.6),
                arrowprops=dict(arrowstyle="<->", color=COLORS["dark"],
                                linewidth=2))
    ax.text(5, 3.2, "El dilema de exploración vs. explotación",
            ha="center", fontsize=13, fontweight="bold", color=COLORS["dark"])

    _save(fig, "03_explore_exploit_spectrum.png")


def plot_04_pure_strategies():
    """Cumulative reward: pure exploit vs explore vs oracle."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    mus_list = [BERNOULLI_MUS, GAUSSIAN_MUS]
    titles = ["Bernoulli (μ = 0.3, 0.5, 0.7)", "Gaussiano (μ = 1.0, 2.0, 3.0; σ = 1.5)"]

    for ax, mus, title in zip(axes, mus_list, titles):
        T = T_HORIZON
        t_vals = np.arange(1, T + 1)
        mu_star = max(mus)
        K = len(mus)

        # Oracle: always best arm
        oracle = mu_star * t_vals

        # Pure exploration: round-robin
        explore_mean = np.mean(mus)
        explore = explore_mean * t_vals

        # Pure exploitation of worst arm (worst-case greedy start)
        mu_worst = min(mus)
        exploit_worst = mu_worst * t_vals

        ax.plot(t_vals, oracle, color=COLORS["green"], linewidth=2.5,
                label=f"Oráculo (siempre brazo óptimo, μ∗={mu_star})")
        ax.plot(t_vals, explore, color=COLORS["blue"], linewidth=2,
                linestyle="--",
                label=f"Exploración pura (round-robin, μ̄={explore_mean:.2f})")
        ax.plot(t_vals, exploit_worst, color=COLORS["orange"], linewidth=2,
                linestyle="-.",
                label=f"Explotación ciega (peor brazo, μ={mu_worst})")
        ax.fill_between(t_vals, exploit_worst, oracle, alpha=0.08,
                        color=COLORS["red"])
        ax.set_xlabel("Ronda $t$", fontsize=11)
        ax.set_ylabel("Recompensa acumulada", fontsize=11)
        ax.set_title(title, fontsize=12)
        ax.legend(fontsize=9, loc="upper left")
        ax.annotate("Regret\nacumulado",
                    xy=(700, (oracle[699] + exploit_worst[699]) / 2),
                    fontsize=9, color=COLORS["red"], fontweight="bold",
                    ha="center")

    fig.suptitle("Estrategias puras: ningún extremo es óptimo", fontsize=14,
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "04_pure_strategies.png")


def plot_05_regret_decomposition():
    """Regret decomposition by arm (stacked bar)."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, strategy_name, eps in zip(axes,
                                       ["ε-greedy (ε=0.1)", "ε-greedy (ε=0.3)"],
                                       [0.1, 0.3]):
        arms, _, regret = _run_epsilon_greedy(BERNOULLI_MUS, T_HORIZON, eps,
                                              seed=42)
        mu_star = max(BERNOULLI_MUS)
        K = len(BERNOULLI_MUS)
        pulls = [np.sum(arms == i) for i in range(K)]
        gaps = [mu_star - BERNOULLI_MUS[i] for i in range(K)]
        regret_per_arm = [pulls[i] * gaps[i] for i in range(K)]

        bars = ax.bar(ARM_LABELS, regret_per_arm, color=ARM_COLORS, alpha=0.85,
                      edgecolor=COLORS["dark"], linewidth=1.2)
        for bar, n, g in zip(bars, pulls, gaps):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 1,
                    f"N={n}\nΔ={g:.1f}",
                    ha="center", va="bottom", fontsize=9)

        ax.set_ylabel("Contribución al regret ($\\Delta_i \\cdot N_i$)",
                      fontsize=11)
        ax.set_title(f"{strategy_name}\nRegret total = {regret[-1]:.1f}",
                     fontsize=11)

    fig.suptitle("Descomposición del regret por brazo: $R_T = \\sum_i \\Delta_i N_i(T)$",
                 fontsize=13, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "05_regret_decomposition.png")


# ---------------------------------------------------------------------------
# Section 02 figures
# ---------------------------------------------------------------------------

def plot_06_egreedy_arm_selection():
    """ε-greedy arm selection scatter plot over time."""
    fig, ax = plt.subplots(figsize=(12, 4))
    arms, _, _ = _run_epsilon_greedy(BERNOULLI_MUS, T_HORIZON, 0.1, seed=42)

    for i in range(3):
        mask = arms == i
        t_vals = np.where(mask)[0]
        ax.scatter(t_vals, np.full_like(t_vals, i), c=ARM_COLORS[i],
                   s=3, alpha=0.6, label=ARM_LABELS[i])

    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(ARM_LABELS)
    ax.set_xlabel("Ronda $t$", fontsize=11)
    ax.set_title("ε-greedy (ε = 0.1): selección de brazos — "
                 "exploración ciega a lo largo de todo el horizonte",
                 fontsize=12)
    ax.legend(fontsize=10, loc="upper right", markerscale=5)
    ax.set_xlim(0, T_HORIZON)

    # Highlight late exploration
    ax.axvspan(800, 1000, alpha=0.1, color=COLORS["red"])
    ax.text(900, 2.4, "Aún explora\nbrazos malos\nen t>800",
            ha="center", fontsize=9, color=COLORS["red"], fontweight="bold")

    _save(fig, "06_egreedy_arm_selection.png")


def plot_07_egreedy_regret_by_epsilon():
    """Cumulative regret for different epsilon values."""
    fig, ax = plt.subplots(figsize=(10, 6))
    eps_values = [0.01, 0.05, 0.1, 0.3]
    line_styles = ["-", "--", "-.", ":"]
    colors = [COLORS["blue"], COLORS["green"], COLORS["orange"], COLORS["red"]]

    for eps, ls, c in zip(eps_values, line_styles, colors):
        _, all_regrets = _run_multi(
            _run_epsilon_greedy, BERNOULLI_MUS, T_HORIZON, N_RUNS, eps=eps)
        mean_regret = np.mean(all_regrets, axis=0)
        std_regret = np.std(all_regrets, axis=0)
        t_vals = np.arange(T_HORIZON)
        ax.plot(t_vals, mean_regret, color=c, linewidth=2, linestyle=ls,
                label=f"ε = {eps}")
        ax.fill_between(t_vals, mean_regret - std_regret,
                        mean_regret + std_regret, alpha=0.1, color=c)

    ax.set_xlabel("Ronda $t$", fontsize=12)
    ax.set_ylabel("Regret acumulado $R_t$", fontsize=12)
    ax.set_title("ε-greedy: sensibilidad al parámetro ε "
                 f"({N_RUNS} ejecuciones, media ± std)", fontsize=13)
    ax.legend(fontsize=11)

    _save(fig, "07_egreedy_regret_by_epsilon.png")


def plot_08_egreedy_pull_count():
    """Arm pull counts vs optimal at T=500."""
    fig, ax = plt.subplots(figsize=(8, 5))
    arms, _, _ = _run_epsilon_greedy(BERNOULLI_MUS, 500, 0.1, seed=42)
    K = len(BERNOULLI_MUS)
    actual = [np.sum(arms == i) for i in range(K)]
    optimal = [0, 0, 500]  # All pulls on best arm

    x = np.arange(K)
    width = 0.35
    bars1 = ax.bar(x - width / 2, actual, width, color=ARM_COLORS, alpha=0.85,
                   edgecolor=COLORS["dark"], linewidth=1.2, label="ε-greedy (ε=0.1)")
    bars2 = ax.bar(x + width / 2, optimal, width, color=ARM_COLORS, alpha=0.3,
                   edgecolor=COLORS["dark"], linewidth=1.2, linestyle="--",
                   label="Óptimo (oráculo)")

    for bar, n in zip(bars1, actual):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                str(n), ha="center", fontsize=11, fontweight="bold")
    for bar, n in zip(bars2, optimal):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                str(n), ha="center", fontsize=11, color=COLORS["gray"])

    ax.set_xticks(x)
    ax.set_xticklabels(ARM_LABELS, fontsize=12)
    ax.set_ylabel("Número de veces jalado", fontsize=12)
    ax.set_title("Distribución de pulls a T=500: ε-greedy vs. óptimo", fontsize=13)
    ax.legend(fontsize=11)

    _save(fig, "08_egreedy_pull_count.png")


# ---------------------------------------------------------------------------
# Section 03 figures
# ---------------------------------------------------------------------------

def plot_09_ucb_confidence_bands():
    """UCB confidence bands per arm shrinking over time."""
    arms, _, _, ucb_hist, q_hist = _run_ucb1(BERNOULLI_MUS, T_HORIZON, seed=42)
    fig, ax = plt.subplots(figsize=(12, 6))
    t_vals = np.arange(T_HORIZON)

    for i in range(3):
        ax.plot(t_vals, q_hist[:, i], color=ARM_COLORS[i], linewidth=1.5,
                label=f"{ARM_LABELS[i]} (μ̂)")
        bonus = ucb_hist[:, i] - q_hist[:, i]
        ax.fill_between(t_vals, q_hist[:, i] - bonus, ucb_hist[:, i],
                        alpha=0.15, color=ARM_COLORS[i])
        # True value
        ax.axhline(BERNOULLI_MUS[i], color=ARM_COLORS[i], linestyle=":",
                   alpha=0.5, linewidth=1)

    ax.set_xlabel("Ronda $t$", fontsize=12)
    ax.set_ylabel("Valor estimado y banda de confianza", fontsize=12)
    ax.set_title("UCB1: las bandas de confianza se estrechan conforme "
                 "$N_i$ crece", fontsize=13)
    ax.legend(fontsize=10, loc="upper right")
    ax.set_xlim(0, T_HORIZON)
    ax.set_ylim(-0.5, 2.0)

    ax.text(800, 1.6, r"$\hat{\mu}_i \pm \sqrt{\frac{2\ln t}{N_i}}$",
            fontsize=14, color=COLORS["dark"],
            bbox=dict(boxstyle="round,pad=0.3", facecolor=COLORS["light"]))

    _save(fig, "09_ucb_confidence_bands.png")


def plot_10_ucb_vs_egreedy_selection():
    """Side-by-side arm selection: UCB1 vs ε-greedy."""
    fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

    # ε-greedy
    arms_eg, _, _ = _run_epsilon_greedy(BERNOULLI_MUS, T_HORIZON, 0.1, seed=42)
    # UCB1
    arms_ucb, _, _, _, _ = _run_ucb1(BERNOULLI_MUS, T_HORIZON, seed=42)

    for ax, arms, title in zip(axes,
                                [arms_eg, arms_ucb],
                                ["ε-greedy (ε = 0.1)", "UCB1"]):
        for i in range(3):
            mask = arms == i
            t_vals = np.where(mask)[0]
            ax.scatter(t_vals, np.full_like(t_vals, i), c=ARM_COLORS[i],
                       s=3, alpha=0.6)
        ax.set_yticks([0, 1, 2])
        ax.set_yticklabels(ARM_LABELS, fontsize=10)
        ax.set_title(title, fontsize=12, fontweight="bold")

    axes[1].set_xlabel("Ronda $t$", fontsize=11)
    fig.suptitle("Selección de brazos: exploración ciega (ε-greedy) vs. "
                 "dirigida (UCB1)", fontsize=13, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "10_ucb_vs_egreedy_selection.png")


def plot_11_ucb_vs_egreedy_regret():
    """UCB1 vs ε-greedy cumulative regret on both canonical problems."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    configs = [
        (BERNOULLI_MUS, "bernoulli", 1.5, "Bernoulli (μ = 0.3, 0.5, 0.7)"),
        (GAUSSIAN_MUS, "gaussian", GAUSSIAN_SIGMA,
         "Gaussiano (μ = 1.0, 2.0, 3.0; σ = 1.5)"),
    ]

    for ax, (mus, rtype, sig, title) in zip(axes, configs):
        # ε-greedy
        _, reg_eg = _run_multi(_run_epsilon_greedy, mus, T_HORIZON, N_RUNS,
                               reward_type=rtype, sigma=sig, eps=0.1)
        mean_eg = np.mean(reg_eg, axis=0)
        std_eg = np.std(reg_eg, axis=0)

        # UCB1
        def _ucb_wrapper(mus, T, seed, reward_type="bernoulli", sigma=1.5):
            return _run_ucb1(mus, T, seed, reward_type, sigma)[:3]
        _, reg_ucb = _run_multi(_ucb_wrapper, mus, T_HORIZON, N_RUNS,
                                reward_type=rtype, sigma=sig)
        mean_ucb = np.mean(reg_ucb, axis=0)
        std_ucb = np.std(reg_ucb, axis=0)

        t = np.arange(T_HORIZON)
        ax.plot(t, mean_eg, color=COLORS["orange"], linewidth=2,
                label="ε-greedy (ε=0.1)")
        ax.fill_between(t, mean_eg - std_eg, mean_eg + std_eg,
                        alpha=0.1, color=COLORS["orange"])
        ax.plot(t, mean_ucb, color=COLORS["blue"], linewidth=2, label="UCB1")
        ax.fill_between(t, mean_ucb - std_ucb, mean_ucb + std_ucb,
                        alpha=0.1, color=COLORS["blue"])
        ax.set_xlabel("Ronda $t$", fontsize=11)
        ax.set_ylabel("Regret acumulado $R_t$", fontsize=11)
        ax.set_title(title, fontsize=12)
        ax.legend(fontsize=10)

    fig.suptitle("UCB1 vs. ε-greedy: regret logarítmico vs. lineal "
                 f"({N_RUNS} ejecuciones)", fontsize=13,
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "11_ucb_vs_egreedy_regret.png")


def plot_12_klucb_vs_ucb1():
    """KL-UCB vs UCB1 regret comparison."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # UCB1
    def _ucb_wrapper(mus, T, seed, reward_type="bernoulli", sigma=1.5):
        return _run_ucb1(mus, T, seed, reward_type, sigma)[:3]
    _, reg_ucb = _run_multi(_ucb_wrapper, BERNOULLI_MUS, T_HORIZON, N_RUNS)
    mean_ucb = np.mean(reg_ucb, axis=0)
    std_ucb = np.std(reg_ucb, axis=0)

    # KL-UCB
    def _klucb_wrapper(mus, T, seed, reward_type="bernoulli", sigma=1.5):
        return _run_klucb(mus, T, seed, reward_type)
    _, reg_kl = _run_multi(_klucb_wrapper, BERNOULLI_MUS, T_HORIZON, N_RUNS)
    mean_kl = np.mean(reg_kl, axis=0)
    std_kl = np.std(reg_kl, axis=0)

    t = np.arange(T_HORIZON)
    ax.plot(t, mean_ucb, color=COLORS["blue"], linewidth=2, label="UCB1")
    ax.fill_between(t, mean_ucb - std_ucb, mean_ucb + std_ucb,
                    alpha=0.1, color=COLORS["blue"])
    ax.plot(t, mean_kl, color=COLORS["purple"], linewidth=2, label="KL-UCB")
    ax.fill_between(t, mean_kl - std_kl, mean_kl + std_kl,
                    alpha=0.1, color=COLORS["purple"])

    ax.set_xlabel("Ronda $t$", fontsize=12)
    ax.set_ylabel("Regret acumulado $R_t$", fontsize=12)
    ax.set_title("KL-UCB vs. UCB1: cota más ajustada usando divergencia KL "
                 f"({N_RUNS} ejecuciones)", fontsize=13)
    ax.legend(fontsize=11)

    _save(fig, "12_klucb_vs_ucb1.png")


# ---------------------------------------------------------------------------
# Section 04 figures
# ---------------------------------------------------------------------------

def plot_13_beta_posterior_evolution():
    """Beta posterior evolution: 4-panel (t=1,10,50,200), all 3 arms."""
    _, _, _, alpha_hist, beta_hist = _run_thompson(
        BERNOULLI_MUS, 200, seed=42, reward_type="bernoulli")

    time_points = [0, 10, 50, 200]
    fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharey=True)
    x = np.linspace(0, 1, 300)

    for ax, tp in zip(axes, time_points):
        for i in range(3):
            a = alpha_hist[tp, i]
            b = beta_hist[tp, i]
            y = stats.beta.pdf(x, a, b)
            ax.plot(x, y, color=ARM_COLORS[i], linewidth=2,
                    label=f"{ARM_LABELS[i]}: Beta({a:.0f},{b:.0f})")
            ax.fill_between(x, y, alpha=0.12, color=ARM_COLORS[i])
            # Mark true mu
            ax.axvline(BERNOULLI_MUS[i], color=ARM_COLORS[i],
                       linestyle=":", alpha=0.5, linewidth=1)
        ax.set_xlabel("θ", fontsize=11)
        ax.set_title(f"t = {tp}", fontsize=12, fontweight="bold")
        ax.legend(fontsize=7, loc="upper left")
        ax.set_xlim(0, 1)

    axes[0].set_ylabel("Densidad posterior", fontsize=11)
    fig.suptitle("Thompson Sampling: evolución del posterior Beta",
                 fontsize=14, fontweight="bold", y=1.05)
    fig.tight_layout()
    _save(fig, "13_beta_posterior_evolution.png")


def plot_14_thompson_samples():
    """Thompson: posterior densities with sampled points and winner."""
    _, _, _, alpha_hist, beta_hist = _run_thompson(
        BERNOULLI_MUS, 50, seed=42, reward_type="bernoulli")

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.linspace(0, 1, 300)
    rng = np.random.RandomState(123)

    # At t=50, draw samples
    samples = []
    for i in range(3):
        a = alpha_hist[50, i]
        b = beta_hist[50, i]
        y = stats.beta.pdf(x, a, b)
        ax.plot(x, y, color=ARM_COLORS[i], linewidth=2.5,
                label=f"{ARM_LABELS[i]}: Beta({a:.0f},{b:.0f})")
        ax.fill_between(x, y, alpha=0.1, color=ARM_COLORS[i])
        # Draw a sample
        theta = rng.beta(a, b)
        samples.append(theta)
        ax.plot(theta, 0, "v", color=ARM_COLORS[i], markersize=15,
                markeredgecolor=COLORS["dark"], markeredgewidth=1.5, zorder=5)
        ax.annotate(f"θ = {theta:.3f}",
                    xy=(theta, 0), xytext=(theta, -0.8),
                    fontsize=9, ha="center", color=ARM_COLORS[i],
                    fontweight="bold")

    # Highlight winner
    winner = np.argmax(samples)
    ax.annotate(f"¡{ARM_LABELS[winner]} gana!\n(θ máximo)",
                xy=(samples[winner], 0.5),
                xytext=(samples[winner] + 0.15, 3),
                fontsize=11, fontweight="bold", color=ARM_COLORS[winner],
                arrowprops=dict(arrowstyle="->", color=ARM_COLORS[winner],
                                linewidth=2))

    ax.set_xlabel("θ (tasa de éxito)", fontsize=12)
    ax.set_ylabel("Densidad posterior", fontsize=12)
    ax.set_title("Thompson Sampling (t=50): muestrear → actuar según la muestra",
                 fontsize=13)
    ax.legend(fontsize=10)
    ax.set_xlim(0, 1)

    _save(fig, "14_thompson_samples.png")


def plot_15_normal_posterior_evolution():
    """Normal-Normal posterior evolution for Gaussian canonical."""
    _, _, _, mu_hist, sigma_hist = _run_thompson(
        GAUSSIAN_MUS, 200, seed=42, reward_type="gaussian",
        sigma=GAUSSIAN_SIGMA)

    time_points = [0, 10, 50, 200]
    fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharey=True)
    x = np.linspace(-4, 8, 400)

    for ax, tp in zip(axes, time_points):
        for i in range(3):
            mu = mu_hist[tp, i]
            sig = sigma_hist[tp, i]
            if sig < 1e-6:
                sig = 1e-6
            y = stats.norm.pdf(x, mu, sig)
            ax.plot(x, y, color=ARM_COLORS[i], linewidth=2,
                    label=f"{ARM_LABELS[i]}: N({mu:.1f},{sig:.1f}²)")
            ax.fill_between(x, y, alpha=0.12, color=ARM_COLORS[i])
            ax.axvline(GAUSSIAN_MUS[i], color=ARM_COLORS[i],
                       linestyle=":", alpha=0.5, linewidth=1)
        ax.set_xlabel("μ", fontsize=11)
        ax.set_title(f"t = {tp}", fontsize=12, fontweight="bold")
        ax.legend(fontsize=7, loc="upper left")
        ax.set_xlim(-4, 8)

    axes[0].set_ylabel("Densidad posterior", fontsize=11)
    fig.suptitle("Thompson Sampling (Gaussiano): evolución del posterior Normal",
                 fontsize=14, fontweight="bold", y=1.05)
    fig.tight_layout()
    _save(fig, "15_normal_posterior_evolution.png")


def plot_16_conjugacy_diagram():
    """Conceptual prior → observe → posterior cycle."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Three boxes in a triangle
    boxes = [
        (2, 6, "Prior\n$p(\\theta)$", COLORS["blue"]),
        (8, 6, "Likelihood\n$p(r \\mid \\theta)$", COLORS["orange"]),
        (5, 1.5, "Posterior\n$p(\\theta \\mid r)$", COLORS["green"]),
    ]

    for x, y, text, color in boxes:
        box = mpatches.FancyBboxPatch((x - 1.3, y - 0.8), 2.6, 1.6,
                                       boxstyle="round,pad=0.3",
                                       facecolor=color, alpha=0.2,
                                       edgecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, text, ha="center", va="center", fontsize=13,
                fontweight="bold", color=COLORS["dark"])

    # Arrows
    ax.annotate("", xy=(6.7, 6), xytext=(3.3, 6),
                arrowprops=dict(arrowstyle="->", color=COLORS["dark"],
                                linewidth=2))
    ax.text(5, 6.5, "× Bayes", fontsize=11, ha="center",
            color=COLORS["dark"], fontweight="bold")

    ax.annotate("", xy=(5, 2.5), xytext=(8, 5.2),
                arrowprops=dict(arrowstyle="->", color=COLORS["dark"],
                                linewidth=2))
    ax.text(7.2, 3.6, "= posterior", fontsize=11, ha="center",
            color=COLORS["dark"], fontweight="bold", rotation=-40)

    ax.annotate("", xy=(2, 5.2), xytext=(5, 2.5),
                arrowprops=dict(arrowstyle="->", color=COLORS["purple"],
                                linewidth=2, linestyle="--"))
    ax.text(2.8, 3.6, "se convierte\nen nuevo prior", fontsize=10,
            ha="center", color=COLORS["purple"], fontweight="bold",
            rotation=40)

    # Conjugacy table
    table_y = 7.5
    ax.text(5, table_y, "Familias conjugadas", ha="center", fontsize=13,
            fontweight="bold", color=COLORS["dark"])

    table_data = [
        ("Bernoulli", "Beta(α,β)", "α+r, β+1−r"),
        ("Normal(μ,σ²)", "Normal(μ₀,σ₀²)", "media ponderada por precisión"),
        ("Poisson(λ)", "Gamma(α,β)", "α+r, β+1"),
    ]

    _save(fig, "16_conjugacy_diagram.png")


def plot_17_thompson_arm_frequency():
    """Stacked area: arm selection probability over time."""
    arms, _, _, _, _ = _run_thompson(BERNOULLI_MUS, T_HORIZON, seed=42,
                                     reward_type="bernoulli")

    # Compute running arm selection frequency
    window = 50
    freq = np.zeros((T_HORIZON, 3))
    for t in range(T_HORIZON):
        start = max(0, t - window)
        segment = arms[start:t + 1]
        for i in range(3):
            freq[t, i] = np.mean(segment == i)

    fig, ax = plt.subplots(figsize=(12, 5))
    t_vals = np.arange(T_HORIZON)
    ax.stackplot(t_vals, freq[:, 0], freq[:, 1], freq[:, 2],
                 colors=ARM_COLORS, alpha=0.7,
                 labels=ARM_LABELS)
    ax.set_xlabel("Ronda $t$", fontsize=12)
    ax.set_ylabel("Fracción de selección (ventana = 50)", fontsize=12)
    ax.set_title("Thompson Sampling: probability matching — "
                 "la selección converge al brazo óptimo", fontsize=13)
    ax.legend(fontsize=10, loc="center right")
    ax.set_xlim(0, T_HORIZON)
    ax.set_ylim(0, 1)

    _save(fig, "17_thompson_arm_frequency.png")


# ---------------------------------------------------------------------------
# Section 05 figures
# ---------------------------------------------------------------------------

def _run_all_algorithms(mus, T, n_runs, reward_type="bernoulli", sigma=1.5):
    """Run all 5 algorithms and return dict of (mean_regret, std_regret)."""
    results = {}

    # ε-greedy
    _, reg = _run_multi(_run_epsilon_greedy, mus, T, n_runs,
                        reward_type=reward_type, sigma=sigma, eps=0.1)
    results["ε-greedy (ε=0.1)"] = (np.mean(reg, axis=0), np.std(reg, axis=0))

    # UCB1
    def _ucb_w(mus, T, seed, reward_type="bernoulli", sigma=1.5):
        return _run_ucb1(mus, T, seed, reward_type, sigma)[:3]
    _, reg = _run_multi(_ucb_w, mus, T, n_runs,
                        reward_type=reward_type, sigma=sigma)
    results["UCB1"] = (np.mean(reg, axis=0), np.std(reg, axis=0))

    # KL-UCB (only for Bernoulli)
    if reward_type == "bernoulli":
        def _kl_w(mus, T, seed, reward_type="bernoulli", sigma=1.5):
            return _run_klucb(mus, T, seed, reward_type)
        _, reg = _run_multi(_kl_w, mus, T, n_runs,
                            reward_type=reward_type, sigma=sigma)
        results["KL-UCB"] = (np.mean(reg, axis=0), np.std(reg, axis=0))

    # Thompson
    def _ts_w(mus, T, seed, reward_type="bernoulli", sigma=1.5):
        return _run_thompson(mus, T, seed, reward_type, sigma)[:3]
    _, reg = _run_multi(_ts_w, mus, T, n_runs,
                        reward_type=reward_type, sigma=sigma)
    results["Thompson"] = (np.mean(reg, axis=0), np.std(reg, axis=0))

    # EXP3
    def _exp3_w(mus, T, seed, reward_type="bernoulli", sigma=1.5):
        return _run_exp3(mus, T, seed, reward_type=reward_type, sigma=sigma)[:3]
    _, reg = _run_multi(_exp3_w, mus, T, n_runs,
                        reward_type=reward_type, sigma=sigma)
    results["EXP3"] = (np.mean(reg, axis=0), np.std(reg, axis=0))

    return results


def plot_18_grand_regret_bernoulli():
    """Grand regret comparison on Bernoulli canonical."""
    results = _run_all_algorithms(BERNOULLI_MUS, T_HORIZON, N_RUNS,
                                  reward_type="bernoulli")

    fig, ax = plt.subplots(figsize=(12, 7))
    algo_colors = {
        "ε-greedy (ε=0.1)": COLORS["orange"],
        "UCB1": COLORS["blue"],
        "KL-UCB": COLORS["purple"],
        "Thompson": COLORS["green"],
        "EXP3": COLORS["red"],
    }

    t = np.arange(T_HORIZON)
    for name, (mean, std) in results.items():
        c = algo_colors[name]
        ax.plot(t, mean, color=c, linewidth=2, label=name)
        ax.fill_between(t, mean - std, mean + std, alpha=0.08, color=c)

    ax.set_xlabel("Ronda $t$", fontsize=12)
    ax.set_ylabel("Regret acumulado $R_t$", fontsize=12)
    ax.set_title("Comparación general: Bernoulli (μ = 0.3, 0.5, 0.7) — "
                 f"{N_RUNS} ejecuciones", fontsize=14)
    ax.legend(fontsize=11, loc="upper left")

    _save(fig, "18_grand_regret_bernoulli.png")


def plot_19_grand_regret_gaussian():
    """Grand regret comparison on Gaussian canonical."""
    results = _run_all_algorithms(GAUSSIAN_MUS, T_HORIZON, N_RUNS,
                                  reward_type="gaussian", sigma=GAUSSIAN_SIGMA)

    fig, ax = plt.subplots(figsize=(12, 7))
    algo_colors = {
        "ε-greedy (ε=0.1)": COLORS["orange"],
        "UCB1": COLORS["blue"],
        "Thompson": COLORS["green"],
        "EXP3": COLORS["red"],
    }

    t = np.arange(T_HORIZON)
    for name, (mean, std) in results.items():
        c = algo_colors.get(name, COLORS["gray"])
        ax.plot(t, mean, color=c, linewidth=2, label=name)
        ax.fill_between(t, mean - std, mean + std, alpha=0.08, color=c)

    ax.set_xlabel("Ronda $t$", fontsize=12)
    ax.set_ylabel("Regret acumulado $R_t$", fontsize=12)
    ax.set_title("Comparación general: Gaussiano (μ = 1.0, 2.0, 3.0; σ = 1.5) — "
                 f"{N_RUNS} ejecuciones", fontsize=14)
    ax.legend(fontsize=11, loc="upper left")

    _save(fig, "19_grand_regret_gaussian.png")


def plot_20_arm_selection_evolution():
    """Multi-panel: 3 algorithms × 3 time points."""
    algos = {
        "ε-greedy (ε=0.1)": lambda s: _run_epsilon_greedy(
            BERNOULLI_MUS, T_HORIZON, 0.1, s)[0],
        "UCB1": lambda s: _run_ucb1(BERNOULLI_MUS, T_HORIZON, s)[0],
        "Thompson": lambda s: _run_thompson(
            BERNOULLI_MUS, T_HORIZON, s, reward_type="bernoulli")[0],
    }
    time_points = [50, 200, 1000]

    fig, axes = plt.subplots(3, 3, figsize=(14, 10))

    for row, (algo_name, algo_fn) in enumerate(algos.items()):
        # Run multiple times to get average arm frequencies
        all_arms = np.zeros((N_RUNS, T_HORIZON), dtype=int)
        for run in range(N_RUNS):
            all_arms[run] = algo_fn(run)

        for col, tp in enumerate(time_points):
            ax = axes[row, col]
            # Compute average arm selection frequencies up to tp
            freqs = np.zeros(3)
            for i in range(3):
                freqs[i] = np.mean(all_arms[:, :tp] == i)

            bars = ax.bar(ARM_LABELS, freqs, color=ARM_COLORS, alpha=0.85,
                         edgecolor=COLORS["dark"], linewidth=1)
            for bar, f in zip(bars, freqs):
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.01,
                        f"{f:.2f}", ha="center", fontsize=9)
            ax.set_ylim(0, 1.0)
            if row == 0:
                ax.set_title(f"T = {tp}", fontsize=12, fontweight="bold")
            if col == 0:
                ax.set_ylabel(algo_name, fontsize=11, fontweight="bold")

    fig.suptitle("Evolución de la selección de brazos (fracción promedio, "
                 f"{N_RUNS} ejecuciones)", fontsize=14,
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "20_arm_selection_evolution.png")


def plot_21_optimal_pulls_pct():
    """% optimal pulls over time for all algorithms."""
    algos = {
        "ε-greedy (ε=0.1)": lambda s: _run_epsilon_greedy(
            BERNOULLI_MUS, T_HORIZON, 0.1, s)[0],
        "UCB1": lambda s: _run_ucb1(BERNOULLI_MUS, T_HORIZON, s)[0],
        "Thompson": lambda s: _run_thompson(
            BERNOULLI_MUS, T_HORIZON, s, reward_type="bernoulli")[0],
        "EXP3": lambda s: _run_exp3(
            BERNOULLI_MUS, T_HORIZON, s, reward_type="bernoulli")[0],
    }
    algo_colors = {
        "ε-greedy (ε=0.1)": COLORS["orange"],
        "UCB1": COLORS["blue"],
        "Thompson": COLORS["green"],
        "EXP3": COLORS["red"],
    }

    fig, ax = plt.subplots(figsize=(12, 6))
    optimal_arm = np.argmax(BERNOULLI_MUS)

    for name, algo_fn in algos.items():
        all_optimal = np.zeros((N_RUNS, T_HORIZON))
        for run in range(N_RUNS):
            arms = algo_fn(run)
            all_optimal[run] = np.cumsum(arms == optimal_arm) / (np.arange(T_HORIZON) + 1)
        mean_opt = np.mean(all_optimal, axis=0)
        ax.plot(np.arange(T_HORIZON), mean_opt * 100, color=algo_colors[name],
                linewidth=2, label=name)

    ax.axhline(100, color=COLORS["gray"], linestyle=":", alpha=0.5)
    ax.set_xlabel("Ronda $t$", fontsize=12)
    ax.set_ylabel("% de veces que se jaló el brazo óptimo", fontsize=12)
    ax.set_title("Convergencia al brazo óptimo "
                 f"({N_RUNS} ejecuciones, Bernoulli)", fontsize=13)
    ax.legend(fontsize=11)
    ax.set_xlim(0, T_HORIZON)
    ax.set_ylim(0, 105)

    _save(fig, "21_optimal_pulls_pct.png")


# ---------------------------------------------------------------------------
# Section 06 figures
# ---------------------------------------------------------------------------

def plot_22_exp3_vs_ucb1():
    """EXP3 vs UCB1: stochastic and adversarial settings."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    T = T_HORIZON

    # Left panel: stochastic setting
    ax = axes[0]
    def _ucb_w(mus, T, seed, reward_type="bernoulli", sigma=1.5):
        return _run_ucb1(mus, T, seed, reward_type, sigma)[:3]
    _, reg_ucb = _run_multi(_ucb_w, BERNOULLI_MUS, T, N_RUNS)
    def _exp3_w(mus, T, seed, reward_type="bernoulli", sigma=1.5):
        return _run_exp3(mus, T, seed, reward_type=reward_type, sigma=sigma)[:3]
    _, reg_exp3 = _run_multi(_exp3_w, BERNOULLI_MUS, T, N_RUNS)

    t_vals = np.arange(T)
    ax.plot(t_vals, np.mean(reg_ucb, axis=0), color=COLORS["blue"],
            linewidth=2, label="UCB1")
    ax.plot(t_vals, np.mean(reg_exp3, axis=0), color=COLORS["red"],
            linewidth=2, label="EXP3")
    ax.set_xlabel("Ronda $t$", fontsize=11)
    ax.set_ylabel("Regret acumulado $R_t$", fontsize=11)
    ax.set_title("Entorno estocástico\n(ambos funcionan; UCB1 es mejor)",
                 fontsize=12)
    ax.legend(fontsize=11)

    # Right panel: adversarial setting
    ax = axes[1]
    K = 3
    # Adversary: cycle rewards to defeat UCB1
    rng = np.random.RandomState(42)
    adv_rewards = np.zeros((T, K))
    # The adversary gives high rewards to a different arm each phase
    phase_len = 50
    for t in range(T):
        best_arm = (t // phase_len) % K
        adv_rewards[t, best_arm] = 1.0

    # Run UCB1 against adversary
    all_reg_ucb_adv = np.zeros((N_RUNS, T))
    all_reg_exp3_adv = np.zeros((N_RUNS, T))
    for run in range(N_RUNS):
        # UCB1 (use stochastic version, but adversary controls rewards)
        rng_run = np.random.RandomState(run)
        Q = np.zeros(K)
        N_counts = np.zeros(K, dtype=int)
        cum_reg = np.zeros(T)
        for t in range(T):
            if t < K:
                a = t
            else:
                ucb_vals = Q + np.sqrt(2 * np.log(t) / np.maximum(N_counts, 1))
                a = np.argmax(ucb_vals)
            r = adv_rewards[t, a]
            N_counts[a] += 1
            Q[a] += (r - Q[a]) / N_counts[a]
            best_reward = np.max(adv_rewards[t])
            cum_reg[t] = (cum_reg[t - 1] if t > 0 else 0) + (best_reward - r)
        all_reg_ucb_adv[run] = cum_reg

        # EXP3 against adversary
        _, _, cum_reg_exp3, _ = _run_exp3(
            BERNOULLI_MUS, T, seed=run, adversarial_rewards=adv_rewards)
        all_reg_exp3_adv[run] = cum_reg_exp3

    ax.plot(t_vals, np.mean(all_reg_ucb_adv, axis=0), color=COLORS["blue"],
            linewidth=2, label="UCB1")
    ax.plot(t_vals, np.mean(all_reg_exp3_adv, axis=0), color=COLORS["red"],
            linewidth=2, label="EXP3")
    ax.set_xlabel("Ronda $t$", fontsize=11)
    ax.set_ylabel("Regret acumulado $R_t$", fontsize=11)
    ax.set_title("Entorno adversarial\n(UCB1 falla; EXP3 es robusto)",
                 fontsize=12)
    ax.legend(fontsize=11)

    fig.suptitle("¿Por qué necesitamos EXP3?", fontsize=14,
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "22_exp3_vs_ucb1.png")


def plot_23_exp3_weights():
    """EXP3 weight/probability evolution."""
    _, _, _, weight_hist = _run_exp3(BERNOULLI_MUS, T_HORIZON, seed=42,
                                     reward_type="bernoulli")

    # Normalize to probabilities
    K = 3
    gamma = min(1.0, np.sqrt(K * np.log(K) / max(T_HORIZON, 1)))
    prob_hist = np.zeros_like(weight_hist)
    for t in range(T_HORIZON + 1):
        w_sum = np.sum(weight_hist[t])
        if w_sum > 0:
            prob_hist[t] = (1 - gamma) * (weight_hist[t] / w_sum) + gamma / K
        else:
            prob_hist[t] = 1.0 / K

    fig, ax = plt.subplots(figsize=(12, 5))
    t_vals = np.arange(T_HORIZON + 1)
    ax.stackplot(t_vals, prob_hist[:, 0], prob_hist[:, 1], prob_hist[:, 2],
                 colors=ARM_COLORS, alpha=0.7, labels=ARM_LABELS)
    ax.set_xlabel("Ronda $t$", fontsize=12)
    ax.set_ylabel("Probabilidad de selección $p_i(t)$", fontsize=12)
    ax.set_title("EXP3: evolución de pesos — las probabilidades se adaptan "
                 "a las recompensas observadas", fontsize=13)
    ax.legend(fontsize=10, loc="center right")
    ax.set_xlim(0, T_HORIZON)
    ax.set_ylim(0, 1)

    _save(fig, "23_exp3_weights.png")


# ---------------------------------------------------------------------------
# Section 07 figures
# ---------------------------------------------------------------------------

def plot_24_ab_testing():
    """A/B testing: traditional 50/50 vs Thompson adaptive."""
    T = 2000
    # 5 variants with different conversion rates
    conv_rates = [0.02, 0.03, 0.05, 0.06, 0.08]
    K = len(conv_rates)
    best_rate = max(conv_rates)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: traditional 50/50 (equal allocation)
    ax = axes[0]
    rng = np.random.RandomState(42)
    alloc = np.zeros((T, K))
    conversions = np.zeros(T)
    for t in range(T):
        a = t % K
        r = 1 if rng.random() < conv_rates[a] else 0
        alloc[t, a] = 1
        conversions[t] = r

    cum_alloc = np.cumsum(alloc, axis=0)
    for i in range(K):
        ax.plot(np.arange(T), cum_alloc[:, i] / (np.arange(T) + 1),
                linewidth=2, label=f"Variante {i+1} (cr={conv_rates[i]})")
    ax.set_xlabel("Usuarios", fontsize=11)
    ax.set_ylabel("Fracción de tráfico", fontsize=11)
    ax.set_title("Tradicional: asignación fija 1/K", fontsize=12)
    ax.legend(fontsize=8, loc="center right")
    ax.set_ylim(0, 0.5)

    total_conv_trad = np.sum(conversions)

    # Right: Thompson adaptive
    ax = axes[1]
    rng = np.random.RandomState(42)
    alpha = np.ones(K)
    beta_p = np.ones(K)
    alloc2 = np.zeros((T, K))
    conversions2 = np.zeros(T)
    for t in range(T):
        theta = np.array([rng.beta(alpha[i], beta_p[i]) for i in range(K)])
        a = np.argmax(theta)
        r = 1 if rng.random() < conv_rates[a] else 0
        alpha[a] += r
        beta_p[a] += 1 - r
        alloc2[t, a] = 1
        conversions2[t] = r

    cum_alloc2 = np.cumsum(alloc2, axis=0)
    for i in range(K):
        ax.plot(np.arange(T), cum_alloc2[:, i] / (np.arange(T) + 1),
                linewidth=2, label=f"Variante {i+1} (cr={conv_rates[i]})")
    ax.set_xlabel("Usuarios", fontsize=11)
    ax.set_ylabel("Fracción de tráfico", fontsize=11)
    ax.set_title("Thompson: asignación adaptativa", fontsize=12)
    ax.legend(fontsize=8, loc="center right")
    ax.set_ylim(0, 1.0)

    total_conv_thomp = np.sum(conversions2)
    improvement = total_conv_thomp - total_conv_trad

    fig.suptitle(f"A/B Testing: Thompson obtiene {improvement:.0f} "
                 f"conversiones adicionales ({improvement/max(total_conv_trad,1)*100:.0f}% más)",
                 fontsize=13, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "24_ab_testing.png")


def plot_25_variant_taxonomy():
    """Concept map connecting all bandit variants."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Central node
    cx, cy = 7, 4
    box = mpatches.FancyBboxPatch((cx - 1.8, cy - 0.5), 3.6, 1.0,
                                   boxstyle="round,pad=0.2",
                                   facecolor=COLORS["blue"], alpha=0.9,
                                   edgecolor=COLORS["dark"], linewidth=2)
    ax.add_patch(box)
    ax.text(cx, cy, "Bandido\nMultibrazo\nEstocástico", ha="center",
            va="center", fontsize=11, fontweight="bold", color="white")

    # Variant nodes
    variants = [
        (2, 7, "Contextual\n(LinUCB)", COLORS["green"],
         "Recompensas dependen\nde features $x_t$"),
        (12, 7, "Adversarial\n(EXP3)", COLORS["red"],
         "Sin supuesto\nestocástico"),
        (2, 1, "No estacionario\n(SW-UCB)", COLORS["orange"],
         "Distribuciones\ncambian con $t$"),
        (12, 1, "Combinatorial\n(CUCB)", COLORS["purple"],
         "Jalar conjuntos\nde brazos"),
        (7, 7.5, "Best-arm ID\n(Successive Elim.)", COLORS["teal"],
         "Encontrar el mejor,\nno maximizar reward"),
        (7, 0.5, "Bayesian Opt.\n(GP-UCB)", COLORS["pink"],
         "Espacio continuo\nde brazos"),
    ]

    for vx, vy, label, color, desc in variants:
        box = mpatches.FancyBboxPatch((vx - 1.3, vy - 0.4), 2.6, 0.8,
                                       boxstyle="round,pad=0.15",
                                       facecolor=color, alpha=0.2,
                                       edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(vx, vy, label, ha="center", va="center", fontsize=9,
                fontweight="bold", color=COLORS["dark"])
        # Description below/above
        if vy > 4:
            ax.text(vx, vy - 0.7, desc, ha="center", va="top",
                    fontsize=7, color=COLORS["gray"], style="italic")
        else:
            ax.text(vx, vy + 0.7, desc, ha="center", va="bottom",
                    fontsize=7, color=COLORS["gray"], style="italic")

        # Line to center
        ax.plot([vx, cx], [vy, cy], color=COLORS["gray"], linewidth=1,
                alpha=0.4, linestyle="--")

    # Title
    ax.text(7, -0.3, "Taxonomía de variantes del problema de bandidos",
            ha="center", fontsize=14, fontweight="bold", color=COLORS["dark"])

    # MCTS connection (special)
    ax.text(13.5, 4, "UCT\n(MCTS)", ha="center", va="center", fontsize=9,
            fontweight="bold", color=COLORS["dark"],
            bbox=dict(boxstyle="round,pad=0.3", facecolor=COLORS["light"],
                      edgecolor=COLORS["dark"], linestyle="--"))
    ax.annotate("UCB1 en\nárboles", xy=(12, 4), xytext=(11, 4),
                fontsize=8, color=COLORS["gray"],
                arrowprops=dict(arrowstyle="->", color=COLORS["gray"]))

    _save(fig, "25_variant_taxonomy.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Generando figuras para Multi-Armed Bandits...\n")

    # Section 01
    plot_01_slot_machines()
    plot_26_reward_distributions()
    plot_27_kl_divergence()
    plot_02_gaussian_densities()
    plot_03_explore_exploit_spectrum()
    plot_04_pure_strategies()
    plot_05_regret_decomposition()

    # Section 02
    plot_06_egreedy_arm_selection()
    plot_07_egreedy_regret_by_epsilon()
    plot_08_egreedy_pull_count()

    # Section 03
    plot_09_ucb_confidence_bands()
    plot_10_ucb_vs_egreedy_selection()
    plot_11_ucb_vs_egreedy_regret()
    plot_12_klucb_vs_ucb1()

    # Section 04
    plot_13_beta_posterior_evolution()
    plot_14_thompson_samples()
    plot_15_normal_posterior_evolution()
    plot_16_conjugacy_diagram()
    plot_17_thompson_arm_frequency()

    # Section 05
    plot_18_grand_regret_bernoulli()
    plot_19_grand_regret_gaussian()
    plot_20_arm_selection_evolution()
    plot_21_optimal_pulls_pct()

    # Section 06
    plot_22_exp3_vs_ucb1()
    plot_23_exp3_weights()

    # Section 07
    plot_24_ab_testing()
    plot_25_variant_taxonomy()

    print(f"\n✓  Todas las {27} figuras generadas en {IMAGES_DIR}/")


if __name__ == "__main__":
    main()
