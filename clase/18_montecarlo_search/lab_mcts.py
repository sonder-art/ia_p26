#!/usr/bin/env python3
"""
Laboratorio: Monte Carlo Tree Search (imágenes para las notas)

Uso:
    cd clase/18_montecarlo_search
    python3 lab_mcts.py

Genera ~18 imágenes en:
    clase/18_montecarlo_search/images/

Dependencias: numpy, matplotlib
"""

from pathlib import Path
import math
import copy
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import RegularPolygon
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

# Player colors
BLACK_COLOR = COLORS["dark"]
WHITE_COLOR = "#FFFFFF"
EMPTY_COLOR = "#F5F0E1"
HIGHLIGHT_COLOR = COLORS["orange"]
WIN_PATH_COLOR = COLORS["green"]
NEIGHBOR_COLOR = COLORS["teal"]

ROOT = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

np.random.seed(42)
random.seed(42)


def _save(fig, name: str) -> None:
    out = IMAGES_DIR / name
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"✓  {out.name}")


# ---------------------------------------------------------------------------
# Hex game engine
# ---------------------------------------------------------------------------

class Hex:
    """Hex game with offset coordinates. Player 1=Black, 2=White."""

    NEIGHBORS = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]

    def __init__(self, size=7, board=None, current_player=1):
        self.size = size
        if board is not None:
            self.board = [row[:] for row in board]
        else:
            self.board = [[0] * size for _ in range(size)]
        self.current_player = current_player

    def actions(self):
        return [(r, c) for r in range(self.size)
                for c in range(self.size) if self.board[r][c] == 0]

    def result(self, action):
        new = Hex(self.size, self.board, 3 - self.current_player)
        r, c = action
        new.board[r][c] = self.current_player
        return new

    def is_terminal(self):
        return self._has_path(1) or self._has_path(2) or not self.actions()

    def utility(self, player):
        if self._has_path(player):
            return 1
        if self._has_path(3 - player):
            return -1
        return 0

    def _has_path(self, player):
        n = self.size
        if player == 1:
            start = [(0, c) for c in range(n) if self.board[0][c] == 1]
            goal_fn = lambda r, c: r == n - 1
        else:
            start = [(r, 0) for r in range(n) if self.board[r][0] == 2]
            goal_fn = lambda r, c: c == n - 1
        visited = set()
        queue = list(start)
        for pos in queue:
            if pos in visited:
                continue
            visited.add(pos)
            r, c = pos
            if goal_fn(r, c):
                return True
            for dr, dc in self.NEIGHBORS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and self.board[nr][nc] == player:
                    queue.append((nr, nc))
        return False

    def get_winning_path(self, player):
        """Return the winning path as a list of (r, c) or empty list."""
        n = self.size
        if player == 1:
            start = [(0, c) for c in range(n) if self.board[0][c] == 1]
            goal_fn = lambda r, c: r == n - 1
        else:
            start = [(r, 0) for r in range(n) if self.board[r][0] == 2]
            goal_fn = lambda r, c: c == n - 1
        visited = {}
        queue = list(start)
        for s in start:
            visited[s] = None
        i = 0
        while i < len(queue):
            pos = queue[i]
            i += 1
            r, c = pos
            if goal_fn(r, c):
                path = []
                cur = pos
                while cur is not None:
                    path.append(cur)
                    cur = visited[cur]
                return path
            for dr, dc in self.NEIGHBORS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < n and 0 <= nc < n
                        and self.board[nr][nc] == player
                        and (nr, nc) not in visited):
                    visited[(nr, nc)] = pos
                    queue.append((nr, nc))
        return []


# ---------------------------------------------------------------------------
# MCTS engine
# ---------------------------------------------------------------------------

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = {}
        self.N = 0
        self.Q = 0.0
        self.unexpanded = list(state.actions())
        random.shuffle(self.unexpanded)


def _uct_value(child, parent_n, c):
    if child.N == 0:
        return float('inf')
    return child.Q / child.N + c * math.sqrt(math.log(parent_n) / child.N)


def _run_mcts(state, iterations, player, c=1.41):
    """Run MCTS with UCT, return (best_action, root_node)."""
    root = MCTSNode(state)
    for _ in range(iterations):
        node = root
        # Selection
        while not node.unexpanded and node.children:
            node = max(node.children.values(),
                       key=lambda ch: _uct_value(ch, node.N, c))
        # Expansion
        if node.unexpanded:
            action = node.unexpanded.pop()
            child_state = node.state.result(action)
            child = MCTSNode(child_state, parent=node)
            node.children[action] = child
            node = child
        # Simulation
        sim = Hex(node.state.size, node.state.board, node.state.current_player)
        while not sim.is_terminal():
            acts = sim.actions()
            a = acts[random.randint(0, len(acts) - 1)]
            sim = sim.result(a)
        reward = sim.utility(player)
        # Backpropagation
        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent

    if not root.children:
        return root.state.actions()[0], root
    best = max(root.children, key=lambda a: root.children[a].N)
    return best, root


def _run_mcts_naive(state, iterations, player):
    """MCTS with greedy selection (no exploration bonus)."""
    root = MCTSNode(state)
    for _ in range(iterations):
        node = root
        while not node.unexpanded and node.children:
            node = max(node.children.values(),
                       key=lambda ch: (ch.Q / ch.N if ch.N > 0 else float('inf')))
        if node.unexpanded:
            action = node.unexpanded.pop()
            child_state = node.state.result(action)
            child = MCTSNode(child_state, parent=node)
            node.children[action] = child
            node = child
        sim = Hex(node.state.size, node.state.board, node.state.current_player)
        while not sim.is_terminal():
            acts = sim.actions()
            sim = sim.result(acts[random.randint(0, len(acts) - 1)])
        reward = sim.utility(player)
        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
    if not root.children:
        return root.state.actions()[0], root
    best = max(root.children, key=lambda a: root.children[a].N)
    return best, root


def _play_game(size, agent1_fn, agent2_fn):
    """Play a game, return 1 if player 1 wins, 2 if player 2 wins."""
    state = Hex(size)
    while not state.is_terminal():
        if state.current_player == 1:
            action = agent1_fn(state, 1)
        else:
            action = agent2_fn(state, 2)
        state = state.result(action)
    if state.utility(1) == 1:
        return 1
    return 2


def _random_agent(state, player):
    acts = state.actions()
    return acts[random.randint(0, len(acts) - 1)]


def _mcts_agent(iterations, c=1.41):
    def agent(state, player):
        a, _ = _run_mcts(state, iterations, player, c)
        return a
    return agent


def _minimax(state, player, depth=99):
    """Simple minimax for small boards.  Returns value from `player`'s perspective."""
    if state.is_terminal() or depth == 0:
        return state.utility(player), None
    is_maximizing = (state.current_player == player)
    best_val = -2 if is_maximizing else 2
    best_act = None
    for a in state.actions():
        val, _ = _minimax(state.result(a), player, depth - 1)
        if is_maximizing and val > best_val:
            best_val = val
            best_act = a
        elif not is_maximizing and val < best_val:
            best_val = val
            best_act = a
    return best_val, best_act


def _alphabeta_agent(depth=3):
    """Alpha-beta agent with simple distance-based eval."""
    def _eval(state, player):
        # Heuristic: how close is player to connecting?
        n = state.size
        if state._has_path(player):
            return 100
        if state._has_path(3 - player):
            return -100
        # Count min distance from each side for each player
        score = 0
        for p, sign in [(player, 1), (3 - player, -1)]:
            # BFS from starting edge
            if p == 1:
                starts = [(0, c) for c in range(n) if state.board[0][c] != (3 - p)]
                goal_fn = lambda r, c: r == n - 1
            else:
                starts = [(r, 0) for r in range(n) if state.board[r][0] != (3 - p)]
                goal_fn = lambda r, c: c == n - 1
            # Simple: count player stones on shortest potential path
            own_count = sum(1 for r in range(n) for c in range(n)
                           if state.board[r][c] == p)
            score += sign * own_count
        return score

    def _ab(state, player, depth_left, alpha, beta, maximizing):
        if state.is_terminal() or depth_left == 0:
            return _eval(state, player), None
        best_act = None
        if maximizing:
            val = -200
            for a in state.actions():
                child = state.result(a)
                v, _ = _ab(child, player, depth_left - 1, alpha, beta, False)
                if v > val:
                    val = v
                    best_act = a
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            return val, best_act
        else:
            val = 200
            for a in state.actions():
                child = state.result(a)
                v, _ = _ab(child, player, depth_left - 1, alpha, beta, True)
                if v < val:
                    val = v
                    best_act = a
                beta = min(beta, val)
                if alpha >= beta:
                    break
            return val, best_act

    def agent(state, player):
        _, act = _ab(state, player, depth, -200, 200, True)
        if act is None:
            acts = state.actions()
            act = acts[0] if acts else None
        return act
    return agent


