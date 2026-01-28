# Prompts para Imágenes - Módulo de Lógica

**Estilo**: Pixel Art 16-bit (SNES/GBA)  
**Guardar en**: `clase/03_logica/images/`

---

## 1. wumpus_world_intro.png

**Propósito**: Introducir el Wumpus World en 01_intro.md. Mostrar el escenario general donde el agente debe razonar para sobrevivir.

**Elementos requeridos**:
- Grid de 4x4 celdas (cueva/dungeon)
- Agente (héroe) en la posición inicial [1,1] (esquina inferior izquierda)
- Wumpus (monstruo peligroso) en alguna celda
- Al menos 1 pozo (pit) - agujero negro mortal
- Oro/tesoro en alguna celda
- Celdas no exploradas con incertidumbre (signos de pregunta)
- Sensación de peligro y misterio

**Tamaño**: 1024x1024

```
Pixel art illustration, 16-bit SNES video game style, top-down perspective view of a dark dungeon cave.

The scene shows a 4x4 square grid of floor tiles representing a dangerous cave. Each tile is a stone floor square with visible borders between tiles.

In the bottom-left corner tile: a small pixel art hero character (knight or adventurer) with a torch, facing toward the unknown darkness. This is position [1,1].

In one of the upper tiles: a menacing purple monster creature (the Wumpus) with glowing eyes, partially hidden in shadows.

In another tile: a black bottomless pit - a dark circular hole in the floor that looks deadly.

In another tile: a shining golden treasure chest or pile of gold coins with a yellow glow effect.

Several tiles are shrouded in darkness with white floating question mark symbols, indicating unexplored and unknown areas.

The overall atmosphere is mysterious and dangerous. Limited 16-color palette. Clean pixel art with no anti-aliasing. Black void surrounds the dungeon grid. The lighting suggests torchlight from the hero illuminating nearby tiles while distant tiles remain dark and uncertain.

Style: retro RPG dungeon crawler, like early Final Fantasy or Dragon Quest games.
```

---

## 2. wumpus_world_grid.png

**Propósito**: Diagrama de referencia en 05_wumpus_world.md mostrando el grid completo con todos los elementos y una leyenda explicativa.

**Elementos requeridos**:
- Grid 4x4 con coordenadas claras [1,1] a [4,4]
- Sistema de coordenadas: columnas 1-4 (horizontal), filas 1-4 (vertical)
- Leyenda con TODOS los símbolos del juego:
  - Agente (posición actual)
  - Wumpus (monstruo)
  - Pit (pozo)
  - Gold (oro)
  - Breeze (brisa - indica pozo adyacente)
  - Stench (hedor - indica Wumpus adyacente)
  - Glitter (brillo - indica oro en la celda)
- Estilo de mapa de juego

**Tamaño**: 1200x900

```
Pixel art game reference diagram, 16-bit retro style, clean educational layout.

LEFT SIDE (main area, about 70% of image width):
A 4x4 grid representing the Wumpus World dungeon map. Each cell is a square stone tile with clear dark borders.

Coordinate system clearly labeled:
- Bottom edge: numbers "1  2  3  4" labeling columns from left to right
- Left edge: numbers "1  2  3  4" labeling rows from bottom to top
- The bottom-left cell is [1,1], top-right cell is [4,4]

The grid shows an example game state:
- Cell [1,1]: Hero/agent sprite (starting position)
- Cell [1,3]: Purple Wumpus monster sprite
- Cell [3,1]: Black pit hole
- Cell [4,4]: Golden treasure/gold
- Cells adjacent to Wumpus: faint green stench clouds
- Cells adjacent to pit: faint blue wind/breeze lines
- Cell with gold: yellow sparkle effects

RIGHT SIDE (legend area, about 30% of image width):
A vertical legend box with retro game UI frame border containing:

"LEGEND" title at top in pixel font

Icon + Label pairs, vertically stacked:
- Knight helmet icon → "Agent"
- Purple monster face → "Wumpus" 
- Black hole circle → "Pit"
- Gold chest/coins → "Gold"
- Blue wavy lines → "Breeze (pit nearby)"
- Green cloud puffs → "Stench (wumpus nearby)"
- Yellow stars/sparkles → "Glitter (gold here)"

Clean pixel art style, limited color palette, dark background, clear readable labels in white pixel font.
```

