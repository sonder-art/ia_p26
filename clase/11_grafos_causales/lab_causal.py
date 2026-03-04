#!/usr/bin/env python3
"""
Laboratorio: Grafos Causales (imágenes para las notas)

Uso:
    cd clase/11_grafos_causales
    python lab_causal.py

Genera imágenes en:
    clase/11_grafos_causales/images/

Dependencias: numpy, matplotlib
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# -----------------------------------------------------------------------------
# Styling (same pattern as lab_prediccion.py)
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
# 1) Simpson's Paradox — Becas y NSE
# -----------------------------------------------------------------------------


def plot_simpson_beca():
    """Simpson's paradox: aggregate vs. stratified scholarship performance."""

    # Beca/NSE data
    # NSE Bajo: con beca 480/800 (60%), sin beca 100/200 (50%)
    # NSE Alto: con beca 180/200 (90%), sin beca 640/800 (80%)
    # Aggregate: con beca 660/1000 (66%), sin beca 740/1000 (74%)

    nse_labels = ["NSE Bajo", "NSE Alto"]
    beca_rates = np.array([0.60, 0.90])
    no_beca_rates = np.array([0.50, 0.80])

    beca_agg = 0.66
    no_beca_agg = 0.74

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # LEFT: Aggregate
    bars = ax1.bar(
        ["Con beca", "Sin beca"],
        [beca_agg * 100, no_beca_agg * 100],
        color=[COLORS["blue"], COLORS["red"]],
        width=0.5,
        edgecolor="white",
        linewidth=1.5,
    )
    for bar, val in zip(bars, [beca_agg * 100, no_beca_agg * 100]):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{val:.0f}%",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=14,
        )
    ax1.set_ylim(0, 100)
    ax1.set_ylabel("Promedio alto (%)")
    ax1.set_title("Datos agregados\n(becados parecen peores)", fontsize=14)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # RIGHT: Stratified by NSE
    x = np.arange(len(nse_labels))
    width = 0.35
    ax2.bar(
        x - width / 2,
        beca_rates * 100,
        width,
        label="Con beca",
        color=COLORS["blue"],
        edgecolor="white",
        linewidth=1.5,
    )
    ax2.bar(
        x + width / 2,
        no_beca_rates * 100,
        width,
        label="Sin beca",
        color=COLORS["red"],
        edgecolor="white",
        linewidth=1.5,
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(nse_labels)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel("Promedio alto (%)")
    ax2.set_title(
        "Desglosado por NSE\n(becados mejores en ambos grupos)", fontsize=14
    )
    ax2.legend(loc="lower right")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.suptitle("Paradoja de Simpson: ¿Las becas perjudican el rendimiento?", fontsize=16, y=1.02)
    fig.tight_layout()
    _save(fig, "simpson_paradox.png")


# -----------------------------------------------------------------------------
# 2) Graph surgery — before/after DAG with cut arrow
# -----------------------------------------------------------------------------


def _draw_node(ax, pos, label, color=COLORS["blue"]):
    """Draw a circular node at position pos."""
    circle = plt.Circle(pos, 0.12, fill=True, color=color, alpha=0.15, linewidth=2)
    ax.add_patch(circle)
    circle_border = plt.Circle(
        pos, 0.12, fill=False, color=color, linewidth=2
    )
    ax.add_patch(circle_border)
    ax.text(pos[0], pos[1], label, ha="center", va="center", fontsize=13, fontweight="bold")


def _draw_arrow(ax, start, end, color=COLORS["gray"], style="-", linewidth=2):
    """Draw an arrow between two node positions, offset by node radius."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dist = np.sqrt(dx**2 + dy**2)
    offset = 0.14
    sx = start[0] + offset * dx / dist
    sy = start[1] + offset * dy / dist
    ex = end[0] - offset * dx / dist
    ey = end[1] - offset * dy / dist

    ax.annotate(
        "",
        xy=(ex, ey),
        xytext=(sx, sy),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=linewidth,
            linestyle=style,
            mutation_scale=18,
        ),
    )


def plot_graph_surgery():
    """Before/after graph surgery with cut arrow."""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Node positions (same for both)
    pos_z = (0.5, 0.85)
    pos_x = (0.2, 0.3)
    pos_y = (0.8, 0.3)

    # LEFT: Original graph
    ax1.set_xlim(-0.05, 1.05)
    ax1.set_ylim(0, 1.1)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("Grafo original (observacional)", fontsize=14, pad=15)

    _draw_node(ax1, pos_z, "Z", COLORS["purple"])
    _draw_node(ax1, pos_x, "X", COLORS["blue"])
    _draw_node(ax1, pos_y, "Y", COLORS["green"])
    _draw_arrow(ax1, pos_z, pos_x, COLORS["gray"])
    _draw_arrow(ax1, pos_z, pos_y, COLORS["gray"])
    _draw_arrow(ax1, pos_x, pos_y, COLORS["gray"])

    ax1.text(0.25, 0.68, "Z → X", ha="center", fontsize=10, color=COLORS["gray"])
    ax1.text(0.75, 0.68, "Z → Y", ha="center", fontsize=10, color=COLORS["gray"])
    ax1.text(0.5, 0.22, "X → Y", ha="center", fontsize=10, color=COLORS["gray"])

    # RIGHT: Mutilated graph (do(X=x))
    ax2.set_xlim(-0.05, 1.05)
    ax2.set_ylim(0, 1.1)
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_title("Grafo mutilado: do(X = x)", fontsize=14, pad=15)

    _draw_node(ax2, pos_z, "Z", COLORS["purple"])
    _draw_node(ax2, pos_x, "X", COLORS["red"])
    _draw_node(ax2, pos_y, "Y", COLORS["green"])

    # Cut arrow Z → X (dashed red with X mark)
    _draw_arrow(ax2, pos_z, pos_x, COLORS["red"], style="--", linewidth=2)
    mid_zx = ((pos_z[0] + pos_x[0]) / 2, (pos_z[1] + pos_x[1]) / 2)
    ax2.text(
        mid_zx[0] - 0.02,
        mid_zx[1] + 0.04,
        "X",
        ha="center",
        va="center",
        fontsize=20,
        color=COLORS["red"],
        fontweight="bold",
    )

    # Active arrows
    _draw_arrow(ax2, pos_z, pos_y, COLORS["gray"])
    _draw_arrow(ax2, pos_x, pos_y, COLORS["gray"])

    ax2.text(0.25, 0.68, "cortada", ha="center", fontsize=10, color=COLORS["red"],
             fontstyle="italic")
    ax2.text(0.75, 0.68, "Z → Y", ha="center", fontsize=10, color=COLORS["gray"])
    ax2.text(0.5, 0.22, "X → Y", ha="center", fontsize=10, color=COLORS["gray"])

    fig.suptitle(
        "Cirugía de grafos: do(X) corta las flechas entrantes a X",
        fontsize=16,
        y=1.02,
    )
    fig.tight_layout()
    _save(fig, "graph_surgery.png")


# -----------------------------------------------------------------------------
# 3) Confounding adjustment — naive vs. adjusted vs. true
# -----------------------------------------------------------------------------


def plot_confounding_adjustment():
    """Bar chart: naive vs adjusted vs true causal effect."""

    # Simulated data with known causal structure:
    # Z -> X (confounder), Z -> Y, X -> Y
    # True causal effect of X on Y = 2.0
    n = 5000
    true_effect = 2.0

    z = np.random.normal(0, 1, n)
    x = 0.8 * z + np.random.normal(0, 0.5, n)  # Z confounds X
    y = true_effect * x + 3.0 * z + np.random.normal(0, 1, n)  # true: X->Y is 2.0

    # Naive estimate (regression of Y on X, ignoring Z)
    naive_beta = np.polyfit(x, y, 1)[0]  # slope ≈ 2.0 + bias from Z

    # Adjusted estimate (regression of Y on X and Z)
    # Using OLS: Y = b0 + b1*X + b2*Z
    X_mat = np.column_stack([np.ones(n), x, z])
    betas = np.linalg.lstsq(X_mat, y, rcond=None)[0]
    adjusted_beta = betas[1]

    fig, ax = plt.subplots(figsize=(8, 6))

    labels = ["Naive\n(sin ajustar)", "Ajustado\n(fórmula de ajuste)", "Efecto causal\nverdadero"]
    values = [naive_beta, adjusted_beta, true_effect]
    colors_list = [COLORS["red"], COLORS["green"], COLORS["blue"]]

    bars = ax.bar(labels, values, color=colors_list, width=0.5, edgecolor="white", linewidth=2)
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.08,
            f"{val:.2f}",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=14,
        )

    ax.set_ylabel("Efecto estimado de X sobre Y")
    ax.set_title("Estimación del efecto causal: naive vs. ajustado", fontsize=14)
    ax.axhline(y=true_effect, color=COLORS["blue"], linestyle="--", alpha=0.4, linewidth=1.5)
    ax.set_ylim(0, max(values) * 1.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Annotation
    ax.annotate(
        "Sesgo por\nconfounder Z",
        xy=(0, naive_beta),
        xytext=(0.5, naive_beta + 0.8),
        fontsize=11,
        color=COLORS["red"],
        arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.5),
        ha="center",
    )

    fig.tight_layout()
    _save(fig, "confounding_adjustment.png")


# -----------------------------------------------------------------------------
# 4) RCT balance — confounder distribution across groups
# -----------------------------------------------------------------------------


def plot_rct_balance():
    """Confounder distribution: observational (unbalanced) vs RCT (balanced)."""

    n = 2000

    # Confounder Z (e.g., soil quality: 0=poor, 1=good)
    z = np.random.binomial(1, 0.5, n)

    # OBSERVATIONAL: treatment assigned based on Z (farmers choose)
    # Good soil → more likely to get fertilizer
    prob_treat_obs = np.where(z == 1, 0.8, 0.3)
    treat_obs = np.random.binomial(1, prob_treat_obs)

    # RCT: treatment assigned randomly (coin flip)
    treat_rct = np.random.binomial(1, 0.5, n)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # LEFT: Observational
    obs_treat_good = z[treat_obs == 1].mean()
    obs_treat_poor = 1 - obs_treat_good
    obs_ctrl_good = z[treat_obs == 0].mean()
    obs_ctrl_poor = 1 - obs_ctrl_good

    x_pos = np.array([0, 1])
    width = 0.35

    ax1.bar(
        x_pos,
        [obs_treat_poor * 100, obs_ctrl_poor * 100],
        width,
        label="Suelo pobre",
        color=COLORS["orange"],
        edgecolor="white",
        linewidth=1.5,
    )
    ax1.bar(
        x_pos,
        [obs_treat_good * 100, obs_ctrl_good * 100],
        width,
        bottom=[obs_treat_poor * 100, obs_ctrl_poor * 100],
        label="Suelo bueno",
        color=COLORS["green"],
        edgecolor="white",
        linewidth=1.5,
    )

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(["Con fertilizante", "Sin fertilizante"])
    ax1.set_ylim(0, 110)
    ax1.set_ylabel("Composición del grupo (%)")
    ax1.set_title("Observacional\n(grupos desbalanceados)", fontsize=14)
    ax1.legend(loc="upper right")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # Annotation for imbalance
    ax1.annotate(
        "Más suelo\nbueno →\nsesgo",
        xy=(0, obs_treat_poor * 100 + obs_treat_good * 50),
        xytext=(-0.45, 60),
        fontsize=10,
        color=COLORS["red"],
        arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.5),
    )

    # RIGHT: RCT
    rct_treat_good = z[treat_rct == 1].mean()
    rct_treat_poor = 1 - rct_treat_good
    rct_ctrl_good = z[treat_rct == 0].mean()
    rct_ctrl_poor = 1 - rct_ctrl_good

    ax2.bar(
        x_pos,
        [rct_treat_poor * 100, rct_ctrl_poor * 100],
        width,
        label="Suelo pobre",
        color=COLORS["orange"],
        edgecolor="white",
        linewidth=1.5,
    )
    ax2.bar(
        x_pos,
        [rct_treat_good * 100, rct_ctrl_good * 100],
        width,
        bottom=[rct_treat_poor * 100, rct_ctrl_poor * 100],
        label="Suelo bueno",
        color=COLORS["green"],
        edgecolor="white",
        linewidth=1.5,
    )

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(["Con fertilizante", "Sin fertilizante"])
    ax2.set_ylim(0, 110)
    ax2.set_ylabel("Composición del grupo (%)")
    ax2.set_title("RCT (aleatorizado)\n(grupos balanceados)", fontsize=14)
    ax2.legend(loc="upper right")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.suptitle(
        "Distribución del confounder (calidad del suelo) por grupo de tratamiento",
        fontsize=16,
        y=1.02,
    )
    fig.tight_layout()
    _save(fig, "rct_balance.png")


# -----------------------------------------------------------------------------
# 5) Residual diagnosis — causal vs. anti-causal direction
# -----------------------------------------------------------------------------


def plot_residual_diagnosis():
    """Residual independence: causal direction vs anti-causal direction.

    Key idea from 'Elements of Causal Inference' (Peters, Janzing, Schölkopf):
    If X → Y with additive noise (Y = f(X) + N, N ⊥ X), then:
      - Causal direction:      residuals of Y ~ f(X) are independent of X
      - Anti-causal direction:  residuals of X ~ g(Y) show dependence on Y
    This asymmetry is a NECESSARY (not sufficient) condition for the causal
    direction.
    """

    n = 800
    x = np.random.uniform(-3, 3, n)
    noise = np.random.normal(0, 0.4, n)
    y = np.tanh(x) + noise  # Y = tanh(X) + N,  N ⊥ X

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # --- Top row: CAUSAL direction (X → Y) ---

    # Top-left: scatter + fit
    ax = axes[0, 0]
    order = np.argsort(x)
    x_fine = np.linspace(-3, 3, 200)

    # Fit polynomial (degree 5 to approximate tanh well)
    coefs_causal = np.polyfit(x, y, 5)
    y_fit = np.polyval(coefs_causal, x_fine)

    ax.scatter(x, y, alpha=0.3, s=12, color=COLORS["blue"])
    ax.plot(x_fine, y_fit, color=COLORS["red"], lw=2.5, label="$\\hat{f}(X)$")
    ax.set_xlabel("X (causa)")
    ax.set_ylabel("Y (efecto)")
    ax.set_title("Dirección causal: Y = f(X) + ruido", fontweight="bold")
    ax.legend(fontsize=11)

    # Top-right: residuals of Y ~ f(X) vs X → should be FLAT
    ax = axes[0, 1]
    residuals_causal = y - np.polyval(coefs_causal, x)
    ax.scatter(x, residuals_causal, alpha=0.3, s=12, color=COLORS["green"])
    ax.axhline(0, color="gray", lw=1, ls="--")
    ax.set_xlabel("X")
    ax.set_ylabel("Residuos: Y − f(X)")
    ax.set_title("Residuos vs X: banda plana (independientes)", fontweight="bold",
                 color=COLORS["green"])

    # Compute correlation for annotation
    corr_causal = np.corrcoef(x, residuals_causal)[0, 1]
    ax.text(0.05, 0.92, f"Corr(residuos, X) = {corr_causal:.3f}",
            transform=ax.transAxes, fontsize=11, fontweight="bold",
            color=COLORS["green"],
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    # --- Bottom row: ANTI-CAUSAL direction (Y → X) ---

    # Bottom-left: scatter + fit (reversed)
    ax = axes[1, 0]
    coefs_anti = np.polyfit(y, x, 5)
    y_fine = np.linspace(y.min(), y.max(), 200)
    x_fit = np.polyval(coefs_anti, y_fine)

    ax.scatter(y, x, alpha=0.3, s=12, color=COLORS["blue"])
    ax.plot(y_fine, x_fit, color=COLORS["red"], lw=2.5, label="$\\hat{g}(Y)$")
    ax.set_xlabel("Y (efecto)")
    ax.set_ylabel("X (causa)")
    ax.set_title("Dirección anti-causal: X = g(Y) + ruido", fontweight="bold")
    ax.legend(fontsize=11)

    # Bottom-right: residuals of X ~ g(Y) vs Y → should show STRUCTURE
    ax = axes[1, 1]
    residuals_anti = x - np.polyval(coefs_anti, y)
    ax.scatter(y, residuals_anti, alpha=0.3, s=12, color=COLORS["red"])
    ax.axhline(0, color="gray", lw=1, ls="--")
    ax.set_xlabel("Y")
    ax.set_ylabel("Residuos: X − g(Y)")
    ax.set_title("Residuos vs Y: estructura visible (dependientes)", fontweight="bold",
                 color=COLORS["red"])

    corr_anti = np.corrcoef(y, residuals_anti)[0, 1]
    ax.text(0.05, 0.92, f"Corr(residuos, Y) = {corr_anti:.3f}",
            transform=ax.transAxes, fontsize=11, fontweight="bold",
            color=COLORS["red"],
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    fig.suptitle(
        "Diagnóstico de residuos: asimetría entre dirección causal y anti-causal\n"
        "(Elements of Causal Inference — Peters, Janzing, Schölkopf)",
        fontsize=14, y=1.03,
    )
    fig.tight_layout()
    _save(fig, "residual_diagnosis.png")


# -----------------------------------------------------------------------------
# 6) Conditional independence — scatter before/after conditioning
# -----------------------------------------------------------------------------


def plot_conditional_independence():
    """Fork Z→X, Z→Y (no direct X→Y): correlation vanishes when conditioning on Z.

    This demonstrates the testable implication of a fork:
    the DAG implies X ⊥ Y | Z, which we can check in the data.
    """

    n = 1500

    # Pure fork: Z causes both X and Y, but X does NOT cause Y
    z = np.random.normal(0, 1, n)
    x = 1.5 * z + np.random.normal(0, 1, n)  # Z → X
    y = 2.0 * z + np.random.normal(0, 1, n)  # Z → Y, no X → Y

    # Define Z terciles for stratification
    z_low = np.percentile(z, 33)
    z_high = np.percentile(z, 67)
    mask_low = z < z_low
    mask_mid = (z >= z_low) & (z < z_high)
    mask_high = z >= z_high

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    # Panel 1: Unconditional scatter — X and Y look correlated
    ax1.scatter(x, y, alpha=0.25, s=15, color=COLORS["blue"])
    # Fit line
    m, b = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min(), x.max(), 100)
    ax1.plot(x_line, m * x_line + b, color=COLORS["red"], lw=2.5)
    corr_total = np.corrcoef(x, y)[0, 1]
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_title("Sin condicionar\n(X e Y parecen correlacionados)", fontweight="bold")
    ax1.text(0.05, 0.92, f"Corr(X,Y) = {corr_total:.3f}",
             transform=ax1.transAxes, fontsize=12, fontweight="bold",
             color=COLORS["red"],
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    # Panel 2: Colored by Z terciles with per-group regression lines
    for mask, label, color in [
        (mask_low, "Z bajo", COLORS["blue"]),
        (mask_mid, "Z medio", COLORS["orange"]),
        (mask_high, "Z alto", COLORS["red"]),
    ]:
        ax2.scatter(x[mask], y[mask], alpha=0.3, s=15, color=color, label=label)
        m_g, b_g = np.polyfit(x[mask], y[mask], 1)
        x_g = np.linspace(x[mask].min(), x[mask].max(), 50)
        ax2.plot(x_g, m_g * x_g + b_g, color=color, lw=2, ls="--")

    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.set_title("Condicionando en Z (terciles)\n(dentro de cada grupo: poca correlación)",
                  fontweight="bold")
    ax2.legend(loc="upper left", fontsize=10)

    # Panel 3: Bar chart of correlations
    corrs_within = []
    for mask in [mask_low, mask_mid, mask_high]:
        corrs_within.append(np.corrcoef(x[mask], y[mask])[0, 1])
    avg_within = np.mean(corrs_within)

    labels_bar = ["Sin\ncondicionar", "Z bajo", "Z medio", "Z alto", "Promedio\n|Z"]
    vals_bar = [corr_total] + corrs_within + [avg_within]
    colors_bar = [COLORS["red"], COLORS["blue"], COLORS["orange"],
                  COLORS["red"], COLORS["green"]]

    bars = ax3.bar(labels_bar, vals_bar, color=colors_bar, width=0.55,
                   edgecolor="white", linewidth=1.5)
    for bar, val in zip(bars, vals_bar):
        ax3.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.02 if val >= 0 else bar.get_height() - 0.05,
                 f"{val:.3f}", ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax3.axhline(0, color="gray", lw=1)
    ax3.set_ylabel("Correlación")
    ax3.set_title("Correlación total vs condicional\n(la espuria desaparece)",
                  fontweight="bold")
    ax3.set_ylim(-0.3, 1.0)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)

    fig.suptitle(
        "Independencia condicional en un fork: X ← Z → Y (sin X → Y)\n"
        "Implicacion del DAG: X indep. Y | Z  ->  la correlacion espuria DESAPARECE al condicionar",
        fontsize=14, y=1.04,
    )
    fig.tight_layout()
    _save(fig, "conditional_independence.png")


# -----------------------------------------------------------------------------
# 7) Causal falsification — testing DAG implications
# -----------------------------------------------------------------------------


def plot_causal_falsification():
    """Visual diagram: how to test (falsify) a causal model with data.

    Shows the framework: Model → Testable Implications → Data Check.
    Necessary but NOT sufficient conditions.
    """

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # --- Title ---
    ax.text(5, 6.6, "Verificación de un modelo causal: condiciones necesarias",
            ha="center", va="center", fontsize=16, fontweight="bold")
    ax.text(5, 6.2,
            '"Los datos no pueden probar causalidad, pero sí pueden refutarla"',
            ha="center", va="center", fontsize=11, fontstyle="italic",
            color=COLORS["gray"])

    # --- Box 1: Model ---
    box1 = mpatches.FancyBboxPatch((0.5, 4.3), 2.5, 1.4,
                                    boxstyle="round,pad=0.15",
                                    facecolor=COLORS["blue"], alpha=0.15,
                                    edgecolor=COLORS["blue"], linewidth=2)
    ax.add_patch(box1)
    ax.text(1.75, 5.3, "1. MODELO", ha="center", va="center",
            fontsize=13, fontweight="bold", color=COLORS["blue"])
    ax.text(1.75, 4.8, "DAG causal\n(conocimiento\ndel dominio)",
            ha="center", va="center", fontsize=10, color=COLORS["blue"])

    # Arrow 1→2
    ax.annotate("", xy=(3.7, 5.0), xytext=(3.1, 5.0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["gray"],
                                lw=2.5, mutation_scale=20))

    # --- Box 2: Testable Implications ---
    box2 = mpatches.FancyBboxPatch((3.7, 4.3), 2.8, 1.4,
                                    boxstyle="round,pad=0.15",
                                    facecolor=COLORS["purple"], alpha=0.15,
                                    edgecolor=COLORS["purple"], linewidth=2)
    ax.add_patch(box2)
    ax.text(5.1, 5.3, "2. IMPLICACIONES", ha="center", va="center",
            fontsize=13, fontweight="bold", color=COLORS["purple"])
    ax.text(5.1, 4.75, "Independencias\ncondicionales\n(d-separación)",
            ha="center", va="center", fontsize=10, color=COLORS["purple"])

    # Arrow 2→3
    ax.annotate("", xy=(7.2, 5.0), xytext=(6.6, 5.0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["gray"],
                                lw=2.5, mutation_scale=20))

    # --- Box 3: Data Check ---
    box3 = mpatches.FancyBboxPatch((7.2, 4.3), 2.3, 1.4,
                                    boxstyle="round,pad=0.15",
                                    facecolor=COLORS["orange"], alpha=0.15,
                                    edgecolor=COLORS["orange"], linewidth=2)
    ax.add_patch(box3)
    ax.text(8.35, 5.3, "3. DATOS", ha="center", va="center",
            fontsize=13, fontweight="bold", color=COLORS["orange"])
    ax.text(8.35, 4.8, "Verificar en\nobservaciones",
            ha="center", va="center", fontsize=10, color=COLORS["orange"])

    # --- Result boxes ---
    # Arrow down from Data to results
    ax.annotate("", xy=(7.3, 3.5), xytext=(7.8, 4.2),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["red"],
                                lw=2, mutation_scale=18))
    ax.annotate("", xy=(9.0, 3.5), xytext=(8.7, 4.2),
                arrowprops=dict(arrowstyle="-|>", color=COLORS["green"],
                                lw=2, mutation_scale=18))

    # Falsified
    box_fail = mpatches.FancyBboxPatch((6.0, 2.4), 2.3, 1.0,
                                        boxstyle="round,pad=0.1",
                                        facecolor=COLORS["red"], alpha=0.15,
                                        edgecolor=COLORS["red"], linewidth=2)
    ax.add_patch(box_fail)
    ax.text(7.15, 3.15, "FALLA", ha="center", va="center",
            fontsize=12, fontweight="bold", color=COLORS["red"])
    ax.text(7.15, 2.75, "Modelo REFUTADO\n(DAG incorrecto)",
            ha="center", va="center", fontsize=9, color=COLORS["red"])

    # Consistent
    box_pass = mpatches.FancyBboxPatch((8.5, 2.4), 1.5, 1.0,
                                        boxstyle="round,pad=0.1",
                                        facecolor=COLORS["green"], alpha=0.15,
                                        edgecolor=COLORS["green"], linewidth=2)
    ax.add_patch(box_pass)
    ax.text(9.25, 3.15, "PASA", ha="center", va="center",
            fontsize=12, fontweight="bold", color=COLORS["green"])
    ax.text(9.25, 2.75, "Evidencia\na favor",
            ha="center", va="center", fontsize=9, color=COLORS["green"])

    # --- Warning box ---
    box_warn = mpatches.FancyBboxPatch((0.5, 1.0), 9.0, 1.0,
                                        boxstyle="round,pad=0.15",
                                        facecolor="#FFF3CD",
                                        edgecolor=COLORS["orange"], linewidth=2)
    ax.add_patch(box_warn)
    ax.text(5.0, 1.65, "IMPORTANTE: Estas pruebas son NECESARIAS pero NO SUFICIENTES",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color="#856404")
    ax.text(5.0, 1.25,
            "Si fallan → el modelo es incorrecto.   Si pasan → el modelo es consistente con los datos, "
            "pero otros DAGs también podrían serlo.",
            ha="center", va="center", fontsize=10, color="#856404")

    # --- Example implications on the left ---
    ax.text(1.75, 3.8, "Ejemplo de implicaciones:", ha="center", va="center",
            fontsize=10, fontweight="bold", color=COLORS["gray"])
    ax.text(1.75, 3.3,
            "Fork  X ← Z → Y:\n"
            "  X indep Y | Z  (espuria desaparece)\n"
            "Collider  X -> C <- Y:\n"
            "  X indep Y  (independientes sin cond)\n"
            "Residuos: asimetría causal",
            ha="center", va="center", fontsize=9, color=COLORS["gray"],
            family="monospace",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#f8f8f8",
                      edgecolor=COLORS["gray"], alpha=0.5))

    fig.tight_layout()
    _save(fig, "causal_testing.png")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    print("Generando imágenes para módulo 11: Grafos Causales\n")
    plot_simpson_beca()
    plot_graph_surgery()
    plot_confounding_adjustment()
    plot_rct_balance()
    plot_residual_diagnosis()
    plot_conditional_independence()
    plot_causal_falsification()
    print("\n¡Todas las imágenes generadas!")


if __name__ == "__main__":
    main()
