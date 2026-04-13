#!/usr/bin/env python3
"""
Laboratorio: Búsqueda Adversarial (imágenes para las notas)

Uso:
    cd clase/15_adversarial_search
    python3 lab_adversarial_search.py

Genera 13 imágenes en:
    clase/15_adversarial_search/images/

Dependencias: numpy, matplotlib
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
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
# Nim game helpers
# ---------------------------------------------------------------------------

def _nim_actions(state):
    """Returns list of (pile_idx, amount) for all valid moves."""
    actions = []
    for i, pile in enumerate(state):
        for amount in range(1, pile + 1):
            actions.append((i, amount))
    return actions


def _nim_result(state, action):
    """Apply action (pile_idx, amount) to state, return new state tuple."""
    pile_idx, amount = action
    new_state = list(state)
    new_state[pile_idx] -= amount
    return tuple(new_state)


def _nim_terminal(state):
    """True if all piles are 0."""
    return all(p == 0 for p in state)


def _nim_utility(state, is_max_turn):
    """Called only on terminal states. Current player can't move -> loses.
    Returns -1 if is_max_turn (MAX is stuck), +1 if MIN is stuck."""
    if is_max_turn:
        return -1
    else:
        return 1


def _nim_xor(state):
    """Returns XOR of all pile sizes (nim-sum)."""
    result = 0
    for p in state:
        result ^= p
    return result


def _minimax(state, is_max_turn):
    """Returns (value, best_action) for Nim game. action is (pile_idx, amount) or None."""
    if _nim_terminal(state):
        return _nim_utility(state, is_max_turn), None

    actions = _nim_actions(state)
    best_action = None

    if is_max_turn:
        best_val = -2
        for action in actions:
            next_state = _nim_result(state, action)
            val, _ = _minimax(next_state, False)
            if val > best_val:
                best_val = val
                best_action = action
        return best_val, best_action
    else:
        best_val = 2
        for action in actions:
            next_state = _nim_result(state, action)
            val, _ = _minimax(next_state, True)
            if val < best_val:
                best_val = val
                best_action = action
        return best_val, best_action


def _minimax_with_count(state, is_max_turn):
    """Returns (value, best_action, nodes_expanded) — counts nodes for comparison plots."""
    count = [0]

    def _mm(s, is_max):
        count[0] += 1
        if _nim_terminal(s):
            return _nim_utility(s, is_max), None
        actions = _nim_actions(s)
        best_action = None
        if is_max:
            best_val = -2
            for action in actions:
                ns = _nim_result(s, action)
                val, _ = _mm(ns, False)
                if val > best_val:
                    best_val = val
                    best_action = action
            return best_val, best_action
        else:
            best_val = 2
            for action in actions:
                ns = _nim_result(s, action)
                val, _ = _mm(ns, True)
                if val < best_val:
                    best_val = val
                    best_action = action
            return best_val, best_action

    val, action = _mm(state, is_max_turn)
    return val, action, count[0]


def _alphabeta(state, is_max_turn, alpha, beta):
    """Returns (value, best_action, nodes_expanded) for Nim. Tracks pruning."""
    count = [0]

    def _ab(s, is_max, a, b):
        count[0] += 1
        if _nim_terminal(s):
            return _nim_utility(s, is_max), None
        actions = _nim_actions(s)
        best_action = None
        if is_max:
            best_val = -2
            for action in actions:
                ns = _nim_result(s, action)
                val, _ = _ab(ns, False, a, b)
                if val > best_val:
                    best_val = val
                    best_action = action
                a = max(a, best_val)
                if a >= b:
                    break
            return best_val, best_action
        else:
            best_val = 2
            for action in actions:
                ns = _nim_result(s, action)
                val, _ = _ab(ns, True, a, b)
                if val < best_val:
                    best_val = val
                    best_action = action
                b = min(b, best_val)
                if a >= b:
                    break
            return best_val, best_action

    val, action = _ab(state, is_max_turn, alpha, beta)
    return val, action, count[0]


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def _draw_node(ax, x, y, label, color, text_color='white', size=0.25, shape='circle'):
    """Draw a node (circle or square) at (x,y) with label. shape='circle' or 'square'."""
    if shape == 'circle':
        patch = plt.Circle((x, y), size, color=color, zorder=4)
        ax.add_patch(patch)
    else:
        rect = mpatches.FancyBboxPatch(
            (x - size, y - size), 2 * size, 2 * size,
            boxstyle="square,pad=0", color=color, zorder=4
        )
        ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center',
            fontsize=8, fontweight='bold', color=text_color, zorder=5)


def _draw_edge(ax, x1, y1, x2, y2, label='', color='#2C3E50', linewidth=1.5, pruned=False):
    """Draw edge from (x1,y1) to (x2,y2) with optional label. pruned=True draws gray dashed."""
    if pruned:
        ax.plot([x1, x2], [y1, y2], color=COLORS["gray"], lw=1.2,
                linestyle='--', zorder=2, alpha=0.6)
    else:
        ax.plot([x1, x2], [y1, y2], color=color, lw=linewidth, zorder=2)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        ax.text(mx, my, label, ha='center', va='bottom',
                fontsize=7, color=color if not pruned else COLORS["gray"],
                bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.8),
                zorder=6)


def _draw_tictactoe_board(ax, board, title='', highlight_cells=None):
    """Draw 3x3 tic-tac-toe board. board is 9-element list: 'X', 'O', or ''.
    highlight_cells: list of cell indices to highlight."""
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_aspect('equal')
    ax.axis('off')

    # Grid lines
    for i in range(1, 3):
        ax.plot([i, i], [0, 3], color=COLORS["dark"], lw=2)
        ax.plot([0, 3], [i, i], color=COLORS["dark"], lw=2)

    # Highlight cells
    if highlight_cells:
        for idx in highlight_cells:
            row = 2 - (idx // 3)
            col = idx % 3
            rect = mpatches.Rectangle((col, row), 1, 1,
                                       color=COLORS["blue"], alpha=0.25, zorder=1)
            ax.add_patch(rect)

    # Draw pieces
    for idx, piece in enumerate(board):
        row = 2 - (idx // 3)
        col = idx % 3
        cx = col + 0.5
        cy = row + 0.5
        if piece == 'X':
            ax.text(cx, cy, 'X', ha='center', va='center',
                    fontsize=22, fontweight='bold', color=COLORS["blue"])
        elif piece == 'O':
            ax.text(cx, cy, 'O', ha='center', va='center',
                    fontsize=22, fontweight='bold', color=COLORS["red"])

    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', pad=6)


# ---------------------------------------------------------------------------
# Tic-tac-toe helpers (for endgame analysis)
# ---------------------------------------------------------------------------

def _ttt_check_winner(board):
    """Returns 'X', 'O', or None."""
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for line in lines:
        vals = [board[i] for i in line]
        if vals[0] == vals[1] == vals[2] and vals[0] != '':
            return vals[0]
    return None


def _ttt_terminal(board):
    """True if game over (winner or board full)."""
    if _ttt_check_winner(board) is not None:
        return True
    return all(cell != '' for cell in board)


def _ttt_utility(board):
    """Returns +1 (X wins), -1 (O wins), 0 (draw)."""
    winner = _ttt_check_winner(board)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    return 0


def _ttt_minimax(board, is_max_turn):
    """Returns (value, best_move_index) for tic-tac-toe."""
    if _ttt_terminal(board):
        return _ttt_utility(board), None

    empty = [i for i, c in enumerate(board) if c == '']
    best_action = None

    if is_max_turn:
        best_val = -2
        for idx in empty:
            new_board = board[:]
            new_board[idx] = 'X'
            val, _ = _ttt_minimax(new_board, False)
            if val > best_val:
                best_val = val
                best_action = idx
        return best_val, best_action
    else:
        best_val = 2
        for idx in empty:
            new_board = board[:]
            new_board[idx] = 'O'
            val, _ = _ttt_minimax(new_board, True)
            if val < best_val:
                best_val = val
                best_action = idx
        return best_val, best_action


# ---------------------------------------------------------------------------
# 1. Single-agent vs adversarial search
# ---------------------------------------------------------------------------

def plot_single_vs_adversarial() -> None:
    """Two-panel figure comparing single-agent pathfinding vs adversarial game tree."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Del camino a la estrategia",
                 fontsize=14, fontweight='bold', y=1.01)

    # --- Left panel: simple path chain S→A→B→C→Goal ---
    ax = axes[0]
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 2.0)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Búsqueda de camino: un agente", fontsize=12, fontweight='bold')

    chain_nodes = [('S', 0, 0.75), ('A', 1, 0.75), ('B', 2, 0.75),
                   ('C', 3, 0.75), ('Meta', 4, 0.75)]
    chain_colors = [COLORS["green"], COLORS["blue"], COLORS["blue"],
                    COLORS["blue"], COLORS["orange"]]

    for i in range(len(chain_nodes) - 1):
        _, x1, y1 = chain_nodes[i]
        _, x2, y2 = chain_nodes[i + 1]
        ax.annotate('', xy=(x2 - 0.26, y2), xytext=(x1 + 0.26, y1),
                    arrowprops=dict(arrowstyle='->', color=COLORS["dark"], lw=2))

    for (label, x, y), color in zip(chain_nodes, chain_colors):
        if label == 'Meta':
            diamond = mpatches.RegularPolygon((x, y), 4, radius=0.28,
                                               orientation=np.pi / 4,
                                               color=color, zorder=4)
            ax.add_patch(diamond)
            ax.text(x, y, label, ha='center', va='center',
                    fontsize=8, fontweight='bold', color='white', zorder=5)
        else:
            circle = plt.Circle((x, y), 0.26, color=color, zorder=4)
            ax.add_patch(circle)
            ax.text(x, y, label, ha='center', va='center',
                    fontsize=9, fontweight='bold', color='white', zorder=5)

    ax.text(0, 0.3, 'Inicio', ha='center', fontsize=9, color=COLORS["green"])
    ax.text(4, 0.3, 'Objetivo', ha='center', fontsize=9, color=COLORS["orange"])
    ax.text(2.0, 1.3,
            "Un agente\nMinimizar costo de camino",
            ha='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.4', fc=COLORS["light"], ec=COLORS["blue"], lw=1.5))

    # --- Right panel: game tree showing MAX/MIN levels ---
    ax = axes[1]
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.3, 3.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Árbol de juego: dos agentes", fontsize=12, fontweight='bold')

    # Level 0: root (MAX)
    _draw_edge(ax, 2.0, 2.8, 1.0, 1.8, color=COLORS["dark"])
    _draw_edge(ax, 2.0, 2.8, 3.0, 1.8, color=COLORS["dark"])
    _draw_node(ax, 2.0, 3.0, 's₀\nMAX', COLORS["blue"], size=0.3)

    # Level 1: two MIN nodes
    _draw_edge(ax, 1.0, 1.8, 0.4, 0.8, color=COLORS["dark"])
    _draw_edge(ax, 1.0, 1.8, 1.6, 0.8, color=COLORS["dark"])
    _draw_edge(ax, 3.0, 1.8, 2.4, 0.8, color=COLORS["dark"])
    _draw_edge(ax, 3.0, 1.8, 3.6, 0.8, color=COLORS["dark"])
    _draw_node(ax, 1.0, 1.9, 'MIN', COLORS["red"], size=0.28)
    _draw_node(ax, 3.0, 1.9, 'MIN', COLORS["red"], size=0.28)

    # Level 2: four terminal leaves
    terminal_data = [
        (0.4, 0.65, '+1'), (1.6, 0.65, '-1'),
        (2.4, 0.65, '-1'), (3.6, 0.65, '+1'),
    ]
    leaf_colors = [COLORS["green"], COLORS["red"], COLORS["red"], COLORS["green"]]
    for (x, y, val), col in zip(terminal_data, leaf_colors):
        rect = mpatches.FancyBboxPatch(
            (x - 0.22, y - 0.18), 0.44, 0.36,
            boxstyle="square,pad=0", color=col, zorder=4
        )
        ax.add_patch(rect)
        ax.text(x, y, val, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white', zorder=5)

    # Level labels on the right
    ax.text(4.3, 3.0, 'MAX', fontsize=10, color=COLORS["blue"],
            fontweight='bold', va='center')
    ax.text(4.3, 1.9, 'MIN', fontsize=10, color=COLORS["red"],
            fontweight='bold', va='center')
    ax.text(4.3, 0.65, 'Terminal', fontsize=9, color=COLORS["dark"], va='center')

    ax.text(2.0, -0.15,
            "Dos agentes\nMAX maximiza, MIN minimiza",
            ha='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.4', fc=COLORS["light"], ec=COLORS["red"], lw=1.5))

    fig.tight_layout()
    _save(fig, "01_single_vs_adversarial.png")


