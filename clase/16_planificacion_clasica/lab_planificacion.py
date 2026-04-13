#!/usr/bin/env python3
"""
Laboratorio: Planificación Clásica (imágenes para las notas)

Uso:
    cd clase/16_planificacion_clasica
    python3 lab_planificacion.py

Genera 15 imágenes en:
    clase/16_planificacion_clasica/images/

Dependencias: numpy, matplotlib
"""

from pathlib import Path
from collections import deque, namedtuple
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
    "teal":   "#1ABC9C",
    "pink":   "#E91E8C",
}

BLOCK_COLORS = {
    "A": COLORS["blue"],
    "B": COLORS["red"],
    "C": COLORS["green"],
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
# Blocks World helpers
# ---------------------------------------------------------------------------

Action = namedtuple("Action", ["name", "preconditions", "add_list", "delete_list"])


def _make_blocks_world_actions():
    """Return all ground STRIPS actions for 3-block Blocks World (A, B, C)."""
    blocks = ["A", "B", "C"]
    actions = []
    for x in blocks:
        for y in blocks:
            if x == y:
                continue
            for z in blocks:
                if z == x or z == y:
                    continue
                # Mover(X, Y, Z): move X from block Y to block Z
                actions.append(Action(
                    name=f"Mover({x},{y},{z})",
                    preconditions=frozenset({f"On({x},{y})", f"Clear({x})", f"Clear({z})"}),
                    add_list=frozenset({f"On({x},{z})", f"Clear({y})"}),
                    delete_list=frozenset({f"On({x},{y})", f"Clear({z})"}),
                ))
        for y in blocks:
            if x == y:
                continue
            # MoverAMesa(X, Y): move X from block Y to Mesa
            actions.append(Action(
                name=f"MoverAMesa({x},{y})",
                preconditions=frozenset({f"On({x},{y})", f"Clear({x})"}),
                add_list=frozenset({f"On({x},Mesa)", f"Clear({y})"}),
                delete_list=frozenset({f"On({x},{y})"}),
            ))
            # MoverDesdeMesa(X, Y): move X from Mesa onto block Y
            actions.append(Action(
                name=f"MoverDesdeMesa({x},{y})",
                preconditions=frozenset({f"On({x},Mesa)", f"Clear({x})", f"Clear({y})"}),
                add_list=frozenset({f"On({x},{y})"}),
                delete_list=frozenset({f"On({x},Mesa)", f"Clear({y})"}),
            ))
    return actions


def _is_applicable(state, action):
    """Check if action's preconditions are satisfied in state."""
    return action.preconditions.issubset(state)


def _apply_action(state, action):
    """Apply action to state: remove delete_list, add add_list."""
    return (state - action.delete_list) | action.add_list


def _get_applicable(state, all_actions):
    """Return list of applicable actions in state."""
    return [a for a in all_actions if _is_applicable(state, a)]


def _generate_state_space(initial, all_actions):
    """BFS to enumerate all reachable states. Returns (states_list, edges_dict)."""
    visited = {initial}
    queue = deque([initial])
    states_list = [initial]
    # edges: {(from_state, to_state): action_name}
    edges = {}
    while queue:
        s = queue.popleft()
        for a in _get_applicable(s, all_actions):
            ns = _apply_action(s, a)
            if ns not in visited:
                visited.add(ns)
                queue.append(ns)
                states_list.append(ns)
            edges[(s, ns)] = a.name
    return states_list, edges


# ---------------------------------------------------------------------------
# BFS forward planner (for trace images)
# ---------------------------------------------------------------------------

def _bfs_plan(initial, goal, all_actions):
    """BFS forward search. Returns (plan, explored_order, parent_map)."""
    queue = deque([initial])
    visited = {initial}
    parent = {initial: (None, None)}  # state -> (parent_state, action)
    explored_order = []

    while queue:
        s = queue.popleft()
        explored_order.append(s)
        if goal.issubset(s):
            # Reconstruct plan
            plan = []
            cur = s
            while parent[cur][0] is not None:
                ps, act = parent[cur]
                plan.append((ps, act, cur))
                cur = ps
            plan.reverse()
            return plan, explored_order, parent
        for a in _get_applicable(s, all_actions):
            ns = _apply_action(s, a)
            if ns not in visited:
                visited.add(ns)
                parent[ns] = (s, a)
                queue.append(ns)
    return None, explored_order, parent


# ---------------------------------------------------------------------------
# Block drawing helpers
# ---------------------------------------------------------------------------

def _parse_stacks(state):
    """Parse a Blocks World state (frozenset) into a list of stacks.
    Returns list of stacks (bottom-to-top), e.g. [['C','B','A'], ['D']]."""
    # Find what each block is on
    on = {}  # block -> support
    blocks_set = set()
    for prop in state:
        if prop.startswith("On("):
            inner = prop[3:-1]
            parts = inner.split(",")
            block, support = parts[0], parts[1]
            on[block] = support
            blocks_set.add(block)
            if support != "Mesa":
                blocks_set.add(support)

    # Find blocks on Mesa (stack bottoms)
    on_mesa = [b for b in blocks_set if on.get(b) == "Mesa"]
    on_mesa.sort()

    # Also find blocks on Mesa that have nothing on top and aren't supporting anything
    # Build stacks
    # reverse mapping: support -> block on top
    supported_by = {}  # support -> block sitting on it
    for b, s in on.items():
        supported_by[s] = b

    stacks = []
    for base in on_mesa:
        stack = [base]
        cur = base
        while cur in supported_by:
            cur = supported_by[cur]
            stack.append(cur)
        stacks.append(stack)
    return stacks


def _draw_blocks(ax, state, cx, cy, block_w=0.6, block_h=0.4,
                 show_props=False, label=None, highlight_border=None):
    """Draw a Blocks World state as colored rectangles on a mesa line.

    cx, cy: center x, y for the mesa line
    """
    stacks = _parse_stacks(state)
    n_stacks = max(len(stacks), 1)
    total_w = n_stacks * (block_w + 0.3) - 0.3
    start_x = cx - total_w / 2

    # Draw mesa line
    mesa_y = cy
    ax.plot([start_x - 0.2, start_x + total_w + 0.2], [mesa_y, mesa_y],
            color=COLORS["gray"], linewidth=4, solid_capstyle="round")

    # Draw each stack
    for si, stack in enumerate(stacks):
        sx = start_x + si * (block_w + 0.3)
        for bi, block in enumerate(stack):
            by = mesa_y + bi * block_h
            color = BLOCK_COLORS.get(block, COLORS["gray"])
            rect = mpatches.FancyBboxPatch(
                (sx, by), block_w, block_h,
                boxstyle="round,pad=0.03",
                facecolor=color, edgecolor="white", linewidth=2,
            )
            ax.add_patch(rect)
            ax.text(sx + block_w / 2, by + block_h / 2, block,
                    ha="center", va="center", fontsize=13, fontweight="bold",
                    color="white")

    # Optional highlight border around entire configuration
    if highlight_border:
        margin = 0.15
        rect = mpatches.FancyBboxPatch(
            (start_x - 0.2 - margin, mesa_y - 0.15 - margin),
            total_w + 0.4 + 2 * margin,
            max(max(len(s) for s in stacks) if stacks else 1, 1) * block_h + 0.3 + 2 * margin,
            boxstyle="round,pad=0.05",
            facecolor="none", edgecolor=highlight_border, linewidth=3,
            linestyle="--",
        )
        ax.add_patch(rect)

    if label:
        max_h = max(len(s) for s in stacks) if stacks else 1
        ax.text(cx, mesa_y + max_h * block_h + 0.2, label,
                ha="center", va="bottom", fontsize=11, fontweight="bold",
                color=COLORS["dark"])

    if show_props:
        props_text = _state_short(state)
        max_h = max(len(s) for s in stacks) if stacks else 1
        ax.text(cx, mesa_y - 0.35, props_text,
                ha="center", va="top", fontsize=7,
                color=COLORS["gray"], fontstyle="italic",
                bbox=dict(boxstyle="round,pad=0.3", facecolor=COLORS["light"],
                          edgecolor=COLORS["gray"], alpha=0.7))


def _state_short(state):
    """Short string representation of a state."""
    on_props = sorted(p for p in state if p.startswith("On("))
    return "{" + ", ".join(on_props) + "}"


def _state_label(state):
    """Very short label: list On() props only."""
    stacks = _parse_stacks(state)
    parts = []
    for stack in stacks:
        parts.append("/".join(stack))
    return " | ".join(sorted(parts))


# ---------------------------------------------------------------------------
# Image 01: Search vs Planning
# ---------------------------------------------------------------------------

def plot_search_vs_planning():
    """Side-by-side: explicit graph (search) vs implicit action-generated space (planning)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # --- Left: Explicit graph (search, mod 13) ---
    ax1.set_title("Búsqueda (Módulos 13–14)\nGrafo explícito", fontsize=13, fontweight="bold",
                  color=COLORS["blue"])
    ax1.set_xlim(-0.5, 4.5)
    ax1.set_ylim(-0.5, 3.5)
    ax1.set_aspect("equal")
    ax1.axis("off")

    nodes = {"A": (0.5, 3), "B": (2, 3), "C": (3.5, 3),
             "D": (0.5, 1.5), "E": (2, 1.5), "F": (3.5, 1.5),
             "G": (1.25, 0), "H": (2.75, 0)}
    edges = [("A", "B"), ("A", "D"), ("B", "C"), ("B", "E"),
             ("C", "F"), ("D", "G"), ("E", "G"), ("E", "H"), ("F", "H")]

    for (n1, n2) in edges:
        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]
        ax1.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle="-", color=COLORS["gray"], lw=1.5))

    for name, (x, y) in nodes.items():
        circle = plt.Circle((x, y), 0.25, facecolor=COLORS["blue"],
                            edgecolor="white", linewidth=2)
        ax1.add_patch(circle)
        ax1.text(x, y, name, ha="center", va="center",
                fontsize=12, fontweight="bold", color="white")

    # Label
    ax1.text(2, -0.7, "Todos los nodos y aristas\nestán dados de antemano",
             ha="center", va="top", fontsize=10, color=COLORS["dark"],
             bbox=dict(boxstyle="round,pad=0.4", facecolor=COLORS["light"],
                       edgecolor=COLORS["blue"], alpha=0.8))

    # --- Right: Implicit space (planning) ---
    ax2.set_title("Planificación (Módulo 16)\nGrafo implícito — generado por acciones", fontsize=13,
                  fontweight="bold", color=COLORS["green"])
    ax2.set_xlim(-0.5, 4.5)
    ax2.set_ylim(-0.5, 3.5)
    ax2.set_aspect("equal")
    ax2.axis("off")

    # Known nodes (explored)
    known = {"s0": (0.5, 3), "s1": (2, 3), "s2": (3.5, 3),
             "s3": (1.25, 1.5)}
    # Unknown nodes
    unknown = {"?": (3.5, 1.5), "??": (0.5, 0), "???": (2.75, 0)}

    action_labels = [("s0", "s1", "a1"), ("s0", "s3", "a2"),
                     ("s1", "s2", "a3")]
    unknown_edges = [("s2", "?"), ("s3", "??"), ("s3", "???")]

    for (n1, n2, lab) in action_labels:
        x1, y1 = known[n1]
        x2, y2 = known[n2]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax2.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle="->", color=COLORS["green"], lw=2))
        ax2.text(mx + 0.1, my + 0.15, lab, fontsize=9, color=COLORS["green"],
                fontweight="bold")

    for (n1, n2) in unknown_edges:
        x1, y1 = known[n1]
        x2, y2 = unknown[n2]
        ax2.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle="->", color=COLORS["gray"],
                                    lw=1.5, linestyle="dashed"))

    for name, (x, y) in known.items():
        circle = plt.Circle((x, y), 0.25, facecolor=COLORS["green"],
                            edgecolor="white", linewidth=2)
        ax2.add_patch(circle)
        ax2.text(x, y, name, ha="center", va="center",
                fontsize=11, fontweight="bold", color="white")

    for name, (x, y) in unknown.items():
        circle = plt.Circle((x, y), 0.25, facecolor=COLORS["light"],
                            edgecolor=COLORS["gray"], linewidth=2, linestyle="dashed")
        ax2.add_patch(circle)
        ax2.text(x, y, "?", ha="center", va="center",
                fontsize=14, fontweight="bold", color=COLORS["gray"])

    ax2.text(2, -0.7, "Los nodos se descubren\naplicando acciones STRIPS",
             ha="center", va="top", fontsize=10, color=COLORS["dark"],
             bbox=dict(boxstyle="round,pad=0.4", facecolor=COLORS["light"],
                       edgecolor=COLORS["green"], alpha=0.8))

    fig.suptitle("Búsqueda vs Planificación: ¿de dónde viene el grafo?",
                 fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "01_search_vs_planning.png")


# ---------------------------------------------------------------------------
# Image 02: Blocks World initial and goal states
# ---------------------------------------------------------------------------

def plot_blocks_world_states():
    """Initial and goal states as colored blocks + proposition sets."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    initial = frozenset({
        "On(A,Mesa)", "On(B,Mesa)", "On(C,Mesa)",
        "Clear(A)", "Clear(B)", "Clear(C)"
    })
    goal_state = frozenset({
        "On(A,B)", "On(B,C)", "On(C,Mesa)",
        "Clear(A)"
    })

    for ax in (ax1, ax2):
        ax.set_xlim(-1, 3)
        ax.set_ylim(-1.2, 2.5)
        ax.set_aspect("equal")
        ax.axis("off")

    ax1.set_title("Estado Inicial", fontsize=14, fontweight="bold", color=COLORS["dark"])
    _draw_blocks(ax1, initial, 1, 0.3, show_props=True,
                 highlight_border=COLORS["green"])

    ax2.set_title("Estado Meta", fontsize=14, fontweight="bold", color=COLORS["dark"])
    _draw_blocks(ax2, goal_state, 1, 0.3, show_props=True,
                 highlight_border=COLORS["orange"])

    fig.suptitle("Blocks World con 3 bloques: A, B, C",
                 fontsize=15, fontweight="bold", y=1.0)
    fig.tight_layout()
    _save(fig, "02_blocks_world_initial_goal.png")