---

## 3. entailment_venn.png

**Propósito**: Explicar el concepto de entailment (consecuencia lógica) en 03_inferencia.md. Mostrar que α ⊨ β significa que todos los modelos donde α es verdadera también hacen β verdadera.

**Elementos requeridos**:
- Diagrama de Venn con dos conjuntos
- Conjunto grande: M(α) - modelos donde α es verdadera
- Conjunto pequeño DENTRO del grande: M(β) - modelos donde β es verdadera
- Visualizar que M(α) ⊆ M(β) o que si α es verdadera, β también
- Símbolo de entailment: α ⊨ β
- Explicación clara de la relación

**Tamaño**: 1024x768

```
Pixel art educational diagram explaining logical entailment, clean minimalist style.

Black background.

CENTER OF IMAGE:
Two circles made of pixel blocks, one inside the other (nested circles, NOT overlapping side by side).

OUTER CIRCLE: 
- Large circle filled with solid BLUE color
- Label above it: "M(α)" in white pixel font
- Subtitle below the label: "Models where α is TRUE"
- This represents all possible worlds/models where alpha is true

INNER CIRCLE:
- Smaller circle COMPLETELY INSIDE the blue circle (not overlapping, fully contained)
- Filled with solid GREEN color  
- Label inside or next to it: "M(β)"
- Subtitle: "Models where β is TRUE"
- This shows that whenever α is true, β must also be true

BOTTOM OF IMAGE:
Large text in white pixel font: "α ⊨ β"
Below that: "Alpha ENTAILS Beta"
Below that in smaller text: "Every model satisfying α also satisfies β"

TOP OF IMAGE:
Title: "LOGICAL ENTAILMENT" in white pixel font

The diagram clearly shows that the green circle (β true) is a SUBSET contained within the blue circle (α true), visually demonstrating that α being true guarantees β is true.

Simple geometric pixel shapes, only colors used: black (background), blue, green, white (text). No gradients, clean 8-bit aesthetic.
```

---

## 4. forward_chaining.png

**Propósito**: Ilustrar forward chaining (encadenamiento hacia adelante) en 03_inferencia.md. Mostrar cómo partimos de hechos conocidos y derivamos nuevos hechos aplicando reglas.

**Elementos requeridos**:
- Flujo de IZQUIERDA a DERECHA (data-driven)
- Sección izquierda: Hechos conocidos (A, B)
- Sección media: Reglas que se aplican
- Sección derecha: Hechos derivados (C, D)
- Flechas mostrando la dirección del flujo
- Claro que es "data-driven" - empezamos con datos

**Tamaño**: 1400x600

```
Pixel art horizontal flowchart diagram, 16-bit retro game style, showing forward chaining inference.

Dark gray or black background. The flow goes from LEFT to RIGHT.

LEFT SECTION (about 25% of width):
- Decorative pixel border box
- Title at top: "KNOWN FACTS" in white pixel text
- Inside the box: Two glowing orb sprites
  - Blue orb labeled "A" 
  - Blue orb labeled "B"
- These represent the starting facts we know to be true

MIDDLE SECTION (about 30% of width):
- Pixel art of stone archway or gate structure
- Title above: "RULES" in white pixel text
- On the gate structure, show rule text:
  - "A ∧ B → C"
  - "C → D"
- Small gear or scroll icons to represent rule processing

RIGHT SECTION (about 25% of width):
- Decorative pixel border box with slight glow effect
- Title at top: "DERIVED FACTS" in white pixel text
- Inside the box: Two glowing orb sprites
  - Green orb labeled "C" with sparkle effect (newly derived)
  - Green orb labeled "D" with sparkle effect (newly derived)
- These represent facts we derived by applying rules

ARROWS:
- Large bold yellow/gold pixel arrows pointing LEFT → RIGHT
- First arrow: from "Known Facts" box to "Rules" gate
- Second arrow: from "Rules" gate to "Derived Facts" box
- Arrows should be prominent and clearly show the flow direction

BOTTOM OF IMAGE:
Text: "Data-Driven: Start with facts, derive conclusions" in white pixel text

Clean 16-bit pixel art style, limited color palette (black, blue, green, yellow, white, gray). Clear visual hierarchy showing the progression from known to derived.
```

