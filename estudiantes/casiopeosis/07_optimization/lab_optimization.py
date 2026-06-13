#!/usr/bin/env python3
"""
Laboratorio: Optimización (imágenes para las notas)

Uso:
    cd clase/07_optimization
    python lab_optimization.py

Genera imágenes en:
    clase/07_optimization/images/

Dependencias: numpy, matplotlib, scipy
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import (
    minimize, minimize_scalar, linprog, milp, dual_annealing,
    differential_evolution, LinearConstraint, Bounds,
)

# -----------------------------------------------------------------------------
# Styling (same vibe as lab_informacion.py)
# -----------------------------------------------------------------------------

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.figsize"] = (12, 8)
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
# 1) Local vs global minima (1D)
# -----------------------------------------------------------------------------


def plot_local_vs_global():
    """1D function with annotated local and global minima."""
    x = np.linspace(-2, 6, 800)
    f = lambda t: (t - 2) ** 2 * np.sin(3 * t) + 0.5 * t

    y = f(x)

    # Find local minima (simple grid search)
    from scipy.signal import argrelextrema

    local_min_idx = argrelextrema(y, np.less, order=20)[0]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, color=COLORS["blue"], linewidth=2, label=r"$f(x) = (x-2)^2 \sin(3x) + 0.5x$")

    # Mark local minima
    global_idx = local_min_idx[np.argmin(y[local_min_idx])]
    for idx in local_min_idx:
        if idx == global_idx:
            ax.scatter(x[idx], y[idx], color=COLORS["red"], s=120, zorder=5,
                       edgecolors="black", linewidths=1.5)
            ax.annotate("Mínimo global", xy=(x[idx], y[idx]),
                        xytext=(x[idx] + 0.5, y[idx] - 3),
                        arrowprops=dict(arrowstyle="->", lw=1.5),
                        fontsize=11, fontweight="bold", color=COLORS["red"])
        else:
            ax.scatter(x[idx], y[idx], color=COLORS["orange"], s=80, zorder=4,
                       edgecolors="black", linewidths=1)
            ax.annotate("Mínimo local", xy=(x[idx], y[idx]),
                        xytext=(x[idx] + 0.4, y[idx] + 3),
                        arrowprops=dict(arrowstyle="->", lw=1),
                        fontsize=10, color=COLORS["orange"])

    ax.set_title("Mínimos locales vs mínimo global")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend(loc="upper left")
    _save(fig, "local_vs_global.png")


# -----------------------------------------------------------------------------
# 2) Saddle point (3D)
# -----------------------------------------------------------------------------


def plot_saddle_point_3d():
    """Contour + heatmap of f(x,y) = x^2 - y^2 showing a saddle point."""
    x = np.linspace(-2, 2, 300)
    y = np.linspace(-2, 2, 300)
    X, Y = np.meshgrid(x, y)
    Z = X**2 - Y**2

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.pcolormesh(X, Y, Z, cmap="coolwarm", shading="auto")
    cs = ax.contour(X, Y, Z, levels=15, colors="black", linewidths=0.5, alpha=0.5)
    ax.clabel(cs, inline=True, fontsize=8)
    fig.colorbar(im, ax=ax, label="f(x,y)")

    ax.scatter([0], [0], color=COLORS["red"], s=150, zorder=5,
               edgecolors="black", linewidths=2)
    ax.annotate("Punto silla (0, 0)\nmín en x, máx en y",
                xy=(0, 0), xytext=(0.5, 1.2),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=COLORS["red"]),
                fontsize=11, color=COLORS["red"], fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))

    # Show directions
    ax.annotate("", xy=(0, -1.5), xytext=(0, -0.3),
                arrowprops=dict(arrowstyle="->", lw=2, color=COLORS["green"]))
    ax.text(0.15, -1.0, "máx (en y)", fontsize=9, color=COLORS["green"])
    ax.annotate("", xy=(1.5, 0), xytext=(0.3, 0),
                arrowprops=dict(arrowstyle="->", lw=2, color=COLORS["blue"]))
    ax.text(0.8, 0.15, "mín (en x)", fontsize=9, color=COLORS["blue"])

    ax.set_title(r"Punto silla: $f(x,y) = x^2 - y^2$")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    _save(fig, "saddle_point_3d.png")


# -----------------------------------------------------------------------------
# 3) Convex vs non-convex
# -----------------------------------------------------------------------------


def plot_convex_vs_nonconvex():
    """Side-by-side: convex function vs non-convex function."""
    x = np.linspace(-3, 3, 400)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Convex: f(x) = x^2
    y_convex = x**2
    ax1.plot(x, y_convex, color=COLORS["blue"], linewidth=2)
    ax1.fill_between(x, y_convex, alpha=0.1, color=COLORS["blue"])
    # Show convexity: chord above curve
    x1, x2 = -2, 1.5
    y1, y2 = x1**2, x2**2
    ax1.plot([x1, x2], [y1, y2], "--", color=COLORS["red"], linewidth=1.5,
             label="Cuerda (siempre arriba)")
    lam = 0.4
    xm = lam * x1 + (1 - lam) * x2
    ax1.scatter([xm], [xm**2], color=COLORS["green"], s=60, zorder=5)
    ax1.scatter([xm], [lam * y1 + (1 - lam) * y2], color=COLORS["red"], s=60, zorder=5)
    ax1.annotate("f(λx₁+(1-λ)x₂)", xy=(xm, xm**2), xytext=(xm + 0.5, xm**2 + 1),
                 arrowprops=dict(arrowstyle="->"), fontsize=9, color=COLORS["green"])
    ax1.annotate("λf(x₁)+(1-λ)f(x₂)", xy=(xm, lam * y1 + (1 - lam) * y2),
                 xytext=(xm + 0.5, lam * y1 + (1 - lam) * y2 + 1.5),
                 arrowprops=dict(arrowstyle="->"), fontsize=9, color=COLORS["red"])
    ax1.set_title(r"Convexa: $f(x) = x^2$")
    ax1.set_xlabel("x")
    ax1.set_ylabel("f(x)")
    ax1.legend(fontsize=9)

    # Non-convex: f(x) = x^4 - 4x^2 + x
    y_nonconvex = x**4 - 4 * x**2 + x
    ax2.plot(x, y_nonconvex, color=COLORS["purple"], linewidth=2)
    # Show chord going below curve
    x1, x2 = -1.8, 1.5
    y1_nc = x1**4 - 4 * x1**2 + x1
    y2_nc = x2**4 - 4 * x2**2 + x2
    ax2.plot([x1, x2], [y1_nc, y2_nc], "--", color=COLORS["red"], linewidth=1.5,
             label="Cuerda (cruza la curva)")
    ax2.set_title(r"No convexa: $f(x) = x^4 - 4x^2 + x$")
    ax2.set_xlabel("x")
    ax2.set_ylabel("f(x)")
    ax2.legend(fontsize=9)

    fig.suptitle("Convexidad: la cuerda siempre queda arriba de la curva", fontsize=13, y=1.02)
    fig.tight_layout()
    _save(fig, "convex_vs_nonconvex.png")


# -----------------------------------------------------------------------------
# 4) Gradient descent on contour plot
# -----------------------------------------------------------------------------


def plot_gradient_descent_contour():
    """Contour plot of a quadratic with GD trajectory and arrows."""
    # f(x,y) = 3x^2 + y^2 (elongated bowl)
    f = lambda x, y: 3 * x**2 + y**2
    grad_f = lambda x, y: np.array([6 * x, 2 * y])

    # GD trajectory
    x0 = np.array([3.0, 3.0])
    lr = 0.08
    trajectory = [x0.copy()]
    for _ in range(25):
        x0 = x0 - lr * grad_f(x0[0], x0[1])
        trajectory.append(x0.copy())
    trajectory = np.array(trajectory)

    # Contour plot
    xg = np.linspace(-4, 4, 300)
    yg = np.linspace(-4, 4, 300)
    X, Y = np.meshgrid(xg, yg)
    Z = f(X, Y)

    fig, ax = plt.subplots(figsize=(8, 7))
    cs = ax.contour(X, Y, Z, levels=20, cmap="viridis", alpha=0.7)
    ax.clabel(cs, inline=True, fontsize=8)

    # Plot trajectory with arrows
    ax.plot(trajectory[:, 0], trajectory[:, 1], "o-", color=COLORS["red"],
            markersize=4, linewidth=1.5, label="Trayectoria GD")
    ax.scatter(trajectory[0, 0], trajectory[0, 1], color=COLORS["orange"],
               s=100, zorder=5, edgecolors="black", label="Inicio")
    ax.scatter(trajectory[-1, 0], trajectory[-1, 1], color=COLORS["green"],
               s=100, zorder=5, edgecolors="black", label="Final")

    # Arrows on a few steps
    for i in range(0, len(trajectory) - 1, 3):
        dx = trajectory[i + 1, 0] - trajectory[i, 0]
        dy = trajectory[i + 1, 1] - trajectory[i, 1]
        ax.annotate("", xy=(trajectory[i + 1, 0], trajectory[i + 1, 1]),
                     xytext=(trajectory[i, 0], trajectory[i, 1]),
                     arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.5))

    ax.set_title(r"Descenso de gradiente en $f(x,y) = 3x^2 + y^2$")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper right")
    _save(fig, "gradient_descent_contour.png")


# -----------------------------------------------------------------------------
# 5) GD on Rosenbrock
# -----------------------------------------------------------------------------


def plot_gd_rosenbrock():
    """GD trajectory on the Rosenbrock function (banana-shaped valley)."""
    rosenbrock = lambda x, y: (1 - x) ** 2 + 100 * (y - x**2) ** 2
    grad_rosen = lambda x, y: np.array([
        -2 * (1 - x) - 400 * x * (y - x**2),
        200 * (y - x**2),
    ])

    # GD with small learning rate
    x0 = np.array([-1.5, 2.0])
    lr = 0.001
    trajectory = [x0.copy()]
    for _ in range(5000):
        g = grad_rosen(x0[0], x0[1])
        x0 = x0 - lr * g
        trajectory.append(x0.copy())
    trajectory = np.array(trajectory)

    # Contour plot
    xg = np.linspace(-2, 2, 400)
    yg = np.linspace(-1, 3, 400)
    X, Y = np.meshgrid(xg, yg)
    Z = rosenbrock(X, Y)

    fig, ax = plt.subplots(figsize=(9, 7))
    cs = ax.contour(X, Y, np.log1p(Z), levels=30, cmap="inferno", alpha=0.7)

    # Subsample trajectory for plotting
    step = max(1, len(trajectory) // 200)
    traj_sub = trajectory[::step]
    ax.plot(traj_sub[:, 0], traj_sub[:, 1], "-", color=COLORS["blue"],
            linewidth=1, alpha=0.7, label="Trayectoria GD")
    ax.scatter(trajectory[0, 0], trajectory[0, 1], color=COLORS["orange"],
               s=100, zorder=5, edgecolors="black", label="Inicio")
    ax.scatter(trajectory[-1, 0], trajectory[-1, 1], color=COLORS["green"],
               s=100, zorder=5, edgecolors="black", label=f"Final ({len(trajectory)} pasos)")
    ax.scatter(1, 1, color=COLORS["red"], s=120, zorder=5,
               marker="*", edgecolors="black", label="Óptimo (1,1)")

    ax.set_title("Descenso de gradiente en la función de Rosenbrock")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper left")
    _save(fig, "gd_rosenbrock.png")


# -----------------------------------------------------------------------------
# 6) 1D scipy minimize
# -----------------------------------------------------------------------------


def plot_minimize_1d():
    """1D minimization with scipy: f(x) = (x-3)^2 + 2*sin(5x)."""
    f = lambda x: (x - 3) ** 2 + 2 * np.sin(5 * x)
    x = np.linspace(-1, 7, 800)
    y = f(x)

    result = minimize_scalar(f, bounds=(0, 6), method="bounded")
    x_min = result.x
    f_min = result.fun

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, color=COLORS["blue"], linewidth=2,
            label=r"$f(x) = (x-3)^2 + 2\sin(5x)$")
    ax.scatter([x_min], [f_min], color=COLORS["red"], s=120, zorder=5,
               edgecolors="black", linewidths=1.5)
    ax.annotate(f"Mínimo: x={x_min:.3f}\nf(x)={f_min:.3f}",
                xy=(x_min, f_min), xytext=(x_min + 1, f_min + 2),
                arrowprops=dict(arrowstyle="->", lw=1.5),
                fontsize=11, color=COLORS["red"],
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    ax.set_title("Minimización 1D con scipy.optimize.minimize_scalar")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend(loc="upper right")
    _save(fig, "minimize_1d.png")


# -----------------------------------------------------------------------------
# 7) Linear programming — feasible region
# -----------------------------------------------------------------------------


def plot_linear_programming_2d():
    """Feasible region of a 2D LP with objective contours."""
    # max 5x1 + 4x2  s.t.  6x1 + 4x2 <= 24,  x1 + 2x2 <= 6, x1,x2 >= 0
    fig, ax = plt.subplots(figsize=(8, 7))

    x1 = np.linspace(0, 5, 400)

    # Constraints
    c1 = (24 - 6 * x1) / 4   # 6x1 + 4x2 <= 24
    c2 = (6 - x1) / 2        # x1 + 2x2 <= 6

    ax.plot(x1, c1, color=COLORS["blue"], linewidth=2, label=r"$6x_1 + 4x_2 \leq 24$")
    ax.plot(x1, c2, color=COLORS["green"], linewidth=2, label=r"$x_1 + 2x_2 \leq 6$")

    # Feasible region
    y_upper = np.minimum(c1, c2)
    y_upper = np.maximum(y_upper, 0)
    ax.fill_between(x1, 0, y_upper, where=(y_upper >= 0) & (x1 >= 0),
                     alpha=0.2, color=COLORS["blue"], label="Región factible")

    # Objective contours: 5x1 + 4x2 = k
    for k in [5, 10, 15, 20]:
        obj_line = (k - 5 * x1) / 4
        ax.plot(x1, obj_line, "--", color=COLORS["gray"], linewidth=0.8, alpha=0.6)
        # Label
        valid = (obj_line >= 0) & (x1 >= 0)
        if np.any(valid):
            idx = np.where(valid)[0][len(np.where(valid)[0]) // 2]
            ax.annotate(f"z={k}", xy=(x1[idx], obj_line[idx]), fontsize=8,
                        color=COLORS["gray"])

    # Vertices
    vertices = np.array([[0, 0], [4, 0], [3, 1.5], [0, 3]])
    ax.scatter(vertices[:, 0], vertices[:, 1], color=COLORS["red"], s=80,
               zorder=5, edgecolors="black")
    for v in vertices:
        ax.annotate(f"({v[0]:.0f}, {v[1]:.1f})", xy=(v[0], v[1]),
                    xytext=(5, 8), textcoords="offset points", fontsize=9)

    # Optimal vertex
    z_vals = 5 * vertices[:, 0] + 4 * vertices[:, 1]
    opt_idx = np.argmax(z_vals)
    ax.scatter(vertices[opt_idx, 0], vertices[opt_idx, 1], color=COLORS["red"],
               s=200, zorder=6, edgecolors="black", linewidths=2, marker="*")
    ax.annotate(f"Óptimo: z={z_vals[opt_idx]:.0f}",
                xy=(vertices[opt_idx, 0], vertices[opt_idx, 1]),
                xytext=(vertices[opt_idx, 0] + 0.3, vertices[opt_idx, 1] + 0.5),
                arrowprops=dict(arrowstyle="->", lw=1.5),
                fontsize=11, color=COLORS["red"], fontweight="bold")

    ax.set_xlim(-0.5, 5)
    ax.set_ylim(-0.5, 5)
    ax.set_title(r"Programación lineal: $\max\ 5x_1 + 4x_2$")
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.legend(loc="upper right")
    _save(fig, "linear_programming_2d.png")


# -----------------------------------------------------------------------------
# 8) LP solution with scipy linprog
# -----------------------------------------------------------------------------


def plot_linprog_feasible():
    """LP solved with scipy.optimize.linprog, solution plotted on feasible region."""
    # Same problem: max 5x1 + 4x2 → min -5x1 - 4x2
    c = [-5, -4]
    A_ub = [[6, 4], [1, 2]]
    b_ub = [24, 6]
    bounds = [(0, None), (0, None)]
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    fig, ax = plt.subplots(figsize=(8, 7))

    x1 = np.linspace(0, 5, 400)
    c1 = (24 - 6 * x1) / 4
    c2 = (6 - x1) / 2

    ax.plot(x1, c1, color=COLORS["blue"], linewidth=2, label=r"$6x_1 + 4x_2 \leq 24$")
    ax.plot(x1, c2, color=COLORS["green"], linewidth=2, label=r"$x_1 + 2x_2 \leq 6$")

    y_upper = np.minimum(c1, c2)
    y_upper = np.maximum(y_upper, 0)
    ax.fill_between(x1, 0, y_upper, where=(y_upper >= 0) & (x1 >= 0),
                     alpha=0.2, color=COLORS["blue"], label="Región factible")

    # scipy solution
    sol = result.x
    ax.scatter([sol[0]], [sol[1]], color=COLORS["red"], s=200, zorder=6,
               edgecolors="black", linewidths=2, marker="*")
    ax.annotate(f"scipy: ({sol[0]:.2f}, {sol[1]:.2f})\nz={-result.fun:.2f}",
                xy=(sol[0], sol[1]),
                xytext=(sol[0] + 0.3, sol[1] + 0.6),
                arrowprops=dict(arrowstyle="->", lw=1.5),
                fontsize=11, color=COLORS["red"], fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    ax.set_xlim(-0.5, 5)
    ax.set_ylim(-0.5, 5)
    ax.set_title("Solución de LP con scipy.optimize.linprog")
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.legend(loc="upper right")
    _save(fig, "linprog_feasible.png")


# -----------------------------------------------------------------------------
# 9) SGD vs Batch GD convergence
# -----------------------------------------------------------------------------


def plot_sgd_vs_gd():
    """Convergence curves comparing batch GD and SGD on linear regression."""
    # Synthetic data: y = 2x + 1 + noise
    N = 200
    X_data = np.random.randn(N, 1)
    y_data = 2 * X_data[:, 0] + 1 + 0.5 * np.random.randn(N)
    X_aug = np.hstack([X_data, np.ones((N, 1))])

    mse = lambda w: np.mean((y_data - X_aug @ w) ** 2)
    grad_full = lambda w: -2 / N * X_aug.T @ (y_data - X_aug @ w)

    def grad_sgd(w, batch_size=32):
        idx = np.random.choice(N, batch_size, replace=False)
        return -2 / batch_size * X_aug[idx].T @ (y_data[idx] - X_aug[idx] @ w)

    w0 = np.array([0.0, 0.0])
    lr, n_steps = 0.05, 150

    # Batch GD
    losses_gd = []
    w = w0.copy()
    for _ in range(n_steps):
        losses_gd.append(mse(w))
        w = w - lr * grad_full(w)

    # SGD (batch_size=32)
    losses_sgd = []
    w = w0.copy()
    for _ in range(n_steps):
        losses_sgd.append(mse(w))
        w = w - lr * grad_sgd(w, batch_size=32)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(losses_gd, linewidth=2, color=COLORS["blue"], label="Batch GD (N=200)")
    ax.plot(losses_sgd, linewidth=1.5, color=COLORS["red"], alpha=0.8,
            label="SGD (batch=32)")
    ax.set_xlabel("Iteración")
    ax.set_ylabel("MSE Loss")
    ax.set_title("SGD vs Batch GD en regresión lineal")
    ax.legend()
    ax.set_yscale("log")
    _save(fig, "sgd_vs_gd.png")


# -----------------------------------------------------------------------------
# Shared: Rastrigin function (used by SA, GA, comparison)
# -----------------------------------------------------------------------------

def _rastrigin(x):
    """Rastrigin function: many local minima, global min at origin."""
    return 10 * len(x) + sum(xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x)


def _rastrigin_2d(X, Y):
    """Vectorized Rastrigin for contour plots."""
    return 20 + X**2 + Y**2 - 10 * np.cos(2 * np.pi * X) - 10 * np.cos(2 * np.pi * Y)


# -----------------------------------------------------------------------------
# 10) Simulated Annealing
# -----------------------------------------------------------------------------


def plot_simulated_annealing():
    """3-panel: SA trajectory on Rastrigin contours, temperature decay, convergence."""
    rng = np.random.default_rng(42)

    # Custom SA
    x = rng.uniform(-5, 5, size=2)
    T0, alpha, n_iter = 10.0, 0.995, 3000
    T = T0
    best_x, best_f = x.copy(), _rastrigin(x)
    history_x, history_T, history_best = [x.copy()], [T], [best_f]

    for _ in range(n_iter):
        x_new = x + rng.normal(0, 0.5, size=2)
        x_new = np.clip(x_new, -5.12, 5.12)
        f_old, f_new = _rastrigin(x), _rastrigin(x_new)
        delta = f_new - f_old
        if delta < 0 or rng.random() < np.exp(-delta / max(T, 1e-10)):
            x = x_new
            if _rastrigin(x) < best_f:
                best_x, best_f = x.copy(), _rastrigin(x)
        T *= alpha
        history_x.append(x.copy())
        history_T.append(T)
        history_best.append(best_f)

    history_x = np.array(history_x)

    # Contour grid
    g = np.linspace(-5.12, 5.12, 300)
    X, Y = np.meshgrid(g, g)
    Z = _rastrigin_2d(X, Y)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Panel 1: trajectory on contours
    ax = axes[0]
    ax.contourf(X, Y, Z, levels=30, cmap="viridis", alpha=0.8)
    ax.plot(history_x[:, 0], history_x[:, 1], "-", color="white", linewidth=0.3, alpha=0.4)
    n = len(history_x)
    colors_traj = plt.cm.hot(np.linspace(0, 0.8, n))
    ax.scatter(history_x[::50, 0], history_x[::50, 1], c=colors_traj[::50],
               s=8, zorder=3, edgecolors="none")
    ax.scatter(*history_x[0], color=COLORS["orange"], s=100, zorder=5,
               edgecolors="black", label="Inicio")
    ax.scatter(*best_x, color=COLORS["green"], s=120, zorder=5,
               edgecolors="black", marker="*", label=f"Mejor: f={best_f:.2f}")
    ax.scatter(0, 0, color="white", s=80, zorder=5, marker="x", linewidths=2,
               label="Global (0,0)")
    ax.set_title("Trayectoria SA en Rastrigin")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.legend(fontsize=8, loc="upper right")

    # Panel 2: temperature decay (log scale)
    ax = axes[1]
    ax.plot(history_T, color=COLORS["red"], linewidth=1.5)
    ax.set_yscale("log")
    ax.set_title("Temperatura $T$ vs iteración")
    ax.set_xlabel("Iteración")
    ax.set_ylabel("Temperatura (log)")
    ax.axhline(y=1.0, color=COLORS["gray"], linestyle="--", linewidth=0.8, label="T=1")
    ax.legend(fontsize=9)

    # Panel 3: best-so-far convergence
    ax = axes[2]
    ax.plot(history_best, color=COLORS["blue"], linewidth=1.5)
    ax.set_title("Mejor $f(x)$ encontrado")
    ax.set_xlabel("Iteración")
    ax.set_ylabel("$f(x^{\\ast})$")
    ax.axhline(y=0, color=COLORS["green"], linestyle="--", linewidth=0.8, label="Óptimo global (0)")
    ax.legend(fontsize=9)

    fig.suptitle("Simulated Annealing en Rastrigin 2D", fontsize=14, y=1.02)
    fig.tight_layout()
    _save(fig, "simulated_annealing.png")


# -----------------------------------------------------------------------------
# 11) Genetic Algorithm
# -----------------------------------------------------------------------------


def plot_genetic_algorithm():
    """3-panel: population snapshots, fitness curves, final distribution."""
    rng = np.random.default_rng(42)

    pop_size, n_gen = 60, 100
    bounds_ga = (-5.12, 5.12)
    mutation_rate, mutation_scale = 0.3, 0.5

    # Initialize population
    pop = rng.uniform(bounds_ga[0], bounds_ga[1], size=(pop_size, 2))
    fitness = np.array([_rastrigin(ind) for ind in pop])

    history_best, history_mean = [], []
    snapshots = {}  # generation -> population copy

    for gen in range(n_gen):
        history_best.append(fitness.min())
        history_mean.append(fitness.mean())

        if gen in (0, n_gen // 3, 2 * n_gen // 3, n_gen - 1):
            snapshots[gen] = pop.copy()

        # Tournament selection
        new_pop = []
        for _ in range(pop_size):
            i, j = rng.choice(pop_size, 2, replace=False)
            winner = pop[i] if fitness[i] < fitness[j] else pop[j]
            new_pop.append(winner.copy())
        new_pop = np.array(new_pop)

        # BLX-alpha crossover
        for k in range(0, pop_size - 1, 2):
            alpha_blx = 0.5
            d = np.abs(new_pop[k] - new_pop[k + 1])
            lo = np.minimum(new_pop[k], new_pop[k + 1]) - alpha_blx * d
            hi = np.maximum(new_pop[k], new_pop[k + 1]) + alpha_blx * d
            new_pop[k] = rng.uniform(lo, hi)
            new_pop[k + 1] = rng.uniform(lo, hi)

        # Gaussian mutation
        mask = rng.random(pop_size) < mutation_rate
        new_pop[mask] += rng.normal(0, mutation_scale, size=(mask.sum(), 2))
        new_pop = np.clip(new_pop, bounds_ga[0], bounds_ga[1])

        # Elitism: keep best from previous generation
        best_idx = np.argmin(fitness)
        new_fitness = np.array([_rastrigin(ind) for ind in new_pop])
        worst_idx = np.argmax(new_fitness)
        new_pop[worst_idx] = pop[best_idx]
        new_fitness[worst_idx] = fitness[best_idx]

        pop, fitness = new_pop, new_fitness

    best_overall = pop[np.argmin(fitness)]
    best_f = fitness.min()

    # Contour grid
    g = np.linspace(-5.12, 5.12, 300)
    Xg, Yg = np.meshgrid(g, g)
    Zg = _rastrigin_2d(Xg, Yg)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Panel 1: population snapshots colored by generation
    ax = axes[0]
    ax.contourf(Xg, Yg, Zg, levels=30, cmap="viridis", alpha=0.6)
    gen_colors = {0: COLORS["red"], n_gen // 3: COLORS["orange"],
                  2 * n_gen // 3: COLORS["blue"], n_gen - 1: COLORS["green"]}
    for gen_k, snap in snapshots.items():
        ax.scatter(snap[:, 0], snap[:, 1], s=15, color=gen_colors[gen_k],
                   alpha=0.7, label=f"Gen {gen_k}")
    ax.scatter(0, 0, color="white", s=80, zorder=5, marker="x", linewidths=2)
    ax.set_title("Población por generación")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.legend(fontsize=8, loc="upper right")

    # Panel 2: best/mean fitness curves
    ax = axes[1]
    ax.plot(history_best, color=COLORS["green"], linewidth=2, label="Mejor")
    ax.plot(history_mean, color=COLORS["blue"], linewidth=1.5, alpha=0.7, label="Media")
    ax.set_title("Fitness por generación")
    ax.set_xlabel("Generación")
    ax.set_ylabel("$f(x)$")
    ax.axhline(y=0, color=COLORS["gray"], linestyle="--", linewidth=0.8)
    ax.legend(fontsize=9)

    # Panel 3: final population fitness histogram
    ax = axes[2]
    ax.hist(fitness, bins=20, color=COLORS["purple"], edgecolor="black", alpha=0.8)
    ax.axvline(best_f, color=COLORS["red"], linewidth=2, linestyle="--",
               label=f"Mejor: {best_f:.2f}")
    ax.set_title("Distribución fitness (última generación)")
    ax.set_xlabel("$f(x)$")
    ax.set_ylabel("Frecuencia")
    ax.legend(fontsize=9)

    fig.suptitle("Algoritmo Genético en Rastrigin 2D", fontsize=14, y=1.02)
    fig.tight_layout()
    _save(fig, "genetic_algorithm.png")


# -----------------------------------------------------------------------------
# 12) Method comparison bar chart
# -----------------------------------------------------------------------------


def plot_method_comparison():
    """2-panel: f(x) bars (log scale) + nfev bars, comparing methods on Rastrigin 2D."""
    rng = np.random.default_rng(42)
    # Starting point near (but not at) integers — traps gradient methods
    x0 = np.array([2.9, 3.9])
    bounds_opt = [(-5.12, 5.12)] * 2

    results = {}

    # GD (custom)
    x_gd = x0.copy()
    lr = 0.001
    for _ in range(2000):
        g = np.array([
            2 * x_gd[0] + 10 * 2 * np.pi * np.sin(2 * np.pi * x_gd[0]),
            2 * x_gd[1] + 10 * 2 * np.pi * np.sin(2 * np.pi * x_gd[1]),
        ])
        x_gd = x_gd - lr * g
        x_gd = np.clip(x_gd, -5.12, 5.12)
    results["GD"] = {"f": _rastrigin(x_gd), "nfev": 2000}

    # L-BFGS-B
    res_bfgs = minimize(_rastrigin, x0, method="L-BFGS-B",
                        bounds=bounds_opt)
    results["L-BFGS-B"] = {"f": res_bfgs.fun, "nfev": res_bfgs.nfev}

    # Custom SA
    x_sa = x0.copy()
    T, alpha_sa, nfev_sa = 10.0, 0.995, 0
    best_sa = x_sa.copy()
    best_f_sa = _rastrigin(x_sa)
    for _ in range(3000):
        x_new = x_sa + rng.normal(0, 0.5, size=2)
        x_new = np.clip(x_new, -5.12, 5.12)
        f_old, f_new = _rastrigin(x_sa), _rastrigin(x_new)
        nfev_sa += 2
        delta = f_new - f_old
        if delta < 0 or rng.random() < np.exp(-delta / max(T, 1e-10)):
            x_sa = x_new
            if f_new < best_f_sa:
                best_sa, best_f_sa = x_sa.copy(), f_new
        T *= alpha_sa
    results["SA (custom)"] = {"f": best_f_sa, "nfev": nfev_sa}

    # Custom GA
    pop = rng.uniform(-5.12, 5.12, size=(60, 2))
    fit = np.array([_rastrigin(ind) for ind in pop])
    nfev_ga = 60
    for _ in range(100):
        new_pop = []
        for __ in range(60):
            i, j = rng.choice(60, 2, replace=False)
            new_pop.append(pop[i].copy() if fit[i] < fit[j] else pop[j].copy())
        new_pop = np.array(new_pop)
        for k in range(0, 59, 2):
            d = np.abs(new_pop[k] - new_pop[k + 1])
            lo = np.minimum(new_pop[k], new_pop[k + 1]) - 0.5 * d
            hi = np.maximum(new_pop[k], new_pop[k + 1]) + 0.5 * d
            new_pop[k] = rng.uniform(lo, hi)
            new_pop[k + 1] = rng.uniform(lo, hi)
        mask = rng.random(60) < 0.3
        new_pop[mask] += rng.normal(0, 0.5, size=(mask.sum(), 2))
        new_pop = np.clip(new_pop, -5.12, 5.12)
        new_fit = np.array([_rastrigin(ind) for ind in new_pop])
        nfev_ga += 60
        best_idx = np.argmin(fit)
        worst_idx = np.argmax(new_fit)
        new_pop[worst_idx] = pop[best_idx]
        new_fit[worst_idx] = fit[best_idx]
        pop, fit = new_pop, new_fit
    results["GA (custom)"] = {"f": fit.min(), "nfev": nfev_ga}

    # dual_annealing
    res_da = dual_annealing(_rastrigin, bounds_opt, seed=42)
    results["dual_annealing"] = {"f": res_da.fun, "nfev": res_da.nfev}

    # differential_evolution
    res_de = differential_evolution(_rastrigin, bounds_opt, seed=42)
    results["diff_evolution"] = {"f": res_de.fun, "nfev": res_de.nfev}

    # Plot: 2 panels
    methods = list(results.keys())
    f_vals = [results[m]["f"] for m in methods]
    nfevs = [results[m]["nfev"] for m in methods]
    found_global = [v < 1.0 for v in f_vals]
    bar_colors = [COLORS["green"] if fg else COLORS["red"] for fg in found_global]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Panel 1: f(x) — log scale so both stuck and global are visible
    # Add small epsilon to zero values for log scale
    f_plot = [max(v, 0.001) for v in f_vals]
    bars1 = ax1.bar(methods, f_plot, color=bar_colors, edgecolor="black", linewidth=1.2)
    ax1.set_yscale("log")
    ax1.axhline(y=1.0, color=COLORS["gray"], linestyle="--", linewidth=0.8,
                label="Umbral: f < 1 = global")
    for bar, fv, fg in zip(bars1, f_vals, found_global):
        label = f"f={fv:.2f}" if fv > 0.01 else "f ≈ 0"
        y_pos = max(fv, 0.001) * 1.5
        ax1.text(bar.get_x() + bar.get_width() / 2, y_pos, label,
                 ha="center", va="bottom", fontsize=9, fontweight="bold",
                 color=COLORS["green"] if fg else COLORS["red"])
    ax1.set_ylabel("Mejor $f(x)$ encontrado (log)")
    ax1.set_title("¿Encuentra el mínimo global?")
    ax1.legend(fontsize=9)
    ax1.tick_params(axis="x", rotation=15)

    # Panel 2: number of function evaluations
    bars2 = ax2.bar(methods, nfevs, color=[COLORS["blue"]] * len(methods),
                    edgecolor="black", linewidth=1.2, alpha=0.8)
    for bar, nf in zip(bars2, nfevs):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                 str(nf), ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax2.set_ylabel("Evaluaciones de $f$")
    ax2.set_title("Costo computacional")
    ax2.tick_params(axis="x", rotation=15)

    fig.suptitle("Comparación de métodos en Rastrigin 2D (inicio: (2.9, 3.9))",
                 fontsize=14, y=1.02)
    fig.tight_layout()
    _save(fig, "method_comparison.png")


# -----------------------------------------------------------------------------
# 13) Integer vs continuous
# -----------------------------------------------------------------------------


def plot_integer_vs_continuous():
    """2D polytope with integer lattice, LP and IP optima marked."""
    fig, ax = plt.subplots(figsize=(8, 7))

    # Constraints: 3x + 2y <= 12, x + 3y <= 9, x,y >= 0
    x1 = np.linspace(0, 5, 400)
    c1 = (12 - 3 * x1) / 2   # 3x + 2y <= 12
    c2 = (9 - x1) / 3         # x + 3y <= 9

    ax.plot(x1, c1, color=COLORS["blue"], linewidth=2, label="$3x_1 + 2x_2 \\leq 12$")
    ax.plot(x1, c2, color=COLORS["green"], linewidth=2, label="$x_1 + 3x_2 \\leq 9$")

    # Feasible region
    y_upper = np.minimum(c1, c2)
    y_upper = np.maximum(y_upper, 0)
    valid = (y_upper >= 0) & (x1 >= 0) & (x1 <= 4)
    ax.fill_between(x1, 0, y_upper, where=valid, alpha=0.15, color=COLORS["blue"],
                     label="Región factible (continua)")

    # Integer lattice points inside feasible region
    for ix in range(5):
        for iy in range(5):
            if 3 * ix + 2 * iy <= 12 and ix + 3 * iy <= 9 and ix >= 0 and iy >= 0:
                ax.scatter(ix, iy, color=COLORS["gray"], s=50, zorder=3,
                           edgecolors="black", linewidths=0.8)

    # LP relaxation: max 5x + 4y s.t. constraints
    res_lp = linprog([-5, -4],
                     A_ub=[[3, 2], [1, 3]],
                     b_ub=[12, 9],
                     bounds=[(0, None), (0, None)],
                     method="highs")
    lp_x = res_lp.x

    # IP solution: max 5x + 4y, integer
    res_ip = milp([-5, -4],
                  constraints=LinearConstraint([[3, 2], [1, 3]], ub=[12, 9]),
                  integrality=[1, 1],
                  bounds=Bounds(lb=0))
    ip_x = res_ip.x

    # Mark LP optimum
    ax.scatter(*lp_x, color=COLORS["orange"], s=250, zorder=6, marker="*",
               edgecolors="black", linewidths=1.5)
    ax.annotate(f"LP: ({lp_x[0]:.2f}, {lp_x[1]:.2f})\nz={-res_lp.fun:.2f}",
                xy=(lp_x[0], lp_x[1]),
                xytext=(lp_x[0] + 0.4, lp_x[1] + 0.5),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=COLORS["orange"]),
                fontsize=10, color=COLORS["orange"], fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))

    # Mark IP optimum
    ax.scatter(*ip_x, color=COLORS["red"], s=250, zorder=6, marker="*",
               edgecolors="black", linewidths=1.5)
    ax.annotate(f"IP: ({ip_x[0]:.0f}, {ip_x[1]:.0f})\nz={-res_ip.fun:.0f}",
                xy=(ip_x[0], ip_x[1]),
                xytext=(ip_x[0] - 1.5, ip_x[1] - 0.8),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=COLORS["red"]),
                fontsize=10, color=COLORS["red"], fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))

    # Gap annotation
    gap = -res_lp.fun - (-res_ip.fun)
    ax.text(0.3, 4.5, f"Gap LP-IP = {gap:.2f}", fontsize=11,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffffcc", alpha=0.9))

    ax.set_xlim(-0.5, 5)
    ax.set_ylim(-0.5, 5)
    ax.set_title("Programación entera vs continua: $\\max\\ 5x_1 + 4x_2$")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.legend(loc="upper right", fontsize=9)
    _save(fig, "integer_vs_continuous.png")


# =============================================================================
# Main
# =============================================================================


def main():
    print("Generando imágenes para módulo 07: Optimización\n")
    plot_local_vs_global()
    plot_saddle_point_3d()
    plot_convex_vs_nonconvex()
    plot_gradient_descent_contour()
    plot_gd_rosenbrock()
    plot_minimize_1d()
    plot_linear_programming_2d()
    plot_linprog_feasible()
    plot_sgd_vs_gd()
    plot_simulated_annealing()
    plot_genetic_algorithm()
    plot_method_comparison()
    plot_integer_vs_continuous()
    print(f"\n✓ Todas las imágenes generadas en {IMAGES_DIR}")


if __name__ == "__main__":
    main()