# ---------------------------------------------------------------------------
# 2. Tic-tac-toe anatomy
# ---------------------------------------------------------------------------

def plot_tictactoe_anatomy() -> None:
    """Single wide figure showing tic-tac-toe board + 7 formal components."""
    fig = plt.figure(figsize=(14, 6))
    fig.suptitle("Anatomía formal: tic-tac-toe",
                 fontsize=14, fontweight='bold', y=1.01)

    # Left: board (40% width)
    ax_board = fig.add_axes([0.03, 0.05, 0.35, 0.85])
    board = ['X', '', 'O', '', 'X', '', '', '', '']
    _draw_tictactoe_board(ax_board, board, title="Posición de ejemplo\n(turno de X)")

    # Empty cells highlighted
    empty_indices = [i for i, c in enumerate(board) if c == '']
    ax_board2 = fig.add_axes([0.03, 0.05, 0.35, 0.85])
    ax_board2.set_xlim(0, 3)
    ax_board2.set_ylim(0, 3)
    ax_board2.set_aspect('equal')
    ax_board2.axis('off')
    ax_board2.patch.set_visible(False)
    for idx in empty_indices:
        row = 2 - (idx // 3)
        col = idx % 3
        rect = mpatches.Rectangle((col + 0.05, row + 0.05), 0.9, 0.9,
                                   color=COLORS["blue"], alpha=0.2, zorder=1)
        ax_board2.add_patch(rect)

    # Right: formal components table (60% width)
    ax_text = fig.add_axes([0.42, 0.02, 0.56, 0.96])
    ax_text.axis('off')

    components = [
        ("Estado (s):", "Tablero 3×3 — 9 celdas ∈ {X, O, vacío}"),
        ("s₀:", "Tablero completamente vacío"),
        ("Jugadores(s):", "Turno de X (MAX) o turno de O (MIN)"),
        ("Acciones(s):", "Celdas vacías disponibles (azules en el tablero)"),
        ("Resultado(s, a):", "Nuevo tablero tras colocar X u O en celda a"),
        ("Terminal(s):", "¿Hay 3 en raya? ¿O está el tablero lleno?"),
        ("Utilidad(s):", "+1 si X gana  |  −1 si O gana  |  0 si empate"),
    ]

    bar_colors = [COLORS["blue"], COLORS["teal"], COLORS["purple"],
                  COLORS["blue"], COLORS["teal"], COLORS["orange"], COLORS["green"]]

    y_start = 0.93
    row_height = 0.115

    for i, ((key, val), bar_col) in enumerate(zip(components, bar_colors)):
        y = y_start - i * row_height
        # Colored left bar
        rect = mpatches.FancyBboxPatch(
            (0.0, y - 0.045), 0.018, 0.085,
            boxstyle="square,pad=0", color=bar_col, zorder=3
        )
        ax_text.add_patch(rect)

        # Background row
        bg = mpatches.FancyBboxPatch(
            (0.02, y - 0.048), 0.97, 0.092,
            boxstyle="round,pad=0.005",
            color='#F8F9FA' if i % 2 == 0 else 'white',
            zorder=2
        )
        ax_text.add_patch(bg)

        ax_text.text(0.04, y + 0.005, key, va='center',
                     fontsize=11, fontweight='bold', color=bar_col, zorder=4)
        ax_text.text(0.35, y + 0.005, val, va='center',
                     fontsize=10, color=COLORS["dark"], zorder=4)

    ax_text.set_xlim(0, 1)
    ax_text.set_ylim(0, 1)
    ax_text.set_title("Componentes del juego (definición formal)",
                       fontsize=12, fontweight='bold', pad=10)

    _save(fig, "02_tictactoe_anatomy.png")


# ---------------------------------------------------------------------------
# 3. Nim rules and tree
# ---------------------------------------------------------------------------

def plot_nim_rules_and_tree() -> None:
    """Two panels: Nim rules illustrated + small game tree for Nim(1,2)."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle("Nim: reglas y árbol de juego",
                 fontsize=13, fontweight='bold', y=1.01)

    # --- Left panel: pile diagram ---
    ax = axes[0]
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-1.0, 3.5)
    ax.axis('off')
    ax.set_title("Nim(1,2): quitar ≥1 de exactamente una pila",
                 fontsize=11, fontweight='bold')

    def draw_pile(ax, cx, pile_size, label, color):
        """Draw a vertical stack of circles at cx."""
        for k in range(pile_size):
            circle = plt.Circle((cx, k * 0.55 + 0.3), 0.22, color=color,
                                 ec='white', lw=1.5, zorder=3)
            ax.add_patch(circle)
        ax.text(cx, -0.25, label, ha='center', fontsize=12,
                fontweight='bold', color=COLORS["dark"])
        ax.text(cx, pile_size * 0.55 + 0.6, str(pile_size),
                ha='center', fontsize=11, color=COLORS["gray"])

    draw_pile(ax, 1.0, 1, 'Pila A', COLORS["blue"])
    draw_pile(ax, 2.5, 2, 'Pila B', COLORS["teal"])

    # Valid move: take 1 from B → (1,1)
    ax.annotate('', xy=(3.8, 0.95), xytext=(2.73, 0.95),
                arrowprops=dict(arrowstyle='->', color=COLORS["green"], lw=2.2))
    ax.text(4.1, 0.95, "(1,1)", ha='left', va='center',
            fontsize=10, color=COLORS["green"], fontweight='bold')
    ax.text(3.3, 1.25, "quitar 1\nde B ✓", ha='center', fontsize=9,
            color=COLORS["green"],
            bbox=dict(boxstyle='round,pad=0.2', fc='#EAFAF1', ec=COLORS["green"]))

    # Invalid move: can't take from 2 piles
    ax.text(2.0, 2.85, "NO: no se puede\nquitar de 2 pilas ✗",
            ha='center', fontsize=9, color=COLORS["red"],
            bbox=dict(boxstyle='round,pad=0.3', fc='#FDEDEC', ec=COLORS["red"]))
    ax.plot([1.0, 2.5], [2.55, 2.55], color=COLORS["red"], lw=2, linestyle='--')
    ax.plot([1.0, 2.5], [2.55, 2.55], 'x', color=COLORS["red"],
            markersize=12, markeredgewidth=2)

    # --- Right panel: Nim(1,2) complete tree (top levels) ---
    ax = axes[1]
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.3, 3.5)
    ax.axis('off')
    ax.set_title("Árbol parcial de Nim(1,2)\n(raíz + hijos, con valores minimax)",
                 fontsize=11, fontweight='bold')

    # Root
    root_x, root_y = 2.0, 3.0
    # Children positions: A-1→(0,2), B-1→(1,1), B-2→(1,0)
    children = [
        (0.6, 1.8, '(0,2)', 'A-1', -1),
        (2.0, 1.8, '(1,1)', 'B-1', 1),
        (3.4, 1.8, '(1,0)', 'B-2', -1),
    ]

    for cx, cy, state_label, edge_label, val in children:
        edge_color = COLORS["green"] if val == 1 else COLORS["dark"]
        lw = 2.5 if val == 1 else 1.5
        ax.plot([root_x, cx], [root_y - 0.3, cy + 0.3],
                color=edge_color, lw=lw, zorder=2)
        mx = (root_x + cx) / 2
        my = (root_y - 0.3 + cy + 0.3) / 2
        ax.text(mx - 0.2, my, edge_label, fontsize=8, color=edge_color,
                bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.8))
        val_str = "+1" if val == 1 else "-1"
        node_label = state_label + "\n" + val_str
        node_color = COLORS["red"]  # MIN nodes
        _draw_node(ax, cx, cy, node_label, node_color, size=0.32)
        if val == 1:
            # Green star marker for optimal
            ax.plot(cx + 0.38, cy + 0.3, '*', color=COLORS["green"],
                    markersize=12, zorder=6)

    _draw_node(ax, root_x, root_y, "(1,2)\n+1", COLORS["blue"], size=0.32)

    # Optimal annotation
    ax.annotate("Óptimo:\nB-1 → (1,1)",
                xy=(2.35, 1.8), fontsize=9, color=COLORS["green"],
                bbox=dict(boxstyle='round,pad=0.3', fc='#EAFAF1', ec=COLORS["green"]))

    # Legend
    legend_elems = [
        mpatches.Patch(color=COLORS["blue"], label='MAX'),
        mpatches.Patch(color=COLORS["red"], label='MIN'),
        mpatches.Patch(color=COLORS["green"], label='Movimiento óptimo'),
    ]
    ax.legend(handles=legend_elems, loc='lower left', fontsize=9)

    fig.tight_layout()
    _save(fig, "03_nim_rules_and_tree.png")


# ---------------------------------------------------------------------------
# 4. Game taxonomy
# ---------------------------------------------------------------------------

def plot_game_taxonomy() -> None:
    """2x2 quadrant grid: Información × Suma cero."""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.axis('off')
    fig.suptitle("Taxonomía de juegos de dos jugadores",
                 fontsize=14, fontweight='bold', y=1.01)

    quadrant_data = [
        # (x0, y0, width, height, color, title, games_text, x_text_off)
        (0, 1, 1, 1, '#D6EAF8', "Perfecta + Suma cero",
         "Ajedrez\nGo\nTic-tac-toe\nNim\nDamas\n(+ Backgammon*)", 0.08),
        (1, 1, 1, 1, '#EBF5FB', "Imperfecta + Suma cero",
         "— (muy raro)\n(suele usarse info\noculta para simetría)", 0.08),
        (0, 0, 1, 1, '#FEF9E7', "Perfecta + No suma cero",
         "— (poco común)\nNegociación con\ninformación completa", 0.08),
        (1, 0, 1, 1, '#FDEBD0', "Imperfecta + No suma cero",
         "Póker\nBridge\nDilema del Prisionero\nNegociación", 0.08),
    ]

    quad_colors_border = [COLORS["blue"], '#85C1E9', '#F9E79F', COLORS["orange"]]

    for (x0, y0, w, h, bg_color, title_text, games_text, _), border_col in zip(
            quadrant_data, quad_colors_border):
        rect = mpatches.FancyBboxPatch(
            (x0 + 0.02, y0 + 0.02), w - 0.04, h - 0.04,
            boxstyle="round,pad=0.02", color=bg_color,
            ec=border_col, lw=2.5, zorder=2
        )
        ax.add_patch(rect)
        cx = x0 + w / 2
        cy = y0 + h / 2
        ax.text(cx, y0 + h - 0.12, title_text,
                ha='center', va='top', fontsize=10,
                fontweight='bold', color=COLORS["dark"], zorder=3)
        ax.text(cx, cy - 0.05, games_text,
                ha='center', va='center', fontsize=9,
                color=COLORS["dark"], zorder=3, linespacing=1.5)

    # Mark "this module" games
    ax.text(0.12, 1.88, "★ Este módulo", fontsize=8,
            color=COLORS["blue"], fontweight='bold', zorder=4)

    # Stochastic annotation
    ax.text(0.5, 1.08, "* Backgammon: estocástico (dado)",
            ha='center', fontsize=8, color=COLORS["purple"],
            style='italic', zorder=4)

    # Axis labels
    ax.text(1.0, 2.05, "INFORMACIÓN", ha='center', fontsize=12,
            fontweight='bold', color=COLORS["dark"])
    ax.text(0.5, 2.02, "Perfecta", ha='center', fontsize=10, color=COLORS["blue"])
    ax.text(1.5, 2.02, "Imperfecta", ha='center', fontsize=10, color=COLORS["gray"])

    ax.text(-0.1, 1.0, "SUMA CERO", rotation=90, ha='center', va='center',
            fontsize=12, fontweight='bold', color=COLORS["dark"])
    ax.text(-0.07, 1.5, "Sí", rotation=90, ha='center', fontsize=10,
            color=COLORS["blue"])
    ax.text(-0.07, 0.5, "No", rotation=90, ha='center', fontsize=10,
            color=COLORS["orange"])

    # Dividing lines
    ax.plot([1, 1], [0, 2], color=COLORS["gray"], lw=1.5, zorder=3)
    ax.plot([0, 2], [1, 1], color=COLORS["gray"], lw=1.5, zorder=3)

    fig.tight_layout()
    _save(fig, "04_game_taxonomy.png")


# ---------------------------------------------------------------------------
# 5. Payoff matrices
# ---------------------------------------------------------------------------

def plot_payoff_matrices() -> None:
    """Two panels: zero-sum (tic-tac-toe summary) and non-zero-sum (prisoner's dilemma)."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Suma cero vs. no suma cero",
                 fontsize=13, fontweight='bold', y=1.01)

    # --- Left: Tic-tac-toe zero-sum summary table ---
    ax = axes[0]
    ax.axis('off')
    ax.set_title("Tic-tac-toe (suma cero)\nU_X + U_O = 0 siempre",
                 fontsize=11, fontweight='bold')

    outcomes = [
        ("X gana", "+1", "-1", COLORS["blue"]),
        ("O gana", "-1", "+1", COLORS["red"]),
        ("Empate", "0", "0", COLORS["gray"]),
    ]

    col_headers = ["Resultado", "U_X", "U_O", "Suma"]
    col_x = [0.05, 0.42, 0.62, 0.80]
    col_widths = [0.35, 0.18, 0.18, 0.18]

    # Header
    for hdr, cx in zip(col_headers, col_x):
        rect = mpatches.FancyBboxPatch(
            (cx, 0.82), col_widths[col_headers.index(hdr)], 0.1,
            boxstyle="square,pad=0", color=COLORS["dark"], zorder=2
        )
        ax.add_patch(rect)
        ax.text(cx + col_widths[col_headers.index(hdr)] / 2, 0.87,
                hdr, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white', zorder=3)

    for i, (label, ux, uo, color) in enumerate(outcomes):
        y = 0.82 - (i + 1) * 0.14
        bg = '#F8F9FA' if i % 2 == 0 else 'white'
        rect = mpatches.FancyBboxPatch(
            (0.03, y), 0.94, 0.12,
            boxstyle="square,pad=0", color=bg, ec=COLORS["light"], zorder=1
        )
        ax.add_patch(rect)

        left_bar = mpatches.FancyBboxPatch(
            (0.03, y), 0.012, 0.12,
            boxstyle="square,pad=0", color=color, zorder=2
        )
        ax.add_patch(left_bar)

        sum_val = int(ux) + int(uo)
        texts = [label, ux, uo, str(sum_val)]
        for txt, cx, cw in zip(texts, col_x, col_widths):
            tc = COLORS["blue"] if txt == "+1" else (COLORS["red"] if txt == "-1" else COLORS["dark"])
            ax.text(cx + cw / 2, y + 0.06, txt, ha='center', va='center',
                    fontsize=11, color=tc, fontweight='bold', zorder=3)

    # Annotation
    ax.text(0.5, 0.25,
            "La suma siempre = 0\nLo que gana X, lo pierde O\n→ Intereses completamente opuestos",
            ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', fc='#EBF5FB',
                      ec=COLORS["blue"], lw=1.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # --- Right: Prisoner's dilemma ---
    ax = axes[1]
    ax.axis('off')
    ax.set_title("Dilema del Prisionero (no suma cero)\nIntereses parcialmente alineados",
                 fontsize=11, fontweight='bold')

    # 2x2 matrix
    strategies = ["Callar", "Confesar"]
    payoffs = [[(-1, -1), (-10, 0)],
               [(0, -10), (-5, -5)]]
    cell_colors = [['#D5F5E3', '#FADBD8'],
                   ['#FADBD8', '#FEF9E7']]

    matrix_x0, matrix_y0 = 0.15, 0.35
    cell_w, cell_h = 0.32, 0.22

    # Column headers (Prisionero B)
    ax.text(matrix_x0 + cell_w, matrix_y0 + 2 * cell_h + 0.08,
            "Prisionero B", ha='center', fontsize=10, fontweight='bold',
            color=COLORS["red"])
    for j, strat in enumerate(strategies):
        ax.text(matrix_x0 + (j + 0.5) * cell_w,
                matrix_y0 + 2 * cell_h + 0.02,
                strat, ha='center', fontsize=9, color=COLORS["red"])

    # Row headers (Prisionero A)
    ax.text(matrix_x0 - 0.12, matrix_y0 + cell_h, "Prisionero A",
            ha='center', va='center', fontsize=10, fontweight='bold',
            color=COLORS["blue"], rotation=90)
    for i, strat in enumerate(strategies):
        ax.text(matrix_x0 - 0.02, matrix_y0 + (1 - i + 0.5) * cell_h,
                strat, ha='right', va='center', fontsize=9, color=COLORS["blue"])

    for i in range(2):
        for j in range(2):
            x = matrix_x0 + j * cell_w
            y = matrix_y0 + (1 - i) * cell_h
            bg = cell_colors[i][j]
            ec_col = COLORS["orange"]
            lw_val = 2.5 if (i == 1 and j == 1) else 1.0
            rect = mpatches.FancyBboxPatch(
                (x + 0.005, y + 0.005), cell_w - 0.01, cell_h - 0.01,
                boxstyle="round,pad=0.005", color=bg,
                ec=ec_col if (i == 1 and j == 1) else COLORS["gray"],
                lw=lw_val, zorder=2
            )
            ax.add_patch(rect)
            ua, ub = payoffs[i][j]
            payoff_str = "(" + str(ua) + ", " + str(ub) + ")"
            color_a = COLORS["blue"] if ua > -5 else COLORS["red"]
            ax.text(x + cell_w / 2, y + cell_h / 2, payoff_str,
                    ha='center', va='center', fontsize=10,
                    fontweight='bold', color=COLORS["dark"], zorder=3)

    # Annotations
    ax.text(matrix_x0 + 0.5 * cell_w, matrix_y0 - 0.08,
            "(-1,-1): Pareto-mejor\n(cooperación mutua)",
            ha='center', fontsize=8, color=COLORS["green"],
            bbox=dict(boxstyle='round,pad=0.2', fc='#EAFAF1', ec=COLORS["green"]))
    ax.text(matrix_x0 + 1.5 * cell_w, matrix_y0 - 0.08,
            "(-5,-5): Nash eq.\n(equilibrio Confesar)",
            ha='center', fontsize=8, color=COLORS["orange"],
            bbox=dict(boxstyle='round,pad=0.2', fc='#FEF9E7', ec=COLORS["orange"]))

    ax.text(0.5, 0.12,
            "Suma NO es constante — intereses parcialmente compartidos",
            ha='center', fontsize=9, color=COLORS["purple"],
            bbox=dict(boxstyle='round,pad=0.3', fc=COLORS["light"], ec=COLORS["purple"]))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    fig.tight_layout()
    _save(fig, "05_payoff_matrices.png")


# ---------------------------------------------------------------------------
# 6. Complete Nim(1,2) game tree — centerpiece
# ---------------------------------------------------------------------------

def plot_nim_complete_tree() -> None:
    """Complete Nim(1,2) game tree with minimax values."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(-0.5, 13.5)
    ax.set_ylim(-0.5, 5.0)
    ax.axis('off')
    ax.set_title("Árbol completo de Nim(1,2) — valores minimax",
                 fontsize=13, fontweight='bold', pad=8)
    ax.text(7.0, 4.7,
            "MAX mueve primero: acción óptima B-1 → (1,1), garantiza valor +1",
            ha='center', fontsize=10, color=COLORS["dark"], style='italic')

    # Node layout: (id, x, y, label, is_max, is_terminal, value, is_optimal)
    # Level 0: root (1,2)
    # Level 1: (0,2), (1,1), (1,0)
    # Level 2: (0,1), (0,0), (0,1), (1,0), (0,0)
    # Level 3: (0,0), (0,0), (0,0)

    # Verified tree:
    # (1,2) MAX=+1
    #   A-1 -> (0,2) MIN=-1
    #     B-1 -> (0,1) MAX=+1
    #       B-1 -> (0,0) [terminal, MIN to move -> +1]
    #     B-2 -> (0,0) [terminal, MAX to move -> -1]
    #   B-1 -> (1,1) MIN=+1  [OPTIMAL]
    #     A-1 -> (0,1) MAX=+1
    #       B-1 -> (0,0) [terminal, MIN to move -> +1]
    #     B-1 -> (1,0) MAX=+1
    #       A-1 -> (0,0) [terminal, MIN to move -> +1]
    #   B-2 -> (1,0) MIN=-1
    #     A-1 -> (0,0) [terminal, MAX to move -> -1]

    nodes = {
        # id: (x, y, label_line1, label_line2, is_max, is_terminal, value)
        'root':    (7.0,  4.2, '(1,2)', '+1', True,  False, 1),
        'n02':     (2.5,  3.0, '(0,2)', '-1', False, False, -1),
        'n11':     (7.0,  3.0, '(1,1)', '+1', False, False, 1),
        'n10a':    (11.5, 3.0, '(1,0)', '-1', False, False, -1),
        'n01a':    (1.0,  1.8, '(0,1)', '+1', True,  False, 1),
        'n00a':    (4.0,  1.8, '(0,0)', '-1', True,  True,  -1),
        'n01b':    (5.5,  1.8, '(0,1)', '+1', True,  False, 1),
        'n10b':    (8.5,  1.8, '(1,0)', '+1', True,  False, 1),
        'n00b':    (11.5, 1.8, '(0,0)', '-1', True,  True,  -1),
        'n00c':    (1.0,  0.6, '(0,0)', '+1', False, True,  1),
        'n00d':    (5.5,  0.6, '(0,0)', '+1', False, True,  1),
        'n00e':    (8.5,  0.6, '(0,0)', '+1', False, True,  1),
    }

    # Edges: (parent_id, child_id, action_label, is_optimal_path)
    edges = [
        ('root',  'n02',   'A-1', False),
        ('root',  'n11',   'B-1', True),
        ('root',  'n10a',  'B-2', False),
        ('n02',   'n01a',  'B-1', False),
        ('n02',   'n00a',  'B-2', False),
        ('n11',   'n01b',  'A-1', True),
        ('n11',   'n10b',  'B-1', True),
        ('n10a',  'n00b',  'A-1', False),
        ('n01a',  'n00c',  'B-1', False),
        ('n01b',  'n00d',  'B-1', True),
        ('n10b',  'n00e',  'A-1', True),
    ]

    # Draw edges first
    for parent_id, child_id, action, is_opt in edges:
        px, py = nodes[parent_id][0], nodes[parent_id][1]
        cx, cy = nodes[child_id][0], nodes[child_id][1]
        edge_color = COLORS["green"] if is_opt else COLORS["dark"]
        lw = 2.8 if is_opt else 1.5
        # Offset endpoints by node radius
        dy = py - cy
        dx = cx - px
        length = (dx ** 2 + dy ** 2) ** 0.5
        r = 0.28
        ox = r * dx / length if length > 0 else 0
        oy = r * dy / length if length > 0 else 0
        ax.plot([px + ox, cx - ox], [py - oy, cy + oy],
                color=edge_color, lw=lw, zorder=2, alpha=0.85)
        # Label at midpoint
        mx = (px + cx) / 2
        my = (py + cy) / 2
        ax.text(mx, my, action, ha='center', va='bottom',
                fontsize=7.5, color=edge_color, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.9),
                zorder=6)

    # Draw nodes
    for node_id, (x, y, lbl1, lbl2, is_max, is_terminal, value) in nodes.items():
        if is_terminal:
            # Terminal: square, green if +1 (MIN loses), gray if -1 (MAX loses)
            sq_color = COLORS["green"] if value == 1 else COLORS["gray"]
            rect = mpatches.FancyBboxPatch(
                (x - 0.28, y - 0.22), 0.56, 0.44,
                boxstyle="square,pad=0", color=sq_color,
                ec='white', lw=1.5, zorder=4
            )
            ax.add_patch(rect)
            ax.text(x, y + 0.06, lbl1, ha='center', va='center',
                    fontsize=7.5, fontweight='bold', color='white', zorder=5)
            ax.text(x, y - 0.1, lbl2, ha='center', va='center',
                    fontsize=7.5, fontweight='bold', color='white', zorder=5)
        else:
            node_color = COLORS["blue"] if is_max else COLORS["red"]
            circle = plt.Circle((x, y), 0.30, color=node_color,
                                 ec='white', lw=1.5, zorder=4)
            ax.add_patch(circle)
            ax.text(x, y + 0.07, lbl1, ha='center', va='center',
                    fontsize=8, fontweight='bold', color='white', zorder=5)
            ax.text(x, y - 0.1, lbl2, ha='center', va='center',
                    fontsize=8, fontweight='bold', color='white', zorder=5)

    # Level labels on the left
    for y_pos, label in [(4.2, 'MAX'), (3.0, 'MIN'), (1.8, 'MAX'), (0.6, 'MIN/term')]:
        ax.text(-0.3, y_pos, label, ha='right', va='center',
                fontsize=9, fontweight='bold',
                color=COLORS["blue"] if 'MAX' in label else COLORS["red"])

    # Legend
    legend_elems = [
        mpatches.Patch(color=COLORS["blue"], label='MAX (nodo redondo)'),
        mpatches.Patch(color=COLORS["red"], label='MIN (nodo redondo)'),
        mpatches.Patch(color=COLORS["green"], label='Terminal +1 (MIN pierde)'),
        mpatches.Patch(color=COLORS["gray"], label='Terminal -1 (MAX pierde)'),
        plt.Line2D([0], [0], color=COLORS["green"], lw=2.5, label='Camino óptimo'),
    ]
    ax.legend(handles=legend_elems, loc='lower right', fontsize=9,
              framealpha=0.9, edgecolor=COLORS["gray"])

    fig.tight_layout()
    _save(fig, "06_nim_complete_tree.png")


# ---------------------------------------------------------------------------
# 7. Minimax step-by-step trace table
# ---------------------------------------------------------------------------

def plot_minimax_step_by_step() -> None:
    """Styled trace table for Minimax on Nim(1,2)."""
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.axis('off')
    ax.set_title("Traza de Minimax: Nim(1,2)",
                 fontsize=13, fontweight='bold', pad=12)

    rows_data = [
        (1,  "max_value",    "(1,2)", "MAX", "—"),
        (2,  "min_value",    "(0,2)", "MIN", "—"),
        (3,  "max_value",    "(0,1)", "MAX", "—"),
        (4,  "utilidad",     "(0,0)", "MIN", "+1 ✓ terminal"),
        (5,  "← max_value",  "(0,1)", "MAX", "+1"),
        (6,  "utilidad",     "(0,0)", "MAX", "-1 ✓ terminal"),
        (7,  "← min_value",  "(0,2)", "MIN", "min(+1,-1)=-1"),
        (8,  "min_value",    "(1,1)", "MIN", "—"),
        (9,  "max_value",    "(0,1)", "MAX", "—"),
        (10, "min_value",    "(0,0)", "MIN", "+1 ✓ terminal"),
        (11, "← max_value",  "(0,1)", "MAX", "+1"),
        (12, "max_value",    "(1,0)", "MAX", "—"),
        (13, "min_value",    "(0,0)", "MIN", "+1 ✓ terminal"),
        (14, "← max_value",  "(1,0)", "MAX", "+1"),
        (15, "← min_value",  "(1,1)", "MIN", "min(+1,+1)=+1"),
        (16, "min_value",    "(1,0)", "MIN", "—"),
        (17, "utilidad",     "(0,0)", "MAX", "-1 ✓ terminal"),
        (18, "← min_value",  "(1,0)", "MIN", "-1"),
        (19, "← max_value",  "(1,2)", "MAX", "max(-1,+1,-1)=+1"),
        (20, "DECISIÓN",     "(1,2)", "MAX", "B-1 → (1,1) ✓"),
    ]

    headers = ["#", "Llamada", "Estado", "Jugador", "Retorna"]
    col_widths = [0.05, 0.22, 0.14, 0.12, 0.38]
    col_x = [0.02, 0.07, 0.30, 0.45, 0.59]

    n_rows = len(rows_data)
    row_height = 0.042
    header_y = 0.96

    # Background and border for table
    table_rect = mpatches.FancyBboxPatch(
        (0.01, 0.01), 0.97, 0.97,
        boxstyle="round,pad=0.005", color='white',
        ec=COLORS["gray"], lw=1.5, zorder=1
    )
    ax.add_patch(table_rect)

    # Header row
    header_bg = mpatches.FancyBboxPatch(
        (0.01, header_y - 0.005), 0.97, row_height + 0.012,
        boxstyle="square,pad=0", color=COLORS["dark"], zorder=2
    )
    ax.add_patch(header_bg)
    for hdr, cx, cw in zip(headers, col_x, col_widths):
        ax.text(cx + cw / 2, header_y + row_height / 2, hdr,
                ha='center', va='center', fontsize=10,
                fontweight='bold', color='white', zorder=3)

    # Terminal row numbers
    terminal_rows = {4, 6, 10, 13, 17}
    return_rows = {5, 7, 11, 14, 15, 18, 19}
    decision_rows = {20}

    for i, row in enumerate(rows_data):
        num, call, state, player, returns = row
        y = header_y - (i + 1) * (row_height + 0.001)

        # Row background
        if num in decision_rows:
            bg_color = COLORS["blue"]
            text_col = 'white'
        elif num in terminal_rows:
            bg_color = '#D5F5E3'
            text_col = COLORS["dark"]
        elif num in return_rows:
            bg_color = '#FEF9E7'
            text_col = COLORS["dark"]
        elif i % 2 == 0:
            bg_color = '#F8F9FA'
            text_col = COLORS["dark"]
        else:
            bg_color = 'white'
            text_col = COLORS["dark"]

        row_rect = mpatches.FancyBboxPatch(
            (0.015, y - 0.003), 0.965, row_height + 0.002,
            boxstyle="square,pad=0", color=bg_color, zorder=2
        )
        ax.add_patch(row_rect)

        row_vals = [str(num), call, state, player, returns]
        for val, cx, cw in zip(row_vals, col_x, col_widths):
            fw = 'bold' if (num in decision_rows or num in terminal_rows) else 'normal'
            ax.text(cx + cw / 2, y + row_height / 2, val,
                    ha='center', va='center', fontsize=9,
                    fontweight=fw, color=text_col, zorder=3)

    # Column separators
    for cx_sep in col_x[1:]:
        ax.plot([cx_sep, cx_sep],
                [header_y - n_rows * (row_height + 0.001) - 0.01,
                 header_y + row_height + 0.012],
                color=COLORS["light"], lw=0.8, zorder=2)

    # Legend
    legend_info = [
        ("#D5F5E3", "Terminal (hoja)"),
        ("#FEF9E7", "Retorno (← propagación)"),
        (COLORS["blue"], "Decisión final"),
    ]
    lx = 0.01
    for (bg, lbl) in legend_info:
        rect = mpatches.FancyBboxPatch((lx, -0.05), 0.025, 0.03,
                                        boxstyle="square,pad=0",
                                        color=bg, ec=COLORS["gray"], zorder=4)
        ax.add_patch(rect)
        ax.text(lx + 0.03, -0.035, lbl, va='center', fontsize=8,
                color=COLORS["dark"], zorder=5)
        lx += 0.28

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.08, 1.04)

    fig.tight_layout()
    _save(fig, "07_minimax_step_by_step.png")


# ---------------------------------------------------------------------------
# 8. Alpha-beta pruning on Nim(2,3)
# ---------------------------------------------------------------------------

def plot_alphabeta_nim23() -> None:
    """Nim(2,3) game tree with alpha-beta pruning visualization."""
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim(-0.5, 15.5)
    ax.set_ylim(-0.8, 5.0)
    ax.axis('off')
    ax.set_title("Alpha-beta en Nim(2,3): ramas podadas en gris",
                 fontsize=13, fontweight='bold', pad=8)

    # Nim(2,3) nim-sum = 2^3 = 1, MAX wins. Optimal: go to (2,2) -> nim-sum=0
    # Root: (2,3) MAX
    # Children (actions on root):
    #   A-1 -> (1,3), A-2 -> (0,3), B-1 -> (2,2)*, B-2 -> (2,1), B-3 -> (2,0)
    # After B-1 -> (2,2): nim-sum=0, MIN loses -> value=-1 for MIN -> MAX gets +1
    # alpha-beta: once we find (2,2)=+1 for MAX, other branches where MIN can force <=+1 get pruned

    # We'll show root, all 5 children, and some grandchildren with pruning

    # Node layout: id -> (x, y, label, is_max, value, alpha_val, beta_val)
    # Pruned branches shown as gray dashed

    root_x, root_y = 7.5, 4.2

    # Level 1: 5 children of root
    child_positions = [
        (1.2,  3.0, '(1,3)', False, -1),
        (4.5,  3.0, '(0,3)', False, -1),
        (7.5,  3.0, '(2,2)', False, 1),   # OPTIMAL
        (10.5, 3.0, '(2,1)', False, 1),
        (13.8, 3.0, '(2,0)', False, -1),
    ]
    child_labels = ['A-1', 'A-2', 'B-1', 'B-2', 'B-3']
    # After exploring B-1 first and getting +1, alpha=+1 at root
    # The first 2 children (A-1, A-2) are explored before B-1 to show contrast
    # B-2, B-3 children might be pruned if ordering is right

    # Level 2: some grandchildren
    # From (2,2) (optimal): show a few moves
    grandchild_pos = [
        (6.0,  1.8, '(1,2)', True,  1, False),
        (7.5,  1.8, '(2,1)', True,  1, False),
        (9.0,  1.8, '(2,0)', True, -1, False),
        # Pruned subtrees under A-1 and A-2 children
        (0.5,  1.8, '...', True, None, True),
        (1.9,  1.8, '...', True, None, True),
        (3.7,  1.8, '...', True, None, True),
        (5.3,  1.8, '...', True, None, True),
        # Pruned under B-2
        (10.5, 1.8, '...', True, None, True),
        # Pruned under B-3
        (13.8, 1.8, '...', True, None, True),
    ]

    # Draw edges root -> children
    for (cx, cy, lbl, is_max, val), edge_lbl in zip(child_positions, child_labels):
        is_opt = (lbl == '(2,2)')
        ec = COLORS["green"] if is_opt else COLORS["dark"]
        lw = 2.5 if is_opt else 1.5
        ax.plot([root_x, cx], [root_y - 0.3, cy + 0.3],
                color=ec, lw=lw, zorder=2, alpha=0.85)
        mx = (root_x + cx) / 2
        my = (root_y - 0.3 + cy + 0.3) / 2
        ax.text(mx, my, edge_lbl, ha='center', va='bottom',
                fontsize=8, color=ec,
                bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.9),
                zorder=6)

    # Draw edges children -> grandchildren
    grandchild_parent_map = [
        ((7.5, 3.0), (6.0,  1.8)),
        ((7.5, 3.0), (7.5,  1.8)),
        ((7.5, 3.0), (9.0,  1.8)),
        ((1.2, 3.0), (0.5,  1.8)),
        ((1.2, 3.0), (1.9,  1.8)),
        ((4.5, 3.0), (3.7,  1.8)),
        ((4.5, 3.0), (5.3,  1.8)),
        ((10.5, 3.0), (10.5, 1.8)),
        ((13.8, 3.0), (13.8, 1.8)),
    ]
    pruned_grand = [False, False, False, True, True, True, True, True, True]

    for (px, py), (cx, cy), is_pruned in zip(
            [m[0] for m in grandchild_parent_map],
            [m[1] for m in grandchild_parent_map],
            pruned_grand):
        if is_pruned:
            ax.plot([px, cx], [py - 0.3, cy + 0.2],
                    color=COLORS["gray"], lw=1.2, linestyle='--', alpha=0.5, zorder=2)
            ax.text((px + cx) / 2, (py - 0.3 + cy + 0.2) / 2 - 0.1,
                    "podado", ha='center', fontsize=7, color=COLORS["gray"],
                    style='italic', zorder=6)
        else:
            ax.plot([px, cx], [py - 0.3, cy + 0.2],
                    color=COLORS["dark"], lw=1.5, zorder=2, alpha=0.85)

    # Draw root
    ax.text(root_x, root_y + 0.45, "α=-∞  β=+∞",
            ha='center', fontsize=8, color=COLORS["orange"])
    circle = plt.Circle((root_x, root_y), 0.32,
                         color=COLORS["blue"], ec='white', lw=1.5, zorder=4)
    ax.add_patch(circle)
    ax.text(root_x, root_y + 0.07, '(2,3)', ha='center', va='center',
            fontsize=8, fontweight='bold', color='white', zorder=5)
    ax.text(root_x, root_y - 0.1, '+1', ha='center', va='center',
            fontsize=8, fontweight='bold', color='white', zorder=5)

    # Draw level-1 children
    ab_annotations = [
        "α=-∞  β=+∞",
        "α=-∞  β=+∞",
        "α=-∞  β=+∞",
        "podado\n(β≤α)",
        "podado\n(β≤α)",
    ]
    child_vals_str = ['-1', '-1', '+1', '+1', '-1']
    for (cx, cy, state_lbl, is_max, val), ab_ann, cv in zip(
            child_positions, ab_annotations, child_vals_str):
        is_pruned_child = 'podado' in ab_ann
        is_opt = (state_lbl == '(2,2)')
        nc = COLORS["red"]  # MIN nodes
        circle = plt.Circle((cx, cy), 0.30, color=nc,
                             ec=COLORS["green"] if is_opt else 'white',
                             lw=2.5 if is_opt else 1.5, zorder=4)
        ax.add_patch(circle)
        ax.text(cx, cy + 0.07, state_lbl, ha='center', va='center',
                fontsize=7.5, fontweight='bold', color='white', zorder=5)
        ax.text(cx, cy - 0.1, cv, ha='center', va='center',
                fontsize=7.5, fontweight='bold', color='white', zorder=5)
        ax.text(cx, cy + 0.42, ab_ann, ha='center', fontsize=7,
                color=COLORS["orange"] if not is_pruned_child else COLORS["red"],
                style='italic')

    # Draw grandchildren
    gc_labels = ['(1,2)\n+1', '(2,1)\n+1', '(2,0)\n-1', '✗', '✗', '✗', '✗', '✗', '✗']
    for (gx, gy, g_state, g_is_max, g_val, g_pruned), gc_lbl in zip(
            grandchild_pos, gc_labels):
        if g_pruned:
            rect = mpatches.FancyBboxPatch(
                (gx - 0.25, gy - 0.18), 0.5, 0.36,
                boxstyle="round,pad=0.02", color=COLORS["gray"],
                ec='white', lw=1, zorder=4, alpha=0.6
            )
            ax.add_patch(rect)
            ax.text(gx, gy, gc_lbl, ha='center', va='center',
                    fontsize=11, fontweight='bold', color='white', zorder=5)
        else:
            gc_color = COLORS["blue"]
            circle = plt.Circle((gx, gy), 0.26,
                                 color=gc_color, ec='white', lw=1.5, zorder=4)
            ax.add_patch(circle)
            ax.text(gx, gy + 0.06, gc_lbl.split('\n')[0], ha='center', va='center',
                    fontsize=7.5, fontweight='bold', color='white', zorder=5)
            ax.text(gx, gy - 0.1, gc_lbl.split('\n')[1] if '\n' in gc_lbl else '',
                    ha='center', va='center',
                    fontsize=7.5, fontweight='bold', color='white', zorder=5)

    # Legend
    legend_elems = [
        mpatches.Patch(color=COLORS["blue"], label='MAX'),
        mpatches.Patch(color=COLORS["red"], label='MIN'),
        mpatches.Patch(color=COLORS["green"], label='Movimiento óptimo'),
        mpatches.Patch(color=COLORS["gray"], label='Nodo/rama podada'),
        plt.Line2D([0], [0], color=COLORS["orange"], lw=0, marker='s',
                   markersize=8, label='α/β anotaciones'),
    ]
    ax.legend(handles=legend_elems, loc='lower left', fontsize=9,
              framealpha=0.9)

    # Nim-sum explanation box
    ax.text(13.5, 4.6,
            "Nim-sum:\n2 ⊕ 3 = 1 ≠ 0\n→ MAX gana\nÓptimo: ir a (2,2)\n2 ⊕ 2 = 0",
            ha='center', fontsize=9, va='top',
            bbox=dict(boxstyle='round,pad=0.4', fc='#EBF5FB',
                      ec=COLORS["blue"], lw=1.5))

    fig.tight_layout()
    _save(fig, "08_alphabeta_nim23.png")


# ---------------------------------------------------------------------------
# 9. Alpha-beta vs minimax node count comparison
# ---------------------------------------------------------------------------

def plot_alphabeta_vs_minimax() -> None:
    """Two panels: bar chart node counts + complexity formulas."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Alpha-beta vs Minimax: misma decisión, menos nodos",
                 fontsize=13, fontweight='bold', y=1.01)

    # Compute actual node counts
    game_instances = [
        ("Nim(1,2)", (1, 2)),
        ("Nim(2,3)", (2, 3)),
        ("Nim(1,2,3)", (1, 2, 3)),
    ]

    mm_counts = []
    ab_counts = []
    labels = []
    for name, state in game_instances:
        _, _, mm_c = _minimax_with_count(state, True)
        _, _, ab_c = _alphabeta(state, True, -2, 2)
        mm_counts.append(mm_c)
        ab_counts.append(ab_c)
        labels.append(name)

    # --- Left: grouped bar chart ---
    ax = axes[0]
    x = np.arange(len(labels))
    width = 0.35
    bars_mm = ax.bar(x - width / 2, mm_counts, width, label='Minimax',
                     color=COLORS["blue"], alpha=0.85, edgecolor='white', lw=1.5)
    bars_ab = ax.bar(x + width / 2, ab_counts, width, label='Alpha-beta',
                     color=COLORS["green"], alpha=0.85, edgecolor='white', lw=1.5)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylabel("Nodos expandidos", fontsize=11)
    ax.set_title("Nodos expandidos:\nMinimax vs Alpha-beta", fontsize=11, fontweight='bold')
    ax.legend(fontsize=10)

    # Add value labels + percentage reduction
    for i, (mm_v, ab_v) in enumerate(zip(mm_counts, ab_counts)):
        ax.text(i - width / 2, mm_v + 0.3, str(mm_v),
                ha='center', va='bottom', fontsize=10, fontweight='bold',
                color=COLORS["blue"])
        ax.text(i + width / 2, ab_v + 0.3, str(ab_v),
                ha='center', va='bottom', fontsize=10, fontweight='bold',
                color=COLORS["green"])
        if mm_v > 0:
            pct = int(100 * (mm_v - ab_v) / mm_v)
            ax.text(i, max(mm_v, ab_v) + 1.2, str(pct) + "% menos",
                    ha='center', fontsize=9, color=COLORS["orange"], fontweight='bold')

    # --- Right: formulas and guarantees ---
    ax = axes[1]
    ax.axis('off')
    ax.set_title("Garantías de Alpha-beta", fontsize=11, fontweight='bold')

    formulas = [
        (COLORS["dark"], "✓  Misma decisión óptima que Minimax", 14),
        (COLORS["blue"], "Minimax", 12),
        (COLORS["blue"], "    Complejidad: O(b^m)", 11),
        (COLORS["red"], "Alpha-beta (peor caso)", 12),
        (COLORS["red"], "    Complejidad: O(b^m)", 11),
        (COLORS["orange"], "Alpha-beta (orden aleatorio)", 12),
        (COLORS["orange"], "    Complejidad: O(b^(3m/4))", 11),
        (COLORS["green"], "Alpha-beta (orden perfecto)", 12),
        (COLORS["green"], "    Complejidad: O(b^(m/2))", 11),
        (COLORS["purple"], "Con orden perfecto:", 11),
        (COLORS["purple"], "    doble profundidad de búsqueda", 10),
        (COLORS["purple"], "    en el mismo tiempo!", 10),
    ]

    y_pos = 0.92
    for color, text, fsize in formulas:
        if text.startswith("✓"):
            bg = '#EAFAF1'
            ec_col = COLORS["green"]
        else:
            bg = 'white'
            ec_col = 'none'
        ax.text(0.1, y_pos, text, va='top', fontsize=fsize,
                color=color, fontweight='bold' if fsize >= 12 else 'normal',
                transform=ax.transAxes,
                bbox=dict(boxstyle='round,pad=0.2', fc=bg, ec=ec_col, lw=1))
        y_pos -= 0.08

    # Formula box
    box_text = ("b = factor de ramificación\n"
                "m = profundidad máxima\n\n"
                "Ejemplo: Ajedrez b≈35, m≈80\n"
                "Minimax: 35^80 ≈ 10^123 nodos\n"
                "Alpha-beta óptimo: ≈ 10^61 nodos")
    ax.text(0.5, 0.2, box_text, va='center', ha='center',
            fontsize=9.5, color=COLORS["dark"],
            transform=ax.transAxes,
            bbox=dict(boxstyle='round,pad=0.5', fc=COLORS["light"],
                      ec=COLORS["blue"], lw=1.5))

    fig.tight_layout()
    _save(fig, "09_alphabeta_vs_minimax.png")


# ---------------------------------------------------------------------------
# 10. Tic-tac-toe endgame minimax decision
# ---------------------------------------------------------------------------

def plot_tictactoe_endgame() -> None:
    """Two panels: board position + minimax decision tree for tic-tac-toe endgame."""
    # Position: X to move, O threatens immediate win at position 5
    # board = ['X', 'O', 'X', 'O', 'O', '', 'X', '', '']
    # Row 0: X,O,X; Row 1: O,O,_; Row 2: X,_,_
    # O has 1,3,4. Row-1 positions are 3,4,5: O at 3,4 -> O wins if plays 5.
    # X must block at 5.
    board = ['X', 'O', 'X', 'O', 'O', '', 'X', '', '']
    empty_cells = [i for i, c in enumerate(board) if c == '']

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle("Minimax: ¿cuál es la jugada óptima de X?",
                 fontsize=13, fontweight='bold', y=1.01)

    # --- Left: board ---
    ax = axes[0]
    _draw_tictactoe_board(ax, board, title="Posición actual — turno de X (MAX)")

    # Highlight empty cells
    for idx in empty_cells:
        row = 2 - (idx // 3)
        col = idx % 3
        rect = mpatches.Rectangle((col + 0.05, row + 0.05), 0.9, 0.9,
                                   color=COLORS["blue"], alpha=0.15, zorder=1)
        ax.add_patch(rect)
        ax.text(col + 0.5, row + 0.5, str(idx),
                ha='center', va='center', fontsize=14, color=COLORS["blue"],
                alpha=0.5, fontweight='bold')

    ax.text(1.5, -0.25, "Celdas vacías: " + str(empty_cells),
            ha='center', va='center', fontsize=10,
            color=COLORS["dark"], transform=ax.transData,
            bbox=dict(boxstyle='round,pad=0.3', fc=COLORS["light"],
                      ec=COLORS["blue"], lw=1.5))

    # O threatens row 1 (cells 3,4,5): annotate
    ax.annotate('', xy=(2.92, 0.5), xytext=(2.55, 0.5),
                arrowprops=dict(arrowstyle='->', color=COLORS["red"], lw=2))
    ax.text(3.2, 0.5, "O amenaza\nganar aquí!",
            va='center', fontsize=8, color=COLORS["red"],
            bbox=dict(boxstyle='round,pad=0.2', fc='#FDEDEC', ec=COLORS["red"]))

    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 3.5)

    # --- Right: decision tree ---
    ax = axes[1]
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.3, 3.5)
    ax.axis('off')
    ax.set_title("Árbol minimax (3 movimientos posibles)",
                 fontsize=11, fontweight='bold')

    # Compute minimax values for each X move
    move_results = {}
    for idx in empty_cells:
        new_board = board[:]
        new_board[idx] = 'X'
        if _ttt_terminal(new_board):
            val = _ttt_utility(new_board)
            move_results[idx] = val
        else:
            val, _ = _ttt_minimax(new_board, False)
            move_results[idx] = val

    # Find best move
    best_move = max(empty_cells, key=lambda i: move_results[i])

    # Draw tree
    root_x, root_y = 2.0, 3.2
    n_children = len(empty_cells)
    child_xs = np.linspace(0.5, 3.5, n_children)

    val_colors = {1: COLORS["green"], 0: COLORS["gray"], -1: COLORS["red"]}
    val_labels = {1: "+1 (X gana)", 0: "0 (empate)", -1: "-1 (O gana)"}

    for cx, move_idx in zip(child_xs, empty_cells):
        cy = 1.8
        val = move_results[move_idx]
        is_opt = (move_idx == best_move)
        ec = COLORS["green"] if is_opt else COLORS["dark"]
        lw = 2.5 if is_opt else 1.5
        ax.plot([root_x, cx], [root_y - 0.3, cy + 0.3],
                color=ec, lw=lw, zorder=2)
        edge_label = "celda " + str(move_idx)
        mx = (root_x + cx) / 2
        my = (root_y - 0.3 + cy + 0.3) / 2
        ax.text(mx, my, edge_label, ha='center', va='bottom',
                fontsize=8, color=ec,
                bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.9))

        # Child node with value
        nc = val_colors.get(val, COLORS["gray"])
        node_label = "X@" + str(move_idx) + "\n" + str(val)
        circle = plt.Circle((cx, cy), 0.30,
                             color=COLORS["red"], ec='white', lw=1.5, zorder=4)
        ax.add_patch(circle)
        ax.text(cx, cy + 0.07, "X@" + str(move_idx),
                ha='center', va='center', fontsize=7.5,
                fontweight='bold', color='white', zorder=5)
        ax.text(cx, cy - 0.09, str(val),
                ha='center', va='center', fontsize=8,
                fontweight='bold', color='white', zorder=5)

        # Value label below
        ax.text(cx, cy - 0.55, val_labels.get(val, str(val)),
                ha='center', fontsize=8, color=nc, fontweight='bold')

        # Star for optimal
        if is_opt:
            ax.plot(cx + 0.38, cy + 0.28, '*', color=COLORS["green"],
                    markersize=14, zorder=6)

    # Root node
    circle = plt.Circle((root_x, root_y), 0.32,
                         color=COLORS["blue"], ec='white', lw=1.5, zorder=4)
    ax.add_patch(circle)
    ax.text(root_x, root_y + 0.07, "MAX",
            ha='center', va='center', fontsize=8,
            fontweight='bold', color='white', zorder=5)
    ax.text(root_x, root_y - 0.1, str(max(move_results.values())),
            ha='center', va='center', fontsize=8,
            fontweight='bold', color='white', zorder=5)

    # Optimal decision annotation
    opt_val = move_results[best_move]
    opt_msg = "Decisión óptima: jugar en celda " + str(best_move)
    if opt_val == 1:
        opt_msg += "\n→ X gana con juego perfecto"
    elif opt_val == 0:
        opt_msg += "\n→ Empate garantizado (mejor que perder)"
    else:
        opt_msg += "\n→ X pierde (pero es lo mejor disponible)"

    ax.text(2.0, 0.5, opt_msg,
            ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.4', fc='#EAFAF1',
                      ec=COLORS["green"], lw=2))

    fig.tight_layout()
    _save(fig, "10_tictactoe_endgame.png")


