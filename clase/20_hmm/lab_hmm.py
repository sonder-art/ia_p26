"""
lab_hmm.py — Genera las imágenes pedagógicas para clase/20_hmm/

Ejecución:
    cd clase/20_hmm && python lab_hmm.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

plt.style.use("seaborn-v0_8-whitegrid")

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
}

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "figure.dpi": 160,
})

ROOT       = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

np.random.seed(42)

# ── Toy example parameters (Lain / Clima) ──────────────────────────────────────
PI  = np.array([0.6,  0.4])
A   = np.array([[0.7, 0.3],
                [0.4, 0.6]])
B   = np.array([[0.9, 0.1],
                [0.2, 0.8]])
OBS = np.array([0, 1, 1])
T   = len(OBS)
N   = len(PI)

SNAMES = ["S", "R"]

# ── Pre-verified values ─────────────────────────────────────────────────────────
ALPHA = np.array([[0.54000, 0.08000],
                  [0.04100, 0.16800],
                  [0.00959, 0.09048]])

BETA  = np.array([[0.14650, 0.26200],
                  [0.31000, 0.52000],
                  [1.00000, 1.00000]])

DELTA = np.array([[0.54000, 0.08000],
                  [0.03780, 0.12960],
                  [0.00518, 0.06221]])

PSI   = np.array([[0, 0],
                  [0, 0],
                  [1, 1]])

GAMMA = np.array([[0.7906, 0.2094],
                  [0.1270, 0.8730],
                  [0.0958, 0.9042]])

P_OBS   = 0.10007
A_HAT   = np.array([[0.159, 0.841], [0.071, 0.929]])
B_HAT   = np.array([[0.780, 0.220], [0.105, 0.895]])


# ── Helper ─────────────────────────────────────────────────────────────────────
def _save(fig, name):
    fig.savefig(IMAGES_DIR / name, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {name}")


# ── Algorithms (for convergence plot) ──────────────────────────────────────────
def _forward(obs, pi, a, b):
    T_ = len(obs)
    N_ = len(pi)
    alpha = np.zeros((T_, N_))
    alpha[0] = pi * b[:, obs[0]]
    for t in range(1, T_):
        alpha[t] = (alpha[t - 1] @ a) * b[:, obs[t]]
    return alpha, alpha[-1].sum()


def _backward(obs, a, b):
    T_ = len(obs)
    N_ = len(a)
    beta = np.zeros((T_, N_))
    beta[-1] = 1.0
    for t in range(T_ - 2, -1, -1):
        beta[t] = a @ (b[:, obs[t + 1]] * beta[t + 1])
    return beta


def _baum_welch_step(obs, pi, a, b):
    T_ = len(obs)
    N_ = len(pi)
    alpha, p_obs = _forward(obs, pi, a, b)
    beta         = _backward(obs, a, b)
    gamma = (alpha * beta) / p_obs
    xi = np.zeros((T_ - 1, N_, N_))
    for t in range(T_ - 1):
        xi[t] = (alpha[t][:, None] * a * b[:, obs[t + 1]][None, :] *
                 beta[t + 1][None, :]) / p_obs
    pi_new = gamma[0]
    a_new  = xi.sum(axis=0) / gamma[:-1].sum(axis=0)[:, None]
    b_new  = np.zeros_like(b)
    for k in range(b.shape[1]):
        mask = (obs == k)
        b_new[:, k] = gamma[mask].sum(axis=0) / gamma.sum(axis=0)
    return pi_new, a_new, b_new, np.log(p_obs)


def _simulate(pi, a, b, length, rng):
    state = rng.choice(len(pi), p=pi)
    obs_seq = []
    for _ in range(length):
        obs_seq.append(rng.choice(b.shape[1], p=b[state]))
        state = rng.choice(len(pi), p=a[state])
    return np.array(obs_seq)


# ── Trellis helpers ─────────────────────────────────────────────────────────────
def _node(ax, x, y, label, facecolor, radius=0.22, fontsize=8.5, alpha_val=1.0,
          textcolor="white"):
    circle = plt.Circle((x, y), radius, color=facecolor, zorder=3,
                        alpha=alpha_val, linewidth=1.5, edgecolor="white")
    ax.add_patch(circle)
    ax.text(x, y, label, ha="center", va="center", fontsize=fontsize,
            fontweight="bold", color=textcolor, zorder=4)


def _build_trellis(title, values, val_fmt, node_color_fn,
                   arrow_dir, figsize=(12, 5.5),
                   extra_fn=None, psi_arrows=None, path_edges=None):
    xs = [1.0, 2.0, 3.0]
    ys = [1.0, 0.0]
    r  = 0.20

    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0.30, 3.70)
    ax.set_ylim(-0.70, 1.80)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=16)

    # state labels (left)
    for s, (y, name) in enumerate(zip(ys, SNAMES)):
        ax.text(xs[0] - 0.50, y, name, ha="center", va="center",
                fontsize=14, fontweight="bold", color=COLORS["dark"])

    # time labels (bottom)
    obs_labels = ["t=1\n(O=0)", "t=2\n(O=1)", "t=3\n(O=1)"]
    for t, x in enumerate(xs):
        ax.text(x, ys[1] - 0.42, obs_labels[t], ha="center", va="top",
                fontsize=9, color=COLORS["gray"])

    # transition arrows
    for t in range(T - 1):
        for s_from in range(N):
            for s_to in range(N):
                if arrow_dir == "right":
                    x0, y0 = xs[t], ys[s_from]
                    x1, y1 = xs[t + 1], ys[s_to]
                else:
                    x0, y0 = xs[t + 1], ys[s_to]
                    x1, y1 = xs[t], ys[s_from]

                lc = COLORS["gray"]
                lw = 0.8
                al = 0.35
                if path_edges and arrow_dir == "right":
                    if (t, s_from) in path_edges and (t + 1, s_to) in path_edges:
                        lc = COLORS["green"]; lw = 3.0; al = 1.0

                ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                            arrowprops=dict(arrowstyle="->", color=lc, lw=lw,
                                           shrinkA=r * 72, shrinkB=r * 72,
                                           connectionstyle="arc3,rad=0.0"),
                            alpha=al, zorder=2)

    # backpointer arrows (orange, Viterbi)
    if psi_arrows:
        for (t, s_to, s_from) in psi_arrows:
            x0, y0 = xs[t - 1], ys[s_from]
            x1, y1 = xs[t], ys[s_to]
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                        arrowprops=dict(arrowstyle="-|>",
                                       color=COLORS["orange"], lw=2.5,
                                       shrinkA=r * 72, shrinkB=r * 72,
                                       connectionstyle="arc3,rad=0.25"),
                        alpha=0.9, zorder=3)

    # draw nodes
    for t, x in enumerate(xs):
        for s, y in enumerate(ys):
            val  = values[t, s]
            col  = node_color_fn(t, s, val)
            attn = 1.0
            if path_edges and (t, s) not in path_edges:
                attn = 0.45  # less aggressive fading for readability

            circle = plt.Circle((x, y), r, color=col, zorder=4,
                                alpha=attn, linewidth=1.5, edgecolor="white")
            ax.add_patch(circle)
            lbl = val_fmt(t, s, val)
            # use dark text for faded nodes so they remain readable
            tc = "white" if attn >= 0.8 else "#2C3E50"
            ax.text(x, y, lbl, ha="center", va="center", fontsize=8,
                    fontweight="bold", color=tc, zorder=5)

    if extra_fn:
        extra_fn(ax)

    return fig


# ── Plot 01: MC vs HMM ──────────────────────────────────────────────────────────
def plot_mc_vs_hmm():
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    for ax in axes:
        ax.set_xlim(0, 4.5)
        ax.set_ylim(-0.8, 2.6)
        ax.axis("off")

    # ── Left: Markov Chain ─────────────────────────────────────────────────────
    ax = axes[0]
    ax.set_title("Cadena de Markov\n(estados observables)", fontsize=12,
                 fontweight="bold", color=COLORS["blue"])

    mc_x = [0.8, 2.0, 3.2]
    # Use mathtext to avoid Unicode subscript rendering failures
    mc_labels = [r"$q_1$", r"$q_2$", r"$q_3$"]
    for x, lbl in zip(mc_x, mc_labels):
        circle = plt.Circle((x, 1.4), 0.30, color=COLORS["blue"], zorder=3)
        ax.add_patch(circle)
        ax.text(x, 1.4, lbl, ha="center", va="center", fontsize=14,
                fontweight="bold", color="white", zorder=4)

    # Transition arrows with A labels
    for i in range(2):
        ax.annotate("", xy=(mc_x[i + 1] - 0.32, 1.4),
                    xytext=(mc_x[i] + 0.32, 1.4),
                    arrowprops=dict(arrowstyle="->", color=COLORS["blue"],
                                   lw=2.0), zorder=2)
        mx = (mc_x[i] + mc_x[i + 1]) / 2
        # Show A matrix values above transition arrows
        ax.text(mx, 1.82, r"$A_{ij}$", ha="center", fontsize=9,
                color=COLORS["blue"], style="italic")

    # π annotation
    ax.text(0.3, 2.1, r"$\pi$:", fontsize=11, color=COLORS["blue"],
            fontweight="bold")
    ax.text(0.3, 1.82, "S=0.6\nR=0.4", fontsize=9, color=COLORS["blue"])

    # A matrix values
    ax.text(2.0, 0.85,
            r"$A$:  S$\!\to\!$S=0.7,  S$\!\to\!$R=0.3" + "\n" +
            r"     R$\!\to\!$S=0.4,  R$\!\to\!$R=0.6",
            ha="center", fontsize=9, color=COLORS["blue"])

    ax.text(2.0, 0.38, "Ves los estados directamente",
            ha="center", fontsize=9.5, color=COLORS["blue"], style="italic")
    ax.text(2.0, 0.05, r"Solo necesitas: $\pi$ y $A$",
            ha="center", fontsize=10, color=COLORS["dark"], fontweight="bold")

    # badge
    badge = mpatches.FancyBboxPatch((0.15, 2.25), 4.0, 0.28,
                                    boxstyle="round,pad=0.05",
                                    facecolor="#D6EAF8", edgecolor=COLORS["blue"],
                                    linewidth=1.5)
    ax.add_patch(badge)
    ax.text(2.15, 2.39, "1 capa", ha="center", va="center", fontsize=12,
            fontweight="bold", color=COLORS["blue"])

    # ── Right: HMM ──────────────────────────────────────────────────────────────
    ax = axes[1]
    ax.set_title("Modelo Oculto de Markov\n(2 capas)", fontsize=12,
                 fontweight="bold", color=COLORS["purple"])

    hmm_x = [0.8, 2.0, 3.2]
    h_labels = [r"$q_1$", r"$q_2$", r"$q_3$"]
    o_labels = [r"$o_1$", r"$o_2$", r"$o_3$"]

    # Hidden layer nodes
    for x, lbl in zip(hmm_x, h_labels):
        circle = plt.Circle((x, 1.7), 0.28, color=COLORS["purple"], zorder=3)
        ax.add_patch(circle)
        ax.text(x, 1.7, lbl, ha="center", va="center", fontsize=13,
                fontweight="bold", color="white", zorder=4)

    # Transition arrows (hidden layer)
    for i in range(2):
        ax.annotate("", xy=(hmm_x[i + 1] - 0.30, 1.7),
                    xytext=(hmm_x[i] + 0.30, 1.7),
                    arrowprops=dict(arrowstyle="->", color=COLORS["purple"],
                                   lw=2.0), zorder=2)
        mx = (hmm_x[i] + hmm_x[i + 1]) / 2
        ax.text(mx, 2.06, r"$A_{ij}$", ha="center", fontsize=9,
                color=COLORS["purple"], style="italic")

    # Observation layer nodes
    for x, lbl in zip(hmm_x, o_labels):
        circle = plt.Circle((x, 0.6), 0.28, color=COLORS["teal"], zorder=3)
        ax.add_patch(circle)
        ax.text(x, 0.6, lbl, ha="center", va="center", fontsize=13,
                fontweight="bold", color="white", zorder=4)

    # Emission arrows with B labels
    for x in hmm_x:
        ax.annotate("", xy=(x, 0.90), xytext=(x, 1.40),
                    arrowprops=dict(arrowstyle="->", color=COLORS["orange"],
                                   lw=1.8), zorder=2)
        ax.text(x + 0.17, 1.15, r"$B_{ik}$", ha="left", fontsize=8.5,
                color=COLORS["orange"], style="italic")

    # Layer side labels
    ax.text(4.1, 1.7, "OCULTOS\n(q)", ha="left", va="center", fontsize=9,
            color=COLORS["purple"], fontweight="bold")
    ax.text(4.1, 0.6, "OBSERVADOS\n(o)", ha="left", va="center", fontsize=9,
            color=COLORS["teal"], fontweight="bold")

    # A and B probability values
    ax.text(2.0, 0.15,
            r"$A$:  S$\!\to\!$S=0.7,  S$\!\to\!$R=0.3" + "\n" +
            r"     R$\!\to\!$S=0.4,  R$\!\to\!$R=0.6",
            ha="center", fontsize=9, color=COLORS["purple"])
    ax.text(2.0, -0.35,
            r"$B$:  S$\!\to\!$sin par.=0.9,  S$\!\to\!$con par.=0.1" + "\n" +
            r"     R$\!\to\!$sin par.=0.2,  R$\!\to\!$con par.=0.8",
            ha="center", fontsize=9, color=COLORS["orange"])

    ax.text(2.0, -0.70, r"Necesitas: $\pi$, $A$ y $B$",
            ha="center", fontsize=10, color=COLORS["dark"], fontweight="bold")

    # badge
    badge2 = mpatches.FancyBboxPatch((0.15, 2.25), 4.0, 0.28,
                                     boxstyle="round,pad=0.05",
                                     facecolor="#E8DAEF", edgecolor=COLORS["purple"],
                                     linewidth=1.5)
    ax.add_patch(badge2)
    ax.text(2.15, 2.39, "2 capas", ha="center", va="center", fontsize=12,
            fontweight="bold", color=COLORS["purple"])

    plt.tight_layout()
    _save(fig, "01_mc_vs_hmm.png")


# ── Plot 02: HMM structure with parameters ─────────────────────────────────────
def plot_estructura_hmm():
    fig, ax = plt.subplots(figsize=(14, 6.5))
    ax.set_xlim(-0.2, 8.0)
    ax.set_ylim(-1.5, 3.5)
    ax.axis("off")
    ax.set_title(
        r"El HMM de Lain: El Clima Oculto  ($\lambda = A, B, \pi$)",
        fontsize=13, fontweight="bold", pad=14
    )

    xs    = [1.5, 3.5, 5.5]
    y_hid = 2.0
    y_obs = 0.5
    r     = 0.34

    # Hidden node labels (mathtext, no Unicode subscripts)
    hid_lbl = [r"$q_1$", r"$q_2$", r"$q_3$"]
    # Observation node labels (plain, no emoji)
    obs_lbl = ["O=0\n(sin par.)", "O=1\n(con par.)", "O=1\n(con par.)"]

    # π annotation (arrow pointing to first hidden node)
    ax.annotate("", xy=(xs[0], y_hid + r + 0.05),
                xytext=(xs[0] - 0.9, y_hid + 0.9),
                arrowprops=dict(arrowstyle="->", color=COLORS["green"], lw=2.0))
    ax.text(xs[0] - 1.1, y_hid + 1.05, r"$\pi$", fontsize=16,
            color=COLORS["green"], fontweight="bold")
    ax.text(xs[0] - 1.45, y_hid + 0.72, "S: 0.6\nR: 0.4", fontsize=9.5,
            color=COLORS["green"], va="top")

    # Hidden nodes
    for x, lbl in zip(xs, hid_lbl):
        circle = plt.Circle((x, y_hid), r, color=COLORS["purple"], zorder=3,
                            linewidth=2, edgecolor="white")
        ax.add_patch(circle)
        ax.text(x, y_hid, lbl, ha="center", va="center", fontsize=14,
                fontweight="bold", color="white", zorder=4)

    # Transition arrows: show all 4 probabilities between each pair
    for i in range(2):
        x0, x1 = xs[i], xs[i + 1]
        ax.annotate("", xy=(x1 - r - 0.04, y_hid),
                    xytext=(x0 + r + 0.04, y_hid),
                    arrowprops=dict(arrowstyle="-|>", color=COLORS["purple"],
                                   lw=2.5, mutation_scale=16), zorder=2)
        mx = (x0 + x1) / 2
        ax.text(mx, y_hid + 0.55,
                "S" + r"$\to$" + "S=0.7   S" + r"$\to$" + "R=0.3\n" +
                "R" + r"$\to$" + "S=0.4   R" + r"$\to$" + "R=0.6",
                ha="center", va="bottom", fontsize=8.5, color=COLORS["purple"])

    # Observation nodes
    for x, lbl in zip(xs, obs_lbl):
        circle = plt.Circle((x, y_obs), r, color=COLORS["teal"], zorder=3)
        ax.add_patch(circle)
        ax.text(x, y_obs, lbl, ha="center", va="center", fontsize=8.5,
                fontweight="bold", color="white", zorder=4)

    # Emission arrows
    for x in xs:
        ax.annotate("", xy=(x, y_obs + r + 0.04),
                    xytext=(x, y_hid - r - 0.04),
                    arrowprops=dict(arrowstyle="-|>", color=COLORS["orange"],
                                   lw=2.0, mutation_scale=14), zorder=2)

    # B matrix annotation — drawn as a clean block on the right
    bx = 7.0
    by_top = y_hid + 0.2
    ax.text(bx, by_top, r"$B$ (emisión):", fontsize=11, fontweight="bold",
            color=COLORS["orange"], ha="left", va="top")
    ax.text(bx, by_top - 0.38,
            "         sin par.   con par.\n"
            "S:    [  0.9        0.1  ]\n"
            "R:    [  0.2        0.8  ]",
            fontsize=9.5, color=COLORS["orange"], ha="left", va="top",
            family="monospace")

    # Layer labels
    ax.text(-0.05, y_hid, "OCULTO\n(estado)", ha="center", va="center",
            fontsize=9.5, color=COLORS["purple"], fontweight="bold")
    ax.text(-0.05, y_obs, "VISIBLE\n(obs)", ha="center", va="center",
            fontsize=9.5, color=COLORS["teal"], fontweight="bold")

    # Sequence label
    ax.text(3.5, -0.85,
            "Secuencia observada por Lain:   O = (0, 1, 1)",
            ha="center", fontsize=11, fontweight="bold", color=COLORS["dark"])
    ax.text(3.5, -1.25,
            r"Pregunta: ¿Qué clima (Sol/Lluvia) hubo en cada día?",
            ha="center", fontsize=10, color=COLORS["gray"], style="italic")

    _save(fig, "02_estructura_hmm.png")


# ── Plot 03: Forward trellis ────────────────────────────────────────────────────
def plot_forward_trellis():
    alpha_norm = (ALPHA - ALPHA.min()) / (ALPHA.max() - ALPHA.min())

    def color_fn(t, s, val):
        intensity = 0.30 + 0.70 * alpha_norm[t, s]
        base  = np.array([0x2E, 0x86, 0xAB]) / 255
        white = np.array([1.0, 1.0, 1.0])
        c = white * (1 - intensity) + base * intensity
        return (c[0], c[1], c[2])

    def val_fmt(t, s, val):
        # Use mathtext for Greek letter + subscript; avoids Unicode box and (R)->® ligature
        state = r'\mathrm{S}' if s == 0 else r'\mathrm{R}'
        return f"$\\alpha_{{{t+1}}}({state})$\n{val:.5f}"

    def extra(ax):
        ax.text(2.0, 1.60,
                r"$P(O \mid \lambda) = \alpha_3(S) + \alpha_3(R)"
                f" = {ALPHA[2,0]:.5f} + {ALPHA[2,1]:.5f} = {P_OBS:.5f}$",
                ha="center", fontsize=9.5, color=COLORS["dark"],
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.35", facecolor="#D6EAF8",
                          edgecolor=COLORS["blue"], alpha=0.9))
        ax.text(3.55, 1.60, "direccion" + r" $\rightarrow$", fontsize=9,
                color=COLORS["blue"], ha="left", va="center")

    fig = _build_trellis(
        title=(r"Algoritmo Forward — $\alpha_t(i) = "
               r"P(O_1\ldots O_t,\; q_t{=}i \mid \lambda)$"),
        values=ALPHA, val_fmt=val_fmt,
        node_color_fn=color_fn,
        arrow_dir="right",
        extra_fn=extra,
    )
    _save(fig, "03_forward_trellis.png")


# ── Plot 04: Backward trellis ───────────────────────────────────────────────────
def plot_backward_trellis():
    beta_norm = (BETA - BETA.min()) / (BETA.max() - BETA.min() + 1e-12)

    def color_fn(t, s, val):
        intensity = 0.30 + 0.70 * beta_norm[t, s]
        base  = np.array([0xE9, 0x4F, 0x37]) / 255
        white = np.array([1.0, 1.0, 1.0])
        c = white * (1 - intensity) + base * intensity
        return (c[0], c[1], c[2])

    def val_fmt(t, s, val):
        state = r'\mathrm{S}' if s == 0 else r'\mathrm{R}'
        return f"$\\beta_{{{t+1}}}({state})$\n{val:.5f}"

    def extra(ax):
        # Initialization box — centered and clearly spaced from direction arrow
        ax.text(2.0, 1.62,
                r"Inicializacion: $\beta_3(S)=1$   $\beta_3(R)=1$",
                ha="center", fontsize=9.5, color=COLORS["red"],
                bbox=dict(boxstyle="round,pad=0.30", facecolor="#FDEDEC",
                          edgecolor=COLORS["red"], alpha=0.9))
        # Direction arrow — placed clearly to the LEFT, away from box
        ax.text(0.37, 1.62, r"$\leftarrow$ direccion", fontsize=9,
                color=COLORS["red"], ha="left", va="center")
        # Cross-check at the bottom
        cross = (PI[0] * B[0, OBS[0]] * BETA[0, 0] +
                 PI[1] * B[1, OBS[0]] * BETA[0, 1])
        ax.text(2.0, -0.62,
                r"Verificacion: $\sum_i \pi_i \cdot B_{i,O_1} \cdot \beta_1(i)"
                f" = {cross:.5f} = P(O \\mid \\lambda)$  [OK]",
                ha="center", fontsize=8.5, color=COLORS["green"],
                fontweight="bold")

    fig = _build_trellis(
        title=(r"Algoritmo Backward — $\beta_t(i) = "
               r"P(O_{t+1}\ldots O_T \mid q_t{=}i,\; \lambda)$"),
        values=BETA, val_fmt=val_fmt,
        node_color_fn=color_fn,
        arrow_dir="left",
        extra_fn=extra,
    )
    _save(fig, "04_backward_trellis.png")


# ── Plot 05: Forward vs Backward comparison ─────────────────────────────────────
def plot_forward_vs_backward():
    fig, ax = plt.subplots(figsize=(14, 6.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(-0.8, 5.2)
    ax.axis("off")
    ax.set_title("Forward vs. Backward — ¿Qué sabe cada algoritmo?",
                 fontsize=13, fontweight="bold", pad=14)

    # ── Forward row (top)
    ax.text(0.1, 4.9, r"FORWARD  $\alpha_t(i)$", fontsize=12,
            fontweight="bold", color=COLORS["blue"])
    ax.text(0.1, 4.50,
            r"Acumula pasado + estado actual  $\rightarrow$",
            fontsize=10, color=COLORS["blue"])

    fwd_boxes = [(1.8, 4.15), (4.8, 4.15), (7.8, 4.15)]
    fwd_info  = [r"$\alpha_1(i)$" + "\n" + r"$= P(O_1,\; q_1{=}i\mid\lambda)$",
                 r"$\alpha_2(i)$" + "\n" + r"$= P(O_1,O_2,\; q_2{=}i\mid\lambda)$",
                 r"$\alpha_3(i)$" + "\n" + r"$= P(O_1,O_2,O_3,\; q_3{=}i\mid\lambda)$"]
    for (x, y), info in zip(fwd_boxes, fwd_info):
        box = mpatches.FancyBboxPatch((x - 1.35, y - 0.65), 2.7, 1.30,
                                      boxstyle="round,pad=0.1",
                                      facecolor="#D6EAF8",
                                      edgecolor=COLORS["blue"], linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, info, ha="center", va="center", fontsize=9,
                color=COLORS["dark"])
    for i in range(2):
        ax.annotate("", xy=(fwd_boxes[i+1][0]-1.35, fwd_boxes[i+1][1]),
                    xytext=(fwd_boxes[i][0]+1.35, fwd_boxes[i][1]),
                    arrowprops=dict(arrowstyle="->", color=COLORS["blue"], lw=2.0))

    # ── Backward row (middle)
    ax.text(0.1, 2.95, r"BACKWARD  $\beta_t(i)$", fontsize=12,
            fontweight="bold", color=COLORS["red"])
    ax.text(0.1, 2.55,
            r"$\leftarrow$  Acumula futuro dado estado actual",
            fontsize=10, color=COLORS["red"])

    bwd_boxes = [(1.8, 2.20), (4.8, 2.20), (7.8, 2.20)]
    bwd_info  = [r"$\beta_1(i)$" + "\n" + r"$= P(O_2,O_3\mid q_1{=}i,\lambda)$",
                 r"$\beta_2(i)$" + "\n" + r"$= P(O_3\mid q_2{=}i,\lambda)$",
                 r"$\beta_3(i)=1$" + "\n" + "(init)"]
    for (x, y), info in zip(bwd_boxes, bwd_info):
        box = mpatches.FancyBboxPatch((x - 1.35, y - 0.65), 2.7, 1.30,
                                      boxstyle="round,pad=0.1",
                                      facecolor="#FDEDEC",
                                      edgecolor=COLORS["red"], linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, info, ha="center", va="center", fontsize=9,
                color=COLORS["dark"])
    for i in range(1, -1, -1):
        ax.annotate("", xy=(bwd_boxes[i][0]+1.35, bwd_boxes[i][1]),
                    xytext=(bwd_boxes[i+1][0]-1.35, bwd_boxes[i+1][1]),
                    arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=2.0))

    # ── Combined γ box (right)
    gamma_box = mpatches.FancyBboxPatch((9.6, 0.5), 4.0, 4.4,
                                        boxstyle="round,pad=0.15",
                                        facecolor="#E8F8F5",
                                        edgecolor=COLORS["green"], linewidth=2.5)
    ax.add_patch(gamma_box)
    ax.text(11.6, 4.65, "JUNTOS", ha="center", fontsize=12,
            fontweight="bold", color=COLORS["green"])
    ax.text(11.6, 4.20, r"$\gamma_t(i) = P(q_t{=}i \mid O, \lambda)$",
            ha="center", fontsize=10, color=COLORS["dark"], fontweight="bold")
    ax.text(11.6, 3.65, r"$\alpha_t(i) \cdot \beta_t(i)$",
            ha="center", fontsize=12, color=COLORS["dark"])
    ax.text(11.6, 3.35, "─" * 18, ha="center", fontsize=10,
            color=COLORS["dark"])
    ax.text(11.6, 3.05, r"$P(O \mid \lambda)$",
            ha="center", fontsize=12, color=COLORS["dark"])
    ax.text(11.6, 2.55, "= Posterior completo\nde cada estado",
            ha="center", fontsize=10, color=COLORS["green"], style="italic")
    ax.text(11.6, 1.90, "Ejemplo:", ha="center", fontsize=9,
            color=COLORS["gray"])
    ax.text(11.6, 1.55,
            r"$\gamma_1(S)=0.791$   $\gamma_1(R)=0.209$",
            ha="center", fontsize=9, color=COLORS["dark"])
    ax.text(11.6, 1.20,
            r"$\gamma_3(R)=0.904$  $\Rightarrow$  Lluvia con 90%",
            ha="center", fontsize=9, color=COLORS["dark"])

    # ── Comparison table (bottom-left)
    ax.text(0.1, 1.55, "¿Cuándo usar cada uno?", fontsize=11,
            fontweight="bold", color=COLORS["dark"])
    rows = [
        ("Forward solo",   r"$P(O\mid\lambda)$",     r"$\rightarrow$",
         "Evaluacion, reconocimiento"),
        ("Backward solo",  "complemento",             r"$\leftarrow$",
         "Rara vez solo"),
        (r"$\alpha \times \beta = \gamma$",
         r"$P(q_t{=}i\mid O,\lambda)$", r"$\leftrightarrow$",
         "Suavizado, Baum-Welch"),
    ]
    col_x = [0.2, 3.6, 5.7, 6.9]
    headers = ["Algoritmo", "Computa", "Dir.", "Uso principal"]
    for j, (hdr, cx) in enumerate(zip(headers, col_x)):
        ax.text(cx, 1.15, hdr, fontsize=9, fontweight="bold",
                color=COLORS["gray"])
    for i, row in enumerate(rows):
        y = 0.82 - i * 0.32
        for j, (val, cx) in enumerate(zip(row, col_x)):
            ax.text(cx, y, val, fontsize=8.5, color=COLORS["dark"])

    _save(fig, "05_forward_vs_backward.png")


# ── Plot 06: γ posterior bar chart ──────────────────────────────────────────────
def plot_gamma_posteriors():
    fig, ax = plt.subplots(figsize=(9, 5.5))

    bar_w = 0.55
    xs    = [1, 2, 3]

    for t, x in enumerate(xs):
        g_s = GAMMA[t, 0]
        g_r = GAMMA[t, 1]
        ax.bar(x, g_s, bar_w, color=COLORS["blue"], alpha=0.88,
               label="Sol (S)" if t == 0 else "")
        ax.bar(x, g_r, bar_w, bottom=g_s, color=COLORS["red"], alpha=0.88,
               label="Lluvia (R)" if t == 0 else "")

        if g_s > 0.05:
            ax.text(x, g_s / 2, f"{g_s*100:.1f}%", ha="center", va="center",
                    fontsize=11, fontweight="bold", color="white")
        if g_r > 0.05:
            ax.text(x, g_s + g_r / 2, f"{g_r*100:.1f}%", ha="center",
                    va="center", fontsize=11, fontweight="bold", color="white")

    ax.set_xticks(xs)
    # No emoji — use plain text for observation labels
    obs_tick = ["t=1\n(O=0, sin par.)", "t=2\n(O=1, con par.)",
                "t=3\n(O=1, con par.)"]
    ax.set_xticklabels(obs_tick, fontsize=10)
    ax.set_ylabel(r"$P(\mathrm{estado} \mid O, \lambda)$", fontsize=11)
    ax.set_ylim(0, 1.18)
    ax.set_title(r"Probabilidades Posteriores $\gamma_t(i) = P(q_t{=}i \mid O, \lambda)$",
                 fontsize=12, fontweight="bold")

    # Legend placed inside the first bar region (clear of top annotations)
    ax.legend(fontsize=11, loc="upper left", bbox_to_anchor=(0.01, 0.98),
              framealpha=0.9)

    ax.axhline(0.5, color=COLORS["gray"], lw=0.8, ls="--", alpha=0.5)
    ax.grid(axis="y", alpha=0.4)
    ax.set_axisbelow(True)

    # Top dominant-state annotations — positioned above bars with enough room
    dominant = ["79% Sol", "87% Lluvia", "90% Lluvia"]
    dom_cols  = [COLORS["blue"], COLORS["red"], COLORS["red"]]
    for i, (x, txt, col) in enumerate(zip(xs, dominant, dom_cols)):
        ax.text(x, 1.11, txt, ha="center", fontsize=9.5,
                color=col, fontweight="bold")

    plt.tight_layout()
    _save(fig, "06_gamma_posteriors.png")


# ── Plot 07: Viterbi trellis ─────────────────────────────────────────────────────
def plot_viterbi_trellis():
    path_edges = {(0, 0), (1, 1), (2, 1)}   # S, R, R

    psi_arrows = [
        (1, 0, 0),   # t=2, state S <- from S
        (1, 1, 0),   # t=2, state R <- from S
        (2, 0, 1),   # t=3, state S <- from R
        (2, 1, 1),   # t=3, state R <- from R
    ]

    delta_norm = (DELTA - DELTA.min()) / (DELTA.max() - DELTA.min() + 1e-12)

    def color_fn(t, s, val):
        intensity = 0.30 + 0.70 * delta_norm[t, s]
        base  = np.array([0x27, 0xAE, 0x60]) / 255
        white = np.array([1.0, 1.0, 1.0])
        c = white * (1 - intensity) + base * intensity
        return (c[0], c[1], c[2])

    def val_fmt(t, s, val):
        state = r'\mathrm{S}' if s == 0 else r'\mathrm{R}'
        return f"$\\delta_{{{t+1}}}({state})$\n{val:.5f}"

    def extra(ax):
        # Optimal path box — at top
        ax.text(2.0, 1.64,
                r"Camino optimo: S $\to$ R $\to$ R  (linea verde)",
                ha="center", fontsize=10, fontweight="bold",
                color=COLORS["green"],
                bbox=dict(boxstyle="round,pad=0.35", facecolor="#D5F5E3",
                          edgecolor=COLORS["green"], alpha=0.9))
        # "Mejor en t=3" annotation — right side, not overlapping
        ax.text(3.55, 0.0, "Mejor\nen t=3:\nLluvia",
                ha="left", va="center", fontsize=8.5, color=COLORS["dark"])
        # Legend — moved to figure bottom, away from time labels
        ax.text(2.0, -0.62,
                "Flechas naranjas = backpointers " + r"$\psi$",
                ha="center", fontsize=8.5, color=COLORS["gray"])
        ax.text(2.0, -0.72,
                "Nodos atenuados = no pertenecen al camino optimo",
                ha="center", fontsize=8.5, color=COLORS["gray"])

    fig = _build_trellis(
        title=(r"Algoritmo de Viterbi — $\delta_t(i)$"
               r" = probabilidad maxima de camino"),
        values=DELTA, val_fmt=val_fmt,
        node_color_fn=color_fn,
        arrow_dir="right",
        extra_fn=extra,
        psi_arrows=psi_arrows,
        path_edges=path_edges,
        figsize=(12, 5.8),
    )
    _save(fig, "07_viterbi_trellis.png")


# ── Plot 08: Baum-Welch convergence ─────────────────────────────────────────────
def plot_baum_welch_convergencia():
    rng      = np.random.default_rng(42)
    long_obs = _simulate(PI, A, B, length=60, rng=rng)

    pi0 = np.array([0.5, 0.5])
    a0  = np.array([[0.6, 0.4], [0.5, 0.5]])
    b0  = np.array([[0.7, 0.3], [0.3, 0.7]])

    pi_cur, a_cur, b_cur = pi0.copy(), a0.copy(), b0.copy()
    log_likes = []
    n_iter = 35

    for _ in range(n_iter):
        pi_cur, a_cur, b_cur, ll = _baum_welch_step(long_obs, pi_cur, a_cur, b_cur)
        log_likes.append(ll)

    fig, ax = plt.subplots(figsize=(10, 5))
    iters = list(range(1, n_iter + 1))
    ax.plot(iters, log_likes, color=COLORS["blue"], lw=2.5, marker="o",
            markersize=5, label=r"$\log P(O \mid \lambda)$")

    converged_ll = log_likes[-1]
    ax.axhline(converged_ll, color=COLORS["gray"], lw=1.2, ls="--",
               alpha=0.8, label=f"Convergencia ≈ {converged_ll:.2f}")

    ax.set_xlabel("Iteracion", fontsize=12)
    ax.set_ylabel(r"$\log P(O \mid \lambda)$", fontsize=12)
    ax.set_title(
        "Baum-Welch: Convergencia de la Log-Verosimilitud (T=60, N=2)",
        fontsize=13, fontweight="bold"
    )
    ax.legend(fontsize=11)
    ax.grid(alpha=0.4)

    ax.text(0.97, 0.05,
            "[OK] Monotonamente no decreciente\n     (garantia del algoritmo EM)",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=9.5, color=COLORS["green"],
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#D5F5E3",
                      edgecolor=COLORS["green"], alpha=0.85))

    plt.tight_layout()
    _save(fig, "08_baum_welch_convergencia.png")


# ── Plot 09: Parameters before / after ──────────────────────────────────────────
def plot_parametros_antes_despues():
    fig, axes = plt.subplots(2, 2, figsize=(12, 7.5))

    titles = [
        r"$A$ original ($\lambda_0$)",
        r"$A$ actualizada (1 iteracion)",
        r"$B$ original ($\lambda_0$)",
        r"$B$ actualizada (1 iteracion)",
    ]
    mats = [A, A_HAT, B, B_HAT]
    col_labels_a = [r"$\to$ S", r"$\to$ R"]
    col_labels_b = ["O=0", "O=1"]
    col_labels   = [col_labels_a, col_labels_a, col_labels_b, col_labels_b]
    colors_border = [COLORS["blue"], COLORS["blue"],
                     COLORS["orange"], COLORS["orange"]]

    ax_list = list(axes.flat)
    for idx, (ax, title, mat, cl, cb) in enumerate(
            zip(ax_list, titles, mats, col_labels, colors_border)):

        im = ax.imshow(mat, vmin=0, vmax=1,
                       cmap="Blues" if idx < 2 else "Oranges",
                       aspect="auto")
        ax.set_title(title, fontsize=11, fontweight="bold", color=cb)

        ax.set_xticks(range(mat.shape[1]))
        ax.set_xticklabels(cl, fontsize=10)
        ax.set_yticks(range(mat.shape[0]))
        ax.set_yticklabels(["S", "R"], fontsize=10)

        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                val = mat[i, j]
                tc = "white" if val > 0.55 else COLORS["dark"]
                ax.text(j, i, f"{val:.3f}", ha="center", va="center",
                        fontsize=12, fontweight="bold", color=tc)

        for spine in ax.spines.values():
            spine.set_edgecolor(cb)
            spine.set_linewidth(2.0)

    fig.suptitle("Parametros antes y despues de una iteracion de Baum-Welch",
                 fontsize=13, fontweight="bold", y=1.01)

    # Highlight key changes
    ax_list[1].add_patch(mpatches.FancyBboxPatch(
        (0.5, 0.5), 1.0, 1.0,
        boxstyle="round,pad=0.05",
        facecolor="none", edgecolor=COLORS["red"], linewidth=3,
        transform=ax_list[1].transData, clip_on=False
    ))
    ax_list[1].text(1.05, -0.65,
                    r"$\uparrow$ $A_{RR}$: 0.60" + r"$\to$" + "0.93\nLluvia mas persistente",
                    ha="center", fontsize=8.5, color=COLORS["red"],
                    fontweight="bold")

    ax_list[3].add_patch(mpatches.FancyBboxPatch(
        (0.5, 0.5), 1.0, 1.0,
        boxstyle="round,pad=0.05",
        facecolor="none", edgecolor=COLORS["red"], linewidth=3,
        transform=ax_list[3].transData, clip_on=False
    ))
    ax_list[3].text(1.05, -0.65,
                    r"$\uparrow$ $B_{R,1}$: 0.80" + r"$\to$" + "0.90\nLluvia mas distinguible",
                    ha="center", fontsize=8.5, color=COLORS["red"],
                    fontweight="bold")

    plt.tight_layout()
    _save(fig, "09_parametros_antes_despues.png")


# ── Main ────────────────────────────────────────────────────────────────────────
def main():
    print("Generando imagenes para clase/20_hmm/ ...")
    plot_mc_vs_hmm()
    plot_estructura_hmm()
    plot_forward_trellis()
    plot_backward_trellis()
    plot_forward_vs_backward()
    plot_gamma_posteriors()
    plot_viterbi_trellis()
    plot_baum_welch_convergencia()
    plot_parametros_antes_despues()
    print("Listo.")


if __name__ == "__main__":
    main()
