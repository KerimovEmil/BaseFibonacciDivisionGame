"""A* shortest-path solver using diagonalized Fibonacci move invariants.

Mathematical foundation
-----------------------
Let R_r and C_c be the row and column Fibonacci weights. Define the row-weighted
and column-weighted projections of a state S:
    W_r(S) = sum_c S[r][c] * C_c
    V_c(S) = sum_r S[r][c] * R_r

Horizontal moves leave W_r(S) invariant, and vertical moves leave V_c(S) invariant.
Furthermore, defining the recurrence coordinates between S and the goal T:
    A_1 = dW_0,  A_2 = dW_1 + A_1,  A_k = dW_{k-1} + A_{k-1} + A_{k-2}
    B_1 = dV_0,  B_2 = dV_1 + B_1,  B_k = dV_{k-1} + B_{k-1} + B_{k-2}
diagonalizes the move operators completely:
  * A vertical move at row k in column c changes ONLY A_k by +-C_c.
  * A horizontal move at column k in row r changes ONLY B_k by +-R_r.

The minimum number of signed Fibonacci terms +-C_c summing to A_k (summed over k)
plus the minimum number of signed Fibonacci terms +-R_r summing to B_k (summed
over k) forms a tight, consistent, O(1)-updatable admissible heuristic for A*.
"""
from collections import deque
import heapq
from zdg.grid import is_win_state
from zdg.settings import SOLVER_MAX_NODES
from zdg.util import get_first_n_zeckendorf_terms


def _min_signed_fib_table(allowed_fibs, max_val):
    """Return a lookup table mapping ``val + max_val`` -> min signed terms to sum to ``val``."""
    dist = {0: 0}
    q = deque([0])
    while q:
        u = q.popleft()
        du = dist[u]
        nd = du + 1
        for f in allowed_fibs:
            for v in (u + f, u - f):
                if -max_val <= v <= max_val and v not in dist:
                    dist[v] = nd
                    q.append(v)
    return [dist.get(abs(i - max_val), 99) for i in range(max_val * 2 + 1)]