# ---------------------------------------------------------------------------
# 11. Nim XOR pattern heatmap
# ---------------------------------------------------------------------------

def plot_nim_xor_pattern() -> None:
    """5x5 heatmap of Nim(a,b) positions colored by nim-sum."""
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.set_title("Patrón de victoria en Nim(a,b): nim-sum = a ⊕ b",
                 fontsize=13, fontweight='bold', pad=8)

    n = 5  # 0..4

    # Build grid
    win_lose = np.zeros((n, n))  # 0=lose (nim-sum=0), 1=win (nim-sum!=0)
    nim_sums = np.zeros((n, n), dtype=int)
    for a in range(n):
        for b in range(n):
            ns = a ^ b
            nim_sums[a, b] = ns
            win_lose[a, b] = 0 if ns == 0 else 1

    # Custom colormap: red for lose (0), green for win (1)
    cmap = mcolors.ListedColormap([COLORS["red"], COLORS["green"]])
    ax.imshow(win_lose, cmap=cmap, aspect='equal', vmin=0, vmax=1,
              interpolation='nearest', alpha=0.7)

    # Cell labels
    for a in range(n):
        for b in range(n):
            ns = nim_sums[a, b]
            fc = 'white'
            ax.text(b, a, str(ns), ha='center', va='center',
                    fontsize=14, fontweight='bold', color=fc)

    # Circle the diagonal (losing positions)
    for k in range(n):
        circle = plt.Circle((k, k), 0.42, fill=False,
                             color='white', lw=2.5, linestyle='--', zorder=5)
        ax.add_patch(circle)

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(range(n), fontsize=12)
    ax.set_yticklabels(range(n), fontsize=12)
    ax.set_xlabel("Tamaño de pila B (b)", fontsize=12, labelpad=8)
    ax.set_ylabel("Tamaño de pila A (a)", fontsize=12, labelpad=8)

    # Subtitle
    fig.text(0.5, 0.01,
             "Verde: jugador en turno GANA (nim-sum ≠ 0)  |  "
             "Rojo: jugador en turno PIERDE (nim-sum = 0)\n"
             "Círculos: diagonal principal — posiciones perdedoras (a=b, nim-sum=0)",
             ha='center', fontsize=9.5, color=COLORS["dark"])

    # Legend
    legend_elems = [
        mpatches.Patch(color=COLORS["green"], alpha=0.7, label='Ganador (nim-sum ≠ 0)'),
        mpatches.Patch(color=COLORS["red"], alpha=0.7, label='Perdedor (nim-sum = 0)'),
        plt.Line2D([0], [0], color='white', lw=2, linestyle='--',
                   label='Diagonal perdedora (a = b)'),
    ]
    ax.legend(handles=legend_elems, loc='upper right', fontsize=9,
              framealpha=0.9, facecolor=COLORS["dark"], labelcolor='white',
              edgecolor=COLORS["gray"])

    fig.tight_layout(rect=[0, 0.06, 1, 1])
    _save(fig, "11_nim_xor_pattern.png")