# ---------------------------------------------------------------------------
# Hex board drawing helper
# ---------------------------------------------------------------------------

def _hex_to_pixel(r, c, hex_size=1.0):
    """Convert offset hex coordinates to pixel coordinates."""
    x = hex_size * 1.5 * c + hex_size * 0.75 * r
    y = -hex_size * math.sqrt(3) * (r + 0.5 * (c % 2 == 1) * 0) - hex_size * math.sqrt(3) / 2 * r
    # Simpler: offset coordinates
    x = c * 1.5 + r * 0.75
    y = -(r * math.sqrt(3) * 0.5 + c * 0.0)
    # Actually use axial-like offset:
    x = c + r * 0.5
    y = -r * math.sqrt(3) / 2
    return x, y


def _draw_hex_board(ax, board, size, hex_size=0.55,
                    highlights=None, win_path=None, neighbor_cell=None,
                    show_coords=False, edge_labels=True):
    """Draw a hex board on the given axes.

    board: 2D list (size x size), values 0=empty, 1=black, 2=white
    highlights: set of (r,c) to highlight (e.g. legal moves)
    win_path: list of (r,c) for winning path highlight
    neighbor_cell: (r,c) to highlight neighbors of
    """
    if highlights is None:
        highlights = set()
    if win_path is None:
        win_path = []
    win_set = set(win_path)

    for r in range(size):
        for c in range(size):
            x, y = _hex_to_pixel(r, c)

            # Determine fill color
            val = board[r][c]
            if (r, c) in win_set:
                fc = WIN_PATH_COLOR
            elif (r, c) in highlights:
                fc = HIGHLIGHT_COLOR
            elif val == 1:
                fc = BLACK_COLOR
            elif val == 2:
                fc = WHITE_COLOR
            else:
                fc = EMPTY_COLOR

            # Edge color for neighbor highlight
            ec = COLORS["dark"]
            lw = 1.0
            if neighbor_cell is not None:
                nr, nc = neighbor_cell
                if (r, c) == (nr, nc):
                    ec = COLORS["red"]
                    lw = 3.0
                elif _is_neighbor(r, c, nr, nc):
                    ec = NEIGHBOR_COLOR
                    lw = 2.5

            hex_patch = RegularPolygon((x, y), numVertices=6, radius=hex_size,
                                       orientation=0, facecolor=fc,
                                       edgecolor=ec, linewidth=lw)
            ax.add_patch(hex_patch)

            if show_coords:
                ax.text(x, y, f"({r},{c})", ha='center', va='center',
                        fontsize=7, color=COLORS["gray"])

    # Edge labels
    if edge_labels:
        # Top edge (Black)
        mid_c = (size - 1) / 2
        x_top, y_top = _hex_to_pixel(-0.8, mid_c)
        ax.text(x_top, y_top, "Negro ↕", ha='center', va='center',
                fontsize=10, fontweight='bold', color=BLACK_COLOR)
        # Bottom edge (Black)
        x_bot, y_bot = _hex_to_pixel(size - 0.2, mid_c)
        ax.text(x_bot, y_bot, "Negro ↕", ha='center', va='center',
                fontsize=10, fontweight='bold', color=BLACK_COLOR)
        # Left edge (White)
        mid_r = (size - 1) / 2
        x_left, y_left = _hex_to_pixel(mid_r, -0.9)
        ax.text(x_left, y_left, "Blanco\n↔", ha='center', va='center',
                fontsize=10, fontweight='bold', color=COLORS["gray"])
        # Right edge (White)
        x_right, y_right = _hex_to_pixel(mid_r, size - 0.1)
        ax.text(x_right, y_right, "Blanco\n↔", ha='center', va='center',
                fontsize=10, fontweight='bold', color=COLORS["gray"])

    ax.set_aspect('equal')
    ax.axis('off')
    # Set limits
    all_x = [_hex_to_pixel(r, c)[0] for r in range(size) for c in range(size)]
    all_y = [_hex_to_pixel(r, c)[1] for r in range(size) for c in range(size)]
    margin = 1.5
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)


def _is_neighbor(r1, c1, r2, c2):
    for dr, dc in Hex.NEIGHBORS:
        if r1 + dr == r2 and c1 + dc == c2:
            return True
    return False


# ---------------------------------------------------------------------------
# Plot functions: Hex board figures (01-06)
# ---------------------------------------------------------------------------

def plot_01_hex_empty_board():
    """Empty 7x7 hex board with edge labels."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    board = [[0] * 7 for _ in range(7)]
    _draw_hex_board(ax, board, 7, show_coords=True)
    ax.set_title("Tablero de Hex 7×7 vacío", fontsize=14, fontweight='bold')
    _save(fig, "01_hex_empty_board.png")


def plot_02_hex_neighbors():
    """Show neighbors of a central cell."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 7))
    size = 5
    board = [[0] * size for _ in range(size)]
    _draw_hex_board(ax, board, size, neighbor_cell=(2, 2),
                    show_coords=True, edge_labels=False)
    ax.set_title("Los 6 vecinos de la celda (2,2)", fontsize=14, fontweight='bold')
    _save(fig, "02_hex_neighbors.png")


def plot_03_hex_legal_moves():
    """Mid-game board with legal moves highlighted."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    size = 7
    board = [[0] * size for _ in range(size)]
    # Place some stones for a mid-game position
    black_moves = [(0, 3), (1, 2), (1, 3), (2, 2), (3, 1), (3, 3), (4, 2)]
    white_moves = [(0, 5), (1, 5), (2, 4), (2, 5), (3, 4), (4, 4), (4, 5)]
    for r, c in black_moves:
        board[r][c] = 1
    for r, c in white_moves:
        board[r][c] = 2
    # Legal moves = empty cells
    legal = set()
    for r in range(size):
        for c in range(size):
            if board[r][c] == 0:
                legal.add((r, c))
    _draw_hex_board(ax, board, size, highlights=legal)
    ax.set_title("Posición a mitad de partida — celdas legales resaltadas",
                 fontsize=13, fontweight='bold')
    _save(fig, "03_hex_legal_moves.png")


def plot_04_hex_winning_path():
    """Completed game with winning path highlighted."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    size = 7
    # Play a scripted game where Black wins
    board = [[0] * size for _ in range(size)]
    black_path = [(0, 3), (1, 2), (2, 2), (3, 2), (4, 1), (5, 1), (6, 0)]
    other_black = [(0, 0), (1, 5), (3, 5), (5, 4)]
    white_stones = [(0, 4), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
                    (0, 6), (2, 5), (4, 5)]
    for r, c in black_path + other_black:
        board[r][c] = 1
    for r, c in white_stones:
        board[r][c] = 2
    _draw_hex_board(ax, board, size, win_path=black_path)
    ax.set_title("Negro gana — cadena conectada de arriba a abajo",
                 fontsize=13, fontweight='bold')
    _save(fig, "04_hex_winning_path.png")


