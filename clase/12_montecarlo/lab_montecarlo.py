#!/usr/bin/env python3
"""
Laboratorio: Métodos de Monte Carlo (imágenes para las notas)

Uso:
    cd clase/12_montecarlo
    python3 lab_montecarlo.py

Genera 5 imágenes en:
    clase/12_montecarlo/images/

Dependencias: numpy, matplotlib, scipy
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy import stats

# -----------------------------------------------------------------------------
# Styling
# -----------------------------------------------------------------------------

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.figsize"] = (12, 7)
plt.rcParams["font.size"] = 11
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.labelsize"] = 11

COLORS = {
    "blue": "#2E86AB",
    "red": "#E94F37",
    "green": "#27AE60",
    "gray": "#7F8C8D",
    "orange": "#F39C12",
    "purple": "#8E44AD",
}

ROOT = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

np.random.seed(42)


def _save(fig, name: str) -> None:
    out = IMAGES_DIR / name
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Generada: {out.name}")


# -----------------------------------------------------------------------------
# 1) Estimación de π — el dartboard
# -----------------------------------------------------------------------------

def plot_pi_estimation() -> None:
    """Dartboard con n=100, 1000, 10000 mostrando la estimación de π."""
    ns = [100, 1_000, 10_000]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    rng = np.random.default_rng(42)

    for ax, n in zip(axes, ns):
        x = rng.uniform(-1, 1, n)
        y = rng.uniform(-1, 1, n)
        inside = x**2 + y**2 <= 1.0

        ax.scatter(x[~inside], y[~inside], s=1.5, color=COLORS["gray"],
                   alpha=0.4, rasterized=True)
        ax.scatter(x[inside], y[inside], s=1.5, color=COLORS["blue"],
                   alpha=0.6, rasterized=True)

        # Draw circle
        theta = np.linspace(0, 2 * np.pi, 400)
        ax.plot(np.cos(theta), np.sin(theta), color=COLORS["red"], lw=1.5)
        ax.set_aspect("equal")
        ax.set_xlim(-1.05, 1.05)
        ax.set_ylim(-1.05, 1.05)

        pi_est = 4 * inside.mean()
        error = abs(pi_est - np.pi)
        ax.set_title(
            f"$n = {n:,}$\n$\\hat{{\\pi}} = {pi_est:.4f}$  |error| = {error:.4f}",
            fontsize=11,
        )
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle(
        "Estimación de $\\pi$ con Monte Carlo\n"
        "Puntos azules: dentro del círculo · grises: fuera",
        fontsize=13,
        y=1.02,
    )
    fig.tight_layout()
    _save(fig, "pi_estimation.png")


# -----------------------------------------------------------------------------
# 2) Convergencia del estimador — promedio acumulado
# -----------------------------------------------------------------------------

def plot_convergence_demo() -> None:
    """Promedio acumulado de f(U) ~ Uniform[0,1]: f(x)=4√(1-x²) → E[f]=π."""
    n_max = 50_000
    n_runs = 3
    true_val = np.pi

    fig, ax = plt.subplots(figsize=(11, 5))
    rng = np.random.default_rng(42)

    palette = [COLORS["blue"], COLORS["orange"], COLORS["purple"]]

    for i in range(n_runs):
        u = rng.uniform(0, 1, n_max)
        f = 4 * np.sqrt(1 - u**2)
        running_mean = np.cumsum(f) / np.arange(1, n_max + 1)
        ns = np.arange(1, n_max + 1)
        ax.semilogx(ns, running_mean, lw=1.2, color=palette[i],
                    alpha=0.85, label=f"Corrida {i + 1}")

    # Confidence bands based on CLT: ±1.96 * sigma / sqrt(n)
    # sigma² = Var[4√(1-U²)] ≈ 0.67 (numerical)
    sigma = np.std(4 * np.sqrt(1 - rng.uniform(0, 1, 200_000)**2))
    ns_band = np.logspace(0, np.log10(n_max), 300)
    margin = 1.96 * sigma / np.sqrt(ns_band)
    ax.fill_between(ns_band, true_val - margin, true_val + margin,
                    alpha=0.12, color=COLORS["green"], label="IC 95%")

    ax.axhline(true_val, color=COLORS["red"], lw=1.8, ls="--",
               label=f"Valor verdadero $\\pi \\approx {true_val:.5f}$")

    ax.set_xlabel("Número de muestras $n$ (escala log)")
    ax.set_ylabel("$\\hat{\\pi}_n$")
    ax.set_title("Convergencia del estimador Monte Carlo de $\\pi$\n"
                 "El promedio acumulado converge al valor verdadero")
    ax.legend(loc="upper right", fontsize=10)
    ax.set_xlim(1, n_max)
    fig.tight_layout()
    _save(fig, "convergence_demo.png")


# -----------------------------------------------------------------------------
# 3) Escalamiento del error — log-log, pendiente -1/2
# -----------------------------------------------------------------------------

def plot_error_scaling() -> None:
    """Error absoluto vs. n en escala log-log; pendiente teórica -0.5."""
    n_values = np.logspace(1, 6, 25).astype(int)
    n_reps = 200
    rng = np.random.default_rng(42)

    true_val = np.pi
    errors = []
    for n in n_values:
        ests = []
        for _ in range(n_reps):
            u = rng.uniform(0, 1, n)
            ests.append(4 * np.sqrt(1 - u**2).mean())
        errors.append(np.mean(np.abs(np.array(ests) - true_val)))

    errors = np.array(errors)

    # Fit slope in log-log space
    log_n = np.log10(n_values)
    log_e = np.log10(errors)
    slope, intercept = np.polyfit(log_n, log_e, 1)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.loglog(n_values, errors, "o", color=COLORS["blue"], ms=6,
              label="Error promedio empírico")

    # Reference line O(1/√n)
    ref = 10**intercept * n_values**(-0.5)
    ax.loglog(n_values, ref, "--", color=COLORS["red"], lw=1.8,
              label=f"Referencia $O(1/\\sqrt{{n}})$")

    ax.set_xlabel("Número de muestras $n$")
    ax.set_ylabel("Error absoluto medio $|\\hat{\\mu}_n - \\mu|$")
    ax.set_title(
        f"Escalamiento del error Monte Carlo\n"
        f"Pendiente empírica: {slope:.3f}  (teoría: $-0.5$)"
    )
    ax.legend(fontsize=10)
    ax.annotate(
        f"pendiente ≈ {slope:.2f}",
        xy=(n_values[12], errors[12]),
        xytext=(n_values[12] * 5, errors[12] * 3),
        fontsize=10,
        color=COLORS["gray"],
        arrowprops=dict(arrowstyle="->", color=COLORS["gray"]),
    )
    fig.tight_layout()
    _save(fig, "error_scaling.png")


# -----------------------------------------------------------------------------
# 4) MC vs. cuadratura — maldición de la dimensionalidad
# -----------------------------------------------------------------------------

def plot_dimension_comparison() -> None:
    """Puntos necesarios para error ε en cuadratura vs. MC como fn de d."""
    dims = np.arange(1, 21)
    eps = 0.01  # target error

    # Quadrature: n = (1/eps)^d  (grid points per dimension)
    # Actual total points: n_grid^d where n_grid = 1/eps^(d/2) roughly
    # Simpler: to achieve error eps with quadrature in d dims, need n = (1/eps)^(2/d)^d = (1/eps)^2...
    # More precisely: for d-dim Simpson, error = O(n^{-2/d}) where n is total points
    # So n_quad = eps^{-d/2}
    n_quad = eps ** (-dims / 2.0)

    # Monte Carlo: n = (sigma / eps)^2 (constant in d, sigma ≈ 0.5 here)
    sigma = 0.5
    n_mc = np.full_like(dims, (sigma / eps) ** 2, dtype=float)

    fig, ax = plt.subplots(figsize=(10, 5))

    # Shade advantage region
    crossover = dims[n_mc < n_quad][0] if np.any(n_mc < n_quad) else dims[-1]
    ax.axvspan(crossover, dims[-1] + 0.5, alpha=0.08, color=COLORS["green"],
               label="Región donde MC es más eficiente")

    ax.semilogy(dims, n_quad, "o-", color=COLORS["red"], lw=2, ms=7,
                label="Cuadratura: $n \\propto \\varepsilon^{-d/2}$")
    ax.semilogy(dims, n_mc, "s--", color=COLORS["blue"], lw=2, ms=7,
                label=f"Monte Carlo: $n = (\\sigma/\\varepsilon)^2 = {int(n_mc[0]):,}$")

    ax.set_xlabel("Dimensión $d$")
    ax.set_ylabel("Muestras necesarias (escala log)")
    ax.set_title(
        "Monte Carlo vs. Cuadratura: costo en función de la dimensión\n"
        f"Para error objetivo $\\varepsilon = {eps}$"
    )
    ax.legend(fontsize=10)
    ax.set_xlim(0.5, dims[-1] + 0.5)
    ax.axvline(crossover, color=COLORS["gray"], ls=":", lw=1.2)
    ax.annotate(f"Cruce\n$d \\approx {crossover}$",
                xy=(crossover, n_mc[0]),
                xytext=(crossover + 1.5, n_mc[0] * 5),
                fontsize=9, color=COLORS["gray"],
                arrowprops=dict(arrowstyle="->", color=COLORS["gray"]))
    fig.tight_layout()
    _save(fig, "dimension_comparison.png")


# -----------------------------------------------------------------------------
# 5) CLT demo — distribución del estimador MC
# -----------------------------------------------------------------------------

def plot_clt_demo() -> None:
    """Histogramas de 1000 estimados MC para n=10 y n=1000."""
    n_experiments = 1_000
    ns = [10, 1_000]
    true_val = np.pi
    rng = np.random.default_rng(42)

    # Precompute sigma
    u_big = rng.uniform(0, 1, 500_000)
    sigma_f = np.std(4 * np.sqrt(1 - u_big**2))

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    palette = [COLORS["blue"], COLORS["orange"]]

    for ax, n, color in zip(axes, ns, palette):
        estimates = np.array([
            4 * np.sqrt(1 - rng.uniform(0, 1, n)**2).mean()
            for _ in range(n_experiments)
        ])
        se = sigma_f / np.sqrt(n)

        ax.hist(estimates, bins=40, density=True, color=color, alpha=0.65,
                edgecolor="white", lw=0.4, label="Estimados empíricos")

        # Theoretical normal
        x_range = np.linspace(estimates.min() - se, estimates.max() + se, 300)
        ax.plot(x_range, stats.norm.pdf(x_range, true_val, se),
                color=COLORS["red"], lw=2.2, label=f"$\\mathcal{{N}}(\\pi,\\ \\sigma/\\sqrt{{n}})$")
        ax.axvline(true_val, color=COLORS["gray"], ls="--", lw=1.5,
                   label=f"$\\pi \\approx {true_val:.4f}$")

        ax.set_xlabel("$\\hat{\\pi}_n$")
        ax.set_ylabel("Densidad")
        ax.set_title(f"$n = {n:,}$\n"
                     f"$\\hat{{\\sigma}}_{{\\hat{{\\mu}}}} = {se:.4f}$")
        ax.legend(fontsize=9)

    fig.suptitle(
        "Teorema Central del Límite en acción\n"
        "La distribución de $\\hat{\\pi}_n$ sobre 1,000 experimentos independientes",
        fontsize=13,
    )
    fig.tight_layout()
    _save(fig, "clt_demo.png")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    print("Generando imágenes para las notas de Monte Carlo...")
    plot_pi_estimation()
    plot_convergence_demo()
    plot_error_scaling()
    plot_dimension_comparison()
    plot_clt_demo()
    print(f"\n✓ Todas las imágenes guardadas en {IMAGES_DIR}")


if __name__ == "__main__":
    main()