# ---------------------------------------------------------------------------
# 12. Depth limit and evaluation function
# ---------------------------------------------------------------------------

def plot_depth_limit_eval() -> None:
    """Abstract game tree with depth cutoff, eval values, and horizon effect."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(-0.5, 13.5)
    ax.set_ylim(-1.0, 5.5)
    ax.axis('off')
    ax.set_title("Minimax con límite de profundidad + función de evaluación",
                 fontsize=13, fontweight='bold', pad=8)

    # Tree layout: 4 levels shown, cutoff at depth=4
    # Level 0 (MAX): root at x=6.5, y=5.0
    # Level 1 (MIN): 3 nodes
    # Level 2 (MAX): 6 nodes
    # Level 3 = cutoff (depth=4): eval nodes — 8 nodes

    level_y = [5.0, 3.8, 2.6, 1.4]
    level_labels = ['MAX', 'MIN', 'MAX', 'eval(s)']
    level_colors = [COLORS["blue"], COLORS["red"], COLORS["blue"], COLORS["orange"]]
    level_is_max = [True, False, True, None]

    # Node positions
    nodes_by_level = [
        [(6.5,)],
        [(2.5,), (6.5,), (10.5,)],
        [(0.8,), (4.2,), (5.2,), (7.8,), (8.8,), (12.2,)],
        [(0.2,), (1.4,), (3.5,), (4.9,), (5.0,), (6.6,), (8.2,), (9.4,), (11.5,), (12.9,)],
    ]

    # Eval values for cutoff nodes
    eval_vals = [0.6, -0.3, 0.1, 0.8, -0.5, 0.4, 0.7, -0.2, 0.3, -0.6]
    # Propagated values (approximate)
    level2_vals = [
        max(0.6, -0.3),   # 0.6
        max(0.1, 0.8),    # 0.8
        min(-0.5, 0.4),   # -0.5
        min(0.7, -0.2),   # -0.2
        max(0.3, -0.6),   # 0.3 (only 2 children for last 2 level2 nodes)
        0.3,
    ]
    # Actually let's simplify: assign values manually
    level2_vals = [0.6, 0.8, -0.5, -0.2, 0.3, 0.3]
    level1_vals = [min(0.6, 0.8), min(-0.5, -0.2), min(0.3, 0.3)]
    level0_val = max(level1_vals)

    all_vals = [
        [level0_val],
        level1_vals,
        level2_vals,
        eval_vals[:10],
    ]

    # Edge connections: level -> children
    # level 0 (1 node) -> level 1 (3 nodes): node 0 -> 0,1,2
    # level 1 (3 nodes) -> level 2 (6 nodes): node i -> 2i, 2i+1
    # level 2 (6 nodes) -> level 3 (10 nodes): last 4 of level2 have 2 children each,
    #   first 2 have 1 child each (simplified)
    l2_to_l3 = {0: [0, 1], 1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [8], 5: [9]}

    # Draw depth-limit line
    cutoff_y = 1.0
    ax.axhline(cutoff_y, color=COLORS["orange"], lw=2.5, linestyle='--',
               alpha=0.8, zorder=1)
    ax.text(13.2, cutoff_y + 0.12, "Límite d=4",
            ha='right', fontsize=11, color=COLORS["orange"],
            fontweight='bold', zorder=5)

    # Draw edges
    def get_pos(level, idx):
        return nodes_by_level[level][idx][0], level_y[level]

    # L0 -> L1
    for j in range(3):
        x0, y0 = get_pos(0, 0)
        x1, y1 = get_pos(1, j)
        ax.plot([x0, x1], [y0 - 0.28, y1 + 0.28],
                color=COLORS["dark"], lw=1.5, zorder=2)

    # L1 -> L2
    for j in range(3):
        for k in [2 * j, 2 * j + 1]:
            x0, y0 = get_pos(1, j)
            x1, y1 = get_pos(2, k)
            ax.plot([x0, x1], [y0 - 0.28, y1 + 0.28],
                    color=COLORS["dark"], lw=1.5, zorder=2)

    # L2 -> L3
    for j, children in l2_to_l3.items():
        for k in children:
            if k < len(nodes_by_level[3]):
                x0, y0 = get_pos(2, j)
                x1, y1 = get_pos(3, k)
                ax.plot([x0, x1], [y0 - 0.28, y1 + 0.28],
                        color=COLORS["dark"], lw=1.5, zorder=2)

    # Horizon effect: one branch goes below cutoff (dashed)
    x_last = nodes_by_level[3][-1][0]
    ax.plot([x_last, x_last - 0.3, x_last + 0.3],
            [cutoff_y - 0.02, cutoff_y - 0.7, cutoff_y - 0.7],
            color=COLORS["gray"], lw=1.5, linestyle='--', alpha=0.6, zorder=2)
    ax.text(x_last, cutoff_y - 0.85, "¿?\nhorizonte",
            ha='center', fontsize=8, color=COLORS["gray"],
            style='italic',
            bbox=dict(boxstyle='round,pad=0.2', fc=COLORS["light"],
                      ec=COLORS["gray"], alpha=0.8))

    # Draw nodes
    for level in range(4):
        for i, (x_val,) in enumerate(nodes_by_level[level]):
            y = level_y[level]
            val = all_vals[level][i] if i < len(all_vals[level]) else 0.0

            if level == 3:
                # Eval nodes: orange squares
                rect = mpatches.FancyBboxPatch(
                    (x_val - 0.3, y - 0.22), 0.6, 0.44,
                    boxstyle="round,pad=0.02", color=COLORS["orange"],
                    ec='white', lw=1.5, zorder=4
                )
                ax.add_patch(rect)
                val_str = ("+" if val > 0 else "") + str(round(val, 1))
                ax.text(x_val, y + 0.07, "eval",
                        ha='center', va='center', fontsize=7,
                        fontweight='bold', color='white', zorder=5)
                ax.text(x_val, y - 0.1, val_str,
                        ha='center', va='center', fontsize=7.5,
                        fontweight='bold', color='white', zorder=5)
            else:
                nc = level_colors[level]
                circle = plt.Circle((x_val, y), 0.28, color=nc,
                                    ec='white', lw=1.5, zorder=4)
                ax.add_patch(circle)
                player_lbl = level_labels[level]
                val_str = ("+" if val > 0 else "") + str(round(val, 2))
                ax.text(x_val, y + 0.07, player_lbl,
                        ha='center', va='center', fontsize=7.5,
                        fontweight='bold', color='white', zorder=5)
                ax.text(x_val, y - 0.1, val_str,
                        ha='center', va='center', fontsize=7.5,
                        fontweight='bold', color='white', zorder=5)

    # Level labels on left
    for lv, (y, lbl) in enumerate(zip(level_y, level_labels)):
        ax.text(-0.3, y, lbl, ha='right', va='center',
                fontsize=10, fontweight='bold', color=level_colors[lv])

    # Annotation box
    ax.text(6.5, 4.85,
            "eval(s) ≈ h(n) del módulo 14: estimación del valor final sin llegar a terminal",
            ha='center', fontsize=9.5, color=COLORS["dark"],
            bbox=dict(boxstyle='round,pad=0.4', fc='#FEF9E7',
                      ec=COLORS["orange"], lw=1.5))

    # Horizon effect annotation
    ax.text(11.5, cutoff_y - 0.55,
            "Efecto horizonte:\nnodo catastrófico\noculto tras el límite",
            ha='center', fontsize=8.5, color=COLORS["red"],
            bbox=dict(boxstyle='round,pad=0.3', fc='#FDEDEC', ec=COLORS["red"]))

    fig.tight_layout()
    _save(fig, "12_depth_limit_eval.png")


# ---------------------------------------------------------------------------
# 13. Chess complexity
# ---------------------------------------------------------------------------

def plot_chess_complexity() -> None:
    """Two panels: log-scale bar chart of game complexities + table."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    fig.suptitle("Complejidad de juegos: ¿por qué no hay minimax exacto para ajedrez?",
                 fontsize=13, fontweight='bold', y=1.01)

    # --- Left: horizontal bar chart (log10 scale) ---
    ax = axes[0]

    # Use (label, log10_value, display_label, category) to avoid float overflow for large exponents
    game_data = [
        ("Nim(1,2)\n(exacto)",           np.log10(12),   "12",       "exact"),
        ("Tic-tac-toe\n(exacto)",        np.log10(9**9), "~10^8.6",  "exact"),
        ("Damas\n(exacto)",              20.7,           "~10^20",   "exact"),
        ("Ajedrez\n(minimax exacto)",    123,            "10^123",   "exact"),
        ("Ajedrez\n(alpha-beta opt.)",   61,             "10^61",    "pruning"),
        ("Ajedrez\n(alpha-beta+orden)",  17,             "~10^17",   "practical"),
        ("Go\n(minimax exacto)",         360,            "10^360",   "exact"),
    ]

    labels = [g[0] for g in game_data]
    log_vals = [g[1] for g in game_data]
    display_labels = [g[2] for g in game_data]
    categories = [g[3] for g in game_data]

    cat_colors = {
        "exact":    COLORS["red"],
        "pruning":  COLORS["orange"],
        "practical": COLORS["green"],
    }
    bar_colors = [cat_colors[c] for c in categories]

    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, log_vals, color=bar_colors, alpha=0.85,
                   edgecolor='white', lw=1.5, height=0.6)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9.5)
    ax.set_xlabel("log₁₀(nodos)", fontsize=11)
    ax.set_title("Nodos en el árbol de búsqueda\n(escala logarítmica)",
                 fontsize=11, fontweight='bold')

    # Add value labels
    for i, (bar, lv, dlbl) in enumerate(zip(bars, log_vals, display_labels)):
        ax.text(lv + 0.5, i, dlbl,
                va='center', fontsize=8, color=COLORS["dark"], fontweight='bold')

    # Vertical line: 1 second threshold
    ax.axvline(9, color=COLORS["purple"], lw=2, linestyle='--', alpha=0.8)
    ax.text(9, len(labels) - 0.3, "~1s\n(10^9 ops)",
            ha='center', fontsize=8.5, color=COLORS["purple"],
            fontweight='bold')

    # Legend
    legend_elems = [
        mpatches.Patch(color=COLORS["red"], alpha=0.85, label='Exacto'),
        mpatches.Patch(color=COLORS["orange"], alpha=0.85, label='Con poda alpha-beta'),
        mpatches.Patch(color=COLORS["green"], alpha=0.85, label='Práctico (con heurística)'),
    ]
    ax.legend(handles=legend_elems, loc='lower right', fontsize=9)
    ax.set_xlim(0, max(log_vals) * 1.15)

    # --- Right: table ---
    ax = axes[1]
    ax.axis('off')
    ax.set_title("Parámetros típicos por juego",
                 fontsize=11, fontweight='bold')

    table_data = [
        ["Juego",       "b",    "d",    "Algoritmo"],
        ["Nim(1,2)",    "3",    "4",    "Minimax exacto"],
        ["Tic-tac-toe", "9",    "9",    "Minimax exacto"],
        ["Damas",       "10",   "50",   "Alpha-beta+eval"],
        ["Ajedrez",     "35",   "80",   "Alpha-beta+eval+NNUE"],
        ["Go",          "250",  "150",  "MCTS+redes neur."],
    ]

    col_widths_t = [0.30, 0.12, 0.12, 0.40]
    col_x_t = [0.03, 0.34, 0.47, 0.60]
    row_height_t = 0.12
    y_start_t = 0.92

    row_bgs = [COLORS["dark"], '#EBF5FB', 'white', '#EBF5FB', 'white', '#EBF5FB']
    row_tcs = ['white', COLORS["dark"], COLORS["dark"],
               COLORS["dark"], COLORS["dark"], COLORS["dark"]]

    for i, (row, bg, tc) in enumerate(zip(table_data, row_bgs, row_tcs)):
        y = y_start_t - i * row_height_t
        rect = mpatches.FancyBboxPatch(
            (0.01, y - row_height_t + 0.005), 0.97, row_height_t - 0.005,
            boxstyle="square,pad=0", color=bg, ec=COLORS["light"],
            lw=0.8, zorder=2
        )
        ax.add_patch(rect)
        for j, (val, cx, cw) in enumerate(zip(row, col_x_t, col_widths_t)):
            fw = 'bold' if i == 0 or j == 0 else 'normal'
            ax.text(cx + cw / 2, y - row_height_t / 2, val,
                    ha='center', va='center', fontsize=10,
                    fontweight=fw, color=tc, zorder=3)

    # Note about Go
    ax.text(0.5, 0.08,
            "b = factor de ramificación promedio\n"
            "d = profundidad típica de la partida\n"
            "MCTS = Monte Carlo Tree Search\n"
            "NNUE = Efficiently Updatable Neural Networks",
            ha='center', va='center', fontsize=8.5, color=COLORS["gray"],
            transform=ax.transAxes, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', fc=COLORS["light"],
                      ec=COLORS["gray"], lw=1))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    fig.tight_layout()
    _save(fig, "13_chess_complexity.png")