# ---------------------------------------------------------------------------
# Image 03: STRIPS action anatomy
# ---------------------------------------------------------------------------

def plot_strips_action_anatomy():
    """Anatomy diagram of Mover(B, Mesa, C) with 3 labeled boxes."""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Title
    ax.text(6, 7.5, "Anatomía de una acción STRIPS: MoverDesdeMesa(B, C)",
            ha="center", fontsize=15, fontweight="bold", color=COLORS["dark"])
    ax.text(6, 7.0, '"mover bloque B desde la mesa hacia encima de C"',
            ha="center", fontsize=11, fontstyle="italic", color=COLORS["gray"])

    # Three boxes
    box_specs = [
        {
            "title": "Precondiciones",
            "color": COLORS["blue"],
            "y": 5.0,
            "items": [
                ("On(B, Mesa)", "B está sobre la mesa"),
                ("Clear(B)", "nada encima de B"),
                ("Clear(C)", "nada encima de C"),
            ]
        },
        {
            "title": "Lista Add  (+)",
            "color": COLORS["green"],
            "y": 3.0,
            "items": [
                ("On(B, C)", "ahora B está sobre C"),
            ]
        },
        {
            "title": "Lista Delete  (−)",
            "color": COLORS["red"],
            "y": 1.0,
            "items": [
                ("On(B, Mesa)", "B ya no está en la mesa"),
                ("Clear(C)", "C ya no está libre"),
            ]
        },
    ]

    for spec in box_specs:
        y = spec["y"]
        color = spec["color"]
        # Box
        rect = mpatches.FancyBboxPatch(
            (1, y), 10, 1.5,
            boxstyle="round,pad=0.15",
            facecolor="white", edgecolor=color, linewidth=2.5,
        )
        ax.add_patch(rect)
        # Title
        ax.text(1.5, y + 1.2, spec["title"],
                fontsize=12, fontweight="bold", color=color)
        # Items
        for i, (prop, expl) in enumerate(spec["items"]):
            ax.text(2.0, y + 0.8 - i * 0.35, f"• {prop}",
                    fontsize=10, fontweight="bold", color=COLORS["dark"],
                    fontfamily="monospace")
            ax.text(5.5, y + 0.8 - i * 0.35, f"← {expl}",
                    fontsize=9, color=COLORS["gray"])

    # Note about Clear(Mesa)
    ax.text(6, 0.4,
            "Nota: Mesa nunca necesita Clear — puede sostener infinitos bloques.\n"
            "Por eso MoverAMesa no tiene Clear(Mesa) como precondición.",
            ha="center", fontsize=9, fontstyle="italic", color=COLORS["gray"],
            bbox=dict(boxstyle="round,pad=0.4", facecolor=COLORS["light"],
                      edgecolor=COLORS["gray"], alpha=0.5))

    _save(fig, "03_strips_action_anatomy.png")


