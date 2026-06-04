# Fibonacci Division Game 2.0 — Build Plan

Spec: `docs/superpowers/specs/2026-06-03-fib-game-2.0-design.md`

## Core logic

- [ ] `rules.py` — pure `is_valid` / `apply` on 2D int array (single source of truth)
- [ ] Refactor `move.py` to delegate to `rules.py`
- [ ] `grid.py` — add `to_state()` / win-on-state helpers
- [ ] `problem.py` — difficulty-aware ranges
- [ ] `solver.py` — BFS shortest path + `hint` + `solve`
- [ ] `history.py` — undo/redo stack

## Presentation

- [ ] `theme.py` — palette, fonts, rounded-rect/shadow/gradient helpers
- [ ] `settings.py` — new tunables + layout
- [ ] `particles.py` — confetti/sparkles
- [ ] `sound.py` — defensive, mute-able (web-safe); ogg conversion
- [ ] `ui/button.py`
- [ ] `ui/board_view.py` — tiles, target slots, highlights, labels, animation
- [ ] `ui/hud.py` — banner, counters, button bar, move log

## App / scenes

- [ ] `scenes/scene.py` base
- [ ] `app.py` — async App + scene manager (the loop)
- [ ] `scenes/menu_scene.py`
- [ ] `scenes/game_scene.py`
- [ ] `scenes/tutorial_scene.py`
- [ ] `scenes/win_overlay.py`
- [ ] `main.py` async entry + `run_main.py` wrapper

## Tests & polish

- [ ] `tests/test_rules.py`, `tests/test_solver.py`
- [ ] `tools/screenshot.py` + generate screenshots
- [ ] Web build via pygbag + verify
- [ ] Rewrite README (beautiful + screenshots + install/run)
- [ ] Update `next_steps.md`
- [ ] Full verification: tests, headless render, desktop run

## Review

(to be filled in)