def plot_05_hex_3x3_games():
    """Two completed 3x3 games side by side."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Game 1: Black wins (top row → bottom row via diagonal path)
    # B placed at (0,1), (1,1), (2,0) — connected chain from row 0 to row 2
    b1 = [[2, 1, 0],
           [0, 1, 2],
           [1, 0, 0]]
    win1 = [(0, 1), (1, 1), (2, 0)]
    _draw_hex_board(ax1, b1, 3, win_path=win1, edge_labels=True)
    ax1.set_title("Negro gana (arriba → abajo)", fontsize=12, fontweight='bold')

    # Game 2: White wins (left col → right col via middle row)
    # W placed at (1,0), (1,1), (1,2) — connected chain from col 0 to col 2
    b2 = [[1, 0, 1],
           [2, 2, 2],
           [0, 1, 0]]
    win2 = [(1, 0), (1, 1), (1, 2)]
    _draw_hex_board(ax2, b2, 3, win_path=win2, edge_labels=True)
    ax2.set_title("Blanco gana (izquierda → derecha)", fontsize=12, fontweight='bold')

    fig.suptitle("Hex 3×3: dos partidas completas", fontsize=14, fontweight='bold')
    _save(fig, "05_hex_3x3_games.png")


def plot_06_hex_strategy():
    """Strategy patterns: bridge, ladder."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Bridge pattern
    b_bridge = [[0]*5 for _ in range(5)]
    b_bridge[2][1] = 1
    b_bridge[2][3] = 1
    bridge_highlight = {(1, 2), (2, 2)}  # the two connecting cells
    _draw_hex_board(axes[0], b_bridge, 5, hex_size=0.5,
                    highlights=bridge_highlight, edge_labels=False)
    axes[0].set_title("Puente (bridge)", fontsize=11, fontweight='bold')

    # Ladder pattern
    b_ladder = [[0]*5 for _ in range(5)]
    b_ladder[0][2] = 1
    b_ladder[1][2] = 1
    b_ladder[2][1] = 1
    b_ladder[3][1] = 1
    b_ladder[4][0] = 1
    _draw_hex_board(axes[1], b_ladder, 5, hex_size=0.5, edge_labels=False)
    axes[1].set_title("Escalera (ladder)", fontsize=11, fontweight='bold')

    # Corner control
    b_corner = [[0]*5 for _ in range(5)]
    b_corner[0][0] = 1
    b_corner[0][4] = 1
    b_corner[4][0] = 1
    b_corner[4][4] = 1
    corner_hl = {(0, 0), (0, 4), (4, 0), (4, 4)}
    _draw_hex_board(axes[2], b_corner, 5, hex_size=0.5,
                    highlights=corner_hl, edge_labels=False)
    axes[2].set_title("Control de esquinas", fontsize=11, fontweight='bold')

    fig.suptitle("Patrones estratégicos en Hex", fontsize=14, fontweight='bold')
    _save(fig, "06_hex_strategy.png")


# ---------------------------------------------------------------------------
# Plot functions: MCTS algorithm figures (07-09)
# ---------------------------------------------------------------------------