# ---------------------------------------------------------------------------
# Image 04: State transition
# ---------------------------------------------------------------------------

def plot_state_transition():
    """One complete state transition: BEFORE → action → AFTER with highlights."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 6),
                             gridspec_kw={"width_ratios": [2, 1, 2]})

    state_before = frozenset({
        "On(A,Mesa)", "On(B,Mesa)", "On(C,Mesa)",
        "Clear(A)", "Clear(B)", "Clear(C)"
    })
    state_after = frozenset({
        "On(A,Mesa)", "On(B,C)", "On(C,Mesa)",
        "Clear(A)", "Clear(B)"
    })

    # Left: BEFORE
    ax1 = axes[0]
    ax1.set_xlim(-1, 3)
    ax1.set_ylim(-2, 2.5)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("ANTES", fontsize=13, fontweight="bold", color=COLORS["dark"])
    _draw_blocks(ax1, state_before, 1, 0.3)

    # Proposition list with coloring
    props_before = [
        ("On(A, Mesa)", "black", "normal"),
        ("On(B, Mesa)", COLORS["red"], "strikethrough"),
        ("On(C, Mesa)", "black", "normal"),
        ("Clear(A)", "black", "normal"),
        ("Clear(B)", "black", "normal"),
        ("Clear(C)", COLORS["red"], "strikethrough"),
    ]
    for i, (prop, color, style) in enumerate(props_before):
        t = ax1.text(1, -0.5 - i * 0.3, prop, fontsize=9,
                     fontfamily="monospace", ha="center", color=color)
        if style == "strikethrough":
            t.set_path_effects([])
            # Draw a line through
            ax1.plot([0.1, 1.9], [-0.5 - i * 0.3, -0.5 - i * 0.3],
                     color=COLORS["red"], linewidth=1.5, alpha=0.7)

    # Middle: ACTION
    ax2 = axes[1]
    ax2.set_xlim(-1, 3)
    ax2.set_ylim(-2, 2.5)
    ax2.set_aspect("equal")
    ax2.axis("off")

    # Arrow
    ax2.annotate("", xy=(2.2, 0.8), xytext=(-0.2, 0.8),
                 arrowprops=dict(arrowstyle="->", color=COLORS["orange"],
                                lw=3, mutation_scale=20))
    # Action label
    action_box = mpatches.FancyBboxPatch(
        (-0.3, 1.2), 2.6, 0.8,
        boxstyle="round,pad=0.15",
        facecolor=COLORS["orange"], edgecolor="white", linewidth=2,
        alpha=0.9,
    )
    ax2.add_patch(action_box)
    ax2.text(1, 1.6, "MoverDesdeMesa\n(B, C)", ha="center", va="center",
             fontsize=11, fontweight="bold", color="white")

    # Delete / Add annotations
    ax2.text(1, 0.2, "− Delete:", ha="center", fontsize=9,
             fontweight="bold", color=COLORS["red"])
    ax2.text(1, -0.1, "On(B,Mesa), Clear(C)", ha="center", fontsize=8,
             fontfamily="monospace", color=COLORS["red"])
    ax2.text(1, -0.6, "+ Add:", ha="center", fontsize=9,
             fontweight="bold", color=COLORS["green"])
    ax2.text(1, -0.9, "On(B,C)", ha="center", fontsize=8,
             fontfamily="monospace", color=COLORS["green"])

    # Right: AFTER
    ax3 = axes[2]
    ax3.set_xlim(-1, 3)
    ax3.set_ylim(-2, 2.5)
    ax3.set_aspect("equal")
    ax3.axis("off")
    ax3.set_title("DESPUÉS", fontsize=13, fontweight="bold", color=COLORS["dark"])
    _draw_blocks(ax3, state_after, 1, 0.3)

    props_after = [
        ("On(A, Mesa)", "black"),
        ("On(B, C)", COLORS["green"]),
        ("On(C, Mesa)", "black"),
        ("Clear(A)", "black"),
        ("Clear(B)", "black"),
    ]
    for i, (prop, color) in enumerate(props_after):
        ax3.text(1, -0.5 - i * 0.3, prop, fontsize=9,
                 fontfamily="monospace", ha="center", color=color,
                 fontweight="bold" if color == COLORS["green"] else "normal")

    fig.suptitle("Transición de estado: aplicar MoverDesdeMesa(B, C)",
                 fontsize=14, fontweight="bold", y=1.0)
    fig.tight_layout()
    _save(fig, "04_state_transition.png")


# ---------------------------------------------------------------------------
# Image 05: Complete state space
# ---------------------------------------------------------------------------

def plot_blocks_world_state_space():
    """Complete ~13-state graph for 3 blocks with block diagrams as nodes."""
    all_actions = _make_blocks_world_actions()
    initial = frozenset({
        "On(A,Mesa)", "On(B,Mesa)", "On(C,Mesa)",
        "Clear(A)", "Clear(B)", "Clear(C)"
    })
    goal = frozenset({"On(A,B)", "On(B,C)", "On(C,Mesa)", "Clear(A)"})

    states, edges = _generate_state_space(initial, all_actions)

    # Assign positions using a manual layout based on state structure
    # Group by "number of blocks on mesa"
    # 3 on mesa: 1 state
    # 2 on mesa: 6 states (one block on another)
    # 1 on mesa: 6 states (tower of 3)

    def _count_on_mesa(s):
        return sum(1 for p in s if p.startswith("On(") and p.endswith(",Mesa)"))

    groups = {3: [], 2: [], 1: []}
    for s in states:
        n = _count_on_mesa(s)
        groups[n].append(s)

    # Assign positions
    pos = {}
    # Row 0 (top): 3 on mesa
    for i, s in enumerate(sorted(groups[3], key=str)):
        pos[s] = (6, 8)

    # Row 1 (middle): 2 on mesa
    g2 = sorted(groups[2], key=str)
    for i, s in enumerate(g2):
        pos[s] = (1 + i * 2, 4.5)

    # Row 2 (bottom): 1 on mesa
    g1 = sorted(groups[1], key=str)
    for i, s in enumerate(g1):
        pos[s] = (1 + i * 2, 1)

    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(-0.5, 13)
    ax.set_ylim(-0.5, 10)
    ax.axis("off")
    ax.set_title("Espacio de estados completo: Blocks World (3 bloques)",
                 fontsize=15, fontweight="bold", pad=20)

    # Draw edges first (behind nodes)
    drawn_edges = set()
    for (s1, s2), aname in edges.items():
        if (s2, s1) in drawn_edges:
            continue
        drawn_edges.add((s1, s2))
        x1, y1 = pos[s1]
        x2, y2 = pos[s2]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle="-", color=COLORS["gray"],
                                    lw=0.8, alpha=0.5))

    # Draw nodes (small block diagrams)
    for s in states:
        x, y = pos[s]
        border = None
        if s == initial:
            border = COLORS["green"]
        elif goal.issubset(s):
            border = COLORS["orange"]
        _draw_blocks(ax, s, x, y, block_w=0.45, block_h=0.3,
                     highlight_border=border)

    # Legend
    ax.text(11.5, 9, "Leyenda:", fontsize=11, fontweight="bold", color=COLORS["dark"])
    rect_init = mpatches.FancyBboxPatch((11, 8.2), 1.5, 0.4,
        boxstyle="round,pad=0.05", facecolor="none",
        edgecolor=COLORS["green"], linewidth=2, linestyle="--")
    ax.add_patch(rect_init)
    ax.text(12.8, 8.4, "Estado inicial", fontsize=9, color=COLORS["green"],
            va="center")

    rect_goal = mpatches.FancyBboxPatch((11, 7.5), 1.5, 0.4,
        boxstyle="round,pad=0.05", facecolor="none",
        edgecolor=COLORS["orange"], linewidth=2, linestyle="--")
    ax.add_patch(rect_goal)
    ax.text(12.8, 7.7, "Estado meta", fontsize=9, color=COLORS["orange"],
            va="center")

    ax.text(6, -0.3, f"Total: {len(states)} estados alcanzables, "
            f"{len(drawn_edges)} transiciones",
            ha="center", fontsize=11, color=COLORS["dark"])

    _save(fig, "05_blocks_world_state_space.png")


# ---------------------------------------------------------------------------
# Image 06: Forward search vs generic search
# ---------------------------------------------------------------------------

def plot_forward_vs_generic():
    """Side-by-side pseudocode comparison with 3 highlighted differences."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))

    generic_lines = [
        ("function GENERIC-SEARCH(problema):", False),
        ("", False),
        ("  frontera ← {problema.inicio}", False),
        ("  explorado ← ∅", False),
        ("  padre ← {inicio: null}", False),
        ("", False),
        ("  while frontera ≠ ∅:", False),
        ("    n ← frontera.pop()", False),
        ("", False),
        ("    if problema.es_meta(n):", True),     # D1
        ("      return camino(padre, n)", False),
        ("", False),
        ("    explorado.add(n)", False),
        ("", False),
        ("    for v in problema.vecinos(n):", True),  # D2+D3
        ("      // (transición implícita)", True),
        ("", False),
        ("      if v ∉ explorado ∪ frontera:", False),
        ("        padre[v] ← n", False),
        ("        frontera.push(v)", False),
        ("", False),
        ("  return FAILURE", False),
    ]

    planning_lines = [
        ("function FORWARD-PLANNING(problema):", False),
        ("", False),
        ("  frontera ← {problema.s₀}", False),
        ("  explorado ← ∅", False),
        ("  padre ← {s₀: null}", False),
        ("", False),
        ("  while frontera ≠ ∅:", False),
        ("    s ← frontera.pop()", False),
        ("", False),
        ("    if problema.meta ⊆ s:        [D1]", True),
        ("      return plan(padre, s)", False),
        ("", False),
        ("    explorado.add(s)", False),
        ("", False),
        ("    for a in aplicables(s):      [D2]", True),
        ("      v ← aplicar(s, a)         [D3]", True),
        ("", False),
        ("      if v ∉ explorado ∪ frontera:", False),
        ("        padre[v] ← (s, a)", False),
        ("        frontera.push(v)", False),
        ("", False),
        ("  return FAILURE", False),
    ]

    for ax, lines, title, color in [
        (ax1, generic_lines, "GENERIC-SEARCH (Módulo 13)", COLORS["blue"]),
        (ax2, planning_lines, "FORWARD-PLANNING (Módulo 16)", COLORS["green"]),
    ]:
        ax.set_xlim(0, 10)
        ax.set_ylim(-0.5, len(lines) + 1)
        ax.axis("off")
        ax.set_title(title, fontsize=13, fontweight="bold", color=color, pad=10)

        for i, (text, is_diff) in enumerate(lines):
            y = len(lines) - i
            bg_color = "#FFF3CD" if is_diff else "white"
            if text:
                ax.text(0.3, y, text, fontsize=9.5, fontfamily="monospace",
                        va="center",
                        bbox=dict(boxstyle="round,pad=0.15",
                                  facecolor=bg_color,
                                  edgecolor=COLORS["orange"] if is_diff else "none",
                                  linewidth=1.5 if is_diff else 0,
                                  alpha=0.9))

    # Legend at bottom
    fig.text(0.5, 0.02,
             "[D1] Meta = subconjunto de proposiciones    "
             "[D2] Vecinos = acciones con precondiciones satisfechas    "
             "[D3] Transición = aplicar add/delete",
             ha="center", fontsize=10, color=COLORS["dark"],
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF3CD",
                       edgecolor=COLORS["orange"], alpha=0.8))

    fig.suptitle("El mismo algoritmo — 3 líneas cambian",
                 fontsize=15, fontweight="bold", y=0.98)
    fig.tight_layout(rect=[0, 0.06, 1, 0.95])
    _save(fig, "06_forward_search_vs_generic.png")