# ---------------------------------------------------------------------------
# Alpha-cutoff example
# ---------------------------------------------------------------------------

def plot_alpha_cutoff_example():
    """
    Illustrates an alpha-cutoff on a small abstract game tree.
    MAX root -> two MIN children -> 4 leaf nodes (one pruned).
    Saves to 14_alpha_cutoff_example.png.
    """
    fig, (ax_tree, ax_table) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("Ejemplo de Poda Alfa (α-cutoff)", fontsize=15, fontweight="bold",
                 color=COLORS["dark"])

    # ------------------------------------------------------------------ tree
    ax = ax_tree
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_facecolor("white")

    dark = COLORS["dark"]
    r = 0.42   # circle radius
    hs = 0.38  # half-size for squares

    # helper: draw circle node
    def draw_circle(cx, cy, color, lines, step_label, step_side="above"):
        circ = plt.Circle((cx, cy), r, color=color, zorder=3)
        ax.add_patch(circ)
        ax.text(cx, cy + 0.07, lines[0], ha="center", va="center",
                fontsize=8.5, fontweight="bold", color="white", zorder=4)
        ax.text(cx, cy - 0.22, lines[1], ha="center", va="center",
                fontsize=8, color="white", zorder=4)
        sy = cy + r + 0.18 if step_side == "above" else cy - r - 0.22
        ax.text(cx, sy, step_label, ha="center", va="center",
                fontsize=8, color=COLORS["gray"], fontstyle="italic", zorder=4)

    # helper: draw square leaf
    def draw_square(cx, cy, color, label, step_label, alpha=1.0):
        sq = plt.Rectangle((cx - hs, cy - hs), 2*hs, 2*hs,
                            color=color, alpha=alpha, zorder=3)
        ax.add_patch(sq)
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=11, fontweight="bold",
                color="white" if alpha > 0.5 else COLORS["gray"], zorder=4)
        ax.text(cx, cy - hs - 0.2, step_label, ha="center", va="top",
                fontsize=8, color=COLORS["gray"], fontstyle="italic", zorder=4)

    # --- nodes ---
    draw_circle(5.0, 5.8, COLORS["blue"], ["MAX", "v=3"], "(1)")
    draw_circle(2.0, 3.5, COLORS["red"],  ["MIN(L)", "v=3"], "(2)")
    draw_circle(8.0, 3.5, COLORS["red"],  ["MIN(R)", "v=1*"], "(7)")

    # alpha/beta labels beside MIN nodes
    ax.text(0.3, 3.5, "α=-∞\nβ=+∞", ha="left", va="center",
            fontsize=7.5, color=COLORS["gray"], fontstyle="italic", zorder=4)
    # highlighted box beside MIN(R) showing inherited alpha
    ax.text(9.9, 3.8, "α=3\nβ=+∞", ha="right", va="center",
            fontsize=8, color=COLORS["orange"], fontweight="bold", zorder=4,
            bbox=dict(boxstyle="round,pad=0.3", fc="#FEF9E7",
                      ec=COLORS["orange"], lw=1.5))

    # --- leaves ---
    draw_square(0.9, 1.4, COLORS["green"], "3", "(3)")
    draw_square(3.1, 1.4, COLORS["green"], "5", "(4)")
    draw_square(6.8, 1.4, COLORS["green"], "1", "(8)")
    draw_square(9.1, 1.4, COLORS["gray"],  "?", " ", alpha=0.4)
    ax.text(9.1, 1.4 - hs - 0.35, "PODADO", ha="center", va="top",
            fontsize=8, color=COLORS["red"], fontweight="bold", zorder=4)

    # --- edges ---
    def edge(x1, y1, x2, y2, style="solid", color=dark, alpha=1.0):
        ls = "--" if style == "dashed" else "-"
        ax.annotate("", xy=(x2, y2 + r + 0.02), xytext=(x1, y1 - r - 0.02),
                    arrowprops=dict(arrowstyle="-", color=color,
                                   lw=2, linestyle=ls, alpha=alpha),
                    zorder=2)

    # root -> MIN children
    edge(5.0, 5.8, 2.0, 3.5)
    edge(5.0, 5.8, 8.0, 3.5)
    # MIN(L) -> leaves 3 and 5
    edge(2.0, 3.5, 0.9, 1.4)
    edge(2.0, 3.5, 3.1, 1.4)
    # MIN(R) -> leaf 1
    edge(8.0, 3.5, 6.8, 1.4)
    # MIN(R) -> leaf ? (dashed + red X)
    edge(8.0, 3.5, 9.1, 1.4, style="dashed", color=COLORS["gray"], alpha=0.5)
    mid_x = (8.0 + 9.1) / 2
    mid_y = (3.5 + 1.4 + r + 0.02 + hs + 0.02) / 2  # rough midpoint in y
    mid_y = (3.5 - r - 0.02 + 1.4 + hs + 0.02) / 2
    ax.text(mid_x + 0.1, mid_y, "✗", ha="center", va="center",
            fontsize=16, color=COLORS["red"], fontweight="bold", zorder=5)

    # --- annotations ---
    # beta <= alpha → PODA
    ax.annotate("β=1 ≤ α=3\n→ PODA!", xy=(8.4, 3.05), xytext=(10.0, 2.8),
                fontsize=8.5, color=COLORS["red"],
                arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.5),
                ha="right", va="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="#FDEDEC",
                          ec=COLORS["red"], lw=1.5))
    # alpha <- 3
    ax.annotate("α ← 3\n(MAX garantiza ≥3)", xy=(4.6, 5.4), xytext=(1.0, 5.1),
                fontsize=8.5, color=COLORS["orange"],
                arrowprops=dict(arrowstyle="->", color=COLORS["orange"], lw=1.5),
                ha="left", va="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="#FEF9E7",
                          ec=COLORS["orange"], lw=1.5))
    # level labels at right margin
    ax.text(9.8, 5.8, "MAX", ha="right", va="center",
            fontsize=9, color=COLORS["blue"], fontweight="bold")
    ax.text(9.8, 3.5, "MIN", ha="right", va="center",
            fontsize=9, color=COLORS["red"], fontweight="bold")
    ax.text(9.8, 1.4, "Hoja", ha="right", va="center",
            fontsize=9, color=COLORS["green"], fontweight="bold")

    # ------------------------------------------------------------------ table
    ax2 = ax_table
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-0.05, 1.05)
    ax2.axis("off")
    ax2.set_facecolor("white")

    col_x = [0.0, 0.08, 0.21, 0.29, 0.37]
    col_widths = [0.08, 0.13, 0.08, 0.08, 0.63]
    headers = ["Paso", "Nodo", "α", "β", "Qué ocurre"]
    row_h = 0.073
    start_y = 0.965

    rows = [
        ("(1)", "MAX(root)",   "-∞", "+∞", "Inicio; llama a MIN(L)"),
        ("(2)", "MIN(L)",      "-∞", "+∞", "Entra con α=-∞, β=+∞"),
        ("(3)", "Hoja 3",      "-∞", "+∞", "Retorna 3 a MIN(L)"),
        ("(4)", "MIN(L)",      "-∞", "3",  "v=3, β←min(+∞,3)=3"),
        ("(5)", "Hoja 5",      "-∞", "3",  "Retorna 5 a MIN(L)"),
        ("(6)", "MIN(L) ←",   "-∞", "3",  "5>v: v queda en 3; retorna 3"),
        ("(7)", "MAX(root)",   "3",  "+∞", "α←max(-∞,3)=3; llama MIN(R)"),
        ("(8)", "MIN(R)",      "3",  "+∞", "Entra con α=3, β=+∞"),
        ("(9)", "Hoja 1",      "3",  "+∞", "Retorna 1 a MIN(R)"),
        ("★",  "MIN(R) PODA", "3",  "1",  "β←1; β=1 ≤ α=3 → PODA! '?' no se explora"),
        (" ",  "MAX(root) ←", "3",  "+∞", "max(3,1)=3; elige rama izquierda"),
    ]

    # header row
    hy = start_y
    for ci, (cx, cw, hdr) in enumerate(zip(col_x, col_widths, headers)):
        rect = plt.Rectangle((cx, hy - row_h), cw, row_h,
                              fc=COLORS["dark"], ec="white", lw=0.5, zorder=2,
                              transform=ax2.transData)
        ax2.add_patch(rect)
        ax2.text(cx + cw / 2, hy - row_h / 2, hdr,
                 ha="center", va="center", fontsize=8, color="white",
                 fontweight="bold", zorder=3)

    for ri, row in enumerate(rows):
        ry = start_y - row_h * (ri + 1)
        is_prune = (ri == 9)   # ★ row
        is_alpha = (ri == 6)   # α←3 row

        if is_prune:
            bg = "#FDEDEC"
            tc = COLORS["red"]
            fw = "bold"
        elif is_alpha:
            bg = "#FEF9E7"
            tc = COLORS["orange"]
            fw = "bold"
        else:
            bg = "#F8F9FA" if ri % 2 == 0 else "white"
            tc = COLORS["dark"]
            fw = "normal"

        for ci, (cx, cw, cell) in enumerate(zip(col_x, col_widths, row)):
            rect = plt.Rectangle((cx, ry - row_h), cw, row_h,
                                  fc=bg, ec="#DEE2E6", lw=0.4, zorder=2,
                                  transform=ax2.transData)
            ax2.add_patch(rect)
            fs = 8 if ci < 4 else 7.5
            ax2.text(cx + cw / 2, ry - row_h / 2, cell,
                     ha="center", va="center", fontsize=fs,
                     color=tc, fontweight=fw, zorder=3,
                     wrap=False)

    # insight box at bottom
    insight = ("α=3: MAX ya tiene garantizado un valor de 3 desde MIN(L).\n"
               "MIN(R) puede forzar a lo sumo 1. MAX jamás elegiría ir ahí.\n"
               "El valor de '?' es completamente irrelevante.")
    ax2.text(0.5, 0.04, insight, ha="center", va="center",
             fontsize=9, color=COLORS["dark"],
             transform=ax2.transAxes,
             bbox=dict(boxstyle="round,pad=0.5", fc="#EBF5FB",
                       ec=COLORS["blue"], lw=1.5))

    fig.tight_layout()
    _save(fig, "14_alpha_cutoff_example.png")