---

## 5. backward_chaining.png

**Propósito**: Ilustrar backward chaining (encadenamiento hacia atrás) en 03_inferencia.md. Mostrar cómo partimos de un objetivo y trabajamos hacia atrás para ver si podemos probarlo.

**Elementos requeridos**:
- Flujo de DERECHA a IZQUIERDA (goal-driven)
- Sección derecha: Objetivo/Goal (D?)
- Sección media: Subgoals que necesitamos probar
- Sección izquierda: Verificación contra hechos conocidos
- Flechas mostrando dirección INVERSA (derecha a izquierda)
- Claro que es "goal-driven" - empezamos con el objetivo

**Tamaño**: 1400x600

```
Pixel art horizontal flowchart diagram, 16-bit retro game style, showing backward chaining inference.

Dark gray or black background. The flow goes from RIGHT to LEFT (opposite of forward chaining).

RIGHT SECTION (about 25% of width):
- Decorative pixel border box with golden/yellow tint
- Title at top: "GOAL" in white pixel text
- Inside the box: 
  - Golden treasure chest or target icon
  - Large text: "D?" with question mark
  - Subtitle: "Can we prove D?"
- This represents what we want to prove/achieve

MIDDLE SECTION (about 35% of width):
- Two stone pillar or pedestal structures
- Title above: "SUBGOALS" in white pixel text
- First pillar shows: "Need C?" with question mark
- Second pillar shows: "Need A ∧ B?" with question mark
- Small thinking/question bubble icons
- These represent intermediate goals we need to verify

LEFT SECTION (about 25% of width):
- Decorative pixel border box with green tint
- Title at top: "VERIFY FACTS" in white pixel text
- Inside the box: Two orb sprites
  - Blue orb "A" with GREEN CHECKMARK overlay ✓
  - Blue orb "B" with GREEN CHECKMARK overlay ✓
- Text below: "Facts confirmed!"
- This shows we found the facts in our knowledge base

ARROWS:
- Large bold PURPLE or MAGENTA pixel arrows pointing RIGHT → LEFT
- Arrows should clearly show BACKWARD flow (opposite direction)
- First arrow: from Goal to Subgoals
- Second arrow: from Subgoals to Verify Facts

BOTTOM OF IMAGE:
Text: "Goal-Driven: Start with goal, work backwards" in white pixel text

Clean 16-bit pixel art style. Make it visually distinct from forward chaining by using purple arrows instead of yellow and having the flow clearly reversed.
```

---

## 6. sat_solver_performance.png

**Propósito**: Mostrar en 04_satisfacibilidad.md cómo los SAT solvers han mejorado dramáticamente a lo largo del tiempo, a pesar de que SAT es NP-completo.

**Elementos requeridos**:
- Gráfico de línea mostrando mejora exponencial
- Eje X: Años (1995-2025)
- Eje Y: Variables resueltas (escala logarítmica: 1K, 10K, 100K, 1M, 10M)
- Línea ascendente mostrando crecimiento exponencial
- Puntos de referencia/milestones: GRASP (1996), Chaff (2001), MiniSat (2003), Modern (2020s)
- Estética de terminal/computadora retro

**Tamaño**: 1200x800