def plot_07_mcts_four_phases():
    """Diagram showing the four MCTS phases."""
    fig, axes = plt.subplots(1, 4, figsize=(16, 5))
    phase_names = ["1. Selección", "2. Expansión", "3. Simulación", "4. Retropropagación"]
    phase_colors = [COLORS["blue"], COLORS["green"], COLORS["orange"], COLORS["purple"]]
    phase_desc = [
        "Bajar por el árbol\nusando UCT",
        "Añadir un\nnodo nuevo",
        "Rollout aleatorio\nhasta terminal",
        "Actualizar N y Q\nhacia la raíz"
    ]

    for i, ax in enumerate(axes):
        # Draw a simple tree
        nodes = [(0.5, 0.9), (0.3, 0.6), (0.7, 0.6),
                 (0.15, 0.3), (0.45, 0.3), (0.55, 0.3), (0.85, 0.3)]
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]

        for p, ch in edges:
            ax.plot([nodes[p][0], nodes[ch][0]], [nodes[p][1], nodes[ch][1]],
                    'k-', linewidth=1, alpha=0.3)

        for j, (x, y) in enumerate(nodes):
            color = COLORS["light"]
            if i == 0 and j in [0, 1, 3]:  # selection path
                color = phase_colors[i]
            elif i == 1 and j == 4:  # new node
                color = phase_colors[i]
            elif i == 3 and j in [0, 1, 4]:  # backprop path
                color = phase_colors[i]
            ax.plot(x, y, 'o', markersize=18, color=color,
                    markeredgecolor=COLORS["dark"], markeredgewidth=1.5)

        if i == 0:  # Selection arrow
            ax.annotate('', xy=(0.15, 0.32), xytext=(0.5, 0.88),
                        arrowprops=dict(arrowstyle='->', color=phase_colors[i],
                                       lw=2.5))
        elif i == 1:  # New node
            ax.plot(0.45, 0.3, 'o', markersize=18, color=phase_colors[i],
                    markeredgecolor=COLORS["dark"], markeredgewidth=2)
            ax.text(0.45, 0.15, "nuevo", ha='center', fontsize=8, color=phase_colors[i])
        elif i == 2:  # Rollout squiggly line
            xs = np.linspace(0.45, 0.45, 10)
            ys = np.linspace(0.28, 0.05, 10)
            xs = xs + np.random.uniform(-0.05, 0.05, 10)
            ax.plot(xs, ys, '--', color=phase_colors[i], linewidth=2)
            ax.text(0.45, 0.0, "terminal", ha='center', fontsize=8,
                    color=phase_colors[i])
        elif i == 3:  # Backprop arrow
            ax.annotate('', xy=(0.5, 0.88), xytext=(0.45, 0.32),
                        arrowprops=dict(arrowstyle='->', color=phase_colors[i],
                                       lw=2.5))

        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.1, 1.05)
        ax.set_title(phase_names[i], fontsize=11, fontweight='bold',
                     color=phase_colors[i])
        ax.text(0.5, -0.07, phase_desc[i], ha='center', va='top',
                fontsize=9, color=COLORS["gray"])
        ax.axis('off')

    fig.suptitle("Las cuatro fases de MCTS", fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    _save(fig, "07_mcts_four_phases.png")


def plot_08_mcts_tree_growth():
    """Tree size after 10, 50, 200 iterations on Hex 3x3."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    iters_list = [10, 50, 200]

    for idx, iters in enumerate(iters_list):
        random.seed(42)
        state = Hex(3)
        _, root = _run_mcts(state, iters, 1, c=1.41)

        # Count tree stats
        def _count(node, depth=0):
            total = 1
            max_d = depth
            for ch in node.children.values():
                t, d = _count(ch, depth + 1)
                total += t
                max_d = max(max_d, d)
            return total, max_d

        total_nodes, max_depth = _count(root)

        # Draw simple bar chart of root children visits
        actions = sorted(root.children.keys())
        visits = [root.children[a].N for a in actions]
        values = [root.children[a].Q / root.children[a].N if root.children[a].N > 0 else 0
                  for a in actions]
        labels = [f"({r},{c})" for r, c in actions]

        colors = [COLORS["blue"] if v > 0 else COLORS["red"] for v in values]
        axes[idx].bar(range(len(actions)), visits, color=colors, alpha=0.8,
                      edgecolor=COLORS["dark"])
        axes[idx].set_xticks(range(len(actions)))
        axes[idx].set_xticklabels(labels, rotation=45, fontsize=8)
        axes[idx].set_ylabel("Visitas N(v)")
        axes[idx].set_title(f"M = {iters} iteraciones\n({total_nodes} nodos, "
                           f"prof. máx. {max_depth})",
                           fontsize=11, fontweight='bold')

    fig.suptitle("Crecimiento del árbol MCTS en Hex 3×3",
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    _save(fig, "08_mcts_tree_growth.png")


def plot_09_mcts_trace():
    """Visual trace of MCTS iterations."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    random.seed(42)
    state = Hex(3)

    # Run 30 iterations and track root children stats
    iterations = 30
    root = MCTSNode(state)
    history = {a: [] for a in state.actions()}

    for it in range(1, iterations + 1):
        node = root
        while not node.unexpanded and node.children:
            node = max(node.children.values(),
                       key=lambda ch: _uct_value(ch, node.N, 1.41))
        if node.unexpanded:
            action = node.unexpanded.pop()
            child_state = node.state.result(action)
            child = MCTSNode(child_state, parent=node)
            node.children[action] = child
            node = child
        sim = Hex(node.state.size, node.state.board, node.state.current_player)
        while not sim.is_terminal():
            acts = sim.actions()
            sim = sim.result(acts[random.randint(0, len(acts) - 1)])
        reward = sim.utility(1)
        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent

        for a in state.actions():
            if a in root.children:
                history[a].append(root.children[a].N)
            else:
                history[a].append(0)

    # Plot visit counts over iterations
    color_cycle = [COLORS["blue"], COLORS["red"], COLORS["green"],
                   COLORS["orange"], COLORS["purple"], COLORS["teal"],
                   COLORS["pink"], COLORS["gray"], COLORS["dark"]]
    for i, a in enumerate(sorted(history.keys())):
        ax.plot(range(1, iterations + 1), history[a],
                label=f"({a[0]},{a[1]})", color=color_cycle[i % len(color_cycle)],
                linewidth=2, alpha=0.8)

    ax.set_xlabel("Iteración", fontsize=12)
    ax.set_ylabel("Visitas acumuladas N(v)", fontsize=12)
    ax.set_title("Traza MCTS: visitas a cada acción de la raíz (Hex 3×3)",
                 fontsize=13, fontweight='bold')
    ax.legend(ncol=3, fontsize=9, title="Acción", title_fontsize=10)
    _save(fig, "09_mcts_trace.png")


# ---------------------------------------------------------------------------
# Plot functions: UCT figures (10-11)
# ---------------------------------------------------------------------------

def plot_10_uct_vs_uniform():
    """Compare UCT vs naive selection on Hex 3x3, with minimax ground truth."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Minimax ground truth for Hex 3x3 first move (precomputed)
    # +1 = winning for Black (player 1), -1 = losing
    minimax_val = {
        (0, 0): -1, (0, 1): -1, (0, 2): +1,
        (1, 0): +1, (1, 1): +1, (1, 2): +1,
        (2, 0): +1, (2, 1): -1, (2, 2): -1,
    }

    for ax, title, runner in [
        (ax1, "Naive (mayor Q/N)", lambda s, it, p: _run_mcts_naive(s, it, p)),
        (ax2, "UCT (c = $\\sqrt{2}$)", lambda s, it, p: _run_mcts(s, it, p, c=1.41))
    ]:
        random.seed(42)
        state = Hex(3)
        _, root = runner(state, 500, 1)
        actions = sorted(root.children.keys())
        visits = [root.children[a].N for a in actions]
        qn = [root.children[a].Q / root.children[a].N if root.children[a].N > 0 else 0
              for a in actions]
        labels = [f"({r},{c})" for r, c in actions]

        # Color by minimax ground truth: green=winning, red=losing
        colors = [COLORS["green"] if minimax_val[a] == 1 else COLORS["red"]
                  for a in actions]
        bars = ax.bar(range(len(actions)), visits, color=colors, alpha=0.75,
                      edgecolor=COLORS["dark"], linewidth=0.8)
        ax.set_xticks(range(len(actions)))
        ax.set_xticklabels(labels, rotation=45, fontsize=9)
        ax.set_ylabel("Visitas N(v)", fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')

        # Annotate Q/N on top of each bar
        max_v = max(visits) if visits else 1
        for j, (v, q) in enumerate(zip(visits, qn)):
            ax.text(j, v + max_v * 0.02, f"Q/N={q:+.2f}",
                    ha='center', fontsize=7.5, color=COLORS["dark"])

    # Legend (shared)
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS["green"], alpha=0.75, edgecolor=COLORS["dark"],
              label='Minimax ganadora (+1)'),
        Patch(facecolor=COLORS["red"], alpha=0.75, edgecolor=COLORS["dark"],
              label='Minimax perdedora (-1)'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=2,
               fontsize=10, frameon=True, bbox_to_anchor=(0.5, -0.02))

    fig.suptitle("UCT vs Naive — 500 iteraciones en Hex 3$\\times$3\n"
                 "(colores = valor minimax real de cada primer movimiento)",
                 fontsize=13, fontweight='bold')
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    _save(fig, "10_uct_vs_uniform.png")


def plot_11_uct_c_effect():
    """Win rate vs exploration constant c — MCTS vs alpha-beta on Hex 5x5."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    c_values = [0.01, 0.1, 0.25, 0.5, 0.75, 1.0, 1.41, 2.0, 3.0, 5.0, 10.0]
    n_games = 50
    iters_per_move = 100
    ab_agent = _alphabeta_agent(3)
    win_rates = []

    for c in c_values:
        wins = 0
        for g in range(n_games):
            # Alternate who plays first for fairness
            random.seed(g * 100 + int(c * 100))
            if g % 2 == 0:
                result = _play_game(5, _mcts_agent(iters_per_move, c), ab_agent)
                if result == 1:
                    wins += 1
            else:
                result = _play_game(5, ab_agent, _mcts_agent(iters_per_move, c))
                if result == -1:
                    wins += 1
        win_rates.append(wins / n_games)
        print(f"  c={c:.2f}: {wins}/{n_games} wins vs alpha-beta")

    ax.plot(c_values, win_rates, 'o-', color=COLORS["blue"], linewidth=2.5,
            markersize=8, markerfacecolor=COLORS["blue"])
    ax.axvline(x=1.41, color=COLORS["red"], linestyle='--', alpha=0.7,
               label="$c = \\sqrt{2} \\approx 1.41$")
    ax.set_xlabel("Constante de exploración $c$", fontsize=12)
    ax.set_ylabel("Tasa de victorias vs Alpha-beta (d=3)", fontsize=12)
    ax.set_title("Efecto de $c$ en MCTS con UCT (Hex 5$\\times$5, 100 iter/mov, vs Alpha-beta)",
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.set_ylim(0, 1.05)
    _save(fig, "11_uct_c_effect.png")


# ---------------------------------------------------------------------------
# Plot functions: Experiment figures (12-15)
# ---------------------------------------------------------------------------

def plot_12_mcts_vs_minimax_3x3():
    """MCTS convergence to minimax-optimal action on Hex 3x3."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    state = Hex(3)
    # Minimax ground truth: which first moves are winning for Black?
    winning_moves = set()
    for a in state.actions():
        child = state.result(a)
        val, _ = _minimax(child, 1)
        if val == 1:  # Black still wins with optimal play → winning first move
            winning_moves.add(a)

    # Run MCTS with increasing iterations, track if chosen action is winning
    iter_values = [5, 10, 20, 50, 100, 200, 500, 1000, 2000]
    n_trials = 60
    correct_rate = []

    for it in iter_values:
        correct = 0
        for trial in range(n_trials):
            random.seed(trial * 7 + it)
            _, root = _run_mcts(state, it, 1, c=1.41)
            if root.children:
                best_a = max(root.children, key=lambda a: root.children[a].N)
                if best_a in winning_moves:
                    correct += 1
        rate = correct / n_trials
        correct_rate.append(rate)
        print(f"  M={it:4d}: {correct}/{n_trials} = {rate:.1%} pick winning move")

    ax.plot(iter_values, correct_rate, 'o-', color=COLORS["blue"],
            linewidth=2.5, markersize=8, markerfacecolor=COLORS["blue"],
            label="MCTS con UCT")
    ax.axhline(y=1.0, color=COLORS["green"], linestyle='--', linewidth=2,
               alpha=0.7, label="Ideal (siempre elige ganadora)")
    ax.axhline(y=5/9, color=COLORS["gray"], linestyle=':', linewidth=1.5,
               alpha=0.7, label=f"Azar (5/9 = {5/9:.1%} ganadoras)")
    ax.set_xscale('log')
    ax.set_xlabel("Iteraciones M", fontsize=12)
    ax.set_ylabel("Fracción de veces que elige un movimiento ganador", fontsize=12)
    ax.set_title("Convergencia de MCTS a la acción minimax-óptima (Hex 3$\\times$3)",
                 fontsize=13, fontweight='bold')
    ax.set_ylim(-0.05, 1.1)
    ax.legend(fontsize=10, loc='lower right')
    _save(fig, "12_mcts_vs_minimax_3x3.png")


def plot_13_tournament_results():
    """Tournament results: MCTS vs alpha-beta vs random on Hex 5x5."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    agents = {
        "MCTS (UCT)": _mcts_agent(300, 1.41),
        "Alpha-beta (d=3)": _alphabeta_agent(3),
        "Aleatorio": _random_agent,
    }
    agent_names = list(agents.keys())
    n_games = 20  # per matchup per side
    results = {name: 0 for name in agent_names}

    print("  Torneo en Hex 5×5...")
    for i, name1 in enumerate(agent_names):
        for j, name2 in enumerate(agent_names):
            if i >= j:
                continue
            wins1, wins2 = 0, 0
            for g in range(n_games):
                random.seed(g * 31 + i * 7 + j * 13)
                r = _play_game(5, agents[name1], agents[name2])
                if r == 1:
                    wins1 += 1
                else:
                    wins2 += 1
            for g in range(n_games):
                random.seed(g * 31 + i * 7 + j * 13 + 1000)
                r = _play_game(5, agents[name2], agents[name1])
                if r == 1:
                    wins2 += 1
                else:
                    wins1 += 1
            results[name1] += wins1
            results[name2] += wins2
            print(f"    {name1} vs {name2}: {wins1}-{wins2}")

    # Bar chart
    colors_bar = [COLORS["blue"], COLORS["orange"], COLORS["gray"]]
    bars = ax.bar(agent_names, [results[n] for n in agent_names],
                  color=colors_bar, edgecolor=COLORS["dark"], alpha=0.85)
    for bar, name in zip(bars, agent_names):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                str(results[name]), ha='center', fontsize=12, fontweight='bold')
    ax.set_ylabel("Victorias totales", fontsize=12)
    ax.set_title("Torneo round-robin en Hex 5×5", fontsize=14, fontweight='bold')
    _save(fig, "13_tournament_results.png")