def solve(start_state, mask, max_nodes=SOLVER_MAX_NODES):
    """Return a shortest list of (row, col, direction) moves, or None.

    ``mask`` is the solution mask (tuple of tuple of bool).
    """
    if is_win_state(start_state, mask):
        return []

    H, W = len(start_state), len(start_state[0])
    R = get_first_n_zeckendorf_terms(H)[::-1]
    C = get_first_n_zeckendorf_terms(W)[::-1]
    goal_grid = [[1 if mask[r][c] else 0 for c in range(W)] for r in range(H)]

    start_val = sum(start_state[r][c] * R[r] * C[c] for r in range(H) for c in range(W))
    goal_val = sum(goal_grid[r][c] * R[r] * C[c] for r in range(H) for c in range(W))
    if start_val != goal_val:
        return None

    def pack(grid):
        val = 0
        for r in range(H):
            for c in range(W):
                val |= (grid[r][c] & 0xFF) << ((r * W + c) * 8)
        return val

    start = pack(start_state)
    goal = pack(goal_grid)
    if start == goal:
        return []

    N = max(1, start_val)
    max_val = N * 2

    tbls = []
    for k in range(1, H):
        allowed_C = [c for c in C if c * R[k - 1] <= N] or [1]
        tbls.append(_min_signed_fib_table(allowed_C, max_val))
    for k in range(1, W):
        allowed_R = [r for r in R if r * C[k - 1] <= N] or [1]
        tbls.append(_min_signed_fib_table(allowed_R, max_val))

    W_s = [sum(start_state[r][c] * C[c] for c in range(W)) for r in range(H)]
    W_g = [sum(goal_grid[r][c] * C[c] for c in range(W)) for r in range(H)]
    V_s = [sum(start_state[r][c] * R[r] for r in range(H)) for c in range(W)]
    V_g = [sum(goal_grid[r][c] * R[r] for r in range(H)) for c in range(W)]

    A0 = []
    for k in range(1, H):
        dw = W_g[k - 1] - W_s[k - 1]
        if k == 1:
            A0.append(dw)
        elif k == 2:
            A0.append(dw + A0[0])
        else:
            A0.append(dw + A0[k - 2] + A0[k - 3])

    B0 = []
    for k in range(1, W):
        dv = V_g[k - 1] - V_s[k - 1]
        if k == 1:
            B0.append(dv)
        elif k == 2:
            B0.append(dv + B0[0])
        else:
            B0.append(dv + B0[k - 2] + B0[k - 3])

    ab0 = tuple(A0 + B0)

    def lookup(tbl, val):
        clamped = max(-max_val, min(max_val, val))
        return tbl[clamped + max_val]

    raw_h0 = sum(lookup(tbls[idx], ab0[idx]) for idx in range(len(ab0)))

    moves = []
    for r in range(H):
        for c in range(W):
            idx = r * W + c
            s1 = idx * 8
            b1 = 1 << s1
            if c != W - 1:
                if c == W - 2:
                    delta = -b1 + (2 << ((idx + 1) * 8))
                else:
                    delta = -b1 + (1 << ((idx + 1) * 8)) + (1 << ((idx + 2) * 8))
                moves.append((0, s1, 0, delta, (H - 1) + c, +R[r], (r, c, "RIGHT")))
            if r != H - 1:
                if r == H - 2:
                    delta = -b1 + (2 << ((idx + W) * 8))
                else:
                    delta = -b1 + (1 << ((idx + W) * 8)) + (1 << ((idx + 2 * W) * 8))
                moves.append((0, s1, 0, delta, r, +C[c], (r, c, "DOWN")))
            if c == W - 1:
                delta = -(2 << s1) + (1 << ((idx - 1) * 8))
                moves.append((1, s1, 0, delta, (H - 1) + c - 1, -R[r], (r, c, "LEFT")))
            elif c > 0:
                s2 = (idx + 1) * 8
                delta = -b1 - (1 << s2) + (1 << ((idx - 1) * 8))
                moves.append((2, s1, s2, delta, (H - 1) + c - 1, -R[r], (r, c, "LEFT")))
            if r == H - 1:
                delta = -(2 << s1) + (1 << ((idx - W) * 8))
                moves.append((1, s1, 0, delta, r - 1, -C[c], (r, c, "UP")))
            elif r > 0:
                s2 = (idx + W) * 8
                delta = -b1 - (1 << s2) + (1 << ((idx - W) * 8))
                moves.append((2, s1, s2, delta, r - 1, -C[c], (r, c, "UP")))

    g_score = {start: 0}
    parent = {start: None}
    pq = [(raw_h0, 0, raw_h0, start, ab0)]
    nodes = 0

    while pq:
        f, g, rh, s, ab = heapq.heappop(pq)
        if s == goal:
            path = []
            while parent[s] is not None:
                s, mv = parent[s]
                path.append(mv)
            path.reverse()
            return path
        if g > g_score.get(s, 10**9):
            continue
        ng = g + 1
        for ctype, s1, s2, delta, ab_idx, dab, mv in moves:
            v1 = (s >> s1) & 0xFF
            if not v1 or (ctype == 1 and v1 < 2) or (ctype == 2 and not ((s >> s2) & 0xFF)):
                continue
            nxt = s + delta
            if ng >= g_score.get(nxt, 10**9):
                continue
            g_score[nxt] = ng
            parent[nxt] = (s, mv)
            old_val = ab[ab_idx]
            new_val = old_val + dab
            tbl = tbls[ab_idx]
            nrh = rh - lookup(tbl, old_val) + lookup(tbl, new_val)
            nab = ab[:ab_idx] + (new_val,) + ab[ab_idx + 1:]
            heapq.heappush(pq, (ng + nrh, ng, nrh, nxt, nab))
            nodes += 1
            if nodes >= max_nodes:
                return None
    return None


def hint(start_state, mask, max_nodes=SOLVER_MAX_NODES):
    """The first move of an optimal solution, or None if unsolvable/solved."""
    path = solve(start_state, mask, max_nodes)
    if not path:
        return None
    return path[0]


def optimal_length(start_state, mask, max_nodes=SOLVER_MAX_NODES):
    path = solve(start_state, mask, max_nodes)
    return None if path is None else len(path)