```
Pixel art line graph in retro computer terminal style, showing SAT solver performance improvement over time.

The entire image looks like an old CRT computer monitor display.

FRAME:
- Outer border resembling a vintage computer monitor bezel (dark gray, chunky)
- Screen area has black background
- Subtle horizontal scanline effect across the screen
- Green or amber phosphor glow aesthetic

GRAPH AREA:
Y-AXIS (left side, vertical):
- Label: "VARIABLES SOLVED" in green pixel text
- Logarithmic scale with tick marks and labels:
  - "10M" at top
  - "1M" 
  - "100K"
  - "10K"
  - "1K" at bottom
- Axis line in green pixels

X-AXIS (bottom, horizontal):
- Label: "YEAR" in green pixel text
- Tick marks and labels at:
  - "1995" (left)
  - "2000"
  - "2005"
  - "2010"
  - "2015"
  - "2020"
  - "2025" (right)
- Axis line in green pixels

THE LINE GRAPH:
- Bright green pixel line (or amber if using amber theme)
- Shows EXPONENTIAL GROWTH curve
- Starts low-left (around 1K in 1995)
- Curves upward steeply
- Ends high-right (around 10M in 2025)
- Line should have slight glow effect

MILESTONE MARKERS (bright dots on the line with labels):
- Dot at ~1996, ~1K level: label "GRASP"
- Dot at ~2001, ~100K level: label "Chaff"  
- Dot at ~2003, ~300K level: label "MiniSat"
- Dot at ~2020, ~5M level: label "Modern"

TITLE:
Top of screen: "SAT SOLVER PERFORMANCE" in large green pixel text

Retro computing aesthetic throughout - looks like output from an old terminal or early computer graphics. Single color (green on black, or amber on black). Clean pixel text, no anti-aliasing.
```

---

## 7. wumpus_reasoning_example.png

**Propósito**: Mostrar en 05_wumpus_world.md un ejemplo concreto de cómo el agente razona sobre el mundo usando las percepciones.

**Elementos requeridos**:
- Grid 4x4 con coordenadas visibles
- Agente en posición [2,1] (segunda columna, primera fila)
- El agente percibe BRISA en [2,1] (indicando pozo cercano)
- Celda [1,1] marcada como SEGURA (ya visitada, sin brisa)
- Celdas [3,1] y [2,2] marcadas con "?" indicando que el pozo podría estar ahí
- Thought bubble del agente mostrando su razonamiento
- Visualizar la incertidumbre

**Tamaño**: 1024x1024

```
Pixel art illustration, 16-bit SNES RPG style, showing logical reasoning in Wumpus World.

A 4x4 dungeon grid viewed from top-down perspective with clear coordinate labels.

COORDINATE SYSTEM:
- Numbers "1 2 3 4" along the bottom edge (columns, left to right)
- Numbers "1 2 3 4" along the left edge (rows, bottom to top)
- Grid lines clearly separating each cell

CELL [1,1] (bottom-left):
- Light green overlay/tint indicating SAFE
- White checkmark symbol ✓
- Small text "SAFE" 
- This cell was visited first with no breeze

CELL [2,1] (second from left, bottom row):
- The AGENT (hero sprite) is standing here
- Blue swirling wind/breeze particle effects around the agent
- Yellow exclamation mark "!" above agent
- Small text "BREEZE!" 
- Agent has detected breeze, meaning pit is adjacent

CELL [3,1] (third from left, bottom row):
- Red-tinted overlay indicating DANGER/UNKNOWN
- Large white question mark "?"
- This cell MIGHT contain the pit

CELL [2,2] (second from left, second row):
- Red-tinted overlay indicating DANGER/UNKNOWN  
- Large white question mark "?"
- This cell MIGHT contain the pit

THOUGHT BUBBLE:
- Classic pixel art thought bubble (cloud shape) coming from the agent
- Inside the bubble:
  - Small pit icon (black hole)
  - Text: "Pit at [3,1] or [2,2]?"
  - Shows the agent reasoning about where the pit could be

OTHER CELLS:
- Remaining cells are dark/unexplored
- No markings

Clean 16-bit pixel art style, limited color palette. The image should clearly communicate: agent detected breeze, knows pit is nearby, but uncertain which of two cells contains it.
```