# ---------------------------------------------------------------------------
# Image 07: Forward search trace (BFS tree)
# ---------------------------------------------------------------------------

def plot_forward_search_trace():
    """BFS search tree with explored/frontier/solution marked."""
    all_actions = _make_blocks_world_actions()
    initial = frozenset({
        "On(A,Mesa)", "On(B,Mesa)", "On(C,Mesa)",
        "Clear(A)", "Clear(B)", "Clear(C)"
    })
    goal = frozenset({"On(A,B)", "On(B,C)", "On(C,Mesa)", "Clear(A)"})

    plan, explored_order, parent = _bfs_plan(initial, goal, all_actions)

    # Build BFS tree for visualization
    # We'll show the first ~12 explored states
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.axis("off")
    ax.set_title("Traza de búsqueda hacia adelante (BFS) en Blocks World",
                 fontsize=14, fontweight="bold", pad=15)

    # Build tree structure
    children = {}  # parent_state -> [(child_state, action)]
    for s, (ps, act) in parent.items():
        if ps is not None:
            if ps not in children:
                children[ps] = []
            children[ps].append((s, act))

    # Get solution path states
    solution_states = {initial}
    if plan:
        for (ps, act, ns) in plan:
            solution_states.add(ps)
            solution_states.add(ns)

    # Layout: BFS levels
    levels = {initial: 0}
    queue = deque([initial])
    while queue:
        s = queue.popleft()
        for cs, _ in children.get(s, []):
            levels[cs] = levels[s] + 1
            queue.append(cs)

    # Position nodes by level
    level_nodes = {}
    for s, lv in levels.items():
        if lv not in level_nodes:
            level_nodes[lv] = []
        level_nodes[lv].append(s)

    positions = {}
    max_level = max(level_nodes.keys()) if level_nodes else 0
    for lv, nodes_at_level in level_nodes.items():
        n = len(nodes_at_level)
        for i, s in enumerate(nodes_at_level):
            x = (i + 0.5) * 14 / max(n, 1)
            y = 8 - lv * 2.5
            positions[s] = (x, y)

    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(-2, 10)

    # Draw edges
    for s, clist in children.items():
        if s not in positions:
            continue
        x1, y1 = positions[s]
        for cs, act in clist:
            if cs not in positions:
                continue
            x2, y2 = positions[cs]
            is_solution = s in solution_states and cs in solution_states
            color = COLORS["green"] if is_solution else COLORS["gray"]
            lw = 2.5 if is_solution else 1
            ax.annotate("", xy=(x2, y2 + 0.4), xytext=(x1, y1 - 0.4),
                        arrowprops=dict(arrowstyle="->", color=color, lw=lw))
            # Short action label
            short = act.name.split("(")[0][:6]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my + 0.1, short, fontsize=6,
                    color=color, ha="center", rotation=0)

    # Draw nodes
    for i, s in enumerate(explored_order):
        if s not in positions:
            continue
        x, y = positions[s]
        is_sol = s in solution_states
        is_goal = goal.issubset(s)

        if is_goal:
            node_color = COLORS["orange"]
        elif is_sol:
            node_color = COLORS["green"]
        else:
            node_color = COLORS["blue"]

        _draw_blocks(ax, s, x, y, block_w=0.35, block_h=0.25)

        # Step number
        ax.text(x - 0.8, y + 0.3, f"({i+1})", fontsize=8,
                fontweight="bold", color=node_color)

    # Legend
    ax.text(0, -1.5, "●  Azul = explorado    ", fontsize=9, color=COLORS["blue"])
    ax.text(4, -1.5, "●  Verde = camino solución    ", fontsize=9, color=COLORS["green"])
    ax.text(9, -1.5, "●  Naranja = meta encontrada", fontsize=9, color=COLORS["orange"])

    _save(fig, "07_forward_search_trace.png")


# ---------------------------------------------------------------------------
# Image 08: Plan found (comic strip)
# ---------------------------------------------------------------------------

def plot_plan_found():
    """Solution plan as horizontal sequence of block diagrams."""
    all_actions = _make_blocks_world_actions()
    initial = frozenset({
        "On(A,Mesa)", "On(B,Mesa)", "On(C,Mesa)",
        "Clear(A)", "Clear(B)", "Clear(C)"
    })
    goal = frozenset({"On(A,B)", "On(B,C)", "On(C,Mesa)", "Clear(A)"})

    plan, _, _ = _bfs_plan(initial, goal, all_actions)

    # Collect states along plan
    plan_states = [initial]
    plan_actions = []
    cur = initial
    if plan:
        for (ps, act, ns) in plan:
            plan_actions.append(act.name)
            plan_states.append(ns)

    n_steps = len(plan_states)
    fig, axes = plt.subplots(1, n_steps, figsize=(5 * n_steps, 5))
    if n_steps == 1:
        axes = [axes]

    for i, (ax, s) in enumerate(zip(axes, plan_states)):
        ax.set_xlim(-1, 3)
        ax.set_ylim(-1, 2.5)
        ax.set_aspect("equal")
        ax.axis("off")

        if i == 0:
            label = "Estado inicial"
            border_c = COLORS["green"]
        elif i == n_steps - 1:
            label = "¡Meta!"
            border_c = COLORS["orange"]
        else:
            label = f"Paso {i}"
            border_c = None

        _draw_blocks(ax, s, 1, 0.3, block_w=0.55, block_h=0.4,
                     highlight_border=border_c, label=label)

        # Action arrow between panels
        if i < n_steps - 1:
            ax.text(2.7, 0.8, "→", fontsize=30, color=COLORS["orange"],
                    fontweight="bold", ha="center", va="center")
            # Action name
            act_short = plan_actions[i].replace("MoverDesdeMesa", "DesdeMesa")
            ax.text(2.7, 0.2, act_short, fontsize=8,
                    color=COLORS["dark"], ha="center", rotation=0,
                    bbox=dict(boxstyle="round,pad=0.2",
                              facecolor=COLORS["light"],
                              edgecolor=COLORS["orange"]))

    fig.suptitle("Plan encontrado por búsqueda hacia adelante (BFS)",
                 fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "08_plan_found.png")