# ---------------------------------------------------------------------------
# Beta-cutoff example
# ---------------------------------------------------------------------------

def plot_beta_cutoff_example():
    """
    Illustrates a beta-cutoff on a small abstract game tree.
    MIN root -> two MAX children -> 4 leaf nodes (one pruned).
    Saves to 15_beta_cutoff_example.png.
    """
    fig, (ax_tree, ax_table) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("Ejemplo de Poda Beta (β-cutoff)", fontsize=15, fontweight="bold",
                 color=COLORS["dark"])

    # ------------------------------------------------------------------ tree
    ax = ax_tree
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_facecolor("white")

    dark = COLORS["dark"]
    r = 0.42
    hs = 0.38

    def draw_circle(cx, cy, color, lines, step_label):
        circ = plt.Circle((cx, cy), r, color=color, zorder=3)
        ax.add_patch(circ)
        ax.text(cx, cy + 0.07, lines[0], ha="center", va="center",
                fontsize=8.5, fontweight="bold", color="white", zorder=4)
        ax.text(cx, cy - 0.22, lines[1], ha="center", va="center",
                fontsize=8, color="white", zorder=4)
        sy = cy + r + 0.18
        ax.text(cx, sy, step_label, ha="center", va="center",
                fontsize=8, color=COLORS["gray"], fontstyle="italic", zorder=4)

    def draw_square(cx, cy, color, label, step_label, alpha=1.0):
        sq = plt.Rectangle((cx - hs, cy - hs), 2*hs, 2*hs,
                            color=color, alpha=alpha, zorder=3)
        ax.add_patch(sq)
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=11, fontweight="bold",
                color="white" if alpha > 0.5 else COLORS["gray"], zorder=4)
        ax.text(cx, cy - hs - 0.2, step_label, ha="center", va="top",
                fontsize=8, color=COLORS["gray"], fontstyle="italic", zorder=4)

    # --- nodes ---
    draw_circle(5.0, 5.8, COLORS["red"],  ["MIN", "v=8"], "(1)")
    draw_circle(2.0, 3.5, COLORS["blue"], ["MAX(L)", "v=8"], "(2)")
    draw_circle(8.0, 3.5, COLORS["blue"], ["MAX(R)", "v=9*"], "(7)")

    # alpha/beta labels beside MAX nodes
    ax.text(0.3, 3.5, "α=-∞\nβ=+∞", ha="left", va="center",
            fontsize=7.5, color=COLORS["gray"], fontstyle="italic", zorder=4)
    # highlighted box beside MAX(R) showing inherited beta
    ax.text(9.9, 3.8, "α=-∞\nβ=8", ha="right", va="center",
            fontsize=8, color=COLORS["orange"], fontweight="bold", zorder=4,
            bbox=dict(boxstyle="round,pad=0.3", fc="#FEF9E7",
                      ec=COLORS["orange"], lw=1.5))

    # --- leaves ---
    draw_square(0.9, 1.4, COLORS["blue"], "8", "(3)")
    draw_square(3.1, 1.4, COLORS["blue"], "6", "(4)")
    draw_square(6.8, 1.4, COLORS["blue"], "9", "(8)")
    draw_square(9.1, 1.4, COLORS["gray"], "?", " ", alpha=0.4)
    ax.text(9.1, 1.4 - hs - 0.35, "PODADO", ha="center", va="top",
            fontsize=8, color=COLORS["red"], fontweight="bold", zorder=4)

    # --- edges ---
    def edge(x1, y1, x2, y2, style="solid", color=dark, alpha=1.0):
        ls = "--" if style == "dashed" else "-"
        ax.annotate("", xy=(x2, y2 + r + 0.02), xytext=(x1, y1 - r - 0.02),
                    arrowprops=dict(arrowstyle="-", color=color,
                                   lw=2, linestyle=ls, alpha=alpha),
                    zorder=2)

    edge(5.0, 5.8, 2.0, 3.5)
    edge(5.0, 5.8, 8.0, 3.5)
    edge(2.0, 3.5, 0.9, 1.4)
    edge(2.0, 3.5, 3.1, 1.4)
    edge(8.0, 3.5, 6.8, 1.4)
    edge(8.0, 3.5, 9.1, 1.4, style="dashed", color=COLORS["gray"], alpha=0.5)
    mid_x = (8.0 + 9.1) / 2
    mid_y = (3.5 - r - 0.02 + 1.4 + hs + 0.02) / 2
    ax.text(mid_x + 0.1, mid_y, "✗", ha="center", va="center",
            fontsize=16, color=COLORS["red"], fontweight="bold", zorder=5)

    # --- annotations ---
    ax.annotate("α=9 ≥ β=8\n→ PODA!", xy=(8.4, 3.05), xytext=(10.0, 2.8),
                fontsize=8.5, color=COLORS["red"],
                arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.5),
                ha="right", va="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="#FDEDEC",
                          ec=COLORS["red"], lw=1.5))
    ax.annotate("β ← 8\n(MIN puede forzar ≤8)", xy=(4.6, 5.4), xytext=(1.0, 5.1),
                fontsize=8.5, color=COLORS["orange"],
                arrowprops=dict(arrowstyle="->", color=COLORS["orange"], lw=1.5),
                ha="left", va="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="#FEF9E7",
                          ec=COLORS["orange"], lw=1.5))
    # level labels at right margin
    ax.text(9.8, 5.8, "MIN", ha="right", va="center",
            fontsize=9, color=COLORS["red"], fontweight="bold")
    ax.text(9.8, 3.5, "MAX", ha="right", va="center",
            fontsize=9, color=COLORS["blue"], fontweight="bold")
    ax.text(9.8, 1.4, "Hoja", ha="right", va="center",
            fontsize=9, color=COLORS["teal"], fontweight="bold")

    # ------------------------------------------------------------------ table
    ax2 = ax_table
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-0.05, 1.05)
    ax2.axis("off")
    ax2.set_facecolor("white")

    col_x = [0.0, 0.08, 0.21, 0.29, 0.37]
    col_widths = [0.08, 0.13, 0.08, 0.08, 0.63]
    headers = ["Paso", "Nodo", "α", "β", "Qué ocurre"]
    row_h = 0.073
    start_y = 0.965

    rows = [
        ("(1)", "MIN(root)",   "-∞", "+∞", "Inicio; llama a MAX(L)"),
        ("(2)", "MAX(L)",      "-∞", "+∞", "Entra con α=-∞, β=+∞"),
        ("(3)", "Hoja 8",      "-∞", "+∞", "Retorna 8 a MAX(L)"),
        ("(4)", "MAX(L)",      "8",  "+∞", "v=8, α←max(-∞,8)=8"),
        ("(5)", "Hoja 6",      "8",  "+∞", "Retorna 6 a MAX(L)"),
        ("(6)", "MAX(L) ←",   "8",  "+∞", "6<v: v queda en 8; retorna 8"),
        ("(7)", "MIN(root)",   "-∞", "8",  "β←min(+∞,8)=8; llama MAX(R)"),
        ("(8)", "MAX(R)",      "-∞", "8",  "Entra con α=-∞, β=8"),
        ("(9)", "Hoja 9",      "-∞", "8",  "Retorna 9 a MAX(R)"),
        ("★",  "MAX(R) PODA", "9",  "8",  "α←9; α=9 ≥ β=8 → PODA! '?' no se explora"),
        (" ",  "MIN(root) ←", "-∞", "8",  "min(8,9)=8; elige rama izquierda"),
    ]

    # header row
    hy = start_y
    for ci, (cx, cw, hdr) in enumerate(zip(col_x, col_widths, headers)):
        rect = plt.Rectangle((cx, hy - row_h), cw, row_h,
                              fc=COLORS["dark"], ec="white", lw=0.5, zorder=2,
                              transform=ax2.transData)
        ax2.add_patch(rect)
        ax2.text(cx + cw / 2, hy - row_h / 2, hdr,
                 ha="center", va="center", fontsize=8, color="white",
                 fontweight="bold", zorder=3)

    for ri, row in enumerate(rows):
        ry = start_y - row_h * (ri + 1)
        is_prune = (ri == 9)
        is_beta = (ri == 6)

        if is_prune:
            bg = "#FDEDEC"
            tc = COLORS["red"]
            fw = "bold"
        elif is_beta:
            bg = "#FEF9E7"
            tc = COLORS["orange"]
            fw = "bold"
        else:
            bg = "#F8F9FA" if ri % 2 == 0 else "white"
            tc = COLORS["dark"]
            fw = "normal"

        for ci, (cx, cw, cell) in enumerate(zip(col_x, col_widths, row)):
            rect = plt.Rectangle((cx, ry - row_h), cw, row_h,
                                  fc=bg, ec="#DEE2E6", lw=0.4, zorder=2,
                                  transform=ax2.transData)
            ax2.add_patch(rect)
            fs = 8 if ci < 4 else 7.5
            ax2.text(cx + cw / 2, ry - row_h / 2, cell,
                     ha="center", va="center", fontsize=fs,
                     color=tc, fontweight=fw, zorder=3)

    # insight box at bottom
    insight = ("β=8: MIN ya puede forzar que MAX obtenga como máximo 8 desde MAX(L).\n"
               "MAX(R) puede ofrecer al menos 9. MIN jamás lo permitiría.\n"
               "El valor de '?' es completamente irrelevante.")
    ax2.text(0.5, 0.04, insight, ha="center", va="center",
             fontsize=9, color=COLORS["dark"],
             transform=ax2.transAxes,
             bbox=dict(boxstyle="round,pad=0.5", fc="#EBF5FB",
                       ec=COLORS["blue"], lw=1.5))

    fig.tight_layout()
    _save(fig, "15_beta_cutoff_example.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Generate all 15 images for the adversarial search module."""
    plot_single_vs_adversarial()
    plot_tictactoe_anatomy()
    plot_nim_rules_and_tree()
    plot_game_taxonomy()
    plot_payoff_matrices()
    plot_nim_complete_tree()
    plot_minimax_step_by_step()
    plot_alphabeta_nim23()
    plot_alphabeta_vs_minimax()
    plot_tictactoe_endgame()
    plot_nim_xor_pattern()
    plot_depth_limit_eval()
    plot_chess_complexity()
    plot_alpha_cutoff_example()
    plot_beta_cutoff_example()


if __name__ == "__main__":
    main()