def plot_14_iteration_budget():
    """Win rate vs iteration budget on Hex 5x5."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    budgets = [50, 100, 200, 500, 1000]
    n_games = 30
    wr_vs_random = []
    wr_vs_ab = []

    ab_agent = _alphabeta_agent(3)

    for budget in budgets:
        wins_r, wins_ab = 0, 0
        for g in range(n_games):
            random.seed(g * 17)
            if _play_game(5, _mcts_agent(budget), _random_agent) == 1:
                wins_r += 1
            random.seed(g * 17 + 5000)
            if _play_game(5, _mcts_agent(budget), ab_agent) == 1:
                wins_ab += 1
        wr_vs_random.append(wins_r / n_games)
        wr_vs_ab.append(wins_ab / n_games)
        print(f"  budget={budget}: vs_random={wins_r}/{n_games}, vs_ab={wins_ab}/{n_games}")

    ax.plot(budgets, wr_vs_random, 'o-', color=COLORS["green"], linewidth=2.5,
            markersize=8, label="vs Aleatorio")
    ax.plot(budgets, wr_vs_ab, 's-', color=COLORS["red"], linewidth=2.5,
            markersize=8, label="vs Alpha-beta (d=3)")
    ax.set_xlabel("Iteraciones por movimiento", fontsize=12)
    ax.set_ylabel("Tasa de victorias MCTS", fontsize=12)
    ax.set_title("Calidad de MCTS vs presupuesto de iteraciones (Hex 5×5)",
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.set_ylim(0, 1.05)
    _save(fig, "14_iteration_budget.png")


def plot_15_asymmetric_tree():
    """Visualize asymmetric MCTS tree as visit distribution."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    random.seed(42)
    state = Hex(5)
    _, root = _run_mcts(state, 1000, 1, c=1.41)

    # Get depth-1 children sorted by visits
    actions = sorted(root.children.keys(), key=lambda a: root.children[a].N, reverse=True)
    visits = [root.children[a].N for a in actions]
    labels = [f"({r},{c})" for r, c in actions]

    # Color by Q/N value
    qn_vals = [root.children[a].Q / root.children[a].N if root.children[a].N > 0 else 0
               for a in actions]
    norm = plt.Normalize(vmin=min(qn_vals) - 0.1, vmax=max(qn_vals) + 0.1)
    cmap = plt.cm.RdYlGn
    colors_mapped = [cmap(norm(v)) for v in qn_vals]

    bars = ax.bar(range(len(actions)), visits, color=colors_mapped,
                  edgecolor=COLORS["dark"], alpha=0.85)
    ax.set_xticks(range(len(actions)))
    ax.set_xticklabels(labels, rotation=60, fontsize=8)
    ax.set_ylabel("Visitas N(v)", fontsize=12)
    ax.set_xlabel("Acción desde la raíz", fontsize=12)
    ax.set_title("Árbol asimétrico: distribución de visitas (Hex 5×5, 1000 iter.)",
                 fontsize=13, fontweight='bold')
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.8)
    cbar.set_label("Q/N (tasa de éxito)", fontsize=10)
    _save(fig, "15_asymmetric_tree.png")


# ---------------------------------------------------------------------------
# Plot functions: AlphaZero figures (16-17)
# ---------------------------------------------------------------------------

