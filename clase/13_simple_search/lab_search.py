#!/usr/bin/env python3
"""
Laboratorio: Búsqueda Simple (imágenes para las notas)

Uso:
    cd clase/13_simple_search
    python3 lab_search.py

Genera ~14 imágenes en:
    clase/13_simple_search/images/

Dependencias: numpy, matplotlib
"""

from pathlib import Path
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
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
# Helpers: draw a graph from pos + edges
# ---------------------------------------------------------------------------
def _draw_graph(ax, pos, edges, directed=False, node_color=None,
                edge_color=None, node_labels=None, title="",
                highlight_nodes=None, highlight_edges=None):
    """Draw a simple graph on ax using explicit positions."""
    nodes = list(pos.keys())
    nc = node_color or {n: COLORS["blue"] for n in nodes}
    ec = edge_color or COLORS["gray"]

    # edges
    for u, v in edges:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        color = COLORS["red"] if (highlight_edges and (u, v) in highlight_edges) else ec
        lw = 2.5 if (highlight_edges and (u, v) in highlight_edges) else 1.5
        if directed:
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                        arrowprops=dict(arrowstyle="-|>", color=color,
                                        lw=lw, mutation_scale=16))
        else:
            ax.plot([x0, x1], [y0, y1], color=color, lw=lw, zorder=1)

    # nodes
    for n in nodes:
        x, y = pos[n]
        color = COLORS["orange"] if (highlight_nodes and n in highlight_nodes) \
            else nc.get(n, COLORS["blue"])
        circle = plt.Circle((x, y), 0.18, color=color, zorder=3)
        ax.add_patch(circle)
        label = node_labels.get(n, str(n)) if node_labels else str(n)
        ax.text(x, y, label, ha="center", va="center",
                fontsize=11, fontweight="bold", color="white", zorder=4)

    ax.set_xlim(-0.4, max(x for x, _ in pos.values()) + 0.4)
    ax.set_ylim(-0.4, max(y for _, y in pos.values()) + 0.4)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=12, fontweight="bold", pad=8)


# ---------------------------------------------------------------------------
# 1. Undirected vs Directed
# ---------------------------------------------------------------------------
def plot_undirected_vs_directed() -> None:
    pos = {0: (0, 1), 1: (1, 2), 2: (2, 1), 3: (1, 0)}
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (1, 3)]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    fig.suptitle("Grafo no dirigido vs. grafo dirigido",
                 fontsize=13, fontweight="bold", y=1.02)

    _draw_graph(axes[0], pos, edges, directed=False,
                title="No dirigido\nlas aristas son conjuntos $\\{u,v\\}$")
    # For directed, add reverse edges too for a mixed look
    dir_edges = [(0, 1), (1, 2), (3, 2), (0, 3), (1, 3)]
    _draw_graph(axes[1], pos, dir_edges, directed=True,
                title="Dirigido\nlas aristas son pares ordenados $(u,v)$")

    fig.tight_layout()
    _save(fig, "01_undirected_vs_directed.png")


# ---------------------------------------------------------------------------
# 2. Simple vs Multigraph
# ---------------------------------------------------------------------------
def plot_simple_vs_multigraph() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    fig.suptitle("Grafo simple vs. multigrafo",
                 fontsize=13, fontweight="bold", y=1.02)

    # Simple graph
    pos_s = {0: (0, 1), 1: (1, 2), 2: (2, 1), 3: (1, 0)}
    edges_s = [(0, 1), (1, 2), (2, 3)]
    _draw_graph(axes[0], pos_s, edges_s, directed=False,
                title="Grafo simple\nsin autoloops, sin aristas múltiples")

    # Multigraph — draw manually to show self-loop and multi-edge
    ax = axes[1]
    pos_m = {0: (0, 1), 1: (1, 2), 2: (2, 1), 3: (1, 0)}
    # draw normal edges
    for u, v in [(0, 1), (2, 3)]:
        x0, y0 = pos_m[u]; x1, y1 = pos_m[v]
        ax.plot([x0, x1], [y0, y1], color=COLORS["gray"], lw=1.5)
    # double edge 1-2
    x0, y0 = pos_m[1]; x1, y1 = pos_m[2]
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-", color=COLORS["red"],
                                lw=2, connectionstyle="arc3,rad=0.3"))
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-", color=COLORS["red"],
                                lw=2, connectionstyle="arc3,rad=-0.3"))
    ax.text(1.5, 1.7, "arista\nmúltiple", ha="center", color=COLORS["red"],
            fontsize=9)
    # self-loop at node 3
    theta = np.linspace(0, 2 * np.pi, 100)
    lx = pos_m[3][0] + 0.22 * np.cos(theta)
    ly = pos_m[3][1] - 0.22 + 0.22 * np.sin(theta)
    ax.plot(lx, ly, color=COLORS["orange"], lw=2)
    ax.text(pos_m[3][0] + 0.5, pos_m[3][1] - 0.25, "autoloop",
            ha="center", color=COLORS["orange"], fontsize=9)
    # nodes
    for n in pos_m:
        x, y = pos_m[n]
        circle = plt.Circle((x, y), 0.18, color=COLORS["blue"], zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, str(n), ha="center", va="center",
                fontsize=11, fontweight="bold", color="white", zorder=4)
    ax.set_xlim(-0.4, 2.4); ax.set_ylim(-0.5, 2.4)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Multigrafo\npermite autoloops y aristas múltiples",
                 fontsize=12, fontweight="bold", pad=8)

    fig.tight_layout()
    _save(fig, "02_simple_vs_multigraph.png")