# ---------------------------------------------------------------------------
# Image 09: State space explosion
# ---------------------------------------------------------------------------

def plot_state_space_explosion():
    """Log-scale bar chart: states vs number of blocks."""
    # Approximate number of states for n blocks in Blocks World
    # Each block can be on any of the n-1 other blocks or on the table,
    # but stacking constraints limit this. Exact count: sum over partitions.
    # We use the formula: states(n) ≈ sum_{k=1}^{n} C(n,k) * k! * states(n-k)
    # Simpler approximation: n! * sum_{k=0}^{n-1} 1/k! ≈ e * n! (Flajolet)
    import math
    n_blocks = [3, 5, 10, 15, 20]
    # Exact for small n, factorial approximation for large
    exact = {3: 13, 5: 501}
    states = []
    for n in n_blocks:
        if n in exact:
            states.append(exact[n])
        else:
            # e * n! is a good approximation for total ordered forests
            states.append(int(math.e * math.factorial(n)))

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar([str(n) for n in n_blocks],
                  [np.log10(s) for s in states],
                  color=[COLORS["green"] if s < 1e6 else
                         COLORS["orange"] if s < 1e12 else
                         COLORS["red"]
                         for s in states],
                  edgecolor="white", linewidth=2)

    # Labels on bars
    for bar, s in zip(bars, states):
        h = bar.get_height()
        if s < 1e6:
            label = f"{s:,}"
        else:
            label = f"~10^{int(np.log10(s))}"
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.3,
                label, ha="center", fontsize=11, fontweight="bold",
                color=COLORS["dark"])

    # BFS feasible line
    bfs_limit = 6  # 10^6 ~ feasible for BFS
    ax.axhline(y=bfs_limit, color=COLORS["blue"], linestyle="--", linewidth=2)
    ax.text(4.2, bfs_limit + 0.3, "BFS factible (~10^6 estados)",
            fontsize=10, color=COLORS["blue"], fontweight="bold")

    ax.set_xlabel("Número de bloques", fontsize=12)
    ax.set_ylabel("log₁₀(estados alcanzables)", fontsize=12)
    ax.set_title("Explosión del espacio de estados en Blocks World",
                 fontsize=14, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    _save(fig, "09_state_space_explosion.png")


# ---------------------------------------------------------------------------
# Image 10: Relaxed problem comparison
# ---------------------------------------------------------------------------

def plot_relaxed_problem():
    """Side-by-side: normal planning vs relaxed (no delete lists)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # --- Left: Normal planning ---
    ax1.set_title("Planificación normal\n(con listas Delete)", fontsize=13,
                  fontweight="bold", color=COLORS["blue"])
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 8)
    ax1.axis("off")

    normal_steps = [
        ("Estado 0", "{On(A,M), On(B,M), On(C,M),\n Clear(A), Clear(B), Clear(C)}", 7),
        ("MoverDesdeMesa(B,C)", None, 5.8),
        ("Estado 1", "{On(A,M), On(B,C), On(C,M),\n Clear(A), Clear(B)}", 5),
        ("MoverDesdeMesa(A,B)", None, 3.8),
        ("Estado 2", "{On(A,B), On(B,C), On(C,M),\n Clear(A)}", 3),
    ]

    for label, content, y in normal_steps:
        if content:
            ax1.text(5, y, content, ha="center", va="center", fontsize=8,
                     fontfamily="monospace",
                     bbox=dict(boxstyle="round,pad=0.4", facecolor=COLORS["light"],
                               edgecolor=COLORS["blue"], linewidth=1.5))
            ax1.text(0.5, y, label, fontsize=9, fontweight="bold",
                     color=COLORS["dark"], va="center")
        else:
            ax1.text(5, y, f"↓ {label}", ha="center", fontsize=9,
                     fontweight="bold", color=COLORS["orange"])

    # Highlight deleted props
    ax1.text(5, 1.8, "Clear(C) desaparece en paso 1\n"
             "Clear(B) desaparece en paso 2\n"
             "On(B,Mesa) desaparece en paso 1",
             ha="center", fontsize=8, fontstyle="italic", color=COLORS["red"],
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FDEDEC",
                       edgecolor=COLORS["red"], alpha=0.7))

    # --- Right: Relaxed planning ---
    ax2.set_title("Planificación relajada\n(sin listas Delete — ignoradas)", fontsize=13,
                  fontweight="bold", color=COLORS["green"])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 8)
    ax2.axis("off")

    relaxed_steps = [
        ("Estado 0", "{On(A,M), On(B,M), On(C,M),\n Clear(A), Clear(B), Clear(C)}", 7),
        ("MoverDesdeMesa(B,C)", None, 5.8),
        ("Estado 1'", "{On(A,M), On(B,M), On(B,C), On(C,M),\n Clear(A), Clear(B), Clear(C)}", 5),
        ("MoverDesdeMesa(A,B)", None, 3.8),
        ("Estado 2'", "{On(A,M), On(A,B), On(B,M), On(B,C),\n On(C,M), Clear(A), Clear(B), Clear(C)}", 3),
    ]

    for label, content, y in relaxed_steps:
        if content:
            ax2.text(5, y, content, ha="center", va="center", fontsize=8,
                     fontfamily="monospace",
                     bbox=dict(boxstyle="round,pad=0.4", facecolor="#EAFAF1",
                               edgecolor=COLORS["green"], linewidth=1.5))
            ax2.text(0.3, y, label, fontsize=9, fontweight="bold",
                     color=COLORS["dark"], va="center")
        else:
            ax2.text(5, y, f"↓ {label}", ha="center", fontsize=9,
                     fontweight="bold", color=COLORS["orange"])

    ax2.text(5, 1.8, "Nada desaparece — solo se acumulan\n"
             "proposiciones. El estado solo CRECE.\n"
             "h(s) = longitud del plan relajado ≤ h*(s)",
             ha="center", fontsize=8, fontstyle="italic", color=COLORS["green"],
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#EAFAF1",
                       edgecolor=COLORS["green"], alpha=0.7))

    fig.suptitle("Relajación: ignorar listas Delete → heurística admisible",
                 fontsize=14, fontweight="bold", y=1.0)
    fig.tight_layout()
    _save(fig, "10_relaxed_problem.png")


# ---------------------------------------------------------------------------
# Plot 11 – Forward vs backward search direction
# ---------------------------------------------------------------------------

def plot_forward_vs_backward():
    """Side-by-side diagram showing forward (s0→G) vs backward (G→s0) search."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    all_actions = _make_blocks_world_actions()
    s0 = frozenset({
        "On(A,Mesa)", "On(B,Mesa)", "On(C,Mesa)",
        "Clear(A)", "Clear(B)", "Clear(C)",
    })
    goal = frozenset({
        "On(A,B)", "On(B,C)", "On(C,Mesa)", "Clear(A)",
    })

    # ── Left panel: Forward ──────────────────────────────────────────────
    ax1.set_xlim(-0.5, 10.5)
    ax1.set_ylim(-0.5, 6)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("Búsqueda hacia adelante (forward)", fontsize=13,
                   fontweight="bold", color=COLORS["blue"])

    # Draw s0
    _draw_blocks(ax1, s0, 1.5, 0.5, block_w=0.5, block_h=0.35,
                 highlight_border=COLORS["green"])
    ax1.text(1.5, 0.1, "$s_0$", ha="center", fontsize=12, fontweight="bold",
             color=COLORS["green"])

    # Draw goal
    _draw_blocks(ax1, goal, 8.5, 0.5, block_w=0.5, block_h=0.35,
                 highlight_border=COLORS["orange"])
    ax1.text(8.5, 0.1, "$G$", ha="center", fontsize=12, fontweight="bold",
             color=COLORS["orange"])

    # Arrow s0 -> G
    ax1.annotate("", xy=(6.8, 1.2), xytext=(3.2, 1.2),
                 arrowprops=dict(arrowstyle="-|>", lw=3, color=COLORS["blue"],
                                 connectionstyle="arc3,rad=0.15"))
    ax1.text(5.0, 2.0, "Aplica acciones\n(Pre ⊆ s)", ha="center", fontsize=10,
             color=COLORS["blue"], fontstyle="italic")

    # Intermediate state bubble
    ax1.text(5.0, 1.2, "estados\ncompletos", ha="center", va="center",
             fontsize=9, color=COLORS["dark"],
             bbox=dict(boxstyle="round,pad=0.4", facecolor=COLORS["light"],
                       edgecolor=COLORS["blue"], linewidth=1.5))

    # Labels
    ax1.text(5.0, 4.5, "Pregunta: ¿qué puedo hacer desde aquí?",
             ha="center", fontsize=10, fontweight="bold", color=COLORS["dark"])
    ax1.text(5.0, 3.8, "Termina cuando:  $G \\subseteq s$",
             ha="center", fontsize=10, color=COLORS["dark"])

    # ── Right panel: Backward ────────────────────────────────────────────
    ax2.set_xlim(-0.5, 10.5)
    ax2.set_ylim(-0.5, 6)
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_title("Búsqueda hacia atrás (backward)", fontsize=13,
                   fontweight="bold", color=COLORS["orange"])

    # Draw s0
    _draw_blocks(ax2, s0, 1.5, 0.5, block_w=0.5, block_h=0.35,
                 highlight_border=COLORS["green"])
    ax2.text(1.5, 0.1, "$s_0$", ha="center", fontsize=12, fontweight="bold",
             color=COLORS["green"])

    # Draw goal
    _draw_blocks(ax2, goal, 8.5, 0.5, block_w=0.5, block_h=0.35,
                 highlight_border=COLORS["orange"])
    ax2.text(8.5, 0.1, "$G$", ha="center", fontsize=12, fontweight="bold",
             color=COLORS["orange"])

    # Arrow G -> s0
    ax2.annotate("", xy=(3.2, 1.2), xytext=(6.8, 1.2),
                 arrowprops=dict(arrowstyle="-|>", lw=3, color=COLORS["orange"],
                                 connectionstyle="arc3,rad=0.15"))
    ax2.text(5.0, 2.0, "Regresión\n(g − Add) ∪ Pre", ha="center", fontsize=10,
             color=COLORS["orange"], fontstyle="italic")

    # Intermediate subgoal bubble
    ax2.text(5.0, 1.2, "sub-\nobjetivos", ha="center", va="center",
             fontsize=9, color=COLORS["dark"],
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF3E0",
                       edgecolor=COLORS["orange"], linewidth=1.5))

    # Labels
    ax2.text(5.0, 4.5, "Pregunta: ¿qué acción pudo producir esto?",
             ha="center", fontsize=10, fontweight="bold", color=COLORS["dark"])
    ax2.text(5.0, 3.8, "Termina cuando:  $g \\subseteq s_0$",
             ha="center", fontsize=10, color=COLORS["dark"])

    fig.suptitle("Dos direcciones de búsqueda en planificación",
                 fontsize=14, fontweight="bold", y=1.0)
    fig.tight_layout()
    _save(fig, "11_forward_vs_backward.png")


