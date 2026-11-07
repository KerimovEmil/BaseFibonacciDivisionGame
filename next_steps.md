# Next Steps

## ✅ Done in the 2.0 redesign

- Beautiful, animated UI: gradient tiles, shadows, pop animations, glowing target
  slots, win confetti, redesigned menu + HUD.
- Valid-move highlighting when a tile is clicked (real `ShowValidMoves`).
- Interactive **How to Play** tutorial illustrating the four moves.
- Difficulty (Easy/Medium/Hard) now changes the numbers and board size.
- Collapsible move log.
- Solver-powered **Hint** and animated **Solve** (optimal path), plus an
  **optimal move count** in the HUD.
- **Undo / Redo / Reset** via state-snapshot history.
- Web build: runs in the browser via pygbag (async loop, no blocking mainloops)
  and deploys automatically to GitHub Pages via `.github/workflows/pages.yml`.
- Pure `rules.py` shared by gameplay and solver; unit tests for rules + solver.

## ✅ Done in 2.1 (Solver, UX, Modes & Persistence)

- **Fast optimal A\* solver (`zdg/solver.py`):** replaced plain BFS with a bit-packed
  A\* solver using diagonalized row/column Fibonacci recurrence coordinates and exact
  signed-Fibonacci heuristic tables, solving all 36 Hard factor pairs (`6 ≤ a ≤ b ≤ 13`)
  to provable optimality in milliseconds.
- **Cached solver path (`zdg/scenes/game_scene.py`):** `Hint`, `Solve`, and `Reset`
  reuse or incrementally advance the cached optimal path without re-solving.
- **Exact integer Fibonacci & Zeckendorf math (`zdg/util.py`):** replaced floating-point
  Binet/log approximations with exact integer arithmetic.
- **Click-to-Move & Keyboard Controls:** click any highlighted destination cell or use
  Arrow keys / `WASD` to move tiles without dragging.
- **Directional Split/Merge Animations & Multi-Tile Drag Badge (`zdg/ui/board_view.py`):**
  smooth cubic ease-out tile flights on every split, merge, and carry, plus cached
  drop shadows and glow rings (`zdg/theme.py`).
- **Synchronized, Scrollable Move Log (`zdg/history.py`, `zdg/ui/hud.py`):** `Undo`,
  `Redo`, and `Reset` stay in lockstep with the move log, which supports mouse-wheel
  scrolling and a close (`×`) button.
- **Auto-Solve vs. Player Win Distinction (`zdg/scenes/win_overlay.py`):** auto-solved
  runs display `"Solution Complete"` without overwriting player best scores.
- **Interactive Tutorial Mini-Board (`zdg/scenes/tutorial_scene.py`):** added a playable
  `"Try It Yourself"` step (`4 = 2 × 2`) with live hint guidance and keyboard navigation.
- **Persistent Best Scores & Preferences (`zdg/persistence.py`):** saves best scores,
  selected difficulty, and mute state to `localStorage` on web and JSON on desktop.
- **Daily Challenge & Custom Factor Mode (`zdg/problem.py`, `zdg/scenes/menu_scene.py`):**
  play today's seeded Daily Challenge or choose custom `a × b` factors on the menu.
- **Live Cell Value Inspector (`zdg/ui/board_view.py`, `zdg/ui/hud.py`):** hovering or
  selecting any board cell shows its `Fᵣ × F𝒸 = value` breakdown in the top bar.

## 💡 Future ideas

- **Different rule sets / sequences:** `rules.py` is isolated as a single
  source of truth — generalize it to inject alternate bases/identities (e.g., Lucas
  or Tribonacci numbers).