# ---------------------------------------------------------------------------
# 3. Adjacency representations
# ---------------------------------------------------------------------------
def plot_adjacency_representations() -> None:
    # 5-node directed graph
    nodes = [0, 1, 2, 3, 4]
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
    pos = {0: (0, 2), 1: (1, 3), 2: (1, 1), 3: (2, 2), 4: (3, 2)}

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle("Representaciones de un grafo dirigido",
                 fontsize=13, fontweight="bold")

    # Graph drawing
    _draw_graph(axes[0], pos, edges, directed=True, title="Grafo")

    # Adjacency list as text
    ax = axes[1]
    ax.axis("off")
    ax.set_title("Lista de adyacencia\n$O(V+E)$ espacio", fontsize=12,
                 fontweight="bold", pad=8)
    adj_list = {n: [v for u, v in edges if u == n] for n in nodes}
    text = "graph = {\n"
    for n in nodes:
        text += f"  {n}: {adj_list[n]},\n"
    text += "}"
    ax.text(0.05, 0.55, text, transform=ax.transAxes,
            fontsize=10, fontfamily="monospace",
            verticalalignment="center",
            bbox=dict(boxstyle="round,pad=0.5", facecolor=COLORS["light"],
                      edgecolor=COLORS["gray"]))

    # Adjacency matrix
    ax = axes[2]
    ax.set_title("Matriz de adyacencia\n$O(V^2)$ espacio", fontsize=12,
                 fontweight="bold", pad=8)
    n = len(nodes)
    mat = np.zeros((n, n), dtype=int)
    for u, v in edges:
        mat[u][v] = 1

    im = ax.imshow(mat, cmap="Blues", vmin=0, vmax=1.5, aspect="equal")
    for i in range(n):
        for j in range(n):
            ax.text(j, i, str(mat[i, j]), ha="center", va="center",
                    fontsize=12, fontweight="bold",
                    color="white" if mat[i, j] else COLORS["dark"])
    ax.set_xticks(range(n)); ax.set_yticks(range(n))
    ax.set_xticklabels(nodes); ax.set_yticklabels(nodes)
    ax.set_xlabel("destino"); ax.set_ylabel("origen")
    ax.xaxis.set_label_position("top"); ax.xaxis.tick_top()

    fig.tight_layout()
    _save(fig, "03_adjacency_representations.png")


# ---------------------------------------------------------------------------
# 4. Walk / Path / Cycle
# ---------------------------------------------------------------------------
def plot_path_walk_cycle() -> None:
    pos = {0: (0, 1), 1: (1, 2), 2: (2, 2), 3: (3, 1), 4: (2, 0), 5: (1, 0)}
    base_edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (1, 4)]

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    fig.suptitle("Conceptos básicos: camino, recorrido, ciclo",
                 fontsize=13, fontweight="bold")

    # Walk: 0→1→4→1→2 (repeats node 1)
    walk_edges = {(0, 1), (1, 4), (4, 1), (1, 2)}
    walk_nodes = {0, 1, 2, 4}
    _draw_graph(axes[0], pos, base_edges,
                node_color={n: COLORS["orange"] if n in walk_nodes else COLORS["blue"]
                            for n in pos},
                highlight_edges=walk_edges,
                title="Recorrido (walk)\n0→1→4→1→2\n(puede repetir nodos)")

    # Path: 0→1→2→3 (no repeats)
    path_edges = {(0, 1), (1, 2), (2, 3)}
    path_nodes = {0, 1, 2, 3}
    _draw_graph(axes[1], pos, base_edges,
                node_color={n: COLORS["green"] if n in path_nodes else COLORS["blue"]
                            for n in pos},
                highlight_edges=path_edges,
                title="Camino (path)\n0→1→2→3\n(no repite nodos)")

    # Cycle: 0→1→2→3→4→5→0
    cycle_edges = {(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)}
    _draw_graph(axes[2], pos, base_edges,
                node_color={n: COLORS["purple"] for n in pos},
                highlight_edges=cycle_edges,
                title="Ciclo\n0→1→2→3→4→5→0\n(camino cerrado)")

    fig.tight_layout()
    _save(fig, "04_walk_path_cycle.png")