# ---------------------------------------------------------------------------
# Plot 12 – Regression trace on Blocks World
# ---------------------------------------------------------------------------

def plot_regression_trace():
    """Show the 2-step regression from G back to s0 in Blocks World."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 7))
    ax.set_xlim(-0.5, 14)
    ax.set_ylim(-1, 7.5)
    ax.set_aspect("equal")
    ax.axis("off")

    # Define the three subgoals
    g0_props = "{ On(A,B), On(B,C),\n  On(C,Mesa), Clear(A) }"
    g1_props = "{ On(A,Mesa), On(B,C),\n  On(C,Mesa), Clear(A),\n  Clear(B) }"
    g2_props = "{ On(A,Mesa), On(B,Mesa),\n  On(C,Mesa), Clear(A),\n  Clear(B), Clear(C) }"

    subgoals = [
        ("$g_0 = G$", g0_props, 11.5, 3.5, COLORS["orange"], "#FFF3E0"),
        ("$g_1$", g1_props, 6.5, 3.5, COLORS["purple"], "#F3E5F5"),
        ("$g_2 = s_0$", g2_props, 1.5, 3.5, COLORS["green"], "#E8F5E9"),
    ]

    box_w, box_h = 4.0, 2.8

    for label, props, cx, cy, border_col, fill_col in subgoals:
        # Box
        rect = mpatches.FancyBboxPatch(
            (cx - box_w / 2, cy - box_h / 2), box_w, box_h,
            boxstyle="round,pad=0.15", facecolor=fill_col,
            edgecolor=border_col, linewidth=2.5,
        )
        ax.add_patch(rect)

        # Label above
        ax.text(cx, cy + box_h / 2 + 0.3, label, ha="center", fontsize=13,
                fontweight="bold", color=border_col)

        # Props inside
        ax.text(cx, cy, props, ha="center", va="center", fontsize=9,
                fontfamily="monospace", color=COLORS["dark"])

    # Arrow from g0 to g1 (regression direction: right to left)
    ax.annotate("", xy=(8.7, 3.5), xytext=(9.3, 3.5),
                arrowprops=dict(arrowstyle="-|>", lw=2.5, color=COLORS["orange"]))
    ax.text(9.0, 5.5, "MoverDesdeMesa(A,B)", ha="center", fontsize=11,
            fontweight="bold", color=COLORS["dark"],
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF3E0",
                      edgecolor=COLORS["orange"], linewidth=1.5))
    ax.annotate("", xy=(9.0, 5.1), xytext=(9.0, 4.2),
                arrowprops=dict(arrowstyle="-", lw=1, color=COLORS["gray"],
                                linestyle="--"))

    # Arrow from g1 to g2
    ax.annotate("", xy=(3.7, 3.5), xytext=(4.3, 3.5),
                arrowprops=dict(arrowstyle="-|>", lw=2.5, color=COLORS["orange"]))
    ax.text(4.0, 5.5, "MoverDesdeMesa(B,C)", ha="center", fontsize=11,
            fontweight="bold", color=COLORS["dark"],
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#F3E5F5",
                      edgecolor=COLORS["purple"], linewidth=1.5))
    ax.annotate("", xy=(4.0, 5.1), xytext=(4.0, 4.2),
                arrowprops=dict(arrowstyle="-", lw=1, color=COLORS["gray"],
                                linestyle="--"))

    # Title and direction label
    ax.text(7.0, 7.0, "Regresión: de la meta $G$ al estado inicial $s_0$",
            ha="center", fontsize=14, fontweight="bold", color=COLORS["dark"])

    # Direction arrow at bottom
    ax.annotate("", xy=(2.5, -0.3), xytext=(11.0, -0.3),
                arrowprops=dict(arrowstyle="-|>", lw=2, color=COLORS["orange"],
                                linestyle="--"))
    ax.text(6.75, -0.7, "dirección de regresión", ha="center", fontsize=10,
            color=COLORS["orange"], fontstyle="italic")

    # Execution direction at bottom
    ax.annotate("", xy=(11.0, -0.3), xytext=(2.5, -0.3),
                arrowprops=dict(arrowstyle="-|>", lw=2, color=COLORS["blue"],
                                linestyle="-"))
    ax.text(6.75, 0.1, "dirección de ejecución del plan →",
            ha="center", fontsize=9, color=COLORS["blue"], fontstyle="italic")

    # Check mark on g2
    ax.text(1.5, 1.7, "$g_2 \\subseteq s_0$  ✓", ha="center", fontsize=12,
            fontweight="bold", color=COLORS["green"])

    fig.tight_layout()
    _save(fig, "12_regression_trace.png")


# ---------------------------------------------------------------------------
# Plot 13 – Forward vs backward branching factor
# ---------------------------------------------------------------------------

def plot_forward_vs_backward_branching():
    """Tree diagrams showing forward (wide) vs backward (narrow) branching."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    def _draw_tree(ax, levels, title, color, direction_label):
        """Draw a schematic search tree.
        levels: list of (num_nodes, y_position) tuples from top to bottom.
        """
        ax.set_xlim(-1, 11)
        ax.set_ylim(-0.5, 8.5)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=13, fontweight="bold", color=color)

        prev_positions = None
        for i, (n_nodes, y) in enumerate(levels):
            # Distribute nodes evenly
            if n_nodes == 1:
                positions = [5.0]
            else:
                margin = 0.5
                positions = [margin + j * (10 - 2 * margin) / (n_nodes - 1)
                             for j in range(n_nodes)]

            # Draw edges from previous level
            if prev_positions is not None:
                for px in prev_positions:
                    for cx in positions:
                        ax.plot([px, cx], [prev_y, y], color=COLORS["gray"],
                                linewidth=0.5, alpha=0.4, zorder=1)

            # Draw nodes
            node_r = 0.2
            for x in positions:
                circle = plt.Circle((x, y), node_r, facecolor=color,
                                    edgecolor="white", linewidth=1.5, zorder=2,
                                    alpha=0.7)
                ax.add_patch(circle)

            prev_positions = positions
            prev_y = y

        # Labels
        ax.text(5.0, levels[0][1] + 0.6, direction_label, ha="center",
                fontsize=10, fontstyle="italic", color=COLORS["dark"])

    # Forward: wide branching from s0
    forward_levels = [
        (1, 7.5),    # s0
        (6, 6.0),    # 6 MoverDesdeMesa from initial
        (6, 4.5),    # ~3 per state, some duplicates
        (6, 3.0),    # towers (dead ends mostly)
    ]
    _draw_tree(ax1, forward_levels, "Forward: factor de ramificación alto",
               COLORS["blue"], "desde $s_0$: 6 acciones aplicables")

    ax1.text(5.0, 7.9, "$s_0$", ha="center", fontsize=12, fontweight="bold",
             color=COLORS["green"])
    ax1.text(5.0, 2.2, "…muchos nodos antes de llegar a $G$",
             ha="center", fontsize=9, color=COLORS["gray"], fontstyle="italic")

    # Backward: narrow branching from G
    backward_levels = [
        (1, 7.5),    # G
        (3, 6.0),    # few relevant actions
        (3, 4.5),    # still few
        (1, 3.0),    # reaches s0
    ]
    _draw_tree(ax2, backward_levels, "Backward: factor de ramificación bajo",
               COLORS["orange"], "desde $G$: 2-3 acciones relevantes")

    ax2.text(5.0, 7.9, "$G$", ha="center", fontsize=12, fontweight="bold",
             color=COLORS["orange"])
    ax2.text(5.0, 2.2, "…llega a $s_0$ explorando menos nodos",
             ha="center", fontsize=9, color=COLORS["gray"], fontstyle="italic")

    # Checkmark at bottom of backward tree
    ax2.text(5.0, 2.6, "$s_0$ ✓", ha="center", fontsize=11, fontweight="bold",
             color=COLORS["green"])

    fig.suptitle("Factor de ramificación: forward (amplio) vs backward (angosto)",
                 fontsize=14, fontweight="bold", y=1.0)
    fig.tight_layout()
    _save(fig, "13_forward_vs_backward_branching.png")


