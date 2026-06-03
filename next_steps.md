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
- Web build: runs in the browser via pygbag (async loop, no blocking mainloops).
- Pure `rules.py` shared by gameplay and solver; unit tests for rules + solver.

## 🔧 Known limitation / next up

- **Solver scaling on Hard:** the BFS solver can hit its node cap on the largest
  Hard puzzles, so Hint / Solve / Optimal occasionally read as unavailable. The
  UI handles `None` gracefully, but the fix is a smarter search
  (bidirectional BFS or A\* with an admissible heuristic). Lowering the Hard upper
  bound is a quick interim mitigation.

## 💡 Future ideas

- **Different rule sets / sequences:** `rules.py` is already isolated as a single
  source of truth — generalize it to inject alternate bases/identities.
- Per-puzzle persistent best scores / daily challenge.
- Deploy the web build to a live site (GitHub Pages / Netlify) from `build/web`.
- Optional move-by-move animation of split/merge (currently a pop on change).