# ---------------------------------------------------------------------------
# 5. Tree as special graph
# ---------------------------------------------------------------------------
def plot_tree_special_case() -> None:
    pos_tree = {0: (2, 3), 1: (1, 2), 2: (3, 2),
                3: (0.5, 1), 4: (1.5, 1), 5: (2.5, 1), 6: (3.5, 1)}
    tree_edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]

    pos_cycle = {0: (1, 2), 1: (2, 3), 2: (3, 2), 3: (2, 1)}
    cycle_edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("El árbol es un grafo especial: conexo + acíclico",
                 fontsize=13, fontweight="bold")

    _draw_graph(axes[0], pos_tree, tree_edges,
                node_color={n: COLORS["green"] for n in pos_tree},
                title="Árbol: conexo + acíclico\n$|E| = |V| - 1 = 6$")
    axes[0].text(2, -0.1, "$|V|=7,\\ |E|=6$", ha="center", fontsize=11,
                 color=COLORS["dark"])

    _draw_graph(axes[1], pos_cycle, cycle_edges,
                node_color={n: COLORS["red"] for n in pos_cycle},
                title="Grafo general: tiene ciclos\n$|E|$ puede ser cualquier valor")

    fig.tight_layout()
    _save(fig, "05_tree_special_case.png")


# ---------------------------------------------------------------------------
# 6. Grid state space
# ---------------------------------------------------------------------------
def plot_grid_state_space() -> None:
    # 3x3 grid, obstacle at (1,1), start (0,0), goal (2,2)
    grid = [['S', '.', '.'],
            ['.', '#', '.'],
            ['.', '.', 'G']]
    rows, cols = 3, 3

    def neighbors_grid(r, c):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                yield (nr, nc)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Espacio de estados: robot en una cuadrícula 3×3",
                 fontsize=13, fontweight="bold")

    # Left: draw grid
    ax = axes[0]
    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            color = (COLORS["dark"] if cell == '#' else
                     COLORS["green"] if cell == 'G' else
                     COLORS["orange"] if cell == 'S' else COLORS["light"])
            rect = plt.Rectangle((c, rows - 1 - r), 1, 1,
                                  facecolor=color, edgecolor=COLORS["gray"], lw=1.5)
            ax.add_patch(rect)
            label = cell if cell in ('#', 'S', 'G') else f"({r},{c})"
            ax.text(c + 0.5, rows - r - 0.5, label, ha="center", va="center",
                    fontsize=10, fontweight="bold",
                    color="white" if color == COLORS["dark"] else COLORS["dark"])
    ax.set_xlim(0, cols); ax.set_ylim(0, rows)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Cuadrícula\n(S=inicio, G=goal, #=obstáculo)",
                 fontsize=11, fontweight="bold")

    # Right: draw state space graph
    ax = axes[1]
    states = [(r, c) for r in range(rows) for c in range(cols)
              if grid[r][c] != '#']
    # Lay out using grid coords
    pos_ss = {(r, c): (c * 1.2, (rows - 1 - r) * 1.2) for r, c in states}
    ss_edges = []
    for (r, c) in states:
        for (nr, nc) in neighbors_grid(r, c):
            if (r, c) < (nr, nc):  # undirected: only add once
                ss_edges.append(((r, c), (nr, nc)))

    node_labels = {s: f"({s[0]},{s[1]})" for s in states}
    nc = {s: (COLORS["green"] if grid[s[0]][s[1]] == 'G' else
              COLORS["orange"] if grid[s[0]][s[1]] == 'S' else
              COLORS["blue"]) for s in states}

    for u, v in ss_edges:
        x0, y0 = pos_ss[u]; x1, y1 = pos_ss[v]
        ax.plot([x0, x1], [y0, y1], color=COLORS["gray"], lw=1.5)
    for s in states:
        x, y = pos_ss[s]
        circle = plt.Circle((x, y), 0.22, color=nc[s], zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, node_labels[s], ha="center", va="center",
                fontsize=7.5, fontweight="bold", color="white", zorder=4)

    ax.set_xlim(-0.4, 3.0); ax.set_ylim(-0.4, 2.9)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Grafo del espacio de estados\n(nodos=estados, aristas=movimientos)",
                 fontsize=11, fontweight="bold")

    fig.tight_layout()
    _save(fig, "06_grid_state_space.png")