# ---------------------------------------------------------------------------
# Plot 14 – Forward apply vs backward regress (same action, two perspectives)
# ---------------------------------------------------------------------------

def plot_apply_vs_regress():
    """Side-by-side: apply(s0, a) forward vs regress(G, a) backward for the
    same action MoverDesdeMesa(A,B), showing which propositions are removed
    and which are added in each case."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))

    def _draw_prop_box(ax, cx, cy, props, title, border_col, fill_col,
                       removed=None, added=None, w=3.8, h_per_line=0.45):
        """Draw a box with a list of propositions, marking removed/added."""
        removed = removed or set()
        added = added or set()
        n = len(props)
        h = max(n * h_per_line + 0.6, 2.0)

        rect = mpatches.FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.12", facecolor=fill_col,
            edgecolor=border_col, linewidth=2.0)
        ax.add_patch(rect)

        ax.text(cx, cy + h / 2 + 0.25, title, ha="center", fontsize=10,
                fontweight="bold", color=border_col)

        y_start = cy + h / 2 - 0.45
        for i, p in enumerate(props):
            y = y_start - i * h_per_line
            if p in removed:
                ax.text(cx, y, p, ha="center", va="center", fontsize=8.5,
                        fontfamily="monospace", color=COLORS["red"],
                        fontstyle="italic",
                        path_effects=[pe.withStroke(linewidth=0, foreground="none")])
                # Strikethrough line
                tw = len(p) * 0.065
                ax.plot([cx - tw, cx + tw], [y, y],
                        color=COLORS["red"], linewidth=1.5, alpha=0.7)
                ax.text(cx + tw + 0.15, y, "[del]", ha="left", va="center",
                        fontsize=6, color=COLORS["red"])
            elif p in added:
                ax.text(cx, y, p, ha="center", va="center", fontsize=8.5,
                        fontfamily="monospace", color=COLORS["green"],
                        fontweight="bold")
                ax.text(cx + len(p) * 0.065 + 0.15, y, "[+]", ha="left",
                        va="center", fontsize=7, fontweight="bold",
                        color=COLORS["green"])
            else:
                ax.text(cx, y, p, ha="center", va="center", fontsize=8.5,
                        fontfamily="monospace", color=COLORS["dark"])
        return h

    # --- Left panel: FORWARD apply(s0, MoverDesdeMesa(A,B)) ---
    ax1.set_xlim(-0.5, 10.5)
    ax1.set_ylim(-1.5, 9)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("FORWARD:  aplicar($s_0$, MoverDesdeMesa(A,B))",
                   fontsize=11, fontweight="bold", color=COLORS["blue"], pad=12)

    s0_props = ["On(A,Mesa)", "On(B,Mesa)", "On(C,Mesa)",
                "Clear(A)", "Clear(B)", "Clear(C)"]
    s0_removed = {"On(A,Mesa)", "Clear(B)"}

    _draw_prop_box(ax1, 2.5, 6.0, s0_props, "Estado $s_0$",
                   COLORS["blue"], "#E3F2FD", removed=s0_removed)

    # Arrow down
    ax1.annotate("", xy=(5.0, 5.0), xytext=(5.0, 5.8),
                 arrowprops=dict(arrowstyle="-|>", lw=2.5, color=COLORS["blue"]))
    ax1.text(5.0, 5.5, "Paso 1\n$s - \\mathrm{Del}(a)$", ha="center",
             fontsize=9, color=COLORS["blue"],
             bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                       edgecolor=COLORS["blue"], linewidth=1))

    # Intermediate
    s_mid = ["On(B,Mesa)", "On(C,Mesa)", "Clear(A)", "Clear(C)"]
    _draw_prop_box(ax1, 7.5, 6.0, s_mid, "después de quitar Del",
                   COLORS["gray"], "#F5F5F5")

    # Arrow down
    ax1.annotate("", xy=(5.0, 2.8), xytext=(5.0, 3.6),
                 arrowprops=dict(arrowstyle="-|>", lw=2.5, color=COLORS["green"]))
    ax1.text(5.0, 3.3, "Paso 2\n$\\cup\\ \\mathrm{Add}(a)$", ha="center",
             fontsize=9, color=COLORS["green"],
             bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                       edgecolor=COLORS["green"], linewidth=1))

    # Result
    s_prime = ["On(A,B)", "On(B,Mesa)", "On(C,Mesa)", "Clear(A)", "Clear(C)"]
    _draw_prop_box(ax1, 5.0, 1.0, s_prime, "Estado $s'$",
                   COLORS["green"], "#E8F5E9", added={"On(A,B)"})

    # Action box
    ax1.text(5.0, 8.3, "Acción: MoverDesdeMesa(A,B)", ha="center", fontsize=10,
             fontweight="bold", color=COLORS["dark"],
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF9C4",
                       edgecolor=COLORS["orange"], linewidth=1.5))

    # Formula summary
    ax1.text(5.0, -1.0,
             "$s' = (s_0 - \\mathrm{Del}) \\cup \\mathrm{Add}$",
             ha="center", fontsize=11, color=COLORS["blue"],
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#E3F2FD",
                       edgecolor=COLORS["blue"], linewidth=1.5))

    # --- Right panel: BACKWARD regress(G, MoverDesdeMesa(A,B)) ---
    ax2.set_xlim(-0.5, 10.5)
    ax2.set_ylim(-1.5, 9)
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_title("BACKWARD:  regress($G$, MoverDesdeMesa(A,B))",
                   fontsize=11, fontweight="bold", color=COLORS["orange"], pad=12)

    g_props = ["On(A,B)", "On(B,C)", "On(C,Mesa)", "Clear(A)"]
    g_removed = {"On(A,B)"}

    _draw_prop_box(ax2, 2.5, 6.0, g_props, "Subobjetivo $G$",
                   COLORS["orange"], "#FFF3E0", removed=g_removed)

    # Arrow down
    ax2.annotate("", xy=(5.0, 5.0), xytext=(5.0, 5.8),
                 arrowprops=dict(arrowstyle="-|>", lw=2.5, color=COLORS["orange"]))
    ax2.text(5.0, 5.5, "Paso 1\n$g - \\mathrm{Add}(a)$", ha="center",
             fontsize=9, color=COLORS["orange"],
             bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                       edgecolor=COLORS["orange"], linewidth=1))

    # Intermediate
    g_mid = ["On(B,C)", "On(C,Mesa)", "Clear(A)"]
    _draw_prop_box(ax2, 7.5, 6.0, g_mid, "después de quitar Add",
                   COLORS["gray"], "#F5F5F5")

    # Arrow down
    ax2.annotate("", xy=(5.0, 2.8), xytext=(5.0, 3.6),
                 arrowprops=dict(arrowstyle="-|>", lw=2.5, color=COLORS["green"]))
    ax2.text(5.0, 3.3, "Paso 2\n$\\cup\\ \\mathrm{Pre}(a)$", ha="center",
             fontsize=9, color=COLORS["green"],
             bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                       edgecolor=COLORS["green"], linewidth=1))

    # Result
    g_prime = ["On(A,Mesa)", "On(B,C)", "On(C,Mesa)", "Clear(A)", "Clear(B)"]
    _draw_prop_box(ax2, 5.0, 1.0, g_prime, "Subobjetivo $g'$",
                   COLORS["teal"], "#E0F2F1", added={"On(A,Mesa)", "Clear(B)"})

    # Action box
    ax2.text(5.0, 8.3, "Acción: MoverDesdeMesa(A,B)", ha="center", fontsize=10,
             fontweight="bold", color=COLORS["dark"],
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF9C4",
                       edgecolor=COLORS["orange"], linewidth=1.5))

    # Formula summary
    ax2.text(5.0, -1.0,
             "$g' = (G - \\mathrm{Add}) \\cup \\mathrm{Pre}$",
             ha="center", fontsize=11, color=COLORS["orange"],
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF3E0",
                       edgecolor=COLORS["orange"], linewidth=1.5))

    fig.suptitle("Misma acción, dos perspectivas: aplicar (forward) vs regresar (backward)",
                 fontsize=13, fontweight="bold", y=1.0)
    fig.tight_layout()
    _save(fig, "14_apply_vs_regress.png")


# ---------------------------------------------------------------------------
# Plot 15 – Algorithm flowchart: forward vs backward side by side
# ---------------------------------------------------------------------------

def plot_algorithm_flowchart():
    """Side-by-side flowchart comparing FORWARD-PLANNING and BACKWARD-PLANNING,
    highlighting the 3 substitution points [D1/D2/D3] vs [B1/B2/B3]."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 11))

    def _flowchart(ax, title, color, steps):
        """Draw a vertical flowchart.
        steps: list of (label, shape, tag) where shape is 'box', 'diamond',
        or 'roundbox', and tag is e.g. '[D1]' or None.
        """
        ax.set_xlim(-1, 11)
        ax.set_ylim(-0.5, 14)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=13, fontweight="bold", color=color, pad=15)

        cx = 5.0
        y_positions = []
        n = len(steps)

        for i, (label, shape, tag) in enumerate(steps):
            y = 12.5 - i * 2.0
            y_positions.append(y)
            w, h = 4.2, 1.1

            if shape == "diamond":
                diamond = plt.Polygon(
                    [(cx, y + h / 2 + 0.15), (cx + w / 2, y),
                     (cx, y - h / 2 - 0.15), (cx - w / 2, y)],
                    facecolor="#FFF9C4", edgecolor=COLORS["orange"],
                    linewidth=2, zorder=2)
                ax.add_patch(diamond)
            elif shape == "roundbox":
                rect = mpatches.FancyBboxPatch(
                    (cx - w / 2, y - h / 2), w, h,
                    boxstyle="round,pad=0.12", facecolor="#E8F5E9",
                    edgecolor=COLORS["green"], linewidth=2, zorder=2)
                ax.add_patch(rect)
            else:
                fill = "#E3F2FD" if "[" not in (tag or "") else "#FFEBEE"
                border = color if "[" not in (tag or "") else COLORS["red"]
                if tag:
                    fill = "#FFEBEE"
                    border = COLORS["red"]
                rect = mpatches.FancyBboxPatch(
                    (cx - w / 2, y - h / 2), w, h,
                    boxstyle="round,pad=0.12", facecolor=fill,
                    edgecolor=border, linewidth=2, zorder=2)
                ax.add_patch(rect)

            ax.text(cx, y, label, ha="center", va="center", fontsize=8.5,
                    fontweight="bold" if tag else "normal",
                    color=COLORS["dark"], zorder=3)

            if tag:
                ax.text(cx + w / 2 + 0.15, y, tag, ha="left", va="center",
                        fontsize=10, fontweight="bold", color=COLORS["red"],
                        zorder=3)

            # Arrow to next
            if i < n - 1:
                next_shape = steps[i + 1][1]
                y_end = 12.5 - (i + 1) * 2.0
                tip_y = y_end + (h / 2 + 0.15 if next_shape == "diamond"
                                 else h / 2)
                ax.annotate("", xy=(cx, tip_y), xytext=(cx, y - h / 2),
                            arrowprops=dict(arrowstyle="-|>", lw=1.5,
                                            color=COLORS["gray"]))

    # Forward steps
    forward_steps = [
        ("frontera ← { $s_0$ }", "box", "[D1]"),
        ("$s$ ← frontera.pop()", "box", None),
        ("¿$G \\subseteq s$ ?", "diamond", "[D2]"),
        ("Para cada $a$:\n¿Pre($a$) $\\subseteq s$ ?", "box", None),
        ("$s' = (s - \\mathrm{Del}) \\cup \\mathrm{Add}$", "box", "[D3]"),
        ("agregar $s'$ a frontera", "box", None),
        ("PLAN encontrado", "roundbox", None),
    ]

    # Backward steps
    backward_steps = [
        ("frontera ← { $G$ }", "box", "[B1]"),
        ("$g$ ← frontera.pop()", "box", None),
        ("¿$g \\subseteq s_0$ ?", "diamond", "[B2]"),
        ("Para cada $a$:\n¿Add($a$) $\\cap\\ g \\neq \\emptyset$ ?\n"
         "¿Del($a$) $\\cap\\ g = \\emptyset$ ?", "box", None),
        ("$g' = (g - \\mathrm{Add}) \\cup \\mathrm{Pre}$", "box", "[B3]"),
        ("agregar $g'$ a frontera", "box", None),
        ("PLAN encontrado", "roundbox", None),
    ]

    _flowchart(ax1, "FORWARD-PLANNING", COLORS["blue"], forward_steps)
    _flowchart(ax2, "BACKWARD-PLANNING", COLORS["orange"], backward_steps)

    # Add "Sí" label for diamond -> PLAN (special branch)
    for ax_i in (ax1, ax2):
        diamond_y = 12.5 - 2 * 2.0  # step index 2
        plan_y = 12.5 - 6 * 2.0     # step index 6
        ax_i.annotate(
            "", xy=(8.5, plan_y), xytext=(7.1, diamond_y),
            arrowprops=dict(arrowstyle="-|>", lw=1.5, color=COLORS["green"],
                            connectionstyle="arc3,rad=-0.3"))
        ax_i.text(8.8, (diamond_y + plan_y) / 2, "Sí", fontsize=10,
                  fontweight="bold", color=COLORS["green"])
        ax_i.text(3.2, diamond_y - 0.8, "No",
                  fontsize=10, fontweight="bold", color=COLORS["gray"])

    fig.suptitle("Algoritmos lado a lado: las 3 diferencias marcadas en rojo",
                 fontsize=13, fontweight="bold", y=0.98)
    fig.tight_layout()
    _save(fig, "15_algorithm_flowchart.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Generate all 15 images for module 16 (Planificación Clásica)."""
    plot_search_vs_planning()         # 01
    plot_blocks_world_states()        # 02
    plot_strips_action_anatomy()      # 03
    plot_state_transition()           # 04
    plot_blocks_world_state_space()   # 05
    plot_forward_vs_generic()         # 06
    plot_forward_search_trace()       # 07
    plot_plan_found()                 # 08
    plot_state_space_explosion()      # 09
    plot_relaxed_problem()            # 10
    plot_forward_vs_backward()        # 11
    plot_regression_trace()           # 12
    plot_forward_vs_backward_branching()  # 13
    plot_apply_vs_regress()           # 14
    plot_algorithm_flowchart()        # 15


if __name__ == "__main__":
    main()