---

## 8. wumpus_inference_scenario.png

**Propósito**: Mostrar en 05_wumpus_world.md el proceso de inferencia paso a paso - cómo el agente combina información de múltiples ubicaciones para deducir dónde está el pozo.

**Elementos requeridos**:
- 3 paneles secuenciales (como un cómic)
- Panel 1: Agente en [1,1], no hay brisa → adyacentes seguros
- Panel 2: Agente en [2,1], brisa detectada → pozo en [3,1] o [2,2]
- Panel 3: Agente en [1,2], no hay brisa → [2,2] es seguro → ¡pozo debe estar en [3,1]!
- Mostrar la progresión lógica claramente
- Numeración de pasos

**Tamaño**: 1800x700

```
Pixel art horizontal triptych (three panels), 16-bit SNES style, showing step-by-step logical inference in Wumpus World.

Dark background. Three equal-width panels arranged horizontally, each with a decorative retro game UI frame border.

===== PANEL 1 (left third) =====
Title at top: "STEP 1" in white pixel text

Shows a small 4x4 grid (simplified, smaller scale to fit panel):
- Agent sprite at cell [1,1] (bottom-left)
- Green glow effect on [1,1]
- Checkmarks on adjacent cells [2,1] and [1,2] indicating "no danger detected"

Speech bubble from agent:
"No breeze, no stench. Cells [2,1] and [1,2] are safe to visit."

Bottom annotation: "[1,1]: No percepts"

===== PANEL 2 (middle third) =====
Title at top: "STEP 2" in white pixel text

Shows a small 4x4 grid:
- Agent sprite now at cell [2,1]
- Blue wind/breeze particles swirling around agent
- Yellow "!" exclamation mark
- Red "?" marks on cells [3,1] and [2,2]

Speech bubble from agent:
"Breeze detected! There's a pit at [3,1] or [2,2]."

Bottom annotation: "[2,1]: Breeze!"

===== PANEL 3 (right third) =====
Title at top: "STEP 3" in white pixel text

Shows a small 4x4 grid:
- Agent sprite now at cell [1,2]
- Golden lightbulb icon above agent (eureka moment)
- Green checkmark on cell [2,2] (now known safe)
- Red X mark on cell [3,1] with small pit icon (pit located!)

Speech bubble from agent:
"No breeze here! So [2,2] is safe. The pit MUST be at [3,1]!"

Bottom annotation: "[1,2]: No breeze → Pit at [3,1]!"

===== CONNECTING ELEMENTS =====
- Large arrow pointing right between Panel 1 and Panel 2
- Large arrow pointing right between Panel 2 and Panel 3
- Or numbers "1 → 2 → 3" shown below panels

The panels should clearly show the PROGRESSION of knowledge: from knowing nothing, to having uncertainty, to resolving that uncertainty through logical deduction.

Clean 16-bit pixel art, limited colors, clear readable text, retro game cutscene aesthetic.
```

---

## Checklist Final

| # | Archivo | Tamaño | Generado |
|---|---------|--------|:--------:|
| 1 | `wumpus_world_intro.png` | 1024×1024 | ☐ |
| 2 | `wumpus_world_grid.png` | 1200×900 | ☐ |
| 3 | `entailment_venn.png` | 1024×768 | ☐ |
| 4 | `forward_chaining.png` | 1400×600 | ☐ |
| 5 | `backward_chaining.png` | 1400×600 | ☐ |
| 6 | `sat_solver_performance.png` | 1200×800 | ☐ |
| 7 | `wumpus_reasoning_example.png` | 1024×1024 | ☐ |
| 8 | `wumpus_inference_scenario.png` | 1800×700 | ☐ |

---

## Instrucciones

1. Copia el contenido del bloque de código (```) para cada imagen
2. Pega directamente en Nano Banana
3. Si el tamaño no es correcto, redimensiona después
4. Guarda en `clase/03_logica/images/` con el nombre exacto indicado
5. Marca el checkbox cuando esté listo