# ---------------------------------------------------------------------------
# Helper: 6-node graph used in BFS and DFS step-by-step
# ---------------------------------------------------------------------------
_DEMO_POS = {
    'A': (0, 1), 'B': (1, 2), 'C': (1, 0),
    'D': (2, 2), 'E': (2, 1), 'F': (3, 1)
}
_DEMO_EDGES_UNDIRECTED = [
    ('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'E'), ('D', 'F'), ('E', 'F')
]
_DEMO_ADJ = {
    'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'E'],
    'D': ['B', 'F'], 'E': ['B', 'C', 'F'], 'F': ['D', 'E']
}


def _draw_search_step(ax, step_num, frontier_contents, explored_set,
                      current_node, title_extra=""):
    """Draw the demo graph colored by search state."""
    pos = _DEMO_POS
    edges = _DEMO_EDGES_UNDIRECTED
    nodes = list(pos.keys())

    for u, v in edges:
        x0, y0 = pos[u]; x1, y1 = pos[v]
        ax.plot([x0, x1], [y0, y1], color=COLORS["gray"], lw=1.5, zorder=1)

    for n in nodes:
        if n == current_node:
            color = COLORS["orange"]
        elif n in explored_set:
            color = COLORS["green"]
        elif n in frontier_contents:
            color = COLORS["blue"]
        else:
            color = COLORS["light"]
        circle = plt.Circle(pos[n], 0.2, color=color, zorder=3,
                             edgecolor=COLORS["dark"], linewidth=1)
        ax.add_patch(circle)
        tc = "white" if color != COLORS["light"] else COLORS["dark"]
        ax.text(pos[n][0], pos[n][1], n, ha="center", va="center",
                fontsize=11, fontweight="bold", color=tc, zorder=4)

    ax.set_xlim(-0.4, 3.4); ax.set_ylim(-0.3, 2.4)
    ax.set_aspect("equal"); ax.axis("off")

    frontier_str = " -> ".join(frontier_contents) if frontier_contents else "(vacia)"
    explored_str = "{" + ", ".join(sorted(explored_set)) + "}" if explored_set else "(vacio)"
    info = f"Paso {step_num}\nFrontera: [{frontier_str}]\nExplorado: {explored_str}"
    if title_extra:
        info = title_extra + "\n" + info
    ax.set_title(info, fontsize=8.5, pad=4)


# ---------------------------------------------------------------------------
# 7. BFS step-by-step
# ---------------------------------------------------------------------------
def plot_bfs_step_by_step() -> None:
    # BFS from A, goal F
    # Step 0: init — frontier=[A], explored={}
    # Step 1: expand A — frontier=[B,C], explored={A}
    # Step 2: expand B — frontier=[C,D,E], explored={A,B}
    # Step 3: expand C — frontier=[D,E], explored={A,B,C}
    # Step 4: expand D — frontier=[E,F], explored={A,B,C,D}
    # Step 5: expand E — frontier=[F], explored={A,B,C,D,E}
    # Step 6: expand F — GOAL found

    steps = [
        (0, ['A'], set(), None, "Inicio: A en frontera"),
        (1, ['B', 'C'], {'A'}, 'A', "Expandimos A"),
        (2, ['C', 'D', 'E'], {'A', 'B'}, 'B', "Expandimos B"),
        (3, ['D', 'E'], {'A', 'B', 'C'}, 'C', "Expandimos C"),
        (4, ['E', 'F'], {'A', 'B', 'C', 'D'}, 'D', "Expandimos D"),
        (5, ['F'], {'A', 'B', 'C', 'D', 'E'}, 'E', "Expandimos E → ¡F en frontera!"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    fig.suptitle("BFS paso a paso: desde A, buscando F\n"
                 "[naranja]=nodo actual  [azul]=frontera  [verde]=explorado  [blanco]=no visitado",
                 fontsize=12, fontweight="bold")
    axes = axes.flatten()
    for i, (step, frontier, explored, current, note) in enumerate(steps):
        _draw_search_step(axes[i], step, frontier, explored, current, note)

    # Legend
    from matplotlib.patches import Patch
    legend_els = [
        Patch(facecolor=COLORS["orange"], label="Nodo actual"),
        Patch(facecolor=COLORS["blue"], label="En frontera (cola)"),
        Patch(facecolor=COLORS["green"], label="Explorado"),
        Patch(facecolor=COLORS["light"], edgecolor=COLORS["dark"], label="No visitado"),
    ]
    fig.legend(handles=legend_els, loc="lower center", ncol=4,
               fontsize=10, frameon=True, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout()
    _save(fig, "07_bfs_step_by_step.png")


# ---------------------------------------------------------------------------
# 8. BFS frontier rings
# ---------------------------------------------------------------------------
def plot_bfs_frontier_rings() -> None:
    pos = _DEMO_POS
    edges = _DEMO_EDGES_UNDIRECTED

    # BFS levels from A
    levels = {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 3}
    level_colors = {0: COLORS["orange"], 1: COLORS["blue"],
                    2: COLORS["purple"], 3: COLORS["green"]}

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("BFS: exploración nivel a nivel (como ondas en el agua)",
                 fontsize=12, fontweight="bold")

    for u, v in edges:
        x0, y0 = pos[u]; x1, y1 = pos[v]
        ax.plot([x0, x1], [y0, y1], color=COLORS["gray"], lw=1.5, zorder=1)

    for n in levels:
        x, y = pos[n]
        lvl = levels[n]
        color = level_colors[lvl]
        circle = plt.Circle((x, y), 0.2, color=color, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, n, ha="center", va="center",
                fontsize=11, fontweight="bold", color="white", zorder=4)
        ax.text(x, y - 0.35, f"nivel {lvl}", ha="center",
                fontsize=8, color=color)

    patches = [mpatches.Patch(color=level_colors[i], label=f"Nivel {i}")
               for i in range(4)]
    ax.legend(handles=patches, loc="upper right", fontsize=10)
    ax.set_xlim(-0.4, 3.4); ax.set_ylim(-0.7, 2.5)
    ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout()
    _save(fig, "08_bfs_frontier_rings.png")


# ---------------------------------------------------------------------------
# 9. BFS flood fill
# ---------------------------------------------------------------------------
def plot_bfs_flood_fill() -> None:
    # 12x12 pixel grid with a region, BFS from seed
    grid_size = 12
    region = np.zeros((grid_size, grid_size), dtype=int)

    # Draw a roughly circular connected region
    cx, cy = 5, 5
    for r in range(grid_size):
        for c in range(grid_size):
            if (r - cx) ** 2 + (c - cy) ** 2 <= 16:
                region[r, c] = 1
    # Add a second smaller region
    for r in range(grid_size):
        for c in range(grid_size):
            if (r - 2) ** 2 + (c - 9) ** 2 <= 4:
                region[r, c] = 2

    seed = (5, 5)  # inside region 1

    # BFS
    visited_order = []
    visited = set()
    queue = deque([seed])
    visited.add(seed)
    while queue:
        r, c = queue.popleft()
        visited_order.append((r, c))
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < grid_size and 0 <= nc < grid_size
                    and region[nr, nc] == 1 and (nr, nc) not in visited):
                visited.add((nr, nc))
                queue.append((nr, nc))

    snapshots = [0, len(visited_order) // 4,
                 len(visited_order) // 2,
                 3 * len(visited_order) // 4,
                 len(visited_order)]

    fig, axes = plt.subplots(1, 5, figsize=(15, 4))
    fig.suptitle("BFS como flood fill: colorear una región conectada de píxeles",
                 fontsize=12, fontweight="bold")

    for idx, snap in enumerate(snapshots):
        ax = axes[idx]
        vis = set(visited_order[:snap])
        img = np.ones((grid_size, grid_size, 3))
        for r in range(grid_size):
            for c in range(grid_size):
                if region[r, c] == 2:
                    img[r, c] = [0.6, 0.4, 0.8]  # purple region
                elif region[r, c] == 1:
                    if (r, c) in vis:
                        img[r, c] = [0.17, 0.53, 0.67]  # filled blue
                    else:
                        img[r, c] = [0.85, 0.85, 0.85]  # unfilled region
                # else white background
        if (seed[0], seed[1]) not in vis and snap == 0:
            img[seed[0], seed[1]] = [1.0, 0.6, 0.2]

        ax.imshow(img, origin="upper", interpolation="nearest")
        ax.set_title(f"Paso {snap}\n({snap} píxeles coloreados)", fontsize=9)
        ax.axis("off")
        # Mark seed
        ax.plot(seed[1], seed[0], 'o', color=COLORS["orange"],
                markersize=6, zorder=5)

    fig.tight_layout()
    _save(fig, "09_bfs_flood_fill.png")


# ---------------------------------------------------------------------------
# 10. DFS step-by-step
# ---------------------------------------------------------------------------
def plot_dfs_step_by_step() -> None:
    # DFS from A (neighbors explored in alphabetical order → B first)
    # Uses stack: push neighbors in reverse order so B is on top
    # Step 0: init — stack=[A], explored={}
    # Step 1: pop A → push C,B (B on top) explored={A}
    # Step 2: pop B → push E,D  explored={A,B}
    # Step 3: pop D → push F    explored={A,B,D}
    # Step 4: pop F → GOAL (or just show explored)
    # Step 5: backtrack ...

    steps = [
        (0, ['A'], set(), None, "Inicio: A en pila"),
        (1, ['C', 'B'], {'A'}, 'A', "Pop A → push B,C (B arriba)"),
        (2, ['C', 'E', 'D'], {'A', 'B'}, 'B', "Pop B → push D,E (D arriba)"),
        (3, ['C', 'E', 'F'], {'A', 'B', 'D'}, 'D', "Pop D → push F"),
        (4, ['C', 'E'], {'A', 'B', 'D', 'F'}, 'F', "Pop F → ¡GOAL encontrado!"),
        (5, ['C'], {'A', 'B', 'D', 'E', 'F'}, 'E', "Backtrack: pop E"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    fig.suptitle("DFS paso a paso: desde A, buscando F\n"
                 "[naranja]=nodo actual  [azul]=en pila  [verde]=explorado  [blanco]=no visitado",
                 fontsize=12, fontweight="bold")
    axes = axes.flatten()
    for i, (step, stack, explored, current, note) in enumerate(steps):
        _draw_search_step(axes[i], step, stack, explored, current, note)

    from matplotlib.patches import Patch
    legend_els = [
        Patch(facecolor=COLORS["orange"], label="Nodo actual"),
        Patch(facecolor=COLORS["blue"], label="En pila"),
        Patch(facecolor=COLORS["green"], label="Explorado"),
        Patch(facecolor=COLORS["light"], edgecolor=COLORS["dark"], label="No visitado"),
    ]
    fig.legend(handles=legend_els, loc="lower center", ncol=4,
               fontsize=10, frameon=True, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout()
    _save(fig, "10_dfs_step_by_step.png")


# ---------------------------------------------------------------------------
# 11. DFS vs BFS traversal tree
# ---------------------------------------------------------------------------
def plot_dfs_vs_bfs_tree() -> None:
    # Show the discovery tree of each on the demo graph
    pos = _DEMO_POS
    edges = _DEMO_EDGES_UNDIRECTED

    # BFS tree edges (from A): A-B, A-C, B-D, B-E, D-F
    bfs_tree = {('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('D', 'F')}
    # DFS tree edges (from A, alphabetical): A-B, B-D, D-F, (backtrack), B-E, (backtrack), A-C
    dfs_tree = {('A', 'B'), ('B', 'D'), ('D', 'F'), ('B', 'E'), ('A', 'C')}

    # BFS order numbers
    bfs_order = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6}
    dfs_order = {'A': 1, 'B': 2, 'D': 3, 'F': 4, 'E': 5, 'C': 6}

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Árbol de búsqueda: BFS vs DFS sobre el mismo grafo",
                 fontsize=13, fontweight="bold")

    for ax, tree_edges, order, title in [
        (axes[0], bfs_tree, bfs_order, "BFS — árbol de búsqueda\n(orden de descubrimiento)"),
        (axes[1], dfs_tree, dfs_order, "DFS — árbol de búsqueda\n(orden de descubrimiento)"),
    ]:
        for u, v in edges:
            x0, y0 = pos[u]; x1, y1 = pos[v]
            is_tree = (u, v) in tree_edges or (v, u) in tree_edges
            ax.plot([x0, x1], [y0, y1],
                    color=COLORS["blue"] if is_tree else COLORS["light"],
                    lw=2.5 if is_tree else 1, zorder=1,
                    linestyle="-" if is_tree else "--")
        for n in pos:
            x, y = pos[n]
            circle = plt.Circle((x, y), 0.22, color=COLORS["blue"], zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, n, ha="center", va="center",
                    fontsize=10, fontweight="bold", color="white", zorder=4)
            ax.text(x + 0.25, y + 0.25, str(order[n]),
                    ha="center", va="center", fontsize=9, color=COLORS["orange"],
                    fontweight="bold", zorder=5)
        ax.set_xlim(-0.4, 3.6); ax.set_ylim(-0.3, 2.5)
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(title, fontsize=11, fontweight="bold")

    fig.tight_layout()
    _save(fig, "11_dfs_vs_bfs_tree.png")


# ---------------------------------------------------------------------------
# 12. IDDFS levels
# ---------------------------------------------------------------------------
def plot_iddfs_levels() -> None:
    # Tree: root A, branching factor 2, depth 3
    # A → B,C; B → D,E; C → F,G; D → H,I; F → J,K
    pos_tree = {
        'A': (4, 4),
        'B': (2, 3), 'C': (6, 3),
        'D': (1, 2), 'E': (3, 2), 'F': (5, 2), 'G': (7, 2),
        'H': (0.5, 1), 'I': (1.5, 1), 'J': (4.5, 1), 'K': (5.5, 1),
    }
    tree_edges = [
        ('A', 'B'), ('A', 'C'),
        ('B', 'D'), ('B', 'E'), ('C', 'F'), ('C', 'G'),
        ('D', 'H'), ('D', 'I'), ('F', 'J'), ('F', 'K'),
    ]
    # Goal is K
    goal = 'K'

    depth_nodes = {
        0: {'A'},
        1: {'A', 'B', 'C'},
        2: {'A', 'B', 'C', 'D', 'E', 'F', 'G'},
        3: set(pos_tree.keys()),
    }

    fig, axes = plt.subplots(1, 4, figsize=(16, 5))
    fig.suptitle("IDDFS: DFS con límite de profundidad creciente\nMeta = K (profundidad 3)",
                 fontsize=12, fontweight="bold")

    for idx, depth_limit in enumerate(range(4)):
        ax = axes[idx]
        active = depth_nodes[depth_limit]
        for u, v in tree_edges:
            x0, y0 = pos_tree[u]; x1, y1 = pos_tree[v]
            alpha = 1.0 if u in active and v in active else 0.15
            ax.plot([x0, x1], [y0, y1], color=COLORS["gray"],
                    lw=1.5, alpha=alpha)
        for n in pos_tree:
            x, y = pos_tree[n]
            in_active = n in active
            color = (COLORS["green"] if n == goal and in_active else
                     COLORS["orange"] if n == 'A' and in_active else
                     COLORS["blue"] if in_active else COLORS["light"])
            alpha = 1.0 if in_active else 0.3
            circle = plt.Circle((x, y), 0.28, color=color, alpha=alpha, zorder=3)
            ax.add_patch(circle)
            tc = "white" if in_active and color != COLORS["light"] else COLORS["gray"]
            ax.text(x, y, n, ha="center", va="center",
                    fontsize=10, fontweight="bold", color=tc, zorder=4, alpha=alpha)

        found = goal in active
        result = "¡Meta encontrada!" if found else "No encontrada"
        color_res = COLORS["green"] if found else COLORS["red"]
        ax.set_title(f"Iteración {depth_limit}: límite = {depth_limit}\n{result}",
                     fontsize=9.5, fontweight="bold", color=color_res)
        ax.set_xlim(-0.2, 8.2); ax.set_ylim(0.5, 4.5)
        ax.set_aspect("equal"); ax.axis("off")

    fig.tight_layout()
    _save(fig, "12_iddfs_levels.png")


# ---------------------------------------------------------------------------
# 13. BFS vs DFS vs IDDFS discovery order comparison
# ---------------------------------------------------------------------------
def plot_bfs_dfs_iddfs_comparison() -> None:
    """Three-panel comparison: same 6-node graph, discovery order for each algorithm."""
    pos = _DEMO_POS
    edges = _DEMO_EDGES_UNDIRECTED

    # BFS discovery order from A (FIFO, alphabetical neighbors)
    bfs_order  = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6}
    bfs_tree   = {('A','B'), ('A','C'), ('B','D'), ('B','E'), ('D','F')}

    # DFS discovery order from A (LIFO, alphabetical → B explored before C)
    dfs_order  = {'A': 1, 'B': 2, 'D': 3, 'F': 4, 'E': 5, 'C': 6}
    dfs_tree   = {('A','B'), ('B','D'), ('D','F'), ('B','E'), ('A','C')}

    # IDDFS: final pass (limit=3) reaches A→B→D→F then stops at goal.
    # Show only the nodes reached in the winning pass.  C and E were explored
    # in earlier passes but not reached again before F was found.
    iddfs_order = {'A': 1, 'B': 2, 'D': 3, 'F': 4, 'E': None, 'C': None}
    iddfs_tree  = {('A','B'), ('B','D'), ('D','F')}
    # Total visits across all passes (limit 0,1,2,3):
    #   A:4  B:3  C:2  D:2  E:1  F:1
    iddfs_visits = {'A': 4, 'B': 3, 'C': 2, 'D': 2, 'E': 1, 'F': 1}

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Árbol de búsqueda: BFS vs DFS vs IDDFS sobre el mismo grafo\n"
                 "Números = orden de descubrimiento  |  ×N = veces que IDDFS visitó el nodo",
                 fontsize=12, fontweight="bold")

    configs = [
        (axes[0], bfs_tree,   bfs_order,   None,
         "BFS — orden de descubrimiento\n(nivel a nivel, FIFO)"),
        (axes[1], dfs_tree,   dfs_order,   None,
         "DFS — orden de descubrimiento\n(primero en profundidad, LIFO)"),
        (axes[2], iddfs_tree, iddfs_order, iddfs_visits,
         "IDDFS — pasada final (límite=3)\n(×N = total de visitas a través de todas las pasadas)"),
    ]

    for ax, tree_edges, order, visits, title in configs:
        # Draw all edges (tree edges solid+blue, non-tree dashed+light)
        for u, v in edges:
            x0, y0 = pos[u]; x1, y1 = pos[v]
            is_tree = (u, v) in tree_edges or (v, u) in tree_edges
            ax.plot([x0, x1], [y0, y1],
                    color=COLORS["blue"] if is_tree else COLORS["light"],
                    lw=2.5 if is_tree else 1.0, zorder=1,
                    linestyle="-" if is_tree else "--")

        # Draw nodes
        for n in pos:
            x, y = pos[n]
            num = order[n]
            if n == 'F':       # goal
                color = COLORS["green"]
            elif num is None:  # IDDFS: reached in earlier pass, not final
                color = COLORS["purple"]
            else:
                color = COLORS["blue"]

            circle = plt.Circle((x, y), 0.22, color=color, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, n, ha="center", va="center",
                    fontsize=10, fontweight="bold", color="white", zorder=4)

            # Discovery order badge (top-right)
            badge_label = str(num) if num is not None else "—"
            ax.text(x + 0.28, y + 0.28, badge_label,
                    ha="center", va="center", fontsize=9,
                    color=COLORS["orange"], fontweight="bold", zorder=5)

            # IDDFS-only: visit count badge (bottom-right)
            if visits is not None:
                ax.text(x + 0.28, y - 0.28, f"×{visits[n]}",
                        ha="center", va="center", fontsize=8,
                        color=COLORS["red"], fontweight="bold", zorder=5)

        ax.set_xlim(-0.5, 3.7); ax.set_ylim(-0.5, 2.6)
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(title, fontsize=10, fontweight="bold", pad=6)

    # Shared legend
    from matplotlib.patches import Patch
    legend_els = [
        Patch(facecolor=COLORS["blue"],   label="Nodo explorado"),
        Patch(facecolor=COLORS["green"],  label="Meta (F)"),
        Patch(facecolor=COLORS["purple"], label="IDDFS: solo en pasadas anteriores"),
    ]
    fig.legend(handles=legend_els, loc="lower center", ncol=3,
               fontsize=10, frameon=True, bbox_to_anchor=(0.5, -0.04))
    fig.tight_layout()
    _save(fig, "14_bfs_dfs_iddfs_comparison.png")


# ---------------------------------------------------------------------------
# 15. Complexity comparison chart
# ---------------------------------------------------------------------------
def plot_complexity_comparison() -> None:
    b = 3  # branching factor
    depths = np.arange(1, 9)

    bfs_time = b ** depths
    bfs_space = b ** depths
    dfs_time = b ** (depths * 1.5)  # assume m = 1.5d for illustration
    dfs_space = b * depths * 1.5
    iddfs_time = b ** depths * 1.1   # ~10% overhead from redundant work
    iddfs_space = b * depths

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(f"Comparación de complejidad (factor de ramificación $b={b}$)",
                 fontsize=13, fontweight="bold")

    # Time
    ax = axes[0]
    ax.semilogy(depths, bfs_time, 'o-', color=COLORS["blue"], label="BFS $O(b^d)$", lw=2)
    ax.semilogy(depths, dfs_time, 's--', color=COLORS["red"], label="DFS $O(b^m)$", lw=2)
    ax.semilogy(depths, iddfs_time, '^:', color=COLORS["green"],
                label="IDDFS $O(b^d)$", lw=2)
    ax.set_xlabel("Profundidad de la solución $d$")
    ax.set_ylabel("Nodos expandidos (escala log)")
    ax.set_title("Complejidad de tiempo")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.4)

    # Space
    ax = axes[1]
    ax.semilogy(depths, bfs_space, 'o-', color=COLORS["blue"],
                label="BFS $O(b^d)$", lw=2)
    ax.semilogy(depths, dfs_space, 's--', color=COLORS["red"],
                label="DFS $O(bm)$", lw=2)
    ax.semilogy(depths, iddfs_space, '^:', color=COLORS["green"],
                label="IDDFS $O(bd)$", lw=2)
    ax.set_xlabel("Profundidad de la solución $d$")
    ax.set_ylabel("Nodos en memoria (escala log)")
    ax.set_title("Complejidad de espacio")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.4)

    fig.tight_layout()
    _save(fig, "13_complexity_comparison.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print("Generando imágenes para 13_simple_search...\n")
    plot_undirected_vs_directed()
    plot_simple_vs_multigraph()
    plot_adjacency_representations()
    plot_path_walk_cycle()
    plot_tree_special_case()
    plot_grid_state_space()
    plot_bfs_step_by_step()
    plot_bfs_frontier_rings()
    plot_bfs_flood_fill()
    plot_dfs_step_by_step()
    plot_dfs_vs_bfs_tree()
    plot_iddfs_levels()
    plot_bfs_dfs_iddfs_comparison()
    plot_complexity_comparison()
    print(f"\n✓ {len(list(IMAGES_DIR.glob('*.png')))} imágenes en {IMAGES_DIR}")


if __name__ == "__main__":
    main()