def plot_16_algorithm_evolution():
    """Timeline of game AI evolution."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 5))

    systems = [
        (1997, "Deep Blue", "Alpha-beta\n+ eval manual", COLORS["gray"]),
        (2008, "Stockfish", "Alpha-beta\n+ NNUE", COLORS["blue"]),
        (2016, "AlphaGo", "MCTS\n+ redes (datos\nhumanos)", COLORS["green"]),
        (2018, "AlphaZero", "MCTS\n+ red (auto-\njuego)", COLORS["orange"]),
    ]

    for year, name, desc, color in systems:
        ax.plot(year, 0.5, 'o', markersize=25, color=color,
                markeredgecolor=COLORS["dark"], markeredgewidth=2, zorder=5)
        ax.text(year, 0.8, name, ha='center', va='bottom',
                fontsize=13, fontweight='bold', color=color)
        ax.text(year, 0.15, desc, ha='center', va='top',
                fontsize=9, color=COLORS["dark"])
        ax.text(year, -0.15, str(year), ha='center', va='top',
                fontsize=11, fontweight='bold', color=COLORS["gray"])

    # Timeline line
    ax.plot([1995, 2020], [0.5, 0.5], '-', color=COLORS["gray"],
            linewidth=2, alpha=0.3, zorder=1)
    # Arrows between
    for i in range(len(systems) - 1):
        ax.annotate('', xy=(systems[i+1][0] - 0.5, 0.5),
                    xytext=(systems[i][0] + 0.5, 0.5),
                    arrowprops=dict(arrowstyle='->', color=COLORS["gray"],
                                   lw=1.5, alpha=0.5))

    ax.set_xlim(1994, 2021)
    ax.set_ylim(-0.4, 1.2)
    ax.axis('off')
    ax.set_title("Evolución de la IA en juegos", fontsize=14, fontweight='bold')
    _save(fig, "16_algorithm_evolution.png")


def plot_17_rollout_convergence():
    """Rollout estimate convergence with increasing N."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    # Mid-game position on Hex 3x3
    state = Hex(3)
    state = state.result((1, 1))  # Black center

    n_values = list(range(1, 201))
    n_trials = 20
    all_estimates = []

    for trial in range(n_trials):
        random.seed(trial * 13)
        estimates = []
        cumsum = 0
        for n in n_values:
            # One rollout
            sim = Hex(state.size, state.board, state.current_player)
            while not sim.is_terminal():
                acts = sim.actions()
                sim = sim.result(acts[random.randint(0, len(acts) - 1)])
            cumsum += sim.utility(1)
            estimates.append(cumsum / n)
        all_estimates.append(estimates)

    all_estimates = np.array(all_estimates)
    mean_est = all_estimates.mean(axis=0)
    std_est = all_estimates.std(axis=0)

    # Plot individual trials faintly
    for trial in range(min(5, n_trials)):
        ax.plot(n_values, all_estimates[trial], alpha=0.2, color=COLORS["blue"],
                linewidth=0.8)

    ax.plot(n_values, mean_est, color=COLORS["blue"], linewidth=2.5,
            label="Media de 20 experimentos")
    ax.fill_between(n_values, mean_est - std_est, mean_est + std_est,
                    alpha=0.15, color=COLORS["blue"])

    ax.axhline(y=0, color=COLORS["gray"], linestyle=':', alpha=0.5)
    ax.set_xlabel("Número de rollouts N", fontsize=12)
    ax.set_ylabel("Estimación del valor", fontsize=12)
    ax.set_title("Convergencia del estimador por rollouts (Hex 3×3, Negro en centro)",
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    _save(fig, "17_rollout_convergence.png")


def plot_18_eval_vs_rollout():
    """Compare heuristic eval vs rollout estimate across positions."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    # Generate several positions on Hex 3x3 by random play
    positions = []
    for seed in range(50):
        random.seed(seed)
        state = Hex(3)
        depth = random.randint(1, 5)
        for _ in range(depth):
            if state.is_terminal():
                break
            acts = state.actions()
            state = state.result(acts[random.randint(0, len(acts) - 1)])
        if not state.is_terminal():
            positions.append(state)

    # Heuristic eval: count stones difference
    heuristic_vals = []
    rollout_vals = []

    for pos in positions:
        # Simple heuristic: (black stones - white stones) / total
        b_count = sum(1 for r in range(pos.size) for c in range(pos.size)
                      if pos.board[r][c] == 1)
        w_count = sum(1 for r in range(pos.size) for c in range(pos.size)
                      if pos.board[r][c] == 2)
        heuristic_vals.append((b_count - w_count) / pos.size**2)

        # Rollout average (100 rollouts)
        total = 0
        for _ in range(100):
            sim = Hex(pos.size, pos.board, pos.current_player)
            while not sim.is_terminal():
                acts = sim.actions()
                sim = sim.result(acts[random.randint(0, len(acts) - 1)])
            total += sim.utility(1)
        rollout_vals.append(total / 100)

    ax.scatter(heuristic_vals, rollout_vals, color=COLORS["blue"], alpha=0.6,
               s=60, edgecolor=COLORS["dark"], linewidth=0.5)
    ax.axhline(y=0, color=COLORS["gray"], linestyle=':', alpha=0.5)
    ax.axvline(x=0, color=COLORS["gray"], linestyle=':', alpha=0.5)

    # Trend line
    z = np.polyfit(heuristic_vals, rollout_vals, 1)
    p = np.poly1d(z)
    x_line = np.linspace(min(heuristic_vals), max(heuristic_vals), 100)
    ax.plot(x_line, p(x_line), '--', color=COLORS["red"], linewidth=1.5,
            alpha=0.7, label=f"Tendencia lineal")

    ax.set_xlabel("Evaluación heurística (diferencia de piedras)", fontsize=12)
    ax.set_ylabel("Evaluación por rollouts (100 por posición)", fontsize=12)
    ax.set_title("Heurística vs rollouts en distintas posiciones (Hex 3×3)",
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    _save(fig, "18_eval_vs_rollout.png")


# ---------------------------------------------------------------------------
# UCT formula breakdown (09)
# ---------------------------------------------------------------------------

def plot_19_rave_example():
    """RAVE information sharing: toy example showing how RAVE bootstraps."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

    def _draw_tree_node(ax, x, y, N, Q, label, radius=0.32,
                        rave_N=None, rave_Q=None, highlight=False):
        color = COLORS["light"]
        ec = COLORS["dark"]
        lw = 1.5
        if highlight:
            color = COLORS["green"]
            ec = COLORS["dark"]
            lw = 2.5
        circle = plt.Circle((x, y), radius, facecolor=color, edgecolor=ec,
                             linewidth=lw, zorder=3)
        ax.add_patch(circle)
        tc = "white" if highlight else COLORS["dark"]
        if N > 0:
            qn = Q / N
            ax.text(x, y + 0.08, f"N={N}, Q/N={qn:+.2f}",
                    ha='center', va='center', fontsize=7, fontweight='bold',
                    color=tc, zorder=4)
        else:
            ax.text(x, y + 0.08, "N=0", ha='center', va='center',
                    fontsize=7, fontweight='bold', color=tc, zorder=4)
        if rave_N is not None and rave_N > 0:
            rave_qn = rave_Q / rave_N
            ax.text(x, y - 0.12, f"RAVE: {rave_N} ({rave_qn:+.2f})",
                    ha='center', va='center', fontsize=6.5,
                    color=COLORS["purple"], zorder=4)
        ax.text(x, y - radius - 0.12, label, ha='center', fontsize=9,
                color=COLORS["dark"], zorder=4)

    def _edge(ax, x1, y1, x2, y2, highlight=False):
        c = COLORS["blue"] if highlight else COLORS["dark"]
        lw = 2.5 if highlight else 1
        alpha = 0.9 if highlight else 0.3
        ax.plot([x1, x2], [y1, y2], '-', color=c, linewidth=lw, alpha=alpha, zorder=1)

    # =========================================================================
    # Panel 1: Standard MCTS after 10 iterations — some nodes have 0 visits
    # =========================================================================
    ax = ax1
    # Root: 10 visits
    rx, ry = 2.5, 5.5
    # 5 children (Hex 3x3 after 4 moves → 5 legal)
    children = [
        (0.5, 3.5, 4, 2, "(1,0)"),    # 4 visits
        (1.5, 3.5, 3, 1, "(1,2)"),    # 3 visits
        (2.5, 3.5, 2, 0, "(2,0)"),    # 2 visits
        (3.5, 3.5, 1, -1, "(2,1)"),   # 1 visit
        (4.5, 3.5, 0, 0, "(2,2)"),    # 0 visits!
    ]
    for cx, cy, _, _, _ in children:
        _edge(ax, rx, ry, cx, cy)
    _draw_tree_node(ax, rx, ry, 10, 2, "Raiz (turno Negro)")
    for cx, cy, n, q, lbl in children:
        hl = (n == 0)
        _draw_tree_node(ax, cx, cy, n, q, lbl, highlight=hl)

    # Annotation for the 0-visit node
    ax.annotate("N=0: no sabemos\nnada sobre (2,2)",
                xy=(4.5, 3.5), xytext=(4.5, 2.0),
                fontsize=8, color=COLORS["red"], ha='center',
                arrowprops=dict(arrowstyle='->', color=COLORS["red"], lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=COLORS["red"], alpha=0.9))

    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(1.2, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("MCTS estandar (10 iteraciones)\nAlgunos nodos sin visitas",
                 fontsize=11, fontweight='bold')

    # =========================================================================
    # Panel 2: Same tree but with RAVE statistics
    # =========================================================================
    ax = ax2
    # Same structure, but now RAVE stats are populated from rollouts
    # that happened THROUGH OTHER NODES but contained these moves
    children_rave = [
        (0.5, 3.5, 4, 2, "(1,0)", 8, 4),     # appeared in 8 rollouts total
        (1.5, 3.5, 3, 1, "(1,2)", 7, 3),     # appeared in 7
        (2.5, 3.5, 2, 0, "(2,0)", 6, 2),     # appeared in 6
        (3.5, 3.5, 1, -1, "(2,1)", 5, -1),   # appeared in 5
        (4.5, 3.5, 0, 0, "(2,2)", 4, 2),     # appeared in 4 rollouts!
    ]
    for cx, cy, _, _, _, _, _ in children_rave:
        _edge(ax, rx, ry, cx, cy)
    _draw_tree_node(ax, rx, ry, 10, 2, "Raiz (turno Negro)")
    for cx, cy, n, q, lbl, rn, rq in children_rave:
        _draw_tree_node(ax, cx, cy, n, q, lbl,
                        rave_N=rn, rave_Q=rq,
                        highlight=(n == 0))

    # Annotation for the 0-visit node with RAVE
    ax.annotate("N=0, pero RAVE sabe que (2,2)\naparecio en 4 rollouts con Q/N=+0.50\n"
                "-> tenemos una estimacion inicial!",
                xy=(4.5, 3.5), xytext=(3.5, 1.6),
                fontsize=8, color=COLORS["green"], ha='center',
                arrowprops=dict(arrowstyle='->', color=COLORS["green"], lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=COLORS["green"], alpha=0.9))

    # Show a rollout path that contributed to RAVE
    ax.annotate("Rollout por (1,0) incluyo\nmovimiento (2,2) en turno 5\n"
                "-> RAVE cuenta ese resultado\npara el nodo (2,2)",
                xy=(0.5, 3.1), xytext=(1.8, 1.6),
                fontsize=7.5, color=COLORS["purple"], ha='center',
                arrowprops=dict(arrowstyle='->', color=COLORS["purple"], lw=1),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=COLORS["purple"], alpha=0.9))

    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(0.8, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("MCTS + RAVE (10 iteraciones)\nRollouts comparten informacion entre nodos",
                 fontsize=11, fontweight='bold')

    fig.suptitle("RAVE: como los rollouts comparten informacion",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    _save(fig, "19_rave_example.png")


def plot_20_puct_vs_uct():
    """PUCT vs UCT: how a policy prior reshapes exploration."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    c = 1.41
    N_parent = 100

    # 5 actions with different visit counts
    actions = ["$a_1$", "$a_2$", "$a_3$", "$a_4$", "$a_5$"]
    N_vals =  [35,      25,      20,      15,      5]
    Q_vals =  [18,      15,      10,      6,       3]

    # --- Panel 1: UCT (uniform prior) ---
    uct_vals = []
    for N, Q in zip(N_vals, Q_vals):
        exploit = Q / N
        explore = c * math.sqrt(math.log(N_parent) / N)
        uct_vals.append((exploit, explore))

    x = np.arange(len(actions))
    width = 0.6
    exploit_bars = [e for e, _ in uct_vals]
    explore_bars = [ex for _, ex in uct_vals]

    ax1.bar(x, exploit_bars, width, label='Explotacion Q/N',
            color=COLORS["blue"], alpha=0.8)
    ax1.bar(x, explore_bars, width, bottom=exploit_bars,
            label='Exploracion UCT', color=COLORS["teal"], alpha=0.8)
    for i, (e, ex) in enumerate(uct_vals):
        ax1.text(i, e + ex + 0.02, f"{e+ex:.2f}", ha='center', fontsize=8,
                 fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(actions, fontsize=10)
    ax1.set_ylabel("Valor UCT", fontsize=11)
    ax1.set_title("UCT: prior uniforme\n(todas las acciones se tratan igual)",
                  fontsize=11, fontweight='bold')
    ax1.legend(fontsize=9, loc='upper right')
    ax1.set_ylim(0, 2.2)

    # --- Panel 2: PUCT with policy prior ---
    # Prior from a "policy network": a₃ is strongly preferred
    prior = [0.10, 0.10, 0.50, 0.20, 0.10]  # sums to 1
    puct_vals = []
    for N, Q, p in zip(N_vals, Q_vals, prior):
        exploit = Q / N
        # PUCT: c * P(a) * sqrt(N_parent) / (1 + N)
        explore = c * p * math.sqrt(N_parent) / (1 + N)
        puct_vals.append((exploit, explore))

    exploit_bars2 = [e for e, _ in puct_vals]
    explore_bars2 = [ex for _, ex in puct_vals]

    ax2.bar(x, exploit_bars2, width, label='Explotacion Q/N',
            color=COLORS["blue"], alpha=0.8)
    ax2.bar(x, explore_bars2, width, bottom=exploit_bars2,
            label='Exploracion PUCT', color=COLORS["orange"], alpha=0.8)
    # Show prior values
    for i, (e, ex, p) in enumerate(zip(exploit_bars2, explore_bars2, prior)):
        ax2.text(i, e + ex + 0.02, f"{e+ex:.2f}", ha='center', fontsize=8,
                 fontweight='bold')
        ax2.text(i, -0.12, f"P={p:.2f}", ha='center', fontsize=8,
                 color=COLORS["orange"], fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(actions, fontsize=10)
    ax2.set_ylabel("Valor PUCT", fontsize=11)
    ax2.set_title("PUCT: prior de red de politica\n($a_3$ tiene P=0.50 -> exploracion dirigida)",
                  fontsize=11, fontweight='bold')
    ax2.legend(fontsize=9, loc='upper right')
    ax2.set_ylim(-0.2, 2.2)

    fig.suptitle("UCT vs PUCT: como el prior de la red cambia la exploracion",
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    _save(fig, "20_puct_vs_uct.png")


def plot_09c_uct_selection_trace():
    """Complete iteration trace: selection→expansion→rollout→backprop."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))

    c_val = 1.41

    def _draw_node(ax, x, y, N, Q, radius=0.30, highlight=False, is_new=False,
                   backprop=False, uct_label=None, uct_color=None):
        color = COLORS["light"]
        ec = COLORS["dark"]
        lw = 1.5
        if highlight:
            color = COLORS["blue"]
            lw = 2.5
        if is_new:
            color = COLORS["green"]
            lw = 2.5
        if backprop:
            color = COLORS["purple"]
            lw = 2.5
        circle = plt.Circle((x, y), radius, facecolor=color, edgecolor=ec,
                             linewidth=lw, zorder=3)
        ax.add_patch(circle)
        txt_color = "white" if (highlight or backprop) else COLORS["dark"]
        ax.text(x, y + 0.06, f"N={N}", ha='center', va='center',
                fontsize=8, fontweight='bold', color=txt_color, zorder=4)
        ax.text(x, y - 0.10, f"Q={Q}", ha='center', va='center',
                fontsize=8, color=txt_color, zorder=4)
        if uct_label is not None:
            col = uct_color if uct_color else COLORS["gray"]
            ax.text(x, y + radius + 0.15, uct_label, ha='center', va='center',
                    fontsize=8, color=col, fontweight='bold', zorder=4,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                              edgecolor=col, alpha=0.9))

    def _draw_edge(ax, x1, y1, x2, y2, highlight=False):
        color = COLORS["dark"] if not highlight else COLORS["blue"]
        lw = 1.0 if not highlight else 2.5
        alpha = 0.3 if not highlight else 0.9
        ax.plot([x1, x2], [y1, y2], '-', color=color, linewidth=lw, alpha=alpha,
                zorder=1)

    # =========================================================================
    # Consistent tree layout used in both panels
    # =========================================================================
    root_x, root_y = 3.0, 7.0
    a1_x, a1_y = 1.0, 5.0      # child: action a₁
    a2_x, a2_y = 3.0, 5.0      # child: action a₂
    a3_x, a3_y = 5.0, 5.0      # child: action a₃
    b1_x, b1_y = 0.3, 3.0      # grandchild of a₁
    b2_x, b2_y = 1.7, 3.0      # grandchild of a₁
    # b2 has one unexpanded action → new node
    new_x, new_y = 1.7, 1.2    # new node from expansion

    def uct_val(Q, N, Np):
        if N == 0:
            return float('inf')
        return Q / N + c_val * math.sqrt(math.log(Np) / N)

    fmt = "UCT={:.2f}"
    sel_fmt = "UCT={:.2f}  <--"

    # =========================================================================
    # Panel 1: BEFORE iteration 101 — tree state with UCT values shown
    # =========================================================================
    ax = ax1

    # Edges (a₁ branch highlighted = selection path)
    _draw_edge(ax, root_x, root_y, a1_x, a1_y, highlight=True)
    _draw_edge(ax, root_x, root_y, a2_x, a2_y)
    _draw_edge(ax, root_x, root_y, a3_x, a3_y)
    _draw_edge(ax, a1_x, a1_y, b1_x, b1_y)
    _draw_edge(ax, a1_x, a1_y, b2_x, b2_y, highlight=True)

    # Root
    _draw_node(ax, root_x, root_y, 100, 58, radius=0.35)
    ax.text(root_x, root_y + 0.55, "Raiz (N=100)", ha='center',
            fontsize=10, fontweight='bold', color=COLORS["dark"])

    # Children — UCT computed with parent N=100
    uct_a1 = uct_val(30, 45, 100)  # 0.67+0.45=1.12
    uct_a2 = uct_val(25, 50, 100)  # 0.50+0.43=0.93
    uct_a3 = uct_val(3, 5, 100)    # 0.60+1.35=1.95

    # a₁ has the highest UCT in this scenario (we want to show multi-level)
    # Actually a₃ has highest UCT. Let's use values where a₁ wins so we go deeper.
    # Adjust: a₃ already got explored, now a₁ leads
    # Use: a₁(N=40,Q=28), a₂(N=35,Q=15), a₃(N=25,Q=14)
    uct_a1 = uct_val(28, 40, 100)  # 0.70+0.48=1.18
    uct_a2 = uct_val(15, 35, 100)  # 0.43+0.51=0.94
    uct_a3 = uct_val(14, 25, 100)  # 0.56+0.61=1.17

    _draw_node(ax, a1_x, a1_y, 40, 28, highlight=True,
               uct_label=sel_fmt.format(uct_a1), uct_color=COLORS["green"])
    _draw_node(ax, a2_x, a2_y, 35, 15,
               uct_label=fmt.format(uct_a2), uct_color=COLORS["gray"])
    _draw_node(ax, a3_x, a3_y, 25, 14,
               uct_label=fmt.format(uct_a3), uct_color=COLORS["gray"])

    ax.text(a1_x, a1_y - 0.44, "$a_1$", ha='center', fontsize=11,
            color=COLORS["dark"])
    ax.text(a2_x, a2_y - 0.44, "$a_2$", ha='center', fontsize=11,
            color=COLORS["dark"])
    ax.text(a3_x, a3_y - 0.44, "$a_3$", ha='center', fontsize=11,
            color=COLORS["dark"])

    # Grandchildren — UCT computed with parent N=40 (a₁'s N)
    uct_b1 = uct_val(10, 18, 40)   # 0.56+0.64=1.20
    uct_b2 = uct_val(15, 20, 40)   # 0.75+0.61=1.36

    _draw_node(ax, b1_x, b1_y, 18, 10, radius=0.27,
               uct_label=fmt.format(uct_b1), uct_color=COLORS["gray"])
    _draw_node(ax, b2_x, b2_y, 20, 15, radius=0.27, highlight=True,
               uct_label=sel_fmt.format(uct_b2), uct_color=COLORS["green"])

    ax.text(b1_x, b1_y - 0.40, "$b_1$", ha='center', fontsize=10,
            color=COLORS["dark"])
    ax.text(b2_x, b2_y - 0.40, "$b_2$", ha='center', fontsize=10,
            color=COLORS["dark"])

    # Phase labels on the right
    ax.text(6.5, root_y, "[M1] Nivel 0\nUCT elige $a_1$",
            fontsize=9, color=COLORS["blue"], ha='center', va='center',
            fontweight='bold')
    ax.text(6.5, a1_y, "[M1] Nivel 1\nUCT elige $b_2$",
            fontsize=9, color=COLORS["blue"], ha='center', va='center',
            fontweight='bold')
    ax.text(6.5, b1_y, "[M2] $b_2$ tiene\nhijo sin expandir\n-> expandir",
            fontsize=9, color=COLORS["green"], ha='center', va='center',
            fontweight='bold')

    # New node from expansion
    _draw_edge(ax, b2_x, b2_y, new_x, new_y, highlight=True)
    _draw_node(ax, new_x, new_y, 0, 0, radius=0.25, is_new=True)
    ax.text(new_x, new_y - 0.40, "nuevo", ha='center', fontsize=9,
            color=COLORS["green"], fontweight='bold')

    # Rollout squiggly from new node
    rs = np.random.RandomState(42)
    roll_ys = np.linspace(new_y - 0.3, new_y - 1.4, 12)
    roll_xs = new_x + rs.uniform(-0.15, 0.15, 12)
    ax.plot(roll_xs, roll_ys, '--', color=COLORS["orange"], linewidth=2, zorder=2)
    ax.text(new_x, new_y - 1.7, "[M3] Rollout\nresultado: +1",
            ha='center', fontsize=9, color=COLORS["orange"], fontweight='bold')

    ax.set_xlim(-1.0, 7.5)
    ax.set_ylim(-1.2, 8.0)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Iteracion 101: seleccion + expansion + rollout\n"
                 "[M1] baja por el arbol, [M2] expande, [M3] simula",
                 fontsize=11, fontweight='bold', color=COLORS["dark"])

    # =========================================================================
    # Panel 2: AFTER — backpropagation updates, then the tree AFTER iter 101
    # =========================================================================
    ax = ax2

    # Same tree, but now show backpropagation: all nodes on the path
    # get N+=1, Q+=1 (the rollout returned +1)
    # Path: new → b₂ → a₁ → root

    # Edges (backprop path highlighted in purple)
    _draw_edge(ax, root_x, root_y, a1_x, a1_y)
    _draw_edge(ax, root_x, root_y, a2_x, a2_y)
    _draw_edge(ax, root_x, root_y, a3_x, a3_y)
    _draw_edge(ax, a1_x, a1_y, b1_x, b1_y)
    _draw_edge(ax, a1_x, a1_y, b2_x, b2_y)
    _draw_edge(ax, b2_x, b2_y, new_x, new_y)
    # Backprop arrows
    for (x1, y1, x2, y2) in [(new_x, new_y, b2_x, b2_y),
                               (b2_x, b2_y, a1_x, a1_y),
                               (a1_x, a1_y, root_x, root_y)]:
        ax.annotate('', xy=(x2, y2 - 0.30), xytext=(x1, y1 + 0.30),
                    arrowprops=dict(arrowstyle='->', color=COLORS["purple"],
                                   lw=2.5, connectionstyle='arc3,rad=-0.15'))

    # Updated nodes: N+=1, Q+=1 on the path
    _draw_node(ax, root_x, root_y, 101, 59, radius=0.35, backprop=True)
    ax.text(root_x, root_y + 0.55, "Raiz: 100->101, 58->59",
            ha='center', fontsize=8, fontweight='bold', color=COLORS["purple"])

    _draw_node(ax, a1_x, a1_y, 41, 29, backprop=True)
    ax.text(a1_x, a1_y - 0.44, "$a_1$: 40->41, 28->29",
            ha='center', fontsize=8, color=COLORS["purple"], fontweight='bold')

    _draw_node(ax, a2_x, a2_y, 35, 15)
    ax.text(a2_x, a2_y - 0.44, "$a_2$: sin cambios",
            ha='center', fontsize=8, color=COLORS["gray"])

    _draw_node(ax, a3_x, a3_y, 25, 14)
    ax.text(a3_x, a3_y - 0.44, "$a_3$: sin cambios",
            ha='center', fontsize=8, color=COLORS["gray"])

    _draw_node(ax, b1_x, b1_y, 18, 10, radius=0.27)
    ax.text(b1_x, b1_y - 0.40, "$b_1$: sin cambios",
            ha='center', fontsize=8, color=COLORS["gray"])

    _draw_node(ax, b2_x, b2_y, 21, 16, radius=0.27, backprop=True)
    ax.text(b2_x, b2_y - 0.40, "$b_2$: 20->21, 15->16",
            ha='center', fontsize=8, color=COLORS["purple"], fontweight='bold')

    _draw_node(ax, new_x, new_y, 1, 1, radius=0.25, backprop=True)
    ax.text(new_x, new_y - 0.40, "nuevo: 0->1, 0->1",
            ha='center', fontsize=8, color=COLORS["purple"], fontweight='bold')

    # Phase label
    ax.text(6.5, 4.0, "[M4] Retropropagacion\n\nEl resultado (+1)\nsube por el camino:\n"
                       "nuevo -> $b_2$ -> $a_1$ -> raiz\n\n"
                       "Cada nodo en el\ncamino recibe:\n"
                       "  N += 1\n  Q += 1",
            fontsize=9, color=COLORS["purple"], ha='center', va='center',
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                      edgecolor=COLORS["purple"], alpha=0.9))

    ax.set_xlim(-1.0, 7.5)
    ax.set_ylim(-1.2, 8.0)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Iteracion 101: retropropagacion\n"
                 "[M4] el resultado (+1) sube actualizando N y Q",
                 fontsize=11, fontweight='bold', color=COLORS["dark"])

    fig.suptitle("Una iteracion completa de MCTS con UCT",
                 fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    _save(fig, "09c_uct_selection_trace.png")


def plot_09b_uct_formula():
    """Visual breakdown of the UCT formula."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 4))

    ax.text(0.5, 0.75, r"$\mathrm{UCT}(v) = $", fontsize=22, ha='right', va='center',
            transform=ax.transAxes)

    # Exploitation box
    rect1 = mpatches.FancyBboxPatch((0.51, 0.55), 0.15, 0.4,
                                     boxstyle="round,pad=0.02",
                                     facecolor=COLORS["blue"], alpha=0.15,
                                     edgecolor=COLORS["blue"], linewidth=2,
                                     transform=ax.transAxes)
    ax.add_patch(rect1)
    ax.text(0.585, 0.75, r"$\frac{Q(v)}{N(v)}$", fontsize=22, ha='center', va='center',
            transform=ax.transAxes, color=COLORS["blue"])
    ax.text(0.585, 0.35, "Explotación\n(tasa de éxito)", fontsize=10, ha='center',
            va='top', transform=ax.transAxes, color=COLORS["blue"])

    ax.text(0.69, 0.75, r"$+$", fontsize=22, ha='center', va='center',
            transform=ax.transAxes)

    # Exploration box
    rect2 = mpatches.FancyBboxPatch((0.72, 0.55), 0.25, 0.4,
                                     boxstyle="round,pad=0.02",
                                     facecolor=COLORS["green"], alpha=0.15,
                                     edgecolor=COLORS["green"], linewidth=2,
                                     transform=ax.transAxes)
    ax.add_patch(rect2)
    ax.text(0.845, 0.75, r"$c\sqrt{\frac{\ln N(\mathrm{padre})}{N(v)}}$",
            fontsize=22, ha='center', va='center',
            transform=ax.transAxes, color=COLORS["green"])
    ax.text(0.845, 0.35, "Exploración\n(bonus para poco visitados)", fontsize=10,
            ha='center', va='top', transform=ax.transAxes, color=COLORS["green"])

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title("Descomposición de la fórmula UCT", fontsize=14, fontweight='bold')
    _save(fig, "09_uct_formula.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Generando imágenes para el módulo 18 (Monte Carlo Tree Search)...\n")

    # Hex board figures
    plot_01_hex_empty_board()
    plot_02_hex_neighbors()
    plot_03_hex_legal_moves()
    plot_04_hex_winning_path()
    plot_05_hex_3x3_games()
    plot_06_hex_strategy()

    # MCTS algorithm figures
    plot_07_mcts_four_phases()
    plot_08_mcts_tree_growth()
    plot_09_mcts_trace()
    plot_09b_uct_formula()
    plot_09c_uct_selection_trace()

    # UCT figures
    plot_10_uct_vs_uniform()
    plot_11_uct_c_effect()

    # Experiment figures
    plot_12_mcts_vs_minimax_3x3()
    plot_13_tournament_results()
    plot_14_iteration_budget()
    plot_15_asymmetric_tree()

    # AlphaZero figures
    plot_16_algorithm_evolution()

    # Rollout figures
    plot_17_rollout_convergence()
    plot_18_eval_vs_rollout()

    # Beyond MCTS figures
    plot_19_rave_example()
    plot_20_puct_vs_uct()

    print(f"\n✓  Todas las imágenes generadas en {IMAGES_DIR}/")


if __name__ == "__main__":
    main()
