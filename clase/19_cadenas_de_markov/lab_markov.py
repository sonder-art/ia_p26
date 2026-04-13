#!/usr/bin/env python3
"""
Laboratorio: Cadenas de Markov (imágenes para las notas)

Uso:
    cd clase/19_cadenas_de_markov
    python3 lab_markov.py

Genera 14 imágenes en:
    clase/19_cadenas_de_markov/images/

Dependencias: numpy, matplotlib
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np

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

ROOT = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

np.random.seed(42)


def _save(fig, name: str) -> None:
    out = IMAGES_DIR / name
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"✓  {out.name}")


# ---------------------------------------------------------------------------
# Markov chain helpers
# ---------------------------------------------------------------------------

def simulate_chain(P, start, n_steps, rng=None):
    """Simulate a Markov chain for n_steps given transition matrix P."""
    if rng is None:
        rng = np.random.default_rng(42)
    k = P.shape[0]
    states = [start]
    for _ in range(n_steps):
        current = states[-1]
        states.append(rng.choice(k, p=P[current]))
    return np.array(states)


def stationary_distribution(P):
    """Compute stationary distribution via eigenvalue decomposition."""
    eigenvalues, eigenvectors = np.linalg.eig(P.T)
    idx = np.argmin(np.abs(eigenvalues - 1.0))
    pi = np.real(eigenvectors[:, idx])
    pi = pi / pi.sum()
    return pi


# ---------------------------------------------------------------------------
# V/C transition matrix (from Spanish text analysis)
# ---------------------------------------------------------------------------
P_VC = np.array([
    [0.35, 0.65],   # V -> V, V -> C
    [0.52, 0.48],   # C -> V, C -> C
])
VC_LABELS = ["V", "C"]
VC_COLORS = [COLORS["blue"], COLORS["red"]]

# ---------------------------------------------------------------------------
# Market regime transition matrix
# ---------------------------------------------------------------------------
P_MARKET = np.array([
    [0.70, 0.15, 0.15],   # Bull -> Bull, Bear, Flat
    [0.10, 0.65, 0.25],   # Bear -> Bull, Bear, Flat
    [0.20, 0.15, 0.65],   # Flat -> Bull, Bear, Flat
])
MARKET_LABELS = ["Alcista", "Bajista", "Lateral"]
MARKET_COLORS = [COLORS["green"], COLORS["red"], COLORS["orange"]]


# ===================================================================
# IMAGE 01: Nekrasov vs Markov timeline
# ===================================================================
def fig_01_timeline():
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(1895, 1960)
    ax.set_ylim(-1.5, 2.5)
    ax.axis("off")

    # Timeline base
    ax.plot([1898, 1955], [0, 0], color=COLORS["dark"], linewidth=2, zorder=1)

    events = [
        (1902, 1.2, "Nekrasov 1902\nLLN requiere\nindependencia → Dios",
         COLORS["red"], "o"),
        (1906, -1.0, "Markov 1906\nIntroduce las\n«cadenas»",
         COLORS["blue"], "s"),
        (1913, 1.2, "Markov 1913\nAnaliza Eugene Onegin\n20,000 caracteres V/C",
         COLORS["blue"], "s"),
        (1936, -1.0, "Kolmogorov 1936\nFormalización\naxiomática",
         COLORS["purple"], "D"),
        (1948, 1.2, "Shannon 1948\nTeoría de la\ninformación",
         COLORS["teal"], "^"),
        (1953, -1.0, "Metropolis 1953\nMCMC",
         COLORS["green"], "p"),
    ]

    for year, y_text, label, color, marker in events:
        ax.plot(year, 0, marker=marker, markersize=12, color=color, zorder=3)
        ax.plot([year, year], [0, y_text * 0.5], color=color,
                linewidth=1, linestyle="--", zorder=2)
        ax.text(year, y_text, label, ha="center", va="center",
                fontsize=9, color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor=color, alpha=0.9))

    ax.set_title("De la disputa teológica a las herramientas modernas",
                 fontsize=14, fontweight="bold", pad=15)
    _save(fig, "01_nekrasov_vs_markov.png")


# ===================================================================
# IMAGE 02: Markov property diagram
# ===================================================================
def fig_02_markov_property():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: full memory (all arrows from past to future)
    ax = axes[0]
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-1, 1.5)
    ax.axis("off")
    ax.set_title("Sin propiedad de Markov\n(memoria completa)", fontsize=12,
                 fontweight="bold")

    positions = np.arange(6)
    labels = [f"$X_{{{i}}}$" for i in range(6)]
    for i, (x, lbl) in enumerate(zip(positions, labels)):
        color = COLORS["gray"] if i < 4 else (COLORS["blue"] if i == 4 else COLORS["green"])
        c = plt.Circle((x, 0), 0.3, color=color, zorder=3, alpha=0.8)
        ax.add_patch(c)
        ax.text(x, 0, lbl, ha="center", va="center", fontsize=12,
                color="white", fontweight="bold", zorder=4)

    # Arrows from ALL past to X_5
    for i in range(5):
        ax.annotate("", xy=(5, 0.35), xytext=(i, 0.35),
                     arrowprops=dict(arrowstyle="->", color=COLORS["red"],
                                     lw=1.5, alpha=0.5))

    # Right: Markov property (only X_t to X_{t+1})
    ax = axes[1]
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-1, 1.5)
    ax.axis("off")
    ax.set_title("Con propiedad de Markov\n(solo depende del presente)", fontsize=12,
                 fontweight="bold")

    for i, (x, lbl) in enumerate(zip(positions, labels)):
        color = COLORS["gray"] if i < 4 else (COLORS["blue"] if i == 4 else COLORS["green"])
        alpha = 0.3 if i < 4 else 0.8
        c = plt.Circle((x, 0), 0.3, color=color, zorder=3, alpha=alpha)
        ax.add_patch(c)
        ax.text(x, 0, lbl, ha="center", va="center", fontsize=12,
                color="white", fontweight="bold", zorder=4,
                alpha=0.4 if i < 4 else 1.0)

    # Only arrow from X_4 to X_5
    ax.annotate("", xy=(5, 0.35), xytext=(4, 0.35),
                 arrowprops=dict(arrowstyle="->", color=COLORS["green"],
                                 lw=3))
    # Cross out old arrows
    for i in range(4):
        ax.plot([i, 5], [0.5, 0.7], color=COLORS["red"], lw=1,
                alpha=0.3, linestyle="--")
        ax.text((i + 5) / 2, 0.7, "x", color=COLORS["red"], fontsize=8,
                ha="center", alpha=0.5)

    fig.tight_layout(pad=2)
    _save(fig, "02_markov_property.png")


# ===================================================================
# IMAGE 03: V/C state diagram
# ===================================================================
def _draw_chain_diagram(ax, P, labels, colors, title, radius=0.6, sep=3.5):
    """Draw a state diagram for a Markov chain on the given axes."""
    k = len(labels)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=15)

    if k == 2:
        positions = [(-sep / 2, 0), (sep / 2, 0)]
    elif k == 3:
        angle_offset = np.pi / 2
        positions = [(sep * np.cos(angle_offset + 2 * np.pi * i / 3),
                      sep * np.sin(angle_offset + 2 * np.pi * i / 3))
                     for i in range(3)]
    else:
        positions = [(sep * np.cos(2 * np.pi * i / k),
                      sep * np.sin(2 * np.pi * i / k)) for i in range(k)]

    # Draw nodes
    for i, (pos, label, color) in enumerate(zip(positions, labels, colors)):
        c = plt.Circle(pos, radius, color=color, zorder=3, alpha=0.85)
        ax.add_patch(c)
        ax.text(pos[0], pos[1], label, ha="center", va="center",
                fontsize=14, color="white", fontweight="bold", zorder=4)

    # Draw transitions
    for i in range(k):
        for j in range(k):
            if P[i, j] < 0.01:
                continue
            if i == j:
                # Self-loop
                px, py = positions[i]
                loop_y = py + radius + 0.2
                # Draw arc for self-loop
                angle = 90
                if k == 3 and i > 0:
                    dx = positions[i][0]
                    dy = positions[i][1]
                    angle = np.degrees(np.arctan2(dy, dx))

                arc = mpatches.Arc((px, py + radius + 0.35), 0.8, 0.8,
                                   angle=0, theta1=210, theta2=330,
                                   color=COLORS["dark"], lw=1.5, zorder=2)
                ax.add_patch(arc)
                ax.text(px, py + radius + 0.85, f"{P[i,j]:.2f}",
                        ha="center", va="center", fontsize=9,
                        color=COLORS["dark"],
                        bbox=dict(boxstyle="round,pad=0.15",
                                  facecolor="white", edgecolor="none"))
            else:
                # Transition arrow
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                dx, dy = x2 - x1, y2 - y1
                dist = np.sqrt(dx**2 + dy**2)
                ux, uy = dx / dist, dy / dist

                start_x = x1 + ux * (radius + 0.05)
                start_y = y1 + uy * (radius + 0.05)
                end_x = x2 - ux * (radius + 0.15)
                end_y = y2 - uy * (radius + 0.15)

                # Offset for bidirectional arrows
                perp_x, perp_y = -uy, ux
                offset = 0.15
                start_x += perp_x * offset
                start_y += perp_y * offset
                end_x += perp_x * offset
                end_y += perp_y * offset

                ax.annotate("", xy=(end_x, end_y),
                            xytext=(start_x, start_y),
                            arrowprops=dict(arrowstyle="-|>",
                                            color=COLORS["dark"],
                                            lw=1.5,
                                            connectionstyle="arc3,rad=0.1"))

                mid_x = (start_x + end_x) / 2 + perp_x * 0.25
                mid_y = (start_y + end_y) / 2 + perp_y * 0.25
                ax.text(mid_x, mid_y, f"{P[i,j]:.2f}",
                        ha="center", va="center", fontsize=9,
                        color=COLORS["dark"],
                        bbox=dict(boxstyle="round,pad=0.15",
                                  facecolor="white", edgecolor="none"))

    margin = sep + radius + 1.5
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)


def fig_03_vc_chain():
    fig, ax = plt.subplots(figsize=(8, 6))
    _draw_chain_diagram(ax, P_VC, VC_LABELS, VC_COLORS,
                        "Cadena de Markov: Vocales y Consonantes",
                        radius=0.7, sep=3.0)
    _save(fig, "03_vc_chain_diagram.png")


# ===================================================================
# IMAGE 04: Market regime diagram
# ===================================================================
def fig_04_market_chain():
    fig, ax = plt.subplots(figsize=(9, 8))
    _draw_chain_diagram(ax, P_MARKET, MARKET_LABELS, MARKET_COLORS,
                        "Cadena de Markov: Regímenes de Mercado",
                        radius=0.9, sep=3.0)
    _save(fig, "04_market_chain_diagram.png")


# ===================================================================
# IMAGE 05: V/C simulation trace
# ===================================================================
def fig_05_vc_simulation():
    rng = np.random.default_rng(42)
    chain = simulate_chain(P_VC, 1, 50, rng=rng)  # start at C

    fig, axes = plt.subplots(2, 1, figsize=(14, 6), gridspec_kw={"height_ratios": [1, 2]})

    # Top: state ribbon
    ax = axes[0]
    for t in range(len(chain)):
        color = VC_COLORS[chain[t]]
        ax.barh(0, 1, left=t, color=color, edgecolor="white", linewidth=0.5)
    ax.set_xlim(0, len(chain))
    ax.set_yticks([])
    ax.set_xlabel("Paso", fontsize=11)
    ax.set_title("Trayectoria de la cadena V/C (50 pasos, inicio = C)",
                 fontsize=13, fontweight="bold")

    legend_elements = [mpatches.Patch(facecolor=VC_COLORS[0], label="V (vocal)"),
                       mpatches.Patch(facecolor=VC_COLORS[1], label="C (consonante)")]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=10)

    # Bottom: running frequency
    ax = axes[1]
    freq_v = np.cumsum(chain == 0) / np.arange(1, len(chain) + 1)
    ax.plot(freq_v, color=COLORS["blue"], linewidth=2, label="Frecuencia de V")
    pi = stationary_distribution(P_VC)
    ax.axhline(pi[0], color=COLORS["dark"], linestyle="--", linewidth=1.5,
               label=f"$\\pi_V = {pi[0]:.3f}$")
    ax.set_xlabel("Paso", fontsize=11)
    ax.set_ylabel("Fracción de V", fontsize=11)
    ax.set_ylim(0, 1)
    ax.legend(fontsize=10)
    ax.set_title("Convergencia de la frecuencia de vocales", fontsize=12)

    fig.tight_layout(pad=2)
    _save(fig, "05_vc_simulation_trace.png")


# ===================================================================
# IMAGE 06: Matrix power convergence
# ===================================================================
def fig_06_matrix_power_convergence():
    powers = [1, 2, 4, 8, 16, 32]
    fig, axes = plt.subplots(1, len(powers), figsize=(18, 3.5))

    pi = stationary_distribution(P_VC)
    for idx, n in enumerate(powers):
        ax = axes[idx]
        Pn = np.linalg.matrix_power(P_VC, n)
        im = ax.imshow(Pn, cmap="YlOrRd", vmin=0, vmax=1, aspect="equal")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(VC_LABELS, fontsize=10)
        ax.set_yticklabels(VC_LABELS, fontsize=10)
        ax.set_title(f"$P^{{{n}}}$", fontsize=13, fontweight="bold")

        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{Pn[i,j]:.3f}", ha="center", va="center",
                        fontsize=11, color="black" if Pn[i, j] < 0.6 else "white")

    fig.suptitle("Las filas de $P^n$ convergen a la distribución estacionaria "
                 f"$\\pi = [{pi[0]:.3f}, {pi[1]:.3f}]$",
                 fontsize=13, fontweight="bold", y=1.05)
    fig.tight_layout(pad=1)
    _save(fig, "06_matrix_power_convergence.png")


# ===================================================================
# IMAGE 07: State classification
# ===================================================================
def fig_07_state_classification():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(-1, 15)
    ax.set_ylim(-2, 4)
    ax.axis("off")
    ax.set_title("Clasificación de estados", fontsize=14, fontweight="bold")

    # States for a student progression model
    states = [
        (1, 1, "1er\nsem", COLORS["blue"], "Transitorio"),
        (3.5, 1, "2do\nsem", COLORS["blue"], ""),
        (6, 1, "3er\nsem", COLORS["blue"], ""),
        (8.5, 1, "4to\nsem", COLORS["blue"], ""),
        (12, 2.5, "Graduado", COLORS["green"], "Absorbente"),
        (12, -0.5, "Deserción", COLORS["red"], "Absorbente"),
    ]

    for x, y, label, color, annotation in states:
        r = 0.6 if "sem" in label else 0.7
        c = plt.Circle((x, y), r, color=color, zorder=3, alpha=0.85)
        ax.add_patch(c)
        ax.text(x, y, label, ha="center", va="center", fontsize=9,
                color="white", fontweight="bold", zorder=4)
        if annotation:
            ax.text(x, y - r - 0.35, annotation, ha="center", fontsize=8,
                    color=color, fontstyle="italic")

    # Forward arrows
    for i in range(3):
        x1 = states[i][0] + 0.65
        x2 = states[i + 1][0] - 0.65
        ax.annotate("", xy=(x2, 1), xytext=(x1, 1),
                     arrowprops=dict(arrowstyle="-|>", color=COLORS["dark"], lw=1.5))

    # To graduated
    ax.annotate("", xy=(11.3, 2.3), xytext=(9.1, 1.3),
                 arrowprops=dict(arrowstyle="-|>", color=COLORS["green"], lw=1.5,
                                 connectionstyle="arc3,rad=-0.2"))
    # To dropout from each semester
    for i in range(4):
        x = states[i][0]
        ax.annotate("", xy=(11.3, -0.3), xytext=(x, 0.4),
                     arrowprops=dict(arrowstyle="-|>", color=COLORS["red"], lw=1,
                                     alpha=0.5, connectionstyle="arc3,rad=0.3"))

    # Self-loops on absorbing states
    for idx in [4, 5]:
        x, y = states[idx][0], states[idx][1]
        arc = mpatches.Arc((x, y + 0.85), 0.8, 0.8, angle=0,
                           theta1=210, theta2=330,
                           color=COLORS["dark"], lw=1.5)
        ax.add_patch(arc)
        ax.text(x, y + 1.4, "1.0", ha="center", fontsize=8, color=COLORS["dark"])

    _save(fig, "07_state_classification.png")


# ===================================================================
# IMAGE 08: Irreducible vs Reducible
# ===================================================================
def fig_08_irreducible_vs_reducible():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: Irreducible (V/C chain — all connected)
    ax = axes[0]
    ax.set_xlim(-3, 3)
    ax.set_ylim(-2, 2.5)
    ax.axis("off")
    ax.set_title("Irreducible\n(todos los estados se comunican)", fontsize=12,
                 fontweight="bold")

    for i, (pos, lbl, col) in enumerate(zip([(-1.2, 0), (1.2, 0)],
                                             ["A", "B"],
                                             [COLORS["blue"], COLORS["teal"]])):
        c = plt.Circle(pos, 0.5, color=col, zorder=3, alpha=0.85)
        ax.add_patch(c)
        ax.text(pos[0], pos[1], lbl, ha="center", va="center",
                fontsize=16, color="white", fontweight="bold", zorder=4)

    # Bidirectional arrows
    ax.annotate("", xy=(0.65, 0.15), xytext=(-0.65, 0.15),
                 arrowprops=dict(arrowstyle="-|>", color=COLORS["dark"], lw=2))
    ax.annotate("", xy=(-0.65, -0.15), xytext=(0.65, -0.15),
                 arrowprops=dict(arrowstyle="-|>", color=COLORS["dark"], lw=2))
    ax.text(0, 0.55, r"A $\to$ B (OK)", ha="center", fontsize=10, color=COLORS["dark"])
    ax.text(0, -0.55, r"B $\to$ A (OK)", ha="center", fontsize=10, color=COLORS["dark"])

    # Right: Reducible (two disconnected groups)
    ax = axes[1]
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-2, 2.5)
    ax.axis("off")
    ax.set_title("Reducible\n(componentes desconectados)", fontsize=12,
                 fontweight="bold")

    group1 = [(-2, 0.5), (-2, -0.8)]
    group2 = [(2, 0.5), (2, -0.8)]
    g1_labels = ["A", "B"]
    g2_labels = ["C", "D"]

    for pos, lbl in zip(group1, g1_labels):
        c = plt.Circle(pos, 0.4, color=COLORS["blue"], zorder=3, alpha=0.85)
        ax.add_patch(c)
        ax.text(pos[0], pos[1], lbl, ha="center", va="center",
                fontsize=14, color="white", fontweight="bold", zorder=4)

    for pos, lbl in zip(group2, g2_labels):
        c = plt.Circle(pos, 0.4, color=COLORS["orange"], zorder=3, alpha=0.85)
        ax.add_patch(c)
        ax.text(pos[0], pos[1], lbl, ha="center", va="center",
                fontsize=14, color="white", fontweight="bold", zorder=4)

    # Arrows within groups
    ax.annotate("", xy=(-2, 0.05), xytext=(-2, -0.35),
                 arrowprops=dict(arrowstyle="<->", color=COLORS["dark"], lw=1.5))
    ax.annotate("", xy=(2, 0.05), xytext=(2, -0.35),
                 arrowprops=dict(arrowstyle="<->", color=COLORS["dark"], lw=1.5))

    # Big X between groups
    ax.text(0, -0.15, "X", ha="center", va="center", fontsize=30,
            color=COLORS["red"], fontweight="bold")
    ax.text(0, -0.85, "No hay camino\nA → C ni C → A", ha="center",
            fontsize=9, color=COLORS["red"])

    # Group boxes
    rect1 = mpatches.FancyBboxPatch((-2.7, -1.5), 1.4, 2.6,
                                     boxstyle="round,pad=0.1",
                                     facecolor=COLORS["blue"], alpha=0.1,
                                     edgecolor=COLORS["blue"], linestyle="--")
    rect2 = mpatches.FancyBboxPatch((1.3, -1.5), 1.4, 2.6,
                                     boxstyle="round,pad=0.1",
                                     facecolor=COLORS["orange"], alpha=0.1,
                                     edgecolor=COLORS["orange"], linestyle="--")
    ax.add_patch(rect1)
    ax.add_patch(rect2)

    fig.tight_layout(pad=2)
    _save(fig, "08_irreducible_vs_reducible.png")


# ===================================================================
# IMAGE 09: Periodic vs Aperiodic
# ===================================================================
def fig_09_periodic_vs_aperiodic():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: Periodic (period 2)
    ax = axes[0]
    ax.set_xlim(-3, 3)
    ax.set_ylim(-2, 2.5)
    ax.axis("off")
    ax.set_title("Periódica (período 2)\nA → B → A → B → ...", fontsize=12,
                 fontweight="bold")

    for pos, lbl, col in zip([(-1.2, 0), (1.2, 0)], ["A", "B"],
                              [COLORS["blue"], COLORS["red"]]):
        c = plt.Circle(pos, 0.5, color=col, zorder=3, alpha=0.85)
        ax.add_patch(c)
        ax.text(pos[0], pos[1], lbl, ha="center", va="center",
                fontsize=16, color="white", fontweight="bold", zorder=4)

    ax.annotate("", xy=(0.65, 0.15), xytext=(-0.65, 0.15),
                 arrowprops=dict(arrowstyle="-|>", color=COLORS["dark"], lw=2))
    ax.text(0, 0.5, "P(A→B) = 1.0", ha="center", fontsize=10, color=COLORS["dark"])
    ax.annotate("", xy=(-0.65, -0.15), xytext=(0.65, -0.15),
                 arrowprops=dict(arrowstyle="-|>", color=COLORS["dark"], lw=2))
    ax.text(0, -0.5, "P(B→A) = 1.0", ha="center", fontsize=10, color=COLORS["dark"])
    ax.text(0, -1.3, "No converge: oscila entre A y B\n$P(X_t = A)$ alterna 0 y 1",
            ha="center", fontsize=9, color=COLORS["red"], fontstyle="italic")

    # Right: Aperiodic (added self-loop)
    ax = axes[1]
    ax.set_xlim(-3, 3)
    ax.set_ylim(-2, 2.5)
    ax.axis("off")
    ax.set_title("Aperiódica (self-loop añadido)\nConverge a π",
                 fontsize=12, fontweight="bold")

    for pos, lbl, col in zip([(-1.2, 0), (1.2, 0)], ["A", "B"],
                              [COLORS["blue"], COLORS["red"]]):
        c = plt.Circle(pos, 0.5, color=col, zorder=3, alpha=0.85)
        ax.add_patch(c)
        ax.text(pos[0], pos[1], lbl, ha="center", va="center",
                fontsize=16, color="white", fontweight="bold", zorder=4)

    ax.annotate("", xy=(0.65, 0.15), xytext=(-0.65, 0.15),
                 arrowprops=dict(arrowstyle="-|>", color=COLORS["dark"], lw=2))
    ax.text(0, 0.5, "0.7", ha="center", fontsize=10, color=COLORS["dark"])
    ax.annotate("", xy=(-0.65, -0.15), xytext=(0.65, -0.15),
                 arrowprops=dict(arrowstyle="-|>", color=COLORS["dark"], lw=2))
    ax.text(0, -0.5, "0.8", ha="center", fontsize=10, color=COLORS["dark"])

    # Self-loops
    for x, prob in [(-1.2, "0.3"), (1.2, "0.2")]:
        arc = mpatches.Arc((x, 0.7), 0.7, 0.7, angle=0,
                           theta1=210, theta2=330,
                           color=COLORS["green"], lw=2)
        ax.add_patch(arc)
        ax.text(x, 1.25, prob, ha="center", fontsize=10, color=COLORS["green"],
                fontweight="bold")

    ax.text(0, -1.3, "Converge: P(A→A) > 0 rompe la periodicidad\n"
                      "$P^n$ → π para todo estado inicial",
            ha="center", fontsize=9, color=COLORS["green"], fontstyle="italic")

    fig.tight_layout(pad=2)
    _save(fig, "09_periodic_vs_aperiodic.png")


# ===================================================================
# IMAGE 10: Stationary distribution
# ===================================================================
def fig_10_stationary_distribution():
    pi = stationary_distribution(P_VC)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: bar chart
    ax = axes[0]
    bars = ax.bar(VC_LABELS, pi, color=VC_COLORS, alpha=0.85, edgecolor="white",
                  linewidth=2, width=0.5)
    for bar, val in zip(bars, pi):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"π = {val:.3f}", ha="center", fontsize=12, fontweight="bold")
    ax.set_ylim(0, 0.7)
    ax.set_ylabel("Probabilidad estacionaria", fontsize=11)
    ax.set_title("Distribución estacionaria π", fontsize=13, fontweight="bold")
    ax.grid(axis="x", visible=False)

    # Right: verification
    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Verificación: πP = π", fontsize=13, fontweight="bold")

    pi_P = pi @ P_VC
    lines = [
        f"π = [{pi[0]:.3f},  {pi[1]:.3f}]",
        "",
        f"πP = [{pi[0]:.3f},  {pi[1]:.3f}]  ×  [0.35  0.65]",
        f"                                [0.52  0.48]",
        "",
        f"   = [{pi[0]:.3f} × 0.35 + {pi[1]:.3f} × 0.52,",
        f"      {pi[0]:.3f} × 0.65 + {pi[1]:.3f} × 0.48]",
        "",
        f"   = [{pi_P[0]:.3f},  {pi_P[1]:.3f}]  =  π  ✓",
    ]
    for i, line in enumerate(lines):
        ax.text(0.5, 9 - i * 0.9, line, fontsize=11, fontfamily="monospace",
                va="top")

    fig.tight_layout(pad=2)
    _save(fig, "10_stationary_distribution.png")


# ===================================================================
# IMAGE 11: Coupling argument
# ===================================================================
def fig_11_coupling_argument():
    rng = np.random.default_rng(123)
    n_steps = 30

    # Generate shared random numbers
    us = rng.random(n_steps)

    # Chain X starts at V (0), Chain Y starts at C (1)
    chain_x = [0]
    chain_y = [1]

    coupling_time = None
    for t in range(n_steps):
        u = us[t]
        # Transition for X
        row_x = P_VC[chain_x[-1]]
        next_x = 0 if u < row_x[0] else 1

        # Transition for Y
        row_y = P_VC[chain_y[-1]]
        next_y = 0 if u < row_y[0] else 1

        chain_x.append(next_x)
        chain_y.append(next_y)

        if coupling_time is None and next_x == next_y:
            coupling_time = t + 1

    chain_x = np.array(chain_x)
    chain_y = np.array(chain_y)

    fig, axes = plt.subplots(2, 1, figsize=(14, 6), sharex=True)

    for ax, chain, label, start_label in zip(axes,
                                              [chain_x, chain_y],
                                              ["Cadena X", "Cadena Y"],
                                              ["V", "C"]):
        for t in range(len(chain)):
            color = VC_COLORS[chain[t]]
            alpha = 0.4 if coupling_time and t > coupling_time + 1 else 0.9
            ax.barh(0, 1, left=t, color=color, alpha=alpha, edgecolor="white",
                    linewidth=0.3)
        ax.set_yticks([])
        ax.set_ylabel(f"{label}\n(inicio={start_label})", fontsize=11,
                      fontweight="bold")

        if coupling_time is not None:
            ax.axvline(coupling_time, color=COLORS["dark"], linestyle="--",
                       linewidth=2, zorder=5)

    axes[0].set_title(
        "Acoplamiento: dos cadenas, MISMOS números aleatorios, distintos inicios",
        fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Paso", fontsize=11)

    if coupling_time is not None:
        axes[0].text(coupling_time + 0.5, 0.4,
                     f"τ = {coupling_time}\n(acopladas)",
                     fontsize=11, color=COLORS["dark"], fontweight="bold",
                     va="center")

    legend_elements = [mpatches.Patch(facecolor=VC_COLORS[0], label="V"),
                       mpatches.Patch(facecolor=VC_COLORS[1], label="C")]
    axes[0].legend(handles=legend_elements, loc="upper right", fontsize=10)

    fig.tight_layout(pad=2)
    _save(fig, "11_coupling_argument.png")


# ===================================================================
# IMAGE 12: Ergodic convergence from multiple starts
# ===================================================================
def fig_12_ergodic_convergence():
    n_steps = 2000
    n_chains = 12
    pi = stationary_distribution(P_VC)

    fig, ax = plt.subplots(figsize=(14, 6))

    cmap = plt.cm.tab10
    for i in range(n_chains):
        rng = np.random.default_rng(i * 7 + 1)
        start = i % 2  # alternate V and C starts
        chain = simulate_chain(P_VC, start, n_steps, rng=rng)
        freq_v = np.cumsum(chain == 0) / np.arange(1, len(chain) + 1)
        ax.plot(freq_v, color=cmap(i / n_chains), alpha=0.6, linewidth=1)

    ax.axhline(pi[0], color=COLORS["dark"], linestyle="--", linewidth=2.5,
               label=f"$\\pi_V = {pi[0]:.3f}$", zorder=10)

    ax.set_xlabel("Paso ($t$)", fontsize=12)
    ax.set_ylabel("Fracción de tiempo en V", fontsize=12)
    ax.set_title("Teorema ergódico: 12 cadenas desde distintos inicios → "
                 "todas convergen a $\\pi_V$",
                 fontsize=13, fontweight="bold")
    ax.set_ylim(0, 1)
    ax.legend(fontsize=12, loc="upper right")

    _save(fig, "12_ergodic_convergence.png")


# ===================================================================
# IMAGE 13: Breaking ergodicity
# ===================================================================
def fig_13_ergodicity_breaking():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: Periodic chain
    ax = axes[0]
    P_periodic = np.array([[0.0, 1.0], [1.0, 0.0]])
    n_steps = 50
    chain = simulate_chain(P_periodic, 0, n_steps, rng=np.random.default_rng(1))
    prob_A = np.array([(chain[:t+1] == 0).mean() for t in range(len(chain))])
    ax.plot(prob_A, color=COLORS["red"], linewidth=2, label="Frac. en A")
    ax.axhline(0.5, color=COLORS["dark"], linestyle="--", linewidth=1.5,
               label="π = 0.5 (si convergiera)")
    ax.set_xlabel("Paso", fontsize=11)
    ax.set_ylabel("Fracción en A", fontsize=11)
    ax.set_title("Cadena periódica: oscila, no converge",
                 fontsize=12, fontweight="bold")
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=9)

    # Right: Reducible chain
    ax = axes[1]
    P_reducible = np.array([
        [0.6, 0.4, 0.0, 0.0],
        [0.3, 0.7, 0.0, 0.0],
        [0.0, 0.0, 0.5, 0.5],
        [0.0, 0.0, 0.4, 0.6],
    ])
    n_steps = 300
    rng1 = np.random.default_rng(10)
    rng2 = np.random.default_rng(20)
    chain1 = simulate_chain(P_reducible, 0, n_steps, rng=rng1)
    chain2 = simulate_chain(P_reducible, 2, n_steps, rng=rng2)

    freq1_s0 = np.cumsum(chain1 == 0) / np.arange(1, len(chain1) + 1)
    freq2_s0 = np.cumsum(chain2 == 0) / np.arange(1, len(chain2) + 1)

    ax.plot(freq1_s0, color=COLORS["blue"], linewidth=2,
            label="Inicio en A (componente {A,B})")
    ax.plot(freq2_s0, color=COLORS["orange"], linewidth=2,
            label="Inicio en C (componente {C,D})")
    ax.set_xlabel("Paso", fontsize=11)
    ax.set_ylabel("Fracción en A", fontsize=11)
    ax.set_title("Cadena reducible: el resultado depende del inicio",
                 fontsize=12, fontweight="bold")
    ax.set_ylim(-0.05, 0.8)
    ax.legend(fontsize=9)

    fig.tight_layout(pad=2)
    _save(fig, "13_ergodicity_breaking.png")


# ===================================================================
# IMAGE 14: MCMC burn-in
# ===================================================================
def fig_14_mcmc_burnin():
    # Target: mixture of two Gaussians
    def target(x):
        return 0.4 * np.exp(-0.5 * ((x - 2) / 0.8) ** 2) + \
               0.6 * np.exp(-0.5 * ((x + 1.5) / 1.2) ** 2)

    # Metropolis-Hastings
    rng = np.random.default_rng(42)
    n_samples = 5000
    burn_in = 500
    samples = [8.0]  # start far from the modes

    for _ in range(n_samples - 1):
        x = samples[-1]
        y = x + rng.normal(0, 0.8)
        alpha = target(y) / target(x) if target(x) > 0 else 1.0
        if rng.random() < alpha:
            samples.append(y)
        else:
            samples.append(x)

    samples = np.array(samples)

    fig, axes = plt.subplots(2, 1, figsize=(14, 7),
                              gridspec_kw={"height_ratios": [2, 1]})

    # Top: trace plot
    ax = axes[0]
    ax.plot(range(burn_in), samples[:burn_in], color=COLORS["gray"],
            alpha=0.5, linewidth=0.8, label="Burn-in (descartar)")
    ax.plot(range(burn_in, n_samples), samples[burn_in:], color=COLORS["blue"],
            alpha=0.7, linewidth=0.5, label="Muestras útiles")
    ax.axvline(burn_in, color=COLORS["red"], linestyle="--", linewidth=2,
               label=f"Fin burn-in (t = {burn_in})")
    ax.set_xlabel("Iteración", fontsize=11)
    ax.set_ylabel("$x$", fontsize=12)
    ax.set_title("Metropolis-Hastings: traza de la cadena", fontsize=13,
                 fontweight="bold")
    ax.legend(fontsize=10)

    # Bottom: histogram vs target
    ax = axes[1]
    x_grid = np.linspace(-5, 6, 300)
    target_vals = np.array([target(x) for x in x_grid])
    target_vals = target_vals / (target_vals.sum() * (x_grid[1] - x_grid[0]))

    ax.hist(samples[burn_in:], bins=60, density=True, color=COLORS["blue"],
            alpha=0.6, edgecolor="white", linewidth=0.5,
            label="Histograma post-burn-in")
    ax.plot(x_grid, target_vals, color=COLORS["red"], linewidth=2.5,
            label="Distribución objetivo $\\pi(x)$")
    ax.set_xlabel("$x$", fontsize=12)
    ax.set_ylabel("Densidad", fontsize=11)
    ax.set_title("Las muestras post-burn-in se distribuyen según π(x)",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=10)

    fig.tight_layout(pad=2)
    _save(fig, "14_mcmc_burnin.png")


# ===================================================================
# Main
# ===================================================================
if __name__ == "__main__":
    print("Generando imágenes para Módulo 19: Cadenas de Markov\n")
    fig_01_timeline()
    fig_02_markov_property()
    fig_03_vc_chain()
    fig_04_market_chain()
    fig_05_vc_simulation()
    fig_06_matrix_power_convergence()
    fig_07_state_classification()
    fig_08_irreducible_vs_reducible()
    fig_09_periodic_vs_aperiodic()
    fig_10_stationary_distribution()
    fig_11_coupling_argument()
    fig_12_ergodic_convergence()
    fig_13_ergodicity_breaking()
    fig_14_mcmc_burnin()
    print(f"\n✓ {len(list(IMAGES_DIR.glob('*.png')))} imágenes generadas en {IMAGES_DIR}")
